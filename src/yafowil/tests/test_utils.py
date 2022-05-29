# -*- coding: utf-8 -*-
from node.base import AttributedNode
from node.base import OrderedNode
from node.behaviors import Attributes
from node.utils import UNSET
from plumber import plumbing
from yafowil.base import factory
from yafowil.compat import BYTES_TYPE
from yafowil.compat import IS_PY2
from yafowil.compat import LONG_TYPE
from yafowil.compat import UNICODE_TYPE
from yafowil.tests import YafowilTestCase
from yafowil.utils import as_data_attrs
from yafowil.utils import attr_value
from yafowil.utils import callable_value
from yafowil.utils import convert_value_to_datatype
from yafowil.utils import convert_values_to_datatype
from yafowil.utils import cssclasses
from yafowil.utils import cssid
from yafowil.utils import data_attrs_helper
from yafowil.utils import EMPTY_VALUE
from yafowil.utils import generic_html5_attrs
from yafowil.utils import get_example
from yafowil.utils import get_example_names
from yafowil.utils import get_plugin_names
from yafowil.utils import get_plugins
from yafowil.utils import managedprops
from yafowil.utils import Tag
from yafowil.utils import tag as deprecated_tag
from yafowil.utils import vocabulary
import uuid
import yafowil.loader  # noqa


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

    def test_EMPTY_VALUE(self):
        self.assertEqual(repr(EMPTY_VALUE), '<EMPTY_VALUE>')
        self.assertEqual(str(EMPTY_VALUE), '')
        self.assertFalse(bool(EMPTY_VALUE))
        self.assertEqual(len(EMPTY_VALUE), 0)

    def test_convert_value_to_datatype(self):
        # Unknown string identifier
        with self.assertRaises(KeyError) as arc:
            convert_value_to_datatype('val', 'inexistent')
        self.assertEqual(str(arc.exception), "'inexistent'")

        # Function returns ``EMPTY_VALUE`` marker if value is ``None`` or empty
        # string
        self.assertEqual(convert_value_to_datatype('', 'uuid'), EMPTY_VALUE)
        self.assertEqual(convert_value_to_datatype(None, 'uuid'), EMPTY_VALUE)

    def test_convert_value_to_datatype_str(self):
        # Convert to string by id
        self.assertEqual(convert_value_to_datatype(UNSET, 'str'), UNSET)

        converted = convert_value_to_datatype(u'string', 'str')
        self.assertEqual(converted, b'string')
        self.assertTrue(isinstance(converted, BYTES_TYPE))

        with self.assertRaises(UnicodeEncodeError) as arc:
            convert_value_to_datatype(u'äöü', 'str')
        self.checkOutput("""
        'ascii' codec can't encode character...: ordinal not in range(128)
        """, str(arc.exception))

        # Convert to string by type
        self.assertEqual(convert_value_to_datatype(UNSET, BYTES_TYPE), UNSET)

        converted = convert_value_to_datatype(u'string', BYTES_TYPE)
        self.assertEqual(converted, b'string')
        self.assertTrue(isinstance(converted, BYTES_TYPE))

        with self.assertRaises(UnicodeEncodeError) as arc:
            convert_value_to_datatype(u'äöü', BYTES_TYPE)
        self.checkOutput("""
        'ascii' codec can't encode character...: ordinal not in range(128)
        """, str(arc.exception))

    def test_convert_value_to_datatype_unicode(self):
        # Convert to unicode by id
        self.assertEqual(convert_value_to_datatype(UNSET, 'unicode'), UNSET)

        converted = convert_value_to_datatype('unicode', 'unicode')
        self.assertEqual(converted, u'unicode')
        self.assertTrue(isinstance(converted, UNICODE_TYPE))

        with self.assertRaises(UnicodeDecodeError) as arc:
            convert_value_to_datatype(b'\xc3\xa4\xc3\xb6\xc3\xbc', 'unicode')
        msg = (
            "'ascii' codec can't decode byte 0xc3 in position 0: "
            "ordinal not in range(128)")
        self.assertEqual(str(arc.exception), msg)

        # Convert to unicode by type
        self.assertEqual(convert_value_to_datatype(UNSET, UNICODE_TYPE), UNSET)

        converted = convert_value_to_datatype('unicode', UNICODE_TYPE)
        self.assertEqual(converted, u'unicode')
        self.assertTrue(isinstance(converted, UNICODE_TYPE))

        with self.assertRaises(UnicodeDecodeError) as arc:
            convert_value_to_datatype(b'\xc3\xa4\xc3\xb6\xc3\xbc', UNICODE_TYPE)
        msg = (
            "'ascii' codec can't decode byte 0xc3 in position 0: "
            "ordinal not in range(128)")
        self.assertEqual(str(arc.exception), msg)

    def test_convert_value_to_datatype_int(self):
        # Convert to int by id
        self.assertEqual(convert_value_to_datatype(UNSET, 'int'), UNSET)

        converted = convert_value_to_datatype('1', 'int')
        self.assertEqual(converted, 1)
        self.assertTrue(isinstance(converted, int))

        with self.assertRaises(ValueError) as arc:
            convert_value_to_datatype('1.0', 'int')
        msg = "invalid literal for int() with base 10: '1.0'"
        self.assertEqual(str(arc.exception), msg)

        with self.assertRaises(ValueError) as arc:
            convert_value_to_datatype('a', 'int')
        msg = "invalid literal for int() with base 10: 'a'"
        self.assertEqual(str(arc.exception), msg)

        converted = convert_value_to_datatype(2.0, 'int')
        self.assertEqual(converted, 2)
        self.assertTrue(isinstance(converted, int))

        # Convert to int by type
        self.assertEqual(convert_value_to_datatype(UNSET, int), UNSET)

        converted = convert_value_to_datatype('3', int)
        self.assertEqual(converted, 3)
        self.assertTrue(isinstance(converted, int))

        with self.assertRaises(ValueError) as arc:
            convert_value_to_datatype('2.0', int)
        msg = "invalid literal for int() with base 10: '2.0'"
        self.assertEqual(str(arc.exception), msg)

        with self.assertRaises(ValueError) as arc:
            convert_value_to_datatype('b', int)
        msg = "invalid literal for int() with base 10: 'b'"
        self.assertEqual(str(arc.exception), msg)

        converted = convert_value_to_datatype(4.0, int)
        self.assertEqual(converted, 4)
        self.assertTrue(isinstance(converted, int))

    def test_convert_value_to_datatype_long(self):
        # Convert to long by id
        self.assertEqual(convert_value_to_datatype(UNSET, 'long'), UNSET)

        converted = convert_value_to_datatype('1', 'long')
        self.assertEqual(converted, LONG_TYPE(1))
        self.assertTrue(isinstance(converted, LONG_TYPE))

        converted = convert_value_to_datatype(2.0, 'long')
        self.assertEqual(converted, LONG_TYPE(2))
        self.assertTrue(isinstance(converted, LONG_TYPE))

        with self.assertRaises(ValueError) as arc:
            convert_value_to_datatype('a', 'long')
        # there is no long type in python 3, falls back to int
        msg = (
            "invalid literal for long() with base 10: 'a'"
            if IS_PY2
            else "invalid literal for int() with base 10: 'a'"
        )
        self.assertEqual(str(arc.exception), msg)

        # Convert to long by type
        self.assertEqual(convert_value_to_datatype(UNSET, LONG_TYPE), UNSET)

        converted = convert_value_to_datatype('3', LONG_TYPE)
        self.assertEqual(converted, LONG_TYPE(3))
        self.assertTrue(isinstance(converted, LONG_TYPE))

        converted = convert_value_to_datatype(4.0, LONG_TYPE)
        self.assertEqual(converted, LONG_TYPE(4))
        self.assertTrue(isinstance(converted, LONG_TYPE))

        with self.assertRaises(ValueError) as arc:
            convert_value_to_datatype('b', LONG_TYPE)
        # there is no long type in python 3, falls back to int
        msg = (
            "invalid literal for long() with base 10: 'b'"
            if IS_PY2
            else "invalid literal for int() with base 10: 'b'"
        )
        self.assertEqual(str(arc.exception), msg)

    def test_convert_value_to_datatype_float(self):
        # Convert to float by id
        self.assertEqual(convert_value_to_datatype(UNSET, 'float'), UNSET)

        converted = convert_value_to_datatype('1,0', 'float')
        self.assertEqual(converted, 1.0)
        self.assertTrue(isinstance(converted, float))

        converted = convert_value_to_datatype('2', 'float')
        self.assertEqual(converted, 2.0)
        self.assertTrue(isinstance(converted, float))

        with self.assertRaises(ValueError) as arc:
            convert_value_to_datatype('a', 'float')
        msg = (
            "could not convert string to float: a"
            if IS_PY2
            else "could not convert string to float: 'a'"
        )
        self.assertEqual(str(arc.exception), msg)

        converted = convert_value_to_datatype(3, 'float')
        self.assertEqual(converted, 3.0)
        self.assertTrue(isinstance(converted, float))

        # Convert to float by type
        self.assertEqual(convert_value_to_datatype(UNSET, float), UNSET)

        converted = convert_value_to_datatype('4,0', float)
        self.assertEqual(converted, 4.0)
        self.assertTrue(isinstance(converted, float))

        converted = convert_value_to_datatype('5', float)
        self.assertEqual(converted, 5.0)
        self.assertTrue(isinstance(converted, float))

        with self.assertRaises(ValueError) as arc:
            convert_value_to_datatype('b', float)
        msg = (
            "could not convert string to float: b"
            if IS_PY2
            else "could not convert string to float: 'b'"
        )
        self.assertEqual(str(arc.exception), msg)

        converted = convert_value_to_datatype(6, float)
        self.assertEqual(converted, 6.0)
        self.assertTrue(isinstance(converted, float))

    def test_convert_value_to_datatype_uuid(self):
        # Convert to uuid by id
        self.assertEqual(convert_value_to_datatype(UNSET, 'uuid'), UNSET)

        converted = convert_value_to_datatype(str(uuid.uuid4()), 'uuid')
        self.assertTrue(isinstance(converted, uuid.UUID))

        with self.assertRaises(ValueError) as arc:
            convert_value_to_datatype('a', 'uuid')
        msg = 'badly formed hexadecimal UUID string'
        self.assertEqual(str(arc.exception), msg)

        # Convert to uuid by type
        self.assertEqual(convert_value_to_datatype(UNSET, uuid.UUID), UNSET)

        converted = convert_value_to_datatype(str(uuid.uuid4()), uuid.UUID)
        self.assertTrue(isinstance(converted, uuid.UUID))

        with self.assertRaises(ValueError) as arc:
            convert_value_to_datatype('a', uuid.UUID)
        msg = 'badly formed hexadecimal UUID string'
        self.assertEqual(str(arc.exception), msg)

    def test_convert_value_to_datatype_function(self):
        # Custom converter as function
        def convert_func(val):
            if val == 'a':
                return 'convertet: {0}'.format(val)
            raise ValueError("Value not 'a'")

        self.assertEqual(
            convert_value_to_datatype('a', convert_func),
            'convertet: a'
        )

        with self.assertRaises(ValueError) as arc:
            convert_value_to_datatype('b', convert_func)
        self.assertEqual(str(arc.exception), "Value not 'a'")

    def test_convert_value_to_datatype_class(self):
        # Custom converters as class
        class Converter(object):

            def __init__(self, val):
                if val != 'a':
                    raise ValueError("Value not 'a'")

        converted = convert_value_to_datatype('a', Converter)
        self.assertTrue(isinstance(converted, Converter))

        with self.assertRaises(ValueError) as arc:
            convert_value_to_datatype('b', Converter)
        self.assertEqual(str(arc.exception), "Value not 'a'")

    def test_convert_value_to_datatype_instance(self):
        # Custom converter as class instance with ``__call__`` function
        class ConverterInst(object):

            def __call__(self, val):
                if val != 'a':
                    raise ValueError("Value not 'a'")
                return 'convertet: {0}'.format(val)

        self.assertEqual(
            convert_value_to_datatype('a', ConverterInst()),
            'convertet: a'
        )

        with self.assertRaises(ValueError) as arc:
            convert_value_to_datatype('b', ConverterInst())
        self.assertEqual(str(arc.exception), "Value not 'a'")

    def test_convert_values_to_datatype(self):
        self.assertEqual(convert_values_to_datatype(UNSET, 'int'), UNSET)
        self.assertEqual(convert_values_to_datatype([UNSET], 'int'), [UNSET])
        self.assertEqual(convert_values_to_datatype('0', int), 0)
        self.assertEqual(convert_values_to_datatype(['0', '1'], int), [0, 1])

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
