# -*- coding: utf-8 -*-

Prepare
-------

Imports::

    >>> from node.base import AttributedNode
    >>> from node.base import OrderedNode
    >>> from node.behaviors import Attributes
    >>> from node.behaviors import Nodespaces
    >>> from node.utils import UNSET
    >>> from plumber import plumbing
    >>> from yafowil.base import factory
    >>> from yafowil.utils import Tag
    >>> from yafowil.utils import attr_value
    >>> from yafowil.utils import convert_value_to_datatype
    >>> from yafowil.utils import convert_values_to_datatype
    >>> from yafowil.utils import cssclasses
    >>> from yafowil.utils import data_attrs_helper
    >>> from yafowil.utils import generic_html5_attrs
    >>> from yafowil.utils import get_entry_points
    >>> from yafowil.utils import get_example
    >>> from yafowil.utils import get_example_names
    >>> from yafowil.utils import get_plugin_names
    >>> from yafowil.utils import managedprops
    >>> from yafowil.utils import tag as deprecated_tag
    >>> from yafowil.utils import vocabulary
    >>> import uuid
    >>> import yafowil.loader


Test entry_point support tools
------------------------------

::

    >>> get_entry_points()
    [...EntryPoint.parse('register = yafowil.loader:register')...]

    >>> get_entry_points('nonexisting')
    []

    >>> get_plugin_names()
    [...'yafowil'...]

    >>> get_plugin_names('nonexisting')
    []


Test examples lookup
--------------------

::

    >>> sorted(get_example_names())
    ['yafowil'...]

    >>> factory.register_macro('field', 'field:label:error', {})

    >>> get_example('inexistent')

    >>> examples = get_example('yafowil')
    >>> examples[0]['doc']
    "Plain Text\n----------..."

    >>> examples[0]['title']
    'Plain Text'

    >>> examples[0]['widget']
    <Widget object 'yafowil-plaintext' at ...>


Test the Vocabulary
-------------------

::

    >>> vocabulary('foo')
    [('foo', 'foo')]

    >>> vocabulary({'key': 'value'})
    [('key', 'value')]

    >>> vocabulary(['value', 'value2'])
    [('value', 'value'), ('value2', 'value2')]

    >>> vocabulary([('key', 'value'), ('key2', 'value2', 'v2.3'), ('key3',)])
    [('key', 'value'), ('key2', 'value2'), ('key3', 'key3')]

    >>> def callme():
    ...     return 'bar'

    >>> vocabulary(callme)
    [('bar', 'bar')]

    >>> vocabulary(None) is None
    True


Test Tag renderer
-----------------

::

    >>> tag = Tag(lambda msg: msg)
    >>> a = {'class': u'fancy', 'id': '2f5b8a234ff'}
    >>> tag('p', 'Lorem Ipsum. ', u'Hello World!',
    ...     class_='fancy', id='2f5b8a234ff')
    u'<p class="fancy" id="2f5b8a234ff">Lorem Ipsum. Hello World!</p>'

    >>> tag('dummy', name='foo', **{'data-foo': 'bar'})
     u'<dummy data-foo=\'bar\' name="foo" />'

    >>> tag('dummy', name=None)
    u'<dummy />'

    >>> tag('dummy', name=UNSET)
    u'<dummy />'

deprecated test::

    >>> deprecated_tag('div', 'foo')
    u'<div>foo</div>'


Test CSS Classes
----------------

