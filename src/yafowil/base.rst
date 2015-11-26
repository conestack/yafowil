Prepare
-------

Imports::

    >>> from yafowil.base import ExtractionError
    >>> from yafowil.base import Factory
    >>> from yafowil.base import RuntimeData
    >>> from yafowil.base import TBSupplementWidget
    >>> from yafowil.base import Widget
    >>> from yafowil.base import fetch_value
    >>> import sys
    >>> import traceback


Runtime Data
------------

Initial RuntimeData is empty::    

    >>> data = RuntimeData()
    >>> data.request
    <UNSET>

    >>> data.value
    <UNSET>

    >>> data.extracted
    <UNSET>

    >>> data.rendered
    <UNSET>

    >>> data.errors
    []

    >>> data.keys()
    []

    >>> repr(data.__name__)
    'None'

Initial RuntimeData can get its name passed in::

    >>> data = RuntimeData('root')
    >>> data.__name__
    'root'    

RuntimeData can have children::   

    >>> data['surname'] = RuntimeData()
    >>> data['fieldset'] = RuntimeData()
    >>> data.keys()
    ['surname', 'fieldset']

    >>> data['surname'].__name__
    'surname'

And each child can have children again::

    >>> data['fieldset']['age'] = RuntimeData()
    >>> data['fieldset']['age'].value = 36

RuntimeData can have arbitrary attributes::

    >>> data['surname'].attrs['somekey'] = 'somevalue'
    >>> data['surname'].attrs['somekey']
    'somevalue'

You can fetch other data also by its dotted absolute path::

    >>> fetched = data.fetch('root.fieldset.age')
    >>> fetched.value 
    36

Or by the absolute path as an list of strings::    

    >>> fetched = data.fetch(['root', 'fieldset', 'age'])
    >>> fetched.value 
    36

It works on children::

    >>> fetched = data['fieldset']['age'].fetch('root.surname')
    >>> fetched.__name__
    'surname'

Same with path as a list::

    >>> fetched = data['fieldset']['age'].fetch(['root', 'surname'])
    >>> fetched.__name__
    'surname'

It fails if if root element name is wrong::

    >>> fetched = data['fieldset']['age'].fetch(['foobar', 'surname']) 
    Traceback (most recent call last):
    ...
    KeyError: 'Invalid name of root element'

It fails if sub path element is wrong::

    >>> fetched = data['fieldset']['age'].fetch('root.unknown') 
    Traceback (most recent call last):
    ...
        data = data[key]
       - __traceback_info__: fetch path: ['root', 'unknown']
    ...
    KeyError: 'unknown'


Base Widget
-----------

Create some test dummies::

    >>> def test_extractor(widget, data):
    ...     return 'e1'

    >>> def test_extractor2(widget, data):
    ...     return 'e2'

    >>> def test_extractor3(widget, data):
    ...     number = data.request[widget.__name__]
    ...     try:
    ...         return int(number)
    ...     except:
    ...         raise ExtractionError('e3: Integer expected, got %s' % number)
    ...     return value

    >>> def fail_extractor(widget, data):
    ...     raise ValueError, 'extractor has to fail'

    >>> def test_edit_renderer(widget, data):
    ...     return 'r1', widget.__name__, str(data), str(widget.attributes)

    >>> def test_edit_renderer2(widget, data):
    ...     return 'r2', widget.__name__, str(data), str(widget.attributes)

    >>> def fail_edit_renderer(widget, data):
    ...     raise ValueError, 'renderer has to fail'

    >>> def test_display_renderer(widget, data):
    ...     return 'disr1', widget.__name__, str(data), str(widget.attributes)

    >>> def fail_display_renderer(widget, data):
    ...     raise ValueError, 'display renderer has to fail'

    >>> def test_preprocessor(widget, data):
    ...     data.attrs['test_preprocessor'] = 'called'
    ...     return data

    >>> def test_getter(widget, data):
    ...     return 'Test Value'

    >>> def test_getter2(widget, data):
    ...     return 999

