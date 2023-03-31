from node.utils import UNSET
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.common import generic_extractor
from yafowil.compat import BYTES_TYPE
from yafowil.compat import IS_PY2
from yafowil.compat import LONG_TYPE
from yafowil.compat import UNICODE_TYPE
from yafowil.datatypes import convert_value_to_datatype
from yafowil.datatypes import convert_values_to_datatype
from yafowil.datatypes import generic_emptyvalue_extractor
from yafowil.datatypes import lookup_datatype_converter
from yafowil.tests import YafowilTestCase
from yafowil.utils import EMPTY_VALUE
import copy
import uuid


class TestDatatypes(YafowilTestCase):

    def test_EMPTY_VALUE(self):
        self.assertEqual(repr(EMPTY_VALUE), '<EMPTY_VALUE>')
        self.assertEqual(str(EMPTY_VALUE), '')
        self.assertFalse(bool(EMPTY_VALUE))
        self.assertEqual(len(EMPTY_VALUE), 0)
        self.assertTrue(copy.copy(EMPTY_VALUE) is EMPTY_VALUE)
        self.assertTrue(copy.deepcopy(EMPTY_VALUE) is EMPTY_VALUE)
        self.assertFalse(EMPTY_VALUE < EMPTY_VALUE)
        self.assertFalse(EMPTY_VALUE <= EMPTY_VALUE)
        self.assertFalse(EMPTY_VALUE > EMPTY_VALUE)
        self.assertFalse(EMPTY_VALUE >= EMPTY_VALUE)


    def test_generic_emptyvalue_extractor(self):
        factory.register(
            'emptyvalue_test',
            extractors=[
                generic_extractor,
                generic_emptyvalue_extractor
            ]
        )
        widget = factory('emptyvalue_test', name='widget')
        data = widget.extract({})
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'widget': ''})
        self.assertEqual(data.extracted, '')

        widget = factory(
            'emptyvalue_test',
            name='widget',
            props={'emptyvalue': EMPTY_VALUE}
        )
        data = widget.extract({})
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'widget': ''})
        self.assertEqual(data.extracted, EMPTY_VALUE)

        widget = factory(
            'emptyvalue_test',
            name='widget',
            props={'emptyvalue': 'EMPTY'}
        )
        data = widget.extract({})
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'widget': ''})
        self.assertEqual(data.extracted, 'EMPTY')

    def test_DatatypeConverter(self):
        from yafowil.datatypes import DatatypeConverter

        converter = DatatypeConverter()
        self.assertEqual(converter.to_form(u'"quoted"'), u'&quot;quoted&quot;')

        converter = DatatypeConverter(int)
        self.assertEqual(converter.to_form(1), '1')
        self.assertEqual(converter.to_value('1'), 1)
        self.assertEqual(converter.to_value(1), 1)
        self.assertEqual(converter.to_value(1.0), 1)

        converter = DatatypeConverter(uuid.UUID)
        uuid_ = uuid.uuid4()
        self.assertEqual(converter.to_form(uuid_), UNICODE_TYPE(uuid_))
        self.assertEqual(converter.to_value(UNICODE_TYPE(uuid_)), uuid_)
        self.assertEqual(converter.to_value(uuid_), uuid_)

    def test_BytesDatatypeConverter(self):
        from yafowil.datatypes import BytesDatatypeConverter

        converter = BytesDatatypeConverter()
        self.assertEqual(
            converter.to_form(b'\r\n\x01\x9a\x03\xff'),
            u'\\r\\n\\x01\\x9a\\x03\\xff'
        )
        self.assertEqual(
            converter.to_form(u'aaa'),
            u'aaa'
        )
        with self.assertRaises(UnicodeEncodeError):
            converter.to_value(u'ä')
        self.assertEqual(
            converter.to_value(u'\\r\\n\\x01\\x9a\\x03\\xff'),
            b'\r\n\x01\x9a\x03\xff'
        )
        self.assertEqual(
            converter.to_value(b'aaa'),
            b'aaa'
        )

    def test_UnicodeDatatypeConverter(self):
        from yafowil.datatypes import UnicodeDatatypeConverter

        converter = UnicodeDatatypeConverter()
        self.assertEqual(converter.to_value(u'äöü'), u'äöü')
        self.assertEqual(converter.to_value(b'aou'), u'aou')

    def test_FloatDatatypeConverter(self):
        from yafowil.datatypes import FloatDatatypeConverter

        converter = FloatDatatypeConverter()
        self.assertEqual(converter.to_value('1.1'), 1.1)
        self.assertEqual(converter.to_value('1,1'), 1.1)
        self.assertEqual(converter.to_value(1.1), 1.1)

    def test_lookup_datatype_converter(self):
        from yafowil.datatypes import DatatypeConverter
        converter = lookup_datatype_converter(int)
        self.assertIsInstance(converter, DatatypeConverter)
        self.assertEqual(converter.type_, int)

        from yafowil.datatypes import BytesDatatypeConverter

        converter = lookup_datatype_converter(BYTES_TYPE)
        self.assertIsInstance(converter, BytesDatatypeConverter)

        from yafowil.datatypes import UnicodeDatatypeConverter

        converter = lookup_datatype_converter(UNICODE_TYPE)
        self.assertIsInstance(converter, UnicodeDatatypeConverter)

        from yafowil.datatypes import FloatDatatypeConverter

        converter = lookup_datatype_converter(float)
        self.assertIsInstance(converter, FloatDatatypeConverter)

    def test_convert_value_to_datatype(self):
        # Unknown string identifier
        with self.assertRaises(KeyError) as arc:
            convert_value_to_datatype('val', 'inexistent')
        self.assertEqual(str(arc.exception), "'inexistent'")

        # Function returns ``EMPTY_VALUE`` marker if value is ``None`` or empty
        # string
        self.assertEqual(convert_value_to_datatype('', 'uuid'), EMPTY_VALUE)
        self.assertEqual(convert_value_to_datatype(None, 'uuid'), EMPTY_VALUE)

    def test_convert_value_to_datatype_bytes(self):
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

        converted = convert_value_to_datatype(b'unicode', 'unicode')
        self.assertEqual(converted, u'unicode')
        self.assertTrue(isinstance(converted, UNICODE_TYPE))

        # Convert to unicode by type
        self.assertEqual(convert_value_to_datatype(UNSET, UNICODE_TYPE), UNSET)

        converted = convert_value_to_datatype(b'unicode', UNICODE_TYPE)
        self.assertEqual(converted, u'unicode')
        self.assertTrue(isinstance(converted, UNICODE_TYPE))

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

    def test_datatype_extractor(self):
        # No datatype given, no datatype conversion happens at all
        widget = factory(
            'text',
            name='MYFIELD',
            value='')
        data = widget.extract({'MYFIELD': u''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, '')

        # Test emptyvalue if ``str`` datatype set
        widget = factory(
            'text',
            name='MYDATATYPEFIELD',
            value='',
            props={
                'datatype': 'str',
            })

        # Default emptyvalue
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, EMPTY_VALUE)

        # None emptyvalue
        widget.attrs['emptyvalue'] = None
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, None)

        # UNSET emptyvalue
        widget.attrs['emptyvalue'] = UNSET
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        # String emptyvalue
        widget.attrs['emptyvalue'] = 'abc'
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, b'abc')

        # Unicode emptyvalue
        widget.attrs['emptyvalue'] = u''
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        # Test emptyvalue if ``int`` datatype set
        widget = factory(
            'text',
            name='MYDATATYPEFIELD',
            value='',
            props={
                'datatype': 'int',
            })

        # Default emptyvalue
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, EMPTY_VALUE)

        # None emptyvalue
        widget.attrs['emptyvalue'] = None
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, None)

        # UNSET emptyvalue
        widget.attrs['emptyvalue'] = UNSET
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        # Int emptyvalue
        widget.attrs['emptyvalue'] = -1
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, -1)

        # String emptyvalue. If convertable still fine
        widget.attrs['emptyvalue'] = '0'
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, 0)

        # Test emptyvalue if ``long`` datatype set
        widget = factory(
            'text',
            name='MYDATATYPEFIELD',
            value='',
            props={
                'datatype': 'long',
            })

        # Default emptyvalue
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, EMPTY_VALUE)

        # None emptyvalue
        widget.attrs['emptyvalue'] = None
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, None)

        # UNSET emptyvalue
        widget.attrs['emptyvalue'] = UNSET
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        # Int emptyvalue
        widget.attrs['emptyvalue'] = -1
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, LONG_TYPE(-1))

        # String emptyvalue. If convertable still fine
        widget.attrs['emptyvalue'] = '0'
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, LONG_TYPE(0))

        # Test emptyvalue if ``float`` datatype set
        widget = factory(
            'text',
            name='MYDATATYPEFIELD',
            value='',
            props={
                'datatype': 'float',
            })

        # Default emptyvalue
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, EMPTY_VALUE)

        # None emptyvalue
        widget.attrs['emptyvalue'] = None
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, None)

        # UNSET emptyvalue
        widget.attrs['emptyvalue'] = UNSET
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        # Float emptyvalue
        widget.attrs['emptyvalue'] = 0.1
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, 0.1)

        # String emptyvalue. If convertable still fine
        widget.attrs['emptyvalue'] = '0,2'
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, 0.2)

        # Test emptyvalue if ``uuid`` datatype set
        widget = factory(
            'text',
            name='MYDATATYPEFIELD',
            value='',
            props={
                'datatype': 'uuid',
            })

        # Default emptyvalue
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, EMPTY_VALUE)

        # None emptyvalue
        widget.attrs['emptyvalue'] = None
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, None)

        # UNSET emptyvalue
        widget.attrs['emptyvalue'] = UNSET
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        # UUID emptyvalue
        uid = uuid.uuid4()
        widget.attrs['emptyvalue'] = uid
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, uid)

        # String emptyvalue. If convertable still fine
        widget.attrs['emptyvalue'] = str(uid)
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, uid)

        # Integer datatype
        widget = factory(
            'text',
            name='MYDATATYPEFIELD',
            value='',
            props={
                'datatype': 'int',
            })
        data = widget.extract({'MYDATATYPEFIELD': '1'})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, 1)

        data = widget.extract({'MYDATATYPEFIELD': 'a'})
        self.assertEqual(
            data.errors,
            [ExtractionError('Input is not a valid integer.')]
        )

        # Float extraction
        widget = factory(
            'text',
            name='MYDATATYPEFIELD',
            value='',
            props={
                'datatype': 'float',
            })
        data = widget.extract({'MYDATATYPEFIELD': '1.2'})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, 1.2)

        data = widget.extract({'MYDATATYPEFIELD': 'a'})
        self.assertEqual(
            data.errors,
            [ExtractionError('Input is not a valid floating point number.')]
        )

        # UUID extraction
        widget = factory(
            'text',
            name='MYDATATYPEFIELD',
            value='',
            props={
                'datatype': 'uuid',
            })
        data = widget.extract({
            'MYDATATYPEFIELD': '3b8449f3-0456-4baa-a670-3066b0fcbda0'
        })
        self.assertEqual(data.errors, [])
        self.assertEqual(
            data.extracted,
            uuid.UUID('3b8449f3-0456-4baa-a670-3066b0fcbda0')
        )

        data = widget.extract({'MYDATATYPEFIELD': 'a'})
        self.assertEqual(
            data.errors,
            [ExtractionError('Input is not a valid UUID.')]
        )

        # Test ``datatype`` not allowed
        widget = factory(
            'text',
            name='MYDATATYPEFIELD',
            value='',
            props={
                'datatype': 'uuid',
                'allowed_datatypes': [int],
            })

        request = {
            'MYDATATYPEFIELD': '3b8449f3-0456-4baa-a670-3066b0fcbda0'
        }
        with self.assertRaises(ValueError) as arc:
            widget.extract(request)
        self.assertEqual(str(arc.exception), 'Datatype not allowed: "uuid"')

        # Test ``datatype_message``
        widget = factory(
            'text',
            name='MYDATATYPEFIELD',
            value='',
            props={
                'datatype': int,
                'datatype_message': 'This did not work'
            })
        request = {
            'MYDATATYPEFIELD': 'a'
        }
        data = widget.extract(request)
        self.assertEqual(data.errors, [ExtractionError('This did not work')])
        self.assertEqual(data.extracted, 'a')

        # Test default error message if custom converter given but no
        # ``datatype_message`` defined
        def custom_converter(val):
            raise ValueError

        widget = factory(
            'text',
            name='MYDATATYPEFIELD',
            value='',
            props={
                'datatype': custom_converter,
            })
        request = {
            'MYDATATYPEFIELD': 'a'
        }
        data = widget.extract(request)
        self.assertEqual(
            data.errors,
            [ExtractionError('Input conversion failed.')]
        )
        self.assertEqual(data.extracted, 'a')

        # Test unknown string ``datatype`` identifier
        widget = factory(
            'text',
            name='MYDATATYPEFIELD',
            value='',
            props={
                'datatype': 'inexistent',
            })
        with self.assertRaises(ValueError) as arc:
            widget.extract({'MYDATATYPEFIELD': 'a'})
        self.assertEqual(str(arc.exception), 'Datatype unknown: "inexistent"')