::

    >>> @plumbing(Nodespaces, Attributes)
    ... class CSSTestNode(OrderedNode):
    ...     pass

    >>> widget = CSSTestNode()
    >>> widget.attrs['required'] = False
    >>> widget.attrs['required_class'] = None
    >>> widget.attrs['required_class_default'] = 'required'
    >>> widget.attrs['error_class'] = None
    >>> widget.attrs['error_class_default'] = 'error'
    >>> widget.attrs['class'] = None
    >>> widget.attrs['class_add'] = None

    >>> class DummyData(object):
    ...     def __init__(self):
    ...         self.errors = []

    >>> data = DummyData()

    >>> print cssclasses(widget, data)
    None

    >>> widget.attrs['class'] = 'foo bar'
    >>> print cssclasses(widget, data)
    bar foo

    >>> widget.attrs['class'] = None
    >>> widget.attrs['required'] = True
    >>> print cssclasses(widget, data)
    None

    >>> widget.required = False
    >>> data.errors = True
    >>> print cssclasses(widget, data)
    None

    >>> widget.attrs['error_class'] = True
    >>> print cssclasses(widget, data)
    error

    >>> widget.attrs['class'] = 'foo bar'
    >>> print cssclasses(widget, data)
    bar error foo

    >>> widget.attrs['class'] = lambda w, d: 'baz'
    >>> print cssclasses(widget, data)
    baz error

    >>> widget.attrs['class_add'] = lambda w, d: 'addclass_from_callable'
    >>> print cssclasses(widget, data)
    addclass_from_callable baz error

    >>> widget.attrs['class_add'] = 'addclass'
    >>> print cssclasses(widget, data)
    addclass baz error

    >>> widget.attrs['class'] = None
    >>> widget.attrs['class_add'] = None
    >>> widget.attrs['error_class'] = 'othererror'
    >>> print cssclasses(widget, data)
    othererror

    >>> data.errors = False
    >>> print cssclasses(widget, data)
    None

    >>> widget.attrs['required'] = True
    >>> print cssclasses(widget, data)
    None

    >>> widget.attrs['required_class'] = True
    >>> print cssclasses(widget, data)
    required

    >>> widget.attrs['required_class'] = 'otherrequired'
    >>> print cssclasses(widget, data)
    otherrequired

    >>> widget.attrs['error_class'] = True
    >>> data.errors = True
    >>> widget.attrs['required_class'] = 'required'
    >>> print cssclasses(widget, data)
    error required

    >>> widget.attrs['class'] = 'foo bar'
    >>> print cssclasses(widget, data)
    bar error foo required

    >>> print cssclasses(widget, data, additional=['zika', 'akiz'])
    akiz bar error foo required zika


Test managedprops annotation
----------------------------

::

    >>> @managedprops('foo', 'bar')
    ... def somefunc(a, b, c):
    ...     return a, b, c

    >>> somefunc(1, 2, 3)
    (1, 2, 3)

    >>> somefunc.__yafowil_managed_props__
    ('foo', 'bar')


Test attr_value
---------------

::

    >>> widget = AttributedNode()
    >>> data = AttributedNode()

    >>> widget.attrs['attr'] = 'value'
    >>> attr_value('attr', widget, data)
    'value'

    >>> def func_callback(widget, data):
    ...     return 'func_callback value'

    >>> widget.attrs['attr'] = func_callback
    >>> attr_value('attr', widget, data)
    'func_callback value'

    >>> def failing_func_callback(widget, data):
    ...     raise Exception('failing_func_callback')

    >>> widget.attrs['attr'] = failing_func_callback
    >>> attr_value('attr', widget, data)
    Traceback (most recent call last):
      ...
    Exception: failing_func_callback

    >>> def bc_func_callback():
    ...     return 'bc_func_callback value'

    >>> widget.attrs['attr'] = bc_func_callback
    >>> attr_value('attr', widget, data)
    'bc_func_callback value'

    >>> def failing_bc_func_callback():
    ...     raise Exception('failing_bc_func_callback')

    >>> widget.attrs['attr'] = failing_bc_func_callback
    >>> attr_value('attr', widget, data)
    Traceback (most recent call last):
      ...
    Exception: failing_bc_func_callback

    >>> class FormContext(object):
    ...     def instance_callback(self, widget, data):
    ...         return 'instance_callback'
    ...
    ...     def failing_instance_callback(self, widget, data):
    ...         raise Exception('failing_instance_callback')
    ...
    ...     def instance_bc_callback(self):
    ...         return 'instance_bc_callback'
    ...
    ...     def failing_instance_bc_callback(self, widget, data):
    ...         raise Exception('failing_instance_bc_callback')

    >>> context = FormContext()
    >>> widget.attrs['attr'] = context.instance_callback
    >>> attr_value('attr', widget, data)
    'instance_callback'

    >>> widget.attrs['attr'] = context.failing_instance_callback
    >>> attr_value('attr', widget, data)
    Traceback (most recent call last):
      ...
    Exception: failing_instance_callback

    >>> widget.attrs['attr'] = context.instance_bc_callback
    >>> attr_value('attr', widget, data)
    'instance_bc_callback'

    >>> widget.attrs['attr'] = context.failing_instance_bc_callback
    >>> attr_value('attr', widget, data)
    Traceback (most recent call last):
      ...
    Exception: failing_instance_bc_callback


Test generic_html5_attrs
------------------------

::

    >>> generic_html5_attrs({
    ...     'foo': 'bar',
    ...     'baz': ['bam'],
    ...     'nada': None,
    ...     'unset': UNSET
    ... })
    {'data-baz': '["bam"]', 'data-foo': 'bar'}


Test data_attrs_helper
----------------------