The widget class::    

    >>> test_request = {'MYUID': 'New Test Value'}
    >>> testwidget = Widget(
    ...     'blueprint_names_goes_here',
    ...     [('1', test_extractor)],
    ...     [('1', test_edit_renderer)],
    ...     [('1', test_display_renderer)],
    ...     [('1', test_preprocessor)],
    ...     'MYUID',
    ...     test_getter,
    ...     dict(test1='Test1', test2='Test2'))

    >>> testwidget() 
    ('r1', 'MYUID', "<RuntimeData MYUID, value='Test Value', extracted=<UNSET>, 
    attrs={'test_preprocessor': 'called'} at ...>", "{'test1': 'Test1', 
    'test2': 'Test2'}")

A passed in request does not trigger extraction::    

    >>> testwidget(request=test_request) 
    ('r1', 'MYUID', "<RuntimeData MYUID, value='Test Value', extracted=<UNSET>, 
    attrs={'test_preprocessor': 'called'} at ...>", "{'test1': 'Test1', 
    'test2': 'Test2'}")

Extraction is an explicit task::    

    >>> data = testwidget.extract(test_request)
    >>> data
    <RuntimeData MYUID, value='Test Value', extracted='e1', 
    attrs={'test_preprocessor': 'called'} at ...>

    >>> data.attrs['test_preprocessor']
    'called'

Preprocessor is only called once!::    

    >>> data.attrs['test_preprocessor'] = 'reset'
    >>> data = testwidget._runpreprocessors(data)
    >>> data.attrs['test_preprocessor']
    'reset'    

Different cases.

a.1) defaults: edit::     

    >>> testwidget = Widget(
    ...     'blueprint_names_goes_here',
    ...     [('1', test_extractor)],
    ...     [('1', test_edit_renderer)],
    ...     [('1', test_display_renderer)],
    ...     [],
    ...     'MYUID',
    ...     test_getter,
    ...     dict(test1='Test1', test2='Test2'))
    >>> testwidget()
    ('r1', 'MYUID', "<RuntimeData MYUID, value='Test Value', extracted=<UNSET> 
    at ...>", "{'test1': 'Test1', 'test2': 'Test2'}")

a.2) mode display::   

    >>> testwidget = Widget(
    ...     'blueprint_names_goes_here',
    ...     [('1', test_extractor)],
    ...     [('1', test_edit_renderer)],
    ...     [('1', test_display_renderer)],
    ...     [],
    ...     'MYUID',
    ...     test_getter,
    ...     dict(test1='Test1', test2='Test2'),
    ...     mode='display')
    >>> testwidget()
    ('disr1', 'MYUID', "<RuntimeData MYUID, value='Test Value', 
    extracted=<UNSET> at ...>", "{'test1': 'Test1', 'test2': 'Test2'}")

a.3) mode skip::   

    >>> testwidget = Widget(
    ...     'blueprint_names_goes_here',
    ...     [('1', test_extractor)],
    ...     [('1', test_edit_renderer)],
    ...     [('1', test_display_renderer)],
    ...     [],
    ...     'MYUID',
    ...     test_getter,
    ...     dict(test1='Test1', test2='Test2'),
    ...     mode='skip')
    >>> testwidget()
    u''

a.4) mode w/o renderer:: 

    >>> testwidget = Widget(
    ...     'blueprint_names_goes_here',
    ...     [('1', test_extractor)],
    ...     [],
    ...     [],
    ...     [],
    ...     'MYUID',
    ...     test_getter,
    ...     dict(test1='Test1', test2='Test2'),
    ...     mode='display')
    >>> testwidget()
    Traceback (most recent call last):
    ...
    ValueError: no renderers given for widget 'MYUID' at mode 'display'

