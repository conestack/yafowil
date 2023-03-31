# -*- coding: utf-8 -*-
from node.base import AttributedNode
from node.base import OrderedNode
from node.behaviors import Attributes
from node.utils import UNSET
from plumber import plumbing
from yafowil.base import factory
from yafowil.tests import YafowilTestCase
from yafowil.utils import Tag
from yafowil.utils import as_data_attrs
from yafowil.utils import attr_value
from yafowil.utils import callable_value
from yafowil.utils import cssclasses
from yafowil.utils import cssid
from yafowil.utils import data_attrs_helper
from yafowil.utils import generic_html5_attrs
from yafowil.utils import get_example
from yafowil.utils import get_example_names
from yafowil.utils import get_plugin_names
from yafowil.utils import get_plugins
from yafowil.utils import managedprops
from yafowil.utils import tag as deprecated_tag
from yafowil.utils import vocabulary


class TestUtils(YafowilTestCase):

    def test_entry_point(self):
        # Test entry_point support tools
        self.checkOutput("""
        [...(EntryPoint.parse('register = yafowil.loader:register'),
        <function register at ...)...]
        """, str(list(get_plugins())))

        self.assertEqual(list(get_plugins('nonexisting')), [])

        self.checkOutput("""
        [...'yafowil'...]
        """, str((get_plugin_names())))

        self.assertEqual(get_plugin_names('nonexisting'), [])

    def test_examples_lookup(self):
        # Test examples lookup
        self.checkOutput("""
        ['yafowil'...]
        """, str(sorted(get_example_names())))

        factory.register_macro('field', 'field:label:error', {})

        self.assertEqual(get_example('inexistent'), None)

        examples = get_example('yafowil')
        self.checkOutput("""
        Plain Text
        ----------
        ...
        """, examples[0]['doc'])

        self.assertEqual(examples[0]['title'], 'Plain Text')
        self.assertEqual(examples[0]['widget'].name, 'yafowil-plaintext')

    def test_vocabulary(self):
        # Test the Vocabulary
        self.assertEqual(vocabulary('foo'), [('foo', 'foo')])
        self.assertEqual(vocabulary({'key': 'value'}), [('key', 'value')])
        self.assertEqual(
            vocabulary(['value', 'value2']),
            [('value', 'value'), ('value2', 'value2')]
        )
        self.assertEqual(
            vocabulary([
                ('key', 'value'),
                ('key2', 'value2', 'v2.3'),
                ('key3',)
            ]),
            [('key', 'value'), ('key2', 'value2'), ('key3', 'key3')]
        )

        def callme():
            return 'bar'
        self.assertEqual(vocabulary(callme), [('bar', 'bar')])
        self.assertTrue(vocabulary(None) is None)

    def test_Tag(self):
        # Test Tag
        tag = Tag(lambda msg: msg)
        t = tag('p', b'Lorem Ipsum. ', u'Hello World!',
                class_=b'fancy', id=u'2f5b8a234ff')
        self.assertEqual(t, (
            u'<p class="fancy" id="2f5b8a234ff">Lorem Ipsum. Hello World!</p>'
        ))
        self.assertEqual(
            tag('dummy', name='foo', **{'data-foo': 'bar'}),
            u'<dummy data-foo=\'bar\' name="foo" />'
        )
        self.assertEqual(tag('dummy', name=None), u'<dummy />')
        self.assertEqual(tag('dummy', name=UNSET), u'<dummy />')
        # deprecated test
        self.assertEqual(deprecated_tag('div', 'foo'), u'<div>foo</div>')

    def test_cssid(self):
        # Test CSS id
        @plumbing(Attributes)
        class CSSTestNode(OrderedNode):
            @property
            def dottedpath(self):
                return u'.'.join([it for it in self.path if it])

        widget = CSSTestNode(name='form')

        widget.attrs['structural'] = True
        self.assertEqual(cssid(widget, 'PREFIX'), None)

        child = widget['child'] = CSSTestNode()
        self.assertEqual(cssid(child, 'PREFIX'), 'PREFIX-form-child')
        self.assertEqual(
            cssid(child, 'PREFIX', postfix='POSTFIX'),
            'PREFIX-form-child-POSTFIX'
        )

        child = widget[u'Hällo Wörld'] = CSSTestNode()
        self.assertEqual(cssid(child, 'PREFIX'), 'PREFIX-form-Hallo_World')

    def test_css_classes(self):
        # Test CSS Classes
        @plumbing(Attributes)
        class CSSTestNode(OrderedNode):
            pass

        widget = CSSTestNode()
        widget.attrs['required'] = False
        widget.attrs['required_class'] = None
        widget.attrs['required_class_default'] = 'required'
        widget.attrs['error_class'] = None
        widget.attrs['error_class_default'] = 'error'
        widget.attrs['valid_class'] = None
        widget.attrs['valid_class_default'] = 'valid'
        widget.attrs['class'] = None
        widget.attrs['class_add'] = None

        class DummyData(object):
            def __init__(self):
                self.errors = []
                self.extracted = UNSET

            @property
            def root(self):
                return self

        data = DummyData()

        self.assertEqual(cssclasses(widget, data), None)

        widget.attrs['class'] = 'foo bar'
        self.assertEqual(cssclasses(widget, data), 'bar foo')

        widget.attrs['class'] = None
        widget.attrs['required'] = True
        self.assertEqual(cssclasses(widget, data), None)

        widget.required = False
        data.errors = True
        self.assertEqual(cssclasses(widget, data), None)

        widget.attrs['error_class'] = True
        self.assertEqual(cssclasses(widget, data), 'error')

        widget.attrs['class'] = 'foo bar'
        self.assertEqual(cssclasses(widget, data), 'bar error foo')

        widget.attrs['class'] = lambda w, d: 'baz'
        self.assertEqual(cssclasses(widget, data), 'baz error')

        widget.attrs['class_add'] = lambda w, d: 'addclass_from_callable'
        self.assertEqual(
            cssclasses(widget, data),
            'addclass_from_callable baz error'
        )

        widget.attrs['class_add'] = 'addclass'
        self.assertEqual(cssclasses(widget, data), 'addclass baz error')

        widget.attrs['class'] = None
        widget.attrs['class_add'] = None
        widget.attrs['error_class'] = 'othererror'
        self.assertEqual(cssclasses(widget, data), 'othererror')

        data.errors = False
        self.assertEqual(cssclasses(widget, data), None)

        widget.attrs['required'] = True
        self.assertEqual(cssclasses(widget, data), None)

        widget.attrs['required_class'] = True
        self.assertEqual(cssclasses(widget, data), 'required')

        widget.attrs['required_class'] = 'otherrequired'
        self.assertEqual(cssclasses(widget, data), 'otherrequired')

        widget.attrs['error_class'] = True
        data.errors = True
        widget.attrs['required_class'] = 'required'
        self.assertEqual(cssclasses(widget, data), 'error required')

        widget.attrs['class'] = 'foo bar'
        self.assertEqual(
            cssclasses(widget, data),
            'bar error foo required'
        )

        self.assertEqual(
            cssclasses(widget, data, additional=['zika', 'akiz']),
            'akiz bar error foo required zika'
        )

        data.errors = []
        data.extracted = True
        widget.attrs['required'] = False
        widget.attrs['class'] = None

        widget.attrs['valid_class'] = True
        self.assertEqual(cssclasses(widget, data), 'valid')

        widget.attrs['valid_class'] = 'custom_valid'
        self.assertEqual(cssclasses(widget, data), 'custom_valid')

    def test_managedprops(self):
        # Test managedprops annotation
        @managedprops('foo', 'bar')
        def somefunc(a, b, c):
            return a, b, c

        self.assertEqual(somefunc(1, 2, 3), (1, 2, 3))

        self.assertEqual(
            somefunc.__yafowil_managed_props__,
            ('foo', 'bar')
        )

    def test_attr_value(self):
        # Test attr_value
        widget = AttributedNode()
        data = AttributedNode()

        widget.attrs['attr'] = 'value'
        self.assertEqual(attr_value('attr', widget, data), 'value')

        def func_callback(widget, data):
            return 'func_callback value'

        widget.attrs['attr'] = func_callback
        self.assertEqual(
            attr_value('attr', widget, data),
            'func_callback value'
        )

        def failing_func_callback(widget, data):
            raise Exception('failing_func_callback')

        widget.attrs['attr'] = failing_func_callback
        with self.assertRaises(Exception) as arc:
            attr_value('attr', widget, data)
        self.assertEqual(str(arc.exception), 'failing_func_callback')

        class FormContext(object):
            def instance_callback(self, widget, data):
                return 'instance_callback'

            def failing_instance_callback(self, widget, data):
                raise Exception('failing_instance_callback')

        context = FormContext()
        widget.attrs['attr'] = context.instance_callback
        self.assertEqual(
            attr_value('attr', widget, data),
            'instance_callback'
        )

        widget.attrs['attr'] = context.failing_instance_callback
        with self.assertRaises(Exception) as arc:
            attr_value('attr', widget, data)
        self.assertEqual(str(arc.exception), 'failing_instance_callback')

    def test_as_data_attrs(self):
        self.assertTrue(as_data_attrs is generic_html5_attrs)
        html5_attrs = as_data_attrs({
            'foo': 'bar',
            'baz': ['bam'],
            'nada': None,
            'unset': UNSET
        })
        self.assertEqual(
            html5_attrs,
            {'data-baz': '["bam"]', 'data-foo': 'bar'}
        )
        html5_attrs = as_data_attrs(None)
        self.assertEqual(html5_attrs, {})
        html5_attrs = as_data_attrs(UNSET)
        self.assertEqual(html5_attrs, {})

    def test_data_attrs_helper(self):
        data = AttributedNode()
        widget = AttributedNode()
        widget.attrs['testattr1'] = 'value'
        widget.attrs['testattr2'] = True
        widget.attrs['testattr3'] = False
        widget.attrs['testattr4'] = None
        widget.attrs['testattr5'] = ['item1', 'item2', 'item3']
        widget.attrs['testattr6'] = {
            'key1': 'item1',
            'key2': 'item2',
            'key3': 'item3'
        }
        widget.attrs['testattr7'] = 1234
        widget.attrs['testattr8'] = 1234.5678
        widget.attrs['testattr9'] = UNSET
        widget.attrs['camelAttrName'] = 'camelValue'
        data_attrs_keys = [
            'testattr1', 'testattr2', 'testattr3', 'testattr4', 'testattr5',
            'testattr6', 'testattr7', 'testattr8', 'camelAttrName'
        ]
        data_attrs = data_attrs_helper(widget, data, data_attrs_keys)

        self.assertEqual(data_attrs['data-testattr1'], 'value')
        self.assertEqual(data_attrs['data-testattr2'], 'true')
        self.assertEqual(data_attrs['data-testattr3'], 'false')
        self.assertFalse('data-testattr4' in data_attrs)
        self.assertEqual(
            data_attrs['data-testattr5'],
            '["item1", "item2", "item3"]'
        )
        self.assertTrue(data_attrs['data-testattr6'].find('"key1": "item1"'))
        self.assertTrue(data_attrs['data-testattr6'].find('"key2": "item2"'))
        self.assertTrue(data_attrs['data-testattr6'].find('"key3": "item3"'))
        self.assertTrue(data_attrs['data-testattr6'].startswith('{'))
        self.assertTrue(data_attrs['data-testattr6'].endswith('}'))
        self.assertEqual(data_attrs['data-testattr7'], '1234')
        self.assertEqual(data_attrs['data-testattr8'], '1234.5678')
        self.assertFalse('data-testattr9' in data_attrs)
        self.assertEqual(data_attrs['data-camel-attr-name'], 'camelValue')

        # Test with Tag renderer
        tag = Tag(lambda msg: msg)
        self.checkOutput("""
        <dummy
          data-camel-attr-name='camelValue'
          data-testattr1='value'
          data-testattr2='true'
          data-testattr3='false'
          data-testattr5='["item1", "item2", "item3"]'
          data-testattr6='{"..."}'
          data-testattr7='1234'
          data-testattr8='1234.5678'
          name="foo" />
        """, tag('dummy', name='foo', **data_attrs))

    def test_callable_value(self):
        # non callbale is returned as is
        self.assertEqual(callable_value('1', None, None), '1')

        # callable expects widget and data
        def dummy_callable(widget, data):
            return "2"
        self.assertEqual(callable_value(dummy_callable, None, None), '2')

        # callable with no parameters raises type error
        def invalid_signature():
            pass  # pragma: no cover
        self.assertRaises(TypeError, invalid_signature, None, None)