::

    >>> widget = AttributedNode()
    >>> data = AttributedNode()

    >>> widget.attrs['testattr1'] = 'value'
    >>> widget.attrs['testattr2'] = True
    >>> widget.attrs['testattr3'] = False
    >>> widget.attrs['testattr4'] = None
    >>> widget.attrs['testattr5'] = ['item1', 'item2', 'item3']
    >>> widget.attrs['testattr6'] = {
    ...     'key1': 'item1',
    ...     'key2': 'item2',
    ...     'key3': 'item3'
    ... }
    >>> widget.attrs['testattr7'] = 1234
    >>> widget.attrs['testattr8'] = 1234.5678
    >>> widget.attrs['camelAttrName'] = 'camelValue'

    >>> data_attrs_keys = [
    ...     'testattr1', 'testattr2', 'testattr3', 'testattr4', 'testattr5',
    ...     'testattr6', 'testattr7', 'testattr8', 'camelAttrName'
    ... ]
    >>> data_attrs = data_attrs_helper(widget, data, data_attrs_keys)

    >>> data_attrs['data-testattr1']
    'value'

    >>> data_attrs['data-testattr2']
    'true'

    >>> data_attrs['data-testattr3']
    'false'

    >>> 'data-testattr4' in data_attrs
    False

    >>> data_attrs['data-testattr5']
    '["item1", "item2", "item3"]'

    >>> data_attrs['data-testattr6']
    '{"key3": "item3", "key2": "item2", "key1": "item1"}'

    >>> data_attrs['data-testattr7']
    '1234'

    >>> data_attrs['data-testattr8']
    '1234.5678'

    >>> data_attrs['data-camel-attr-name']
    'camelValue'

Test with Tag renderer::

    >>> tag = Tag(lambda msg: msg)
    >>> tag('dummy', name='foo', **data_attrs)
    u'<dummy data-camel-attr-name=\'camelValue\' data-testattr1=\'value\' 
    data-testattr2=\'true\' data-testattr3=\'false\' 
    data-testattr5=\'["item1", "item2", "item3"]\' 
    data-testattr6=\'{"key3": "item3", "key2": "item2", "key1": "item1"}\' 
    data-testattr7=\'1234\' data-testattr8=\'1234.5678\' name="foo" />'


Test convert_value_to_datatype
------------------------------

Unknown string identifier::

    >>> convert_value_to_datatype('val', 'inexistent')
    Traceback (most recent call last):
      ...
    KeyError: 'inexistent'

Function returns ``EMPTY_VALUE`` marker if value is ``None`` or empty string::

    >>> convert_value_to_datatype('', 'uuid')
    <EMPTY_VALUE>

    >>> convert_value_to_datatype(None, 'uuid')
    <EMPTY_VALUE>

Convert to string::

    >>> convert_value_to_datatype(UNSET, 'str')
    <UNSET>

    >>> convert_value_to_datatype(u'string', 'str')
    'string'

    >>> convert_value_to_datatype(u'äöü', 'str')
    Traceback (most recent call last):
      ...
    UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-5: 
    ordinal not in range(128)

    >>> convert_value_to_datatype(UNSET, str)
    <UNSET>

    >>> convert_value_to_datatype(u'string', str)
    'string'

    >>> convert_value_to_datatype(u'äöü', str)
    Traceback (most recent call last):
      ...
    UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-5: 
    ordinal not in range(128)

Convert to unicode::

    >>> convert_value_to_datatype(UNSET, 'unicode')
    <UNSET>

    >>> convert_value_to_datatype('unicode', 'unicode')
    u'unicode'

    >>> convert_value_to_datatype('\xc3\xa4\xc3\xb6\xc3\xbc', 'unicode')
    Traceback (most recent call last):
      ...
    UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 0: 
    ordinal not in range(128)

    >>> convert_value_to_datatype(UNSET, unicode)
    <UNSET>

    >>> convert_value_to_datatype('unicode', unicode)
    u'unicode'

    >>> convert_value_to_datatype('\xc3\xa4\xc3\xb6\xc3\xbc', unicode)
    Traceback (most recent call last):
      ...
    UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 0: 
    ordinal not in range(128)

Convert to int::

    >>> convert_value_to_datatype(UNSET, 'int')
    <UNSET>

    >>> convert_value_to_datatype('1', 'int')
    1

    >>> convert_value_to_datatype('1.0', 'int')
    Traceback (most recent call last):
      ...
    ValueError: invalid literal for int() with base 10: '1.0'

    >>> convert_value_to_datatype('a', 'int')
    Traceback (most recent call last):
      ...
    ValueError: invalid literal for int() with base 10: 'a'

    >>> convert_value_to_datatype(1.0, 'int')
    1

    >>> convert_value_to_datatype(UNSET, int)
    <UNSET>

    >>> convert_value_to_datatype('1', int)
    1

    >>> convert_value_to_datatype('1.0', int)
    Traceback (most recent call last):
      ...
    ValueError: invalid literal for int() with base 10: '1.0'

    >>> convert_value_to_datatype('a', int)
    Traceback (most recent call last):
      ...
    ValueError: invalid literal for int() with base 10: 'a'

    >>> convert_value_to_datatype(1.0, int)
    1