b.1) two extractors w/o request:: 

    >>> testwidget = Widget(
    ...     'blueprint_names_goes_here',
    ...     [('1', test_extractor), ('2', test_extractor2)],
    ...     [('1', test_edit_renderer), ('2', test_edit_renderer2)],
    ...     [('1', test_display_renderer)],
    ...     [],
    ...     'MYUID2',
    ...     test_getter,
    ...     dict(test1='Test1', test2='Test2'))
    >>> testwidget()
    ('r2', 'MYUID2', "<RuntimeData MYUID2, value='Test Value', 
    extracted=<UNSET> at ...>", "{'test1': 'Test1', 'test2': 'Test2'}")

b.2) extractor with request, non int has to fail::

    >>> testwidget = Widget(
    ...     'blueprint_names_goes_here',
    ...     [('1', test_extractor3)],
    ...     [('1', test_edit_renderer)],
    ...     [('1', test_display_renderer)],
    ...     [],
    ...     'MYUID2',
    ...     test_getter2,
    ...     dict(test1='Test1', test2='Test2'))
    >>> testwidget.extract({'MYUID2': 'ABC'})
    <RuntimeData MYUID2, value=999, extracted=<UNSET>, 1 error(s) at ...>    

b.3) extractor with request, but mode display::

    >>> testwidget = Widget(
    ...     'blueprint_names_goes_here',
    ...     [('1', test_extractor3)],
    ...     [('1', test_edit_renderer)],
    ...     [('1', test_display_renderer)],
    ...     [],
    ...     'MYUID2',
    ...     test_getter2,
    ...     dict(test1='Test1', test2='Test2'),
    ...     mode='display')
    >>> testwidget.extract({'MYUID2': '123'})
    <RuntimeData MYUID2, value=999, extracted=<UNSET> ...>    

b.3) two extractors with request::

    >>> testwidget = Widget(
    ...     'blueprint_names_goes_here',
    ...     [('1', test_extractor3)],
    ...     [('1', test_edit_renderer)],
    ...     [('1', test_display_renderer)],
    ...     [],
    ...     'MYUID2',
    ...     test_getter2,
    ...     dict(test1='Test1', test2='Test2'))
    >>> testwidget.extract({'MYUID2': '123'})
    <RuntimeData MYUID2, value=999, extracted=123 at ...>

A failing widget::

    >>> testwidget = Widget(
    ...     'blueprint_names_goes_here',
    ...     [('1', fail_extractor)],
    ...     [('1', fail_edit_renderer)],
    ...     [('1', test_display_renderer)],
    ...     [],
    ...     'MYFAIL',
    ...     '',
    ...     dict())
    >>> try:
    ...    testwidget.extract({})
    ... except Exception, e:
    ...    traceback.print_exc(file=sys.stdout)
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

    >>> try:
    ...    testwidget()
    ... except Exception, e:
    ...    traceback.print_exc(file=sys.stdout)
    Traceback (most recent call last):
    ...
        yafowil widget processing info:
        - path      : MYFAIL
        - blueprints: blueprint_names_goes_here
        - task      : render
        - descr     : failed at '1' in mode 'edit'
    ...
    ValueError: renderer has to fail        

Plausability::

    >>> testwidget(data=data, request={})
    Traceback (most recent call last):
    ...
    ValueError: if data is passed in, don't pass in request!

Widget dottedpath.

Fails with no name in root::

    >>> testwidget = Widget('blueprint_names_goes_here', [], [], [], [])
    >>> testwidget.dottedpath
    Traceback (most recent call last):
    ...
    ValueError: Root widget has no name! Pass it to factory.

At this test level the factory is not used, so we pass it directly to Widget::    

    >>> testwidget = Widget(
    ...     'blueprint_names_goes_here', [], [], [], [], uniquename='root')
    >>> testwidget.dottedpath
    'root'

    >>> testwidget['child'] = Widget(
    ...     'blueprint_names_goes_here', [], [], [], [])
    >>> testwidget['child'].dottedpath
    'root.child'

    >>> testwidget['child']['level3'] = Widget(
    ...     'blueprint_names_goes_here', [], [], [], [])
    >>> testwidget['child']['level3'].dottedpath
    'root.child.level3'

