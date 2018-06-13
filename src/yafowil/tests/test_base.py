from node.tests import NodeTestCase
from node.utils import UNSET
from yafowil.base import ExtractionError
from yafowil.base import Factory
from yafowil.base import RuntimeData
from yafowil.base import TBSupplementWidget
from yafowil.base import Widget
from yafowil.base import fetch_value

import traceback


###############################################################################
# Helpers
###############################################################################

def test_extractor(widget, data):
    return 'e1'


def test_edit_renderer(widget, data):
    return 'r1, {}, {}, {}'.format(
        widget.__name__,
        str(data),
        str(widget.attributes)
    )


def test_getter(widget, data):
    return 'Test Value'


def test_preprocessor(widget, data):
    data.attrs['test_preprocessor'] = 'called'
    return data


###############################################################################
# Tests
###############################################################################

class TestBase(NodeTestCase):

    def test_RuntimeData(self):
        # Initial RuntimeData is empty
        data = RuntimeData()
        self.assertEqual(data.request, UNSET)
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, UNSET)
        self.assertEqual(data.rendered, UNSET)
        self.assertEqual(data.errors, [])
        self.assertEqual(data.keys(), [])
        self.assertEqual(repr(data.__name__), 'None')

        # Initial RuntimeData can get its name passed in
        data = RuntimeData('root')
        self.assertEqual(data.__name__, 'root')

        # RuntimeData can have children
        data['surname'] = RuntimeData()
        data['fieldset'] = RuntimeData()
        self.assertEqual(data.keys(), ['surname', 'fieldset'])
        self.assertEqual(data['surname'].__name__, 'surname')

        # And each child can have children again
        data['fieldset']['age'] = RuntimeData()
        data['fieldset']['age'].value = 36

        # RuntimeData can have arbitrary attributes
        data['surname'].attrs['somekey'] = 'somevalue'
        self.assertEqual(data['surname'].attrs['somekey'], 'somevalue')

        # You can fetch other data also by its dotted absolute path
        fetched = data.fetch('root.fieldset.age')
        self.assertEqual(fetched.value, 36)

        # Or by the absolute path as an list of strings
        fetched = data.fetch(['root', 'fieldset', 'age'])
        self.assertEqual(fetched.value, 36)

        # It works on children::
        fetched = data['fieldset']['age'].fetch('root.surname')
        self.assertEqual(fetched.__name__, 'surname')

        # Same with path as a list
        fetched = data['fieldset']['age'].fetch(['root', 'surname'])
        self.assertEqual(fetched.__name__, 'surname')

        # It fails if if root element name is wrong
        err = self.expect_error(
            KeyError,
            data['fieldset']['age'].fetch,
            ['foobar', 'surname']
        )
        self.assertEqual(str(err), "'Invalid name of root element'")

        # It fails if sub path element is wrong
        try:
            data['fieldset']['age'].fetch('root.unknown')
        except KeyError:
            self.check_output("""
            Traceback (most recent call last):
            ...
                data = data[key]
            - __traceback_info__: fetch path: ['root', 'unknown']
            ...
            KeyError: 'unknown'
            """, traceback.format_exc())
        else:
            raise Exception('Exception expected but not thrown')

    def test_Widget(self):
        def test_extractor2(widget, data):
            return 'e2'

        def test_extractor3(widget, data):
            number = data.request[widget.__name__]
            try:
                return int(number)
            except Exception:
                raise ExtractionError('e3: Integer expected, got %s' % number)
            return number

        def fail_extractor(widget, data):
            raise ValueError('extractor has to fail')

        def test_edit_renderer2(widget, data):
            return 'r2, {}, {}, {}'.format(
                widget.__name__,
                str(data),
                str(widget.attributes)
            )

        def fail_edit_renderer(widget, data):
            raise ValueError('renderer has to fail')

        def test_display_renderer(widget, data):
            return 'disr1, {}, {}, {}'.format(
                widget.__name__,
                str(data),
                str(widget.attributes)
            )

        def fail_display_renderer(widget, data):
            raise ValueError('display renderer has to fail')

        def test_getter2(widget, data):
            return 999

        # The widget class
        test_request = {'MYUID': 'New Test Value'}
        testwidget = Widget(
            'blueprint_names_goes_here',
            [('1', test_extractor)],
            [('1', test_edit_renderer)],
            [('1', test_display_renderer)],
            [('1', test_preprocessor)],
            'MYUID',
            test_getter,
            dict(test1='Test1', test2='Test2'))

        self.check_output("""
        r1,
        MYUID,
        <RuntimeData MYUID, value='Test Value', extracted=<UNSET>,
        attrs={'test_preprocessor': 'called'} at ...>,
        {...'test1': 'Test1'...}
        """, testwidget())

        # A passed in request does not trigger extraction
        self.check_output("""
        r1,
        MYUID,
        <RuntimeData MYUID, value='Test Value', extracted=<UNSET>,
        attrs={'test_preprocessor': 'called'} at ...>,
        {...'test2': 'Test2'...}
        """, testwidget(request=test_request))

        # Extraction is an explicit task
        data = testwidget.extract(test_request)
        self.check_output("""
        <RuntimeData MYUID, value='Test Value', extracted='e1',
        attrs={'test_preprocessor': 'called'} at ...>
        """, str(data))

        self.assertEqual(data.attrs['test_preprocessor'], 'called')

        # Preprocessor is only called once!
        data.attrs['test_preprocessor'] = 'reset'
        data = testwidget._runpreprocessors(data)
        self.assertEqual(data.attrs['test_preprocessor'], 'reset')

        # Different cases

        # a.1) defaults: edit
        testwidget = Widget(
            'blueprint_names_goes_here',
            [('1', test_extractor)],
            [('1', test_edit_renderer)],
            [('1', test_display_renderer)],
            [],
            'MYUID',
            test_getter,
            dict(test1='Test1', test2='Test2'))
        self.check_output("""
        r1,
        MYUID,
        <RuntimeData MYUID, value='Test Value', extracted=<UNSET> at ...>,
        {...'test1': 'Test1'...}
        """, testwidget())

        # a.2) mode display
        testwidget = Widget(
            'blueprint_names_goes_here',
            [('1', test_extractor)],
            [('1', test_edit_renderer)],
            [('1', test_display_renderer)],
            [],
            'MYUID',
            test_getter,
            dict(test1='Test1', test2='Test2'),
            mode='display')
        self.check_output("""
        disr1,
        MYUID,
        <RuntimeData MYUID, value='Test Value', extracted=<UNSET> at ...>,
        {...'test2': 'Test2'...}
        """, testwidget())

        # a.3) mode skip
        testwidget = Widget(
            'blueprint_names_goes_here',
            [('1', test_extractor)],
            [('1', test_edit_renderer)],
            [('1', test_display_renderer)],
            [],
            'MYUID',
            test_getter,
            dict(test1='Test1', test2='Test2'),
            mode='skip')
        self.assertEqual(testwidget(), u'')

        # a.4) mode w/o renderer
        testwidget = Widget(
            'blueprint_names_goes_here',
            [('1', test_extractor)],
            [],
            [],
            [],
            'MYUID',
            test_getter,
            dict(test1='Test1', test2='Test2'),
            mode='display')
        err = self.expect_error(ValueError, testwidget)
        msg = "no renderers given for widget 'MYUID' at mode 'display'"
        self.assertEqual(str(err), msg)

        # b.1) two extractors w/o request
        testwidget = Widget(
            'blueprint_names_goes_here',
            [('1', test_extractor), ('2', test_extractor2)],
            [('1', test_edit_renderer), ('2', test_edit_renderer2)],
            [('1', test_display_renderer)],
            [],
            'MYUID2',
            test_getter,
            dict(test1='Test1', test2='Test2'))
        self.check_output("""
        r2,
        MYUID2,
        <RuntimeData MYUID2, value='Test Value', extracted=<UNSET> at ...>,
        {...'test1': 'Test1'...}
        """, testwidget())

        # b.2) extractor with request, non int has to fail
        testwidget = Widget(
            'blueprint_names_goes_here',
            [('1', test_extractor3)],
            [('1', test_edit_renderer)],
            [('1', test_display_renderer)],
            [],
            'MYUID2',
            test_getter2,
            dict(test1='Test1', test2='Test2'))

        self.check_output("""
        <RuntimeData MYUID2, value=999, extracted=<UNSET>, 1 error(s) at ...>
        """, str(testwidget.extract({'MYUID2': 'ABC'})))

        # b.3) extractor with request, but mode display
        testwidget = Widget(
            'blueprint_names_goes_here',
            [('1', test_extractor3)],
            [('1', test_edit_renderer)],
            [('1', test_display_renderer)],
            [],
            'MYUID2',
            test_getter2,
            dict(test1='Test1', test2='Test2'),
            mode='display')
        self.check_output("""
        <RuntimeData MYUID2, value=999, extracted=<UNSET> ...>
        """, str(testwidget.extract({'MYUID2': '123'})))

        # b.4) two extractors with request
        testwidget = Widget(
            'blueprint_names_goes_here',
            [('1', test_extractor3)],
            [('1', test_edit_renderer)],
            [('1', test_display_renderer)],
            [],
            'MYUID2',
            test_getter2,
            dict(test1='Test1', test2='Test2'))
        self.check_output("""
        <RuntimeData MYUID2, value=999, extracted=123 at ...>
        """, str(testwidget.extract({'MYUID2': '123'})))

        # A failing widget
        testwidget = Widget(
            'blueprint_names_goes_here',
            [('1', fail_extractor)],
            [('1', fail_edit_renderer)],
            [('1', test_display_renderer)],
            [],
            'MYFAIL',
            '',
            dict())

        try:
            testwidget.extract({})
        except Exception:
            self.check_output("""
            Traceback (most recent call last):
            ...
                data.extracted = extractor(self, data)
                yafowil widget processing info:
                - path      : MYFAIL
                - blueprints: blueprint_names_goes_here
                - task      : extract
                - descr     : failed at '1'
            ...
            ValueError: extractor has to fail
            """, traceback.format_exc())
        else:
            raise Exception('Exception expected but not thrown')

        try:
            testwidget()
        except Exception:
            self.check_output("""
            Traceback (most recent call last):
            ...
                yafowil widget processing info:
                - path      : MYFAIL
                - blueprints: blueprint_names_goes_here
                - task      : render
                - descr     : failed at '1' in mode 'edit'
            ...
            ValueError: renderer has to fail
            """, traceback.format_exc())
        else:
            raise Exception('Exception expected but not thrown')

        # Plausability
        err = self.expect_error(
            ValueError,
            testwidget,
            data=data,
            request={}
        )
        msg = "if data is passed in, don't pass in request!"
        self.assertEqual(str(err), msg)

        # Widget dottedpath

        # Fails with no name in root
        testwidget = Widget('blueprint_names_goes_here', [], [], [], [])
        err = self.expect_error(
            ValueError,
            lambda: testwidget.dottedpath
        )
        msg = 'Root widget has no name! Pass it to factory.'
        self.assertEqual(str(err), msg)

        # At this test level the factory is not used,
        # so we pass it directly to Widget
        testwidget = Widget(
            'blueprint_names_goes_here', [], [], [], [], uniquename='root')
        self.assertEqual(testwidget.dottedpath, 'root')

        testwidget['child'] = Widget(
            'blueprint_names_goes_here', [], [], [], [])
        self.assertEqual(testwidget['child'].dottedpath, 'root.child')

        testwidget['child']['level3'] = Widget(
            'blueprint_names_goes_here', [], [], [], [])
        self.assertEqual(
            testwidget['child']['level3'].dottedpath,
            'root.child.level3'
        )

        # The mode
        testwidget = Widget(
            'blueprint_names_goes_here', [], [], [], [], uniquename='root')
        data = testwidget.extract({})
        self.assertEqual(data.mode, 'edit')

        testwidget = Widget(
            'blueprint_names_goes_here',
            [], [], [], [],
            uniquename='root',
            mode='display')
        data = testwidget.extract({})
        self.assertEqual(data.mode, 'display')

        testwidget = Widget(
            'blueprint_names_goes_here',
            [], [], [], [],
            uniquename='root',
            mode='skip')
        data = testwidget.extract({})
        self.assertEqual(data.mode, 'skip')

        testwidget = Widget(
            'blueprint_names_goes_here',
            [], [], [], [],
            uniquename='root',
            mode='other')
        err = self.expect_error(
            ValueError,
            testwidget.extract,
            {}
        )
        msg = (
            "mode must be one out of 'edit', 'display', 'skip', "
            "but 'other' was given"
        )
        self.assertEqual(str(err), msg)

        def mode(widget, data):
            return 'edit'
        testwidget = Widget(
            'blueprint_names_goes_here',
            [], [], [], [],
            uniquename='root',
            mode=mode)
        data = testwidget.extract({})
        self.assertEqual(data.mode, 'edit')

        def mode(widget, data):
            return 'display'
        testwidget = Widget(
            'blueprint_names_goes_here',
            [], [], [], [],
            uniquename='root',
            mode=mode)
        data = testwidget.extract({})
        self.assertEqual(data.mode, 'display')

        # Check whether error occurred somewhere in Tree::

        def value_extractor(widget, data):
            return data.request[widget.dottedpath]

        def child_extractor(widget, data):
            for child in widget.values():
                child.extract(request=data.request, parent=data)

        def error_extractor(widget, data):
            raise ExtractionError(widget.dottedpath)

        root = Widget(
            'root_blueprint',
            [('child_extractor', child_extractor)],
            [],
            [],
            [],
            uniquename='root')
        root['child_0'] = Widget(
            'child_blueprint',
            [('value_extractor', value_extractor)],
            [],
            [],
            [])
        root['child_1'] = Widget(
            'child_blueprint',
            [('error_extractor', error_extractor)],
            [],
            [],
            [])

        self.check_output("""
        <class 'yafowil.base.Widget'>: root
        <class 'yafowil.base.Widget'>: child_0
        <class 'yafowil.base.Widget'>: child_1
        """, root.treerepr())

        data = root.extract({
            'root.child_0': 'a',
            'root.child_1': 'b',
        })
        self.check_output("""
        <RuntimeData root, value=<UNSET>, extracted=None at ...>
        <RuntimeData root.child_0,
            value=<UNSET>, extracted='a' at ...>
        <RuntimeData root.child_1,
            value=<UNSET>, extracted=<UNSET>, 1 error(s) at ...>
        """, data.treerepr())

        self.assertTrue(data.has_errors, True)
        self.assertFalse(data['child_0'].has_errors, False)
        self.assertTrue(data['child_1'].has_errors, True)

    def test_factory(self):
        # Fill factory with test blueprints
        factory = Factory()
        factory.register('widget_test', [test_extractor], [test_edit_renderer])
        self.assertEqual(
            factory.extractors('widget_test'),
            [test_extractor]
        )
        self.assertEqual(
            factory.edit_renderers('widget_test'),
            [test_edit_renderer]
        )

        testwidget = factory(
            'widget_test',
            name='MYFAC',
            value=test_getter,
            props=dict(foo='bar'))
        self.check_output("""
        r1,
        MYFAC,
        <RuntimeData MYFAC, value='Test Value', extracted=<UNSET> at ...>,
        {'foo': 'bar'}
        """, testwidget())

        factory.register(
            'widget_test',
            [test_extractor],
            [test_edit_renderer],
            preprocessors=[test_preprocessor])
        self.assertEqual(
            factory.preprocessors('widget_test'),
            [test_preprocessor]
        )

        def test_global_preprocessor(widget, data):
            return data

        factory.register_global_preprocessors([test_global_preprocessor])
        self.assertEqual(
            factory.preprocessors('widget_test'),
            [test_global_preprocessor, test_preprocessor]
        )

        testwidget = factory(
            'widget_test',
            name='MYFAC',
            value=test_getter,
            props=dict(foo='bar'), mode='display')
        data = testwidget.extract({})
        self.assertEqual(data.mode, 'display')

        # We can create sets of static builders, i.e. to have a validating
        # password field with two input fields in. Here a simpler example
        def create_static_compound(widget, factory):
            widget['one'] = factory('widget_test', widget.attrs)
            widget['two'] = factory('widget_test', widget.attrs)

        factory.register(
            'static_compound', [], [], builders=[create_static_compound])
        widget = factory('static_compound', props={})
        self.assertEqual(widget.keys(), ['one', 'two'])
        self.assertEqual(
            factory.builders('static_compound'),
            [create_static_compound]
        )

        # Some basic name checks are done
        err = self.expect_error(ValueError, factory._name_check, '*notallowed')
        self.assertEqual(str(err), '"*" as char not allowed as name.')

        err = self.expect_error(ValueError, factory._name_check, 'not:allowed')
        self.assertEqual(str(err), '":" as char not allowed as name.')

        err = self.expect_error(ValueError, factory._name_check, '#notallowed')
        self.assertEqual(str(err), '"#" as char not allowed as name.')

        # Test the macros
        factory.register_macro(
            'test_macro', 'foo:*bar:baz', {'foo.newprop': 'abc'})

        self.assertEqual(
            factory._macros,
            {'test_macro': (['foo', '*bar', 'baz'], {'foo.newprop': 'abc'})}
        )
        self.assertEqual(
            factory._expand_blueprints('#test_macro', {'foo.newprop': '123'}),
            (['foo', '*bar', 'baz'], {'foo.newprop': '123'})
        )
        self.assertEqual(
            factory._expand_blueprints(
                '#test_macro',
                {'foo.newprop2': '123'}
            ),
            (
                ['foo', '*bar', 'baz'],
                {'foo.newprop': 'abc', 'foo.newprop2': '123'}
            )
        )

        err = self.expect_error(
            ValueError,
            factory._expand_blueprints,
            '#nonexisting', {}
        )
        msg = "Macro named 'nonexisting' is not registered in factory"
        self.assertEqual(str(err), msg)

        factory.register_macro('test_macro2', 'alpha:#test_macro:beta', {})

        self.assertEqual(
            factory._expand_blueprints('#test_macro2', {}),
            (['alpha', 'foo', '*bar', 'baz', 'beta'], {'foo.newprop': 'abc'})
        )

    def test_theme_registry(self):
        # Theme to use
        factory = Factory()
        self.assertEqual(factory.theme, 'default')

        # Register addon widget resources for default theme
        factory.register_theme(
            'default',
            'yafowil.widget.someaddon',
            '/foo/bar/resources',
            js=[{'resource': 'default/widget.js',
                 'thirdparty': False,
                 'order': 10,
                 'merge': False}],
            css=[{'resource': 'default/widget.css',
                  'thirdparty': False,
                  'order': 10,
                  'merge': False}])

        # Register addon widget resources for custom theme
        factory.register_theme(
            'custom',
            'yafowil.widget.someaddon',
            '/foo/bar/resources',
            js=[{'resource': 'custom/widget.js',
                 'thirdparty': False,
                 'order': 10,
                 'merge': False}],
            css=[{'resource': 'custom/widget.css',
                  'thirdparty': False,
                  'order': 10,
                  'merge': False}])

        # Lookup resouces for addon widget
        self.assertEqual(factory.resources_for('yafowil.widget.someaddon'), {
            'resourcedir': '/foo/bar/resources',
            'css': [{
                'merge': False,
                'thirdparty': False,
                'resource': 'default/widget.css',
                'order': 10
            }],
            'js': [{
                'merge': False,
                'thirdparty': False,
                'resource': 'default/widget.js',
                'order': 10
            }]
        })

        # Set theme on factory
        factory.theme = 'custom'
        self.assertEqual(factory.resources_for('yafowil.widget.someaddon'), {
            'resourcedir': '/foo/bar/resources',
            'css': [{
                'merge': False,
                'thirdparty': False,
                'resource': 'custom/widget.css',
                'order': 10
            }],
            'js': [{
                'merge': False,
                'thirdparty': False,
                'resource': 'custom/widget.js',
                'order': 10
            }]
        })

        # If no resources found for theme name, return default resources
        factory.theme = 'inexistent'
        self.assertEqual(factory.resources_for('yafowil.widget.someaddon'), {
            'resourcedir': '/foo/bar/resources',
            'css': [{
                'merge': False,
                'thirdparty': False,
                'resource': 'default/widget.css',
                'order': 10
            }],
            'js': [{
                'merge': False,
                'thirdparty': False,
                'resource': 'default/widget.js',
                'order': 10
            }]
        })

        # If no resources registered at all for widget, None is returned
        factory.theme = 'default'
        self.assertTrue(
            factory.resources_for('yafowil.widget.inexistent') is None
        )

        # Resources are returned as deepcopy of the original resources
        # definition by default
        resources = factory.resources_for('yafowil.widget.someaddon')
        self.assertFalse(
            resources is factory.resources_for('yafowil.widget.someaddon')
        )

        # Some might want the resource definitions as original instance
        resources = factory.resources_for(
            'yafowil.widget.someaddon', copy_resources=False)
        self.assertTrue(
            resources is factory.resources_for(
                'yafowil.widget.someaddon', copy_resources=False)
        )

    def test_widget_tree_manipulation(self):
        # Widget trees provide functionality described in
        # ``node.interfaces.IOrder``, which makes it possible to insert widgets
        # at a specific place in an existing widget tree

        factory = Factory()
        factory.register('widget_test', [test_extractor], [test_edit_renderer])

        widget = factory('widget_test', name='root')
        widget['1'] = factory('widget_test')
        widget['2'] = factory('widget_test')
        self.check_output("""
        <class 'yafowil.base.Widget'>: root
        <class 'yafowil.base.Widget'>: 1
        <class 'yafowil.base.Widget'>: 2
        """, widget.treerepr())

        new = factory('widget_test', name='3')
        ref = widget['1']
        widget.insertbefore(new, ref)
        new = factory('widget_test', name='4')
        widget.insertafter(new, ref)
        self.check_output("""
        <class 'yafowil.base.Widget'>: root
        <class 'yafowil.base.Widget'>: 3
        <class 'yafowil.base.Widget'>: 1
        <class 'yafowil.base.Widget'>: 4
        <class 'yafowil.base.Widget'>: 2
        """, widget.treerepr())

    def test_factory_chain(self):
        # Sometimes we want to wrap inputs by UI candy, primary for usability
        # reasons. This might be a label, some error output or div around. We
        # dont want to register an amount of X possible widgets with an amount
        # of Y possible wrappers. Therefore we can factor a widget in a chain
        # defined colon-separated, i.e 'outer:inner' or 'field:error:text'.
        # Chaining works for all parts: edit_renderers, display_renderes,
        # extractors, preprocessors and builders. Most inner and first executed
        # is right (we prefix with wrappers)!. The chain can be defined as list
        # instead of a colon seperated string as well

        def inner_renderer(widget, data):
            return u'<INNER />'

        def inner_display_renderer(widget, data):
            return u'<INNERDISPLAY />'

        def inner_extractor(widget, data):
            return ['extracted inner']

        def outer_renderer(widget, data):
            return u'<OUTER>%s</OUTER>' % data.rendered

        def outer_display_renderer(widget, data):
            return u'<OUTERDISPLAY>%s</OUTERDISPLAY>' % data.rendered

        def outer_extractor(widget, data):
            return data.extracted + ['extracted outer']

        factory = Factory()
        factory.register(
            'inner',
            [inner_extractor],
            [inner_renderer],
            [],
            [],
            [inner_display_renderer])
        factory.register(
            'outer',
            [outer_extractor],
            [outer_renderer],
            [],
            [],
            [outer_display_renderer])
        self.assertEqual(
            factory.display_renderers('inner'),
            [inner_display_renderer]
        )
        self.assertEqual(
            factory.edit_renderers('inner'),
            [inner_renderer]
        )
        err = self.expect_error(
            RuntimeError,
            factory.renderers,
            'inner'
        )
        msg = 'Deprecated since 1.2, use edit_renderers or display_renderers'
        self.assertEqual(str(err), msg)

        # Colon seperated blueprint chain definition
        widget = factory('outer:inner', name='OUTER_INNER')
        data = widget.extract({})
        self.assertEqual(
            data.extracted,
            ['extracted inner', 'extracted outer']
        )
        self.assertEqual(widget(data), u'<OUTER><INNER /></OUTER>')

        # Blueprint chain definition as list
        widget = factory(['outer', 'inner'], name='OUTER_INNER')
        data = widget.extract({})
        self.assertEqual(
            data.extracted,
            ['extracted inner', 'extracted outer']
        )
        self.assertEqual(widget(data), u'<OUTER><INNER /></OUTER>')

        # Inject custom specials blueprints into chain

        # You may need an behavior just one time and just for one special
        # widget. Here you can inject your custom special render or extractor
        # into the chain

        def special_renderer(widget, data):
            return u'<SPECIAL>%s</SPECIAL>' % data.rendered

        def special_extractor(widget, data):
            return data.extracted + ['extracted special']

        # Inject as dict
        widget = factory(
            'outer:*special:inner',
            name='OUTER_SPECIAL_INNER',
            custom={
                'special': {
                    'extractors': [special_extractor],
                    'edit_renderers': [special_renderer]
                }
            })
        data = widget.extract({})
        self.assertEqual(
            data.extracted,
            ['extracted inner', 'extracted special', 'extracted outer']
        )
        self.assertEqual(
            widget(data),
            u'<OUTER><SPECIAL><INNER /></SPECIAL></OUTER>'
        )

        # Inject as list
        widget = factory(
            'outer:*special:inner',
            name='OUTER_SPECIAL_INNER',
            custom={
                'special': (
                    [special_extractor],
                    [special_renderer],
                    [],
                    [],
                    []
                )
            })
        data = widget.extract({})
        self.assertEqual(
            data.extracted,
            ['extracted inner', 'extracted special', 'extracted outer']
        )
        self.assertEqual(
            widget(data),
            u'<OUTER><SPECIAL><INNER /></SPECIAL></OUTER>'
        )

        # BBB, w/o display_renderer
        widget = factory(
            'outer:*special:inner',
            name='OUTER_SPECIAL_INNER',
            custom={
                'special': (
                    [special_extractor],
                    [special_renderer],
                    [],
                    []
                )
            })
        data = widget.extract({})
        self.assertEqual(
            data.extracted,
            ['extracted inner', 'extracted special', 'extracted outer']
        )

    def test_prefixes_and_defaults(self):
        # Prefixes with widgets and factories
        # Factory called widget attributes should know about its factory name
        # with a prefix

        def prefix_renderer(widget, data):
            return u'<ID>%s</ID>' % widget.attrs['id']

        factory = Factory()
        factory.register('prefix', [], [prefix_renderer])
        widget = factory('prefix', props={'prefix.id': 'Test'})
        self.assertEqual(widget(), u'<ID>Test</ID>')

        widget = factory('prefix', name='test', props={'id': 'Test2'})
        self.assertEqual(widget(), u'<ID>Test2</ID>')

        # modify defaults for widgets attributes via factory

        # We have the following value resolution order for properties:

        # 1) prefixed property
        # 2) unprefixed property
        # 3) prefixed default
        # 4) unprefixed default
        # 5) KeyError

        # Case for (5): We have only some unprefixed default
        widget = factory('prefix', name='test')
        try:
            widget()
        except KeyError as e:
            msg = (
                "'Property with key \"id\" is not given on "
                "widget \"test\" (no default)'"
            )
            self.assertEqual(str(e), msg)
        else:
            raise Exception('Exception expected but not thrown')

        # Case for (4): Unprefixed default
        factory.defaults['id'] = 'Test4'
        widget = factory('prefix', name='test')
        self.assertEqual(widget(), u'<ID>Test4</ID>')

        # Case for (3): Prefixed default overrides unprefixed
        factory.defaults['prefix.id'] = 'Test3'
        widget = factory('prefix', name='test')
        self.assertEqual(widget(), u'<ID>Test3</ID>')

        # Case for (2): Unprefixed property overides any default
        widget = factory('prefix', name='test', props={'id': 'Test2'})
        self.assertEqual(widget(), u'<ID>Test2</ID>')

        # Case for (1): Prefixed property overrules all others
        widget = factory('prefix', name='test', props={'prefix.id': 'Test1'})
        self.assertEqual(widget(), u'<ID>Test1</ID>')

    def test_fetch_value(self):
        dmarker = list()
        defaults = dict(default=dmarker)
        widget_no_return = Widget(
            'blueprint_names_goes_here', [], [], [], 'empty', defaults=defaults)  # noqa
        widget_with_value = Widget(
            'blueprint_names_goes_here',
            [], [], [],
            'value',
            value_or_getter='withvalue',
            defaults=defaults)
        widget_with_default = Widget(
            'blueprint_names_goes_here',
            [], [], [],
            'default',
            properties=dict(default='defaultvalue'),
            defaults=defaults)
        widget_with_both = Widget(
            'blueprint_names_goes_here',
            [], [], [],
            'both',
            value_or_getter='valueboth',
            properties=dict(default='defaultboth'),
            defaults=defaults)
        data_empty = RuntimeData()
        data_filled = RuntimeData()
        data_filled.extracted = 'extractedvalue'

        data_empty.value = widget_no_return.getter
        self.assertTrue(fetch_value(widget_no_return, data_empty) is dmarker)

        data_filled.value = widget_no_return.getter
        self.assertEqual(
            fetch_value(widget_no_return, data_filled),
            'extractedvalue'
        )

        data_empty.value = widget_with_value.getter
        self.assertEqual(
            fetch_value(widget_with_value, data_empty),
            'withvalue'
        )

        data_filled.value = widget_with_value.getter
        self.assertEqual(
            fetch_value(widget_with_value, data_filled),
            'extractedvalue'
        )

        data_empty.value = widget_with_default.getter
        self.assertEqual(
            fetch_value(widget_with_default, data_empty),
            'defaultvalue'
        )

        data_filled.value = widget_with_default.getter
        self.assertEqual(
            fetch_value(widget_with_default, data_filled),
            'extractedvalue'
        )

        data_empty.value = widget_with_both.getter
        self.assertEqual(
            fetch_value(widget_with_both, data_empty),
            'valueboth'
        )

        data_filled.value = widget_with_both.getter
        self.assertEqual(
            fetch_value(widget_with_default, data_filled),
            'extractedvalue'
        )

    def test_TBSupplementWidget(self):
        class NoNameMock(object):
            blueprints = 'blue:prints:here'

            @property
            def dottedpath(self):
                raise ValueError('fail')

        mock = NoNameMock()
        suppl = TBSupplementWidget(
            mock, lambda x: x, 'testtask', 'some description')

        self.check_output("""
        yafowil widget processing info:
            - path      : (name not set)
            - blueprints: blue:prints:here
            - task      : testtask
            - descr     : some description
        """, suppl.getInfo())

        class Mock(object):
            dottedpath = 'test.path.abc'
            blueprints = 'blue:prints:here'
        mock = Mock()
        suppl = TBSupplementWidget(mock, lambda x: x, 'testtask',
                                   'some description')

        self.check_output("""
        yafowil widget processing info:
            - path      : test.path.abc
            - blueprints: blue:prints:here
            - task      : testtask
            - descr     : some description
        """, suppl.getInfo())

        self.check_output("""
        <p>yafowil widget processing info:<ul><li>path:
        <strong>test.path.abc</strong></li><li>blueprints:
        <strong>blue:prints:here</strong></li><li>task:
        <strong>testtask</strong></li><li>description: <strong>some
        description</strong></li></ul></p>
        """, suppl.getInfo(as_html=1))