Convert to long::

    >>> convert_value_to_datatype(UNSET, 'long')
    <UNSET>

    >>> convert_value_to_datatype('1', 'long')
    1L

    >>> convert_value_to_datatype(1.0, 'long')
    1L

    >>> convert_value_to_datatype('a', 'long')
    Traceback (most recent call last):
      ...
    ValueError: invalid literal for long() with base 10: 'a'

    >>> convert_value_to_datatype(UNSET, long)
    <UNSET>

    >>> convert_value_to_datatype('1', long)
    1L

    >>> convert_value_to_datatype(1.0, long)
    1L

    >>> convert_value_to_datatype('a', long)
    Traceback (most recent call last):
      ...
    ValueError: invalid literal for long() with base 10: 'a'

Convert to float::

    >>> convert_value_to_datatype(UNSET, 'float')
    <UNSET>

    >>> convert_value_to_datatype('1,0', 'float')
    1.0

    >>> convert_value_to_datatype('1', 'float')
    1.0

    >>> convert_value_to_datatype('a', 'float')
    Traceback (most recent call last):
      ...
    ValueError: could not convert string to float: a

    >>> convert_value_to_datatype(1, 'float')
    1.0

    >>> convert_value_to_datatype(UNSET, float)
    <UNSET>

    >>> convert_value_to_datatype('1,0', float)
    1.0

    >>> convert_value_to_datatype('1', float)
    1.0

    >>> convert_value_to_datatype('a', float)
    Traceback (most recent call last):
      ...
    ValueError: could not convert string to float: a

    >>> convert_value_to_datatype(1, float)
    1.0

Convert to uuid::

    >>> convert_value_to_datatype(UNSET, 'uuid')
    <UNSET>

    >>> convert_value_to_datatype(str(uuid.uuid4()), 'uuid')
    UUID('...')

    >>> convert_value_to_datatype('a', 'uuid')
    Traceback (most recent call last):
      ...
    ValueError: badly formed hexadecimal UUID string

    >>> convert_value_to_datatype(UNSET, uuid.UUID)
    <UNSET>

    >>> convert_value_to_datatype(str(uuid.uuid4()), uuid.UUID)
    UUID('...')

    >>> convert_value_to_datatype('a', uuid.UUID)
    Traceback (most recent call last):
      ...
    ValueError: badly formed hexadecimal UUID string

Custom converter as function::

    >>> def convert_func(val):
    ...     if val == 'a':
    ...         return 'convertet: {0}'.format(val)
    ...     raise ValueError("Value not 'a'")

    >>> convert_value_to_datatype('a', convert_func)
    'convertet: a'

    >>> convert_value_to_datatype('b', convert_func)
    Traceback (most recent call last):
      ...
    ValueError: Value not 'a'

Custom converters as class::

    >>> class Converter(object):
    ... 
    ...     def __init__(self, val):
    ...         if val != 'a':
    ...             raise ValueError("Value not 'a'")
    ... 
    ...     def __repr__(self):
    ...         return '<Converter instance>'

    >>> convert_value_to_datatype('a', Converter)
    <Converter instance>

    >>> convert_value_to_datatype('b', Converter)
    Traceback (most recent call last):
      ...
    ValueError: Value not 'a'

Custom converter as class instance with ``__call__`` function::

    >>> class ConverterInst(object):
    ... 
    ...     def __call__(self, val):
    ...         if val != 'a':
    ...             raise ValueError("Value not 'a'")
    ...         return 'convertet: {0}'.format(val)

    >>> convert_value_to_datatype('a', ConverterInst())
    'convertet: a'

    >>> convert_value_to_datatype('b', ConverterInst())
    Traceback (most recent call last):
      ...
    ValueError: Value not 'a'


Test convert_values_to_datatype
-------------------------------

::

    >>> convert_values_to_datatype(UNSET, 'int')
    <UNSET>

    >>> convert_values_to_datatype([UNSET], 'int')
    [<UNSET>]

    >>> convert_values_to_datatype('0', int)
    0

    >>> convert_values_to_datatype(['0', '1'], int)
    [0, 1]