The mode::

    >>> testwidget = Widget(
    ...     'blueprint_names_goes_here', [], [], [], [], uniquename='root')
    >>> data = testwidget.extract({})
    >>> data.mode
    'edit'    

    >>> testwidget = Widget(
    ...     'blueprint_names_goes_here',
    ...     [], [], [], [],
    ...     uniquename='root',
    ...     mode='display')
    >>> data = testwidget.extract({})
    >>> data.mode
    'display'    

    >>> testwidget = Widget(
    ...     'blueprint_names_goes_here',
    ...     [], [], [], [],
    ...     uniquename='root',
    ...     mode='skip')
    >>> data = testwidget.extract({})
    >>> data.mode
    'skip'    

    >>> testwidget = Widget(
    ...     'blueprint_names_goes_here',
    ...     [], [], [], [],
    ...     uniquename='root',
    ...     mode='other')
    >>> data = testwidget.extract({})
    Traceback (most recent call last):
    ...      
    ValueError: mode must be one out of 'edit', 'display', 'skip', but 
    'other' was given

    >>> def mode(widget, data):
    ...     return 'edit'
    >>> testwidget = Widget(
    ...     'blueprint_names_goes_here',
    ...     [], [], [], [],
    ...     uniquename='root',
    ...     mode=mode)
    >>> data = testwidget.extract({})
    >>> data.mode
    'edit'    

    >>> def mode(widget, data):
    ...     return 'display'
    >>> testwidget = Widget(
    ...     'blueprint_names_goes_here',
    ...     [], [], [], [],
    ...     uniquename='root',
    ...     mode=mode)
    >>> data = testwidget.extract({})
    >>> data.mode
    'display'    

Check whether error occurred somewhere in Tree::

    >>> def value_extractor(widget, data):
    ...     return data.request[widget.dottedpath]

    >>> def child_extractor(widget, data):
    ...     for child in widget.values():
    ...          child.extract(request=data.request, parent=data)

    >>> def error_extractor(widget, data):
    ...     raise ExtractionError(widget.dottedpath)

    >>> root = Widget(
    ...     'root_blueprint',
    ...     [('child_extractor', child_extractor)],
    ...     [],
    ...     [],
    ...     [],
    ...     uniquename='root')
    >>> child_0 = root['child_0'] = Widget(
    ...     'child_blueprint',
    ...     [('value_extractor', value_extractor)],
    ...     [],
    ...     [],
    ...     [])
    >>> child_1 = root['child_1'] = Widget(
    ...     'child_blueprint',
    ...     [('error_extractor', error_extractor)],
    ...     [],
    ...     [],
    ...     [])

    >>> root.printtree()
    <class 'yafowil.base.Widget'>: root
      <class 'yafowil.base.Widget'>: child_0
      <class 'yafowil.base.Widget'>: child_1

    >>> data = root.extract({
    ...     'root.child_0': 'a',
    ...     'root.child_1': 'b',
    ... })
    >>> data.printtree()
    <RuntimeData root, value=<UNSET>, extracted=None at ...>
      <RuntimeData root.child_0, 
        value=<UNSET>, extracted='a' at ...>
      <RuntimeData root.child_1, 
        value=<UNSET>, extracted=<UNSET>, 1 error(s) at ...>

    >>> data.has_errors
    True

    >>> data['child_0'].has_errors
    False

    >>> data['child_1'].has_errors
    True


factory
-------

Fill factory with test blueprints::

    >>> factory = Factory()
    >>> factory.register('widget_test', [test_extractor], [test_edit_renderer])
    >>> factory.extractors('widget_test')
    [<function test_extractor at ...>]

    >>> factory.edit_renderers('widget_test')
    [<function test_edit_renderer at ...>]

    >>> testwidget = factory(
    ...     'widget_test',
    ...     name='MYFAC',
    ...     value=test_getter,
    ...     props=dict(foo='bar'))
    >>> testwidget()
    ('r1', 'MYFAC', "<RuntimeData MYFAC, value='Test Value', extracted=<UNSET> 
    at ...>", "{'foo': 'bar'}")

    >>> factory.register(
    ...     'widget_test',
    ...     [test_extractor],
    ...     [test_edit_renderer],
    ...     preprocessors=[test_preprocessor])
    >>> factory.preprocessors('widget_test')
    [<function test_preprocessor at 0x...>]

    >>> def test_global_preprocessor(widget, data):
    ...     return data

    >>> factory.register_global_preprocessors([test_global_preprocessor])
    >>> factory.preprocessors('widget_test')
    [<function test_global_preprocessor at 0x...>, 
    <function test_preprocessor at 0x...>]

    >>> testwidget = factory(
    ...     'widget_test',
    ...     name='MYFAC',
    ...     value=test_getter,
    ...     props=dict(foo='bar'), mode='display')
    >>> data = testwidget.extract({})
    >>> data.mode
    'display'    

We can create sets of static builders, i.e. to have a validating password
field with two input fields in. Here a simpler example:: 

    >>> def create_static_compound(widget, factory):
    ...     widget['one'] = factory('widget_test', widget.attrs)
    ...     widget['two'] = factory('widget_test', widget.attrs)

    >>> factory.register(
    ...     'static_compound', [], [], builders=[create_static_compound])

    >>> widget = factory('static_compound', props={})
    >>> widget.keys()
    ['one', 'two']

    >>> factory.builders('static_compound')
    [<function create_static_compound at 0x...>]

Some basic name checks are done::

    >>> factory._name_check('*notallowed')
    Traceback (most recent call last):
    ...
    ValueError: "*" as char not allowed as name.

    >>> factory._name_check('not:allowed')
    Traceback (most recent call last):
    ...
    ValueError: ":" as char not allowed as name.

    >>> factory._name_check('#notallowed')
    Traceback (most recent call last):
    ...
    ValueError: "#" as char not allowed as name.

Test the macros::

    >>> factory.register_macro(
    ...     'test_macro', 'foo:*bar:baz', {'foo.newprop': 'abc'})
    >>> factory._macros
    {'test_macro': (['foo', '*bar', 'baz'], {'foo.newprop': 'abc'})}

    >>> factory._expand_blueprints('#test_macro', {'foo.newprop' : '123'})
    (['foo', '*bar', 'baz'], {'foo.newprop': '123'})

    >>> ex = factory._expand_blueprints('#test_macro', {'foo.newprop2' : '123'})
    >>> pprint(ex)
    (['foo', '*bar', 'baz'], {'foo.newprop': 'abc', 'foo.newprop2': '123'})

    >>> factory._expand_blueprints('#nonexisting', {})
    Traceback (most recent call last):
    ...
    ValueError: Macro named 'nonexisting' is not registered in factory

    >>> factory.register_macro('test_macro2', 'alpha:#test_macro:beta', {})
    >>> factory._expand_blueprints('#test_macro2', {})
    (['alpha', 'foo', '*bar', 'baz', 'beta'], {'foo.newprop': 'abc'})


Test theme registry
-------------------

Theme to use::

    >>> factory.theme
    'default'

Register addon widget resources for default theme::

    >>> factory.register_theme(
    ...     'default',
    ...     'yafowil.widget.someaddon',
    ...     '/foo/bar/resources',
    ...     js=[{'resource': 'default/widget.js',
    ...          'thirdparty': False,
    ...          'order': 10,
    ...          'merge': False}],
    ...     css=[{'resource': 'default/widget.css',
    ...           'thirdparty': False,
    ...           'order': 10,
    ...           'merge': False}])

Register addon widget resources for custom theme::

    >>> factory.register_theme(
    ...     'custom',
    ...     'yafowil.widget.someaddon',
    ...     '/foo/bar/resources',
    ...     js=[{'resource': 'custom/widget.js',
    ...          'thirdparty': False,
    ...          'order': 10,
    ...          'merge': False}],
    ...     css=[{'resource': 'custom/widget.css',
    ...           'thirdparty': False,
    ...           'order': 10,
    ...           'merge': False}])

Lookup resouces for addon widget::

    >>> factory.resources_for('yafowil.widget.someaddon')
    {'resourcedir': '/foo/bar/resources', 
    'css': [{'merge': False, 'thirdparty': False, 
    'resource': 'default/widget.css', 'order': 10}], 
    'js': [{'merge': False, 'thirdparty': False, 
    'resource': 'default/widget.js', 'order': 10}]}

Set theme on factory::

    >>> factory.theme = 'custom'
    >>> factory.resources_for('yafowil.widget.someaddon')
    {'resourcedir': '/foo/bar/resources', 
    'css': [{'merge': False, 'thirdparty': False, 
    'resource': 'custom/widget.css', 'order': 10}], 
    'js': [{'merge': False, 'thirdparty': False, 
    'resource': 'custom/widget.js', 'order': 10}]}

If no resources found for theme name, return default resources::

    >>> factory.theme = 'inexistent'
    >>> factory.resources_for('yafowil.widget.someaddon')
    {'resourcedir': '/foo/bar/resources', 
    'css': [{'merge': False, 'thirdparty': False, 
    'resource': 'default/widget.css', 'order': 10}], 
    'js': [{'merge': False, 'thirdparty': False, 
    'resource': 'default/widget.js', 'order': 10}]}

If no resources registered at all for widget, None is returned::

    >>> factory.theme = 'default'
    >>> factory.resources_for('yafowil.widget.inexistent') is None
    True

Resources are returned as deepcopy of the original resources definition by
default::

    >>> resources = factory.resources_for('yafowil.widget.someaddon')
    >>> resources is factory.resources_for('yafowil.widget.someaddon')
    False

Some might want the resource definitions as original instance::

    >>> resources = factory.resources_for(
    ...     'yafowil.widget.someaddon', copy_resources=False)
    >>> resources is factory.resources_for(
    ...     'yafowil.widget.someaddon', copy_resources=False)
    True


Widget tree manipulation
------------------------

Widget trees provide functionality described in ``node.interfaces.IOrder``,
which makes it possible to insert widgets at a specific place in an existing
widget tree::

    >>> widget = factory('widget_test', name='root')
    >>> widget['1'] = factory('widget_test')
    >>> widget['2'] = factory('widget_test')
    >>> widget.printtree()
    <class 'yafowil.base.Widget'>: root
      <class 'yafowil.base.Widget'>: 1
      <class 'yafowil.base.Widget'>: 2

    >>> new = factory('widget_test', name='3')
    >>> ref = widget['1']
    >>> widget.insertbefore(new, ref)
    >>> new = factory('widget_test', name='4')
    >>> widget.insertafter(new, ref)
    >>> widget.printtree()
    <class 'yafowil.base.Widget'>: root
      <class 'yafowil.base.Widget'>: 3
      <class 'yafowil.base.Widget'>: 1
      <class 'yafowil.base.Widget'>: 4
      <class 'yafowil.base.Widget'>: 2


Request chains via factory
--------------------------

Sometimes we want to wrap inputs by UI candy, primary for usability reasons.
This might be a label, some error output or div around. We dont want to register
an amount of X possible widgets with an amount of Y possible wrappers. Therefore
we can factor a widget in a chain defined colon-separated, i.e 'outer:inner' or
'field:error:text'. Chaining works for all parts: edit_renderers,
display_renderes, extractors, preprocessors and builders. Most inner and first
executed is right (we prefix with wrappers)!. The chain can be defined as list
instead of a colon seperated string as well::

    >>> def inner_renderer(widget, data):
    ...     return u'<INNER />'

    >>> def inner_display_renderer(widget, data):
    ...     return u'<INNERDISPLAY />'

    >>> def inner_extractor(widget, data):
    ...     return ['extracted inner']

    >>> def outer_renderer(widget, data):
    ...     return u'<OUTER>%s</OUTER>' % data.rendered

    >>> def outer_display_renderer(widget, data):
    ...     return u'<OUTERDISPLAY>%s</OUTERDISPLAY>' % data.rendered

    >>> def outer_extractor(widget, data):
    ...     return data.extracted + ['extracted outer']

    >>> factory.register(
    ...     'inner',
    ...     [inner_extractor],
    ...     [inner_renderer],
    ...     [],
    ...     [],
    ...     [inner_display_renderer])
    >>> factory.register(
    ...     'outer',
    ...     [outer_extractor],
    ...     [outer_renderer],
    ...     [],
    ...     [],
    ...     [outer_display_renderer])
    >>> factory.display_renderers('inner')
    [<function inner_display_renderer at ...>]

    >>> factory.edit_renderers('inner')
    [<function inner_renderer at ...>]

    >>> factory.renderers('inner')
    Traceback (most recent call last):
    ...
    RuntimeError: Deprecated since 1.2, use edit_renderers or display_renderers

Colon seperated blueprint chain definition::

    >>> widget = factory('outer:inner', name='OUTER_INNER')
    >>> data = widget.extract({})
    >>> data.extracted
    ['extracted inner', 'extracted outer']

    >>> widget(data)
    u'<OUTER><INNER /></OUTER>'

Blueprint chain definition as list::

    >>> widget = factory(['outer', 'inner'], name='OUTER_INNER')
    >>> data = widget.extract({})
    >>> data.extracted
    ['extracted inner', 'extracted outer']

    >>> widget(data)
    u'<OUTER><INNER /></OUTER>'


Inject custom specials blueprints into chain
--------------------------------------------

You may need an behavior just one time and just for one special widget. Here
you can inject your custom special render or extractor into the chain::

    >>> def special_renderer(widget, data):
    ...     return u'<SPECIAL>%s</SPECIAL>' % data.rendered

    >>> def special_extractor(widget, data):
    ...     return data.extracted + ['extracted special']

Inject as dict::

    >>> widget = factory(
    ...     'outer:*special:inner',
    ...     name='OUTER_SPECIAL_INNER',
    ...     custom={
    ...         'special': {
    ...             'extractors': [special_extractor],
    ...             'edit_renderers': [special_renderer]
    ...         }
    ...     })
    >>> data = widget.extract({})
    >>> data.extracted
    ['extracted inner', 'extracted special', 'extracted outer']

    >>> widget(data)
    u'<OUTER><SPECIAL><INNER /></SPECIAL></OUTER>'

Inject as list::

    >>> widget = factory(
    ...     'outer:*special:inner',
    ...     name='OUTER_SPECIAL_INNER',
    ...     custom={
    ...         'special': (
    ...             [special_extractor],
    ...             [special_renderer],
    ...             [],
    ...             [],
    ...             []
    ...         )
    ...     })
    >>> data = widget.extract({})
    >>> data.extracted
    ['extracted inner', 'extracted special', 'extracted outer']

    >>> widget(data)
    u'<OUTER><SPECIAL><INNER /></SPECIAL></OUTER>'

BBB, w/o display_renderer::  
      
    >>> widget = factory(
    ...     'outer:*special:inner',
    ...     name='OUTER_SPECIAL_INNER',
    ...     custom={
    ...         'special': (
    ...             [special_extractor],
    ...             [special_renderer],
    ...             [],
    ...             []
    ...         )
    ...     })
    >>> data = widget.extract({})
    >>> data.extracted
    ['extracted inner', 'extracted special', 'extracted outer']


Prefixes with widgets and factories
-----------------------------------

Factory called widget attributes should know about its factory name with a
prefix:: 

    >>> def prefix_renderer(widget, data):
    ...     return u'<ID>%s</ID>' % widget.attrs['id']

    >>> factory.register('prefix', [], [prefix_renderer])
    >>> widget = factory('prefix', props={'prefix.id': 'Test'})
    >>> widget()
    u'<ID>Test</ID>'

    >>> widget = factory('prefix', name='test', props={'id': 'Test2'})
    >>> widget()
    u'<ID>Test2</ID>'


modify defaults for widgets attributes via factory
--------------------------------------------------

We have the following value resolution order for properties:

1) prefixed property
2) unprefixed property
3) prefixed default
4) unprefixed default
5) KeyError

Case for (5): We have only some unprefixed default:: 

    >>> widget = factory('prefix', name='test')
    >>> try:
    ...     widget()
    ... except KeyError, e:
    ...     print e
    'Property with key "id" is not given on widget "test" (no default)'

Case for (4): Unprefixed default::

    >>> factory.defaults['id'] = 'Test4'
    >>> widget = factory('prefix', name='test')
    >>> widget()
    u'<ID>Test4</ID>'

Case for (3): Prefixed default overrides unprefixed::

    >>> factory.defaults['prefix.id'] = 'Test3'
    >>> widget = factory('prefix', name='test')
    >>> widget()
    u'<ID>Test3</ID>'

Case for (2): Unprefixed property overides any default:: 

    >>> widget = factory('prefix', name='test', props={'id': 'Test2'})
    >>> widget()
    u'<ID>Test2</ID>'

Case for (1): Prefixed property overrules all others::

    >>> widget = factory('prefix', name='test', props={'prefix.id': 'Test1'})
    >>> widget()
    u'<ID>Test1</ID>'

Clean up::

    >>> del factory.defaults['id']
    >>> del factory.defaults['prefix.id']


fetch value
-----------

::

    >>> dmarker = list()
    >>> defaults = dict(default=dmarker)
    >>> widget_no_return = Widget(
    ...     'blueprint_names_goes_here', [],[],[], 'empty', defaults=defaults)
    >>> widget_with_value = Widget(
    ...     'blueprint_names_goes_here',
    ...     [], [], [],
    ...     'value',
    ...     value_or_getter='withvalue',
    ...     defaults=defaults)
    >>> widget_with_default = Widget(
    ...     'blueprint_names_goes_here',
    ...     [], [], [],
    ...     'default',
    ...     properties=dict(default='defaultvalue'),
    ...     defaults=defaults)
    >>> widget_with_both = Widget(
    ...     'blueprint_names_goes_here',
    ...     [], [], [],
    ...     'both',
    ...     value_or_getter='valueboth',
    ...     properties=dict(default='defaultboth'),
    ...     defaults=defaults)
    >>> data_empty = RuntimeData()
    >>> data_filled = RuntimeData()
    >>> data_filled.extracted = 'extractedvalue'    
    
    >>> data_empty.value = widget_no_return.getter
    >>> fetch_value(widget_no_return, data_empty) is dmarker
    True

    >>> data_filled.value = widget_no_return.getter
    >>> fetch_value(widget_no_return, data_filled)
    'extractedvalue'

    >>> data_empty.value = widget_with_value.getter
    >>> fetch_value(widget_with_value, data_empty)
    'withvalue'

    >>> data_filled.value = widget_with_value.getter
    >>> fetch_value(widget_with_value, data_filled)
    'extractedvalue'    

    >>> data_empty.value = widget_with_default.getter
    >>> fetch_value(widget_with_default, data_empty)
    'defaultvalue'

    >>> data_filled.value = widget_with_default.getter
    >>> fetch_value(widget_with_default, data_filled)
    'extractedvalue'        

    >>> data_empty.value = widget_with_both.getter
    >>> fetch_value(widget_with_both, data_empty)
    'valueboth'

    >>> data_filled.value = widget_with_both.getter
    >>> fetch_value(widget_with_default, data_filled)
    'extractedvalue'        


TraceBack Supplment
-------------------

::

    >>> class NoNameMock(object):
    ...     blueprints='blue:prints:here'
    ...     @property
    ...     def dottedpath(self):
    ...          raise ValueError('fail')
    >>> mock = NoNameMock()
    >>> suppl = TBSupplementWidget(
    ...     mock, lambda x:x, 'testtask', 'some description')
    >>> print suppl.getInfo()
    yafowil widget processing info:
        - path      : (name not set)
        - blueprints: blue:prints:here
        - task      : testtask
        - descr     : some description

    >>> class Mock(object): 
    ...     dottedpath='test.path.abc'
    ...     blueprints='blue:prints:here'
    >>> mock = Mock()
    >>> suppl = TBSupplementWidget(mock, lambda x:x, 'testtask',
    ...                            'some description')
    >>> print suppl.getInfo()
        yafowil widget processing info:
        - path      : test.path.abc
        - blueprints: blue:prints:here
        - task      : testtask
        - descr     : some description

    >>> suppl.getInfo(as_html=1)
    u'<p>yafowil widget processing info:<ul><li>path: 
    <strong>test.path.abc</strong></li><li>blueprints: 
    <strong>blue:prints:here</strong></li><li>task: 
    <strong>testtask</strong></li><li>description: <strong>some 
    description</strong></li></ul></p>'
