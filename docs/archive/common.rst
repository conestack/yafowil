# -*- coding: utf-8 -*-

Common Blueprints
=================

This test creates widgets from ist blueprints with different properties.


Prepare
-------

Imports::

    >>> from StringIO import StringIO
    >>> from node.utils import UNSET
    >>> from yafowil.base import factory
    >>> from yafowil.common import convert_bytes
    >>> from yafowil.persistence import write_mapping_writer
    >>> from yafowil.utils import EMPTY_VALUE
    >>> from yafowil.utils import Tag
    >>> import uuid

Helpers::

    >>> tag = Tag(lambda msg: msg)

    >>> def wrapped_pxml(value):
    ...     pxml(u'<div>' + value + u'</div>')

Hidden
------

Hidden input widget::

    >>> widget = factory(
    ...     'hidden',
    ...     name='MYHIDDEN',
    ...     value='Test Hidden')
    >>> widget()
    u'<input class="hidden" id="input-MYHIDDEN" name="MYHIDDEN" type="hidden"
    value="Test Hidden" />'

Display mode of hidden widget renders empty string.::

    >>> widget = factory(
    ...     'hidden',
    ...     name='MYHIDDEN',
    ...     value='Test Hidden',
    ...     mode='display')
    >>> widget()
    u''

As well does skip mode::

    >>> widget = factory(
    ...     'hidden',
    ...     name='MYHIDDEN',
    ...     value='Test Hidden',
    ...     mode='skip')
    >>> widget()
    u''

Generic HTML5 Data::

    >>> widget = factory(
    ...     'hidden',
    ...     name='MYHIDDEN',
    ...     value='Test Hidden',
    ...     props={
    ...         'data':{
    ...             'foo': 'bar'
    ...         }
    ...     })
    >>> widget()
    u'<input class="hidden" data-foo=\'bar\' id="input-MYHIDDEN" 
    name="MYHIDDEN" type="hidden" value="Test Hidden" />'

Emptyvalue::

    >>> widget = factory(
    ...     'hidden',
    ...     name='MYHIDDEN',
    ...     props={
    ...         'emptyvalue': 'EMPTYVALUE'
    ...     })
    >>> widget.extract(request={'MYHIDDEN': ''})
    <RuntimeData MYHIDDEN, value=<UNSET>, extracted='EMPTYVALUE' at ...>

Datatype::

    >>> widget = factory(
    ...     'hidden',
    ...     name='MYHIDDEN',
    ...     props={
    ...         'emptyvalue': 0,
    ...         'datatype': int
    ...     })
    >>> widget.extract(request={'MYHIDDEN': ''})
    <RuntimeData MYHIDDEN, value=<UNSET>, extracted=0 at ...>

Default emptyvalue extraction::

    >>> del widget.attrs['emptyvalue']
    >>> widget.extract(request={'MYHIDDEN': ''})
    <RuntimeData MYHIDDEN, value=<UNSET>, extracted=<EMPTY_VALUE> at ...>

Persist property::

    >>> widget = factory(
    ...     'hidden',
    ...     name='MYHIDDEN',
    ...     props={
    ...         'emptyvalue': 0,
    ...         'datatype': int,
    ...         'persist_writer': write_mapping_writer,
    ...     })
    >>> data = widget.extract(request={'MYHIDDEN': '10'})
    >>> model = dict()
    >>> data.write(model)
    >>> model
    {'MYHIDDEN': 10}

    >>> data.persist_target = 'myhidden'
    >>> model = dict()
    >>> data.write(model)
    >>> model
    {'myhidden': 10}


Generic tag
-----------

Custom tag widget::

    >>> widget = factory(
    ...     'tag',
    ...     name='MYTAG',
    ...     props={
    ...         'tag': 'h3',
    ...         'text': 'A Headline',
    ...         'class': 'form_heading'
    ...     })
    >>> widget()
    u'<h3 class="form_heading" id="tag-MYTAG">A Headline</h3>'

Skip tag::

    >>> widget = factory(
    ...     'tag',
    ...     name='MYTAG',
    ...     props={
    ...         'tag': 'h3',
    ...         'text': 'A Headline',
    ...         'class': 'form_heading'
    ...     },
    ...     mode='skip')
    >>> widget()
    u''


Text Input
----------

Regular text input::

    >>> widget = factory(
    ...     'text',
    ...     name='MYTEXT',
    ...     value='Test Text "Some Text"')
    >>> widget()
    u'<input class="text" id="input-MYTEXT" name="MYTEXT" type="text" 
    value="Test Text &quot;Some Text&quot;" />'

    >>> widget.mode = 'display'
    >>> widget()
    u'<div class="display-text" id="display-MYTEXT">Test Text "Some Text"</div>'

Render with title attribute::

    >>> widget = factory(
    ...     'text',
    ...     name='MYTEXT',
    ...     value='ja ha!',
    ...     props={
    ...         'title': 'My awesome title'
    ...     })
    >>> widget()
    u'<input class="text" id="input-MYTEXT" name="MYTEXT" 
    title="My awesome title" type="text" value="ja ha!" />'

Generic HTML5 Data::

    >>> widget = factory(
    ...     'text',
    ...     name='MYTEXT',
    ...     value='ja ha!',
    ...     props={
    ...         'title': 'My awesome title',
    ...         'data': {'foo': 'bar'}
    ...     })
    >>> widget()
    u'<input class="text" data-foo=\'bar\' id="input-MYTEXT" 
    name="MYTEXT" title="My awesome title" type="text" value="ja ha!" />'

Extract and persist::

    >>> widget = factory(
    ...     'text',
    ...     name='MYTEXT',
    ...     props={
    ...         'persist_writer': write_mapping_writer
    ...     })
    >>> data = widget.extract(request={'MYTEXT': '10'})
    >>> data
    <RuntimeData MYTEXT, value=<UNSET>, extracted='10' at ...>

    >>> model = dict()
    >>> data.write(model)
    >>> model
    {'MYTEXT': '10'}


Empty values
------------

::

    >>> widget = factory(
    ...     'text',
    ...     name='MYTEXT',
    ...     props={
    ...         'title': 'Default tests',
    ...         'data': {'foo': 'bar'},
    ...         'default': 'defaultvalue'
    ...     })
    >>> widget()
    u'<input class="text" data-foo=\'bar\' id="input-MYTEXT" name="MYTEXT" 
    title="Default tests" type="text" value="defaultvalue" />'

    >>> data = widget.extract(request={})
    >>> data.extracted
    <UNSET>

    >>> data = widget.extract(request={'MYTEXT': ''})
    >>> data.extracted
    ''

    >>> widget.attrs['emptyvalue'] = 'emptyvalue'
    >>> data = widget.extract(request={'MYTEXT': ''})
    >>> data.extracted
    'emptyvalue'

    >>> widget.attrs['emptyvalue'] = False
    >>> data = widget.extract(request={})
    >>> data.extracted
    <UNSET>

    >>> data = widget.extract(request={'MYTEXT': ''})
    >>> data.extracted
    False

    >>> widget.attrs['emptyvalue'] = UNSET
    >>> data = widget.extract(request={})
    >>> data.extracted
    <UNSET>

    >>> data = widget.extract(request={'MYTEXT': ''})
    >>> data.extracted
    <UNSET>


Autofocus Text Input
--------------------

Widget with autofocus property::

    >>> widget = factory(
    ...     'text',
    ...     name='AUTOFOCUS',
    ...     value='',
    ...     props={
    ...         'autofocus': True
    ...     })
    >>> widget()
    u'<input autofocus="autofocus" class="text" id="input-AUTOFOCUS"
    name="AUTOFOCUS" type="text" value="" />'


Placeholder Text Input
----------------------

Widget with placeholder property::

    >>> widget = factory(
    ...     'text',
    ...     name='PLACEHOLDER',
    ...     value='',
    ...     props={
    ...         'placeholder': 'This is a placeholder.'
    ...     })
    >>> widget()
    u'<input class="text" id="input-PLACEHOLDER" name="PLACEHOLDER"
    placeholder="This is a placeholder." type="text" value="" />'


Required Input
--------------

Widget with requires input::

    >>> widget = factory(
    ...     'text',
    ...     name='REQUIRED',
    ...     value='',
    ...     props={
    ...         'required': True,
    ...         'error_class': True
    ...     })
    >>> widget()
    u'<input class="required text" id="input-REQUIRED" name="REQUIRED"
    required="required" type="text" value="" />'

Extract with empty request, key not in request therefore no error::

    >>> data = widget.extract({})
    >>> data
    <RuntimeData REQUIRED, value='', extracted=<UNSET> at ...>

Extract with empty input sent, required error expected::

    >>> data = widget.extract({'REQUIRED': ''})
    >>> data
    <RuntimeData REQUIRED, value='', extracted='', 1 error(s) at ...>

    >>> data.errors
    [ExtractionError('Mandatory field was empty',)]

With getter value set, empty request, no error expected::

    >>> widget = factory(
    ...     'text',
    ...     name='REQUIRED',
    ...     value='Test Text',
    ...     props={
    ...         'required': True,
    ...         'error_class': True
    ...     })
    >>> data = widget.extract({})
    >>> data
    <RuntimeData REQUIRED, value='Test Text', extracted=<UNSET> at ...>

    >>> widget(data=data)
    u'<input class="required text" id="input-REQUIRED" name="REQUIRED"
    required="required" type="text" value="Test Text" />'

With getter value set, request given, error expected::

    >>> data = widget.extract({'REQUIRED': ''})
    >>> data
    <RuntimeData REQUIRED, value='Test Text', extracted='', 1 error(s) at ...>

    >>> widget(data=data)
    u'<input class="error required text" id="input-REQUIRED" name="REQUIRED"
    required="required" type="text" value="" />'

Create a custom error message::

    >>> widget = factory(
    ...     'text',
    ...     name='REQUIRED',
    ...     value='',
    ...     props={
    ...         'required': 'You fool, fill in a value!'
    ...     })
    >>> data = widget.extract({'REQUIRED': ''})
    >>> data
    <RuntimeData REQUIRED, value='', extracted='', 1 error(s) at ...>

    >>> data.errors
    [ExtractionError('You fool, fill in a value!',)]

``required`` property could be a callable as well::

    >>> def required_callback(widget, data):
    ...     return u"Foooo"
    >>> widget = factory(
    ...     'text',
    ...     name='REQUIRED',
    ...     value='',
    ...     props={
    ...         'required': required_callback
    ...     })
    >>> data = widget.extract({'REQUIRED': ''})
    >>> data.errors
    [ExtractionError('Foooo',)]


Generic display renderer
------------------------

Display mode of text widget uses ``generic_display_renderer``::

    >>> widget = factory(
    ...     'text',
    ...     name='DISPLAY',
    ...     value='lorem ipsum',
    ...     mode='display')
    >>> widget()
    u'<div class="display-text" id="display-DISPLAY">lorem ipsum</div>'

    >>> widget = factory(
    ...     'text',
    ...     name='DISPLAY',
    ...     value=123.4567890,
    ...     mode='display',
    ...     props={
    ...         'template': '%0.3f'
    ...     })
    >>> widget()
    u'<div class="display-text" id="display-DISPLAY">123.457</div>'

    >>> def mytemplate(widget, data):
    ...     return '<TEMPLATE>%s</TEMPLATE>' % data.value
    >>> widget = factory(
    ...     'text',
    ...     name='DISPLAY',
    ...     value='lorem ipsum',
    ...     mode='display',
    ...     props={
    ...         'template': mytemplate
    ...     })
    >>> pxml(widget())
    <div class="display-text" id="display-DISPLAY">
      <TEMPLATE>lorem ipsum</TEMPLATE>
    </div>
    <BLANKLINE>

``display_proxy`` can be used if mode is 'display' to proxy the value in a
hidden field::

    >>> widget = factory(
    ...     'text',
    ...     name='DISPLAY',
    ...     value='lorem ipsum',
    ...     mode='display',
    ...     props={
    ...         'display_proxy': True
    ...     })
    >>> wrapped_pxml(widget())
    <div>
      <div class="display-text" id="display-DISPLAY">lorem ipsum</div>
      <input class="text" id="input-DISPLAY" name="DISPLAY" type="hidden" 
        value="lorem ipsum"/>
    </div>
    <BLANKLINE>

On widgets with display mode display_proxy property set, the data gets
extracted::

    >>> widget.extract(request={'DISPLAY': 'lorem ipsum'})
    <RuntimeData DISPLAY, value='lorem ipsum', extracted='lorem ipsum' at ...>

Skip mode renders empty string.::

    >>> widget = factory(
    ...     'text',
    ...     name='SKIP',
    ...     value='lorem ipsum',
    ...     mode='skip')
    >>> widget()
    u''


Datatype extraction
-------------------

No datatype given, no datatype conversion happens at all::

    >>> widget = factory(
    ...     'text',
    ...     name='MYFIELD',
    ...     value='')
    >>> data = widget.extract({'MYFIELD': u''})
    >>> data.errors, data.extracted
    ([], u'')

Test emptyvalue if ``str`` datatype set::

    >>> widget = factory(
    ...     'text',
    ...     name='MYDATATYPEFIELD',
    ...     value='',
    ...     props={
    ...         'datatype': 'str',
    ...     })

Default emptyvalue::

    >>> data = widget.extract({})
    >>> data.errors, data.extracted
    ([], <UNSET>)

    >>> data = widget.extract({'MYDATATYPEFIELD': ''})
    >>> data.errors, data.extracted
    ([], <EMPTY_VALUE>)

None emptyvalue::

    >>> widget.attrs['emptyvalue'] = None
    >>> data = widget.extract({})
    >>> data.errors, data.extracted
    ([], <UNSET>)

    >>> data = widget.extract({'MYDATATYPEFIELD': ''})
    >>> data.errors, data.extracted
    ([], None)

UNSET emptyvalue::

    >>> widget.attrs['emptyvalue'] = UNSET
    >>> data = widget.extract({})
    >>> data.errors, data.extracted
    ([], <UNSET>)

    >>> data = widget.extract({'MYDATATYPEFIELD': ''})
    >>> data.errors, data.extracted
    ([], <UNSET>)

String emptyvalue::

    >>> widget.attrs['emptyvalue'] = 'abc'
    >>> data.errors, data.extracted
    ([], <UNSET>)

    >>> data = widget.extract({'MYDATATYPEFIELD': ''})
    >>> data.errors, data.extracted
    ([], 'abc')

Unicode emptyvalue::

    >>> widget.attrs['emptyvalue'] = u''
    >>> data = widget.extract({})
    >>> data.errors, data.extracted
    ([], <UNSET>)

Test emptyvalue if ``int`` datatype set::

    >>> widget = factory(
    ...     'text',
    ...     name='MYDATATYPEFIELD',
    ...     value='',
    ...     props={
    ...         'datatype': 'int',
    ...     })

Default emptyvalue::

    >>> data = widget.extract({})
    >>> data.errors, data.extracted
    ([], <UNSET>)

    >>> data = widget.extract({'MYDATATYPEFIELD': ''})
    >>> data.errors, data.extracted
    ([], <EMPTY_VALUE>)

None emptyvalue::

    >>> widget.attrs['emptyvalue'] = None
    >>> data = widget.extract({})
    >>> data.errors, data.extracted
    ([], <UNSET>)

    >>> data = widget.extract({'MYDATATYPEFIELD': ''})
    >>> data.errors, data.extracted
    ([], None)

UNSET emptyvalue::

    >>> widget.attrs['emptyvalue'] = UNSET
    >>> data = widget.extract({})
    >>> data.errors, data.extracted
    ([], <UNSET>)

    >>> data = widget.extract({'MYDATATYPEFIELD': ''})
    >>> data.errors, data.extracted
    ([], <UNSET>)

Int emptyvalue::

    >>> widget.attrs['emptyvalue'] = -1
    >>> data = widget.extract({})
    >>> data.errors, data.extracted
    ([], <UNSET>)

    >>> data = widget.extract({'MYDATATYPEFIELD': ''})
    >>> data.errors, data.extracted
    ([], -1)

String emptyvalue. If convertable still fine::

    >>> widget.attrs['emptyvalue'] = '0'
    >>> data = widget.extract({})
    >>> data.errors, data.extracted
    ([], <UNSET>)

    >>> data = widget.extract({'MYDATATYPEFIELD': ''})
    >>> data.errors, data.extracted
    ([], 0)

Test emptyvalue if ``long`` datatype set::

    >>> widget = factory(
    ...     'text',
    ...     name='MYDATATYPEFIELD',
    ...     value='',
    ...     props={
    ...         'datatype': 'long',
    ...     })

Default emptyvalue::

    >>> data = widget.extract({})
    >>> data.errors, data.extracted
    ([], <UNSET>)

    >>> data = widget.extract({'MYDATATYPEFIELD': ''})
    >>> data.errors, data.extracted
    ([], <EMPTY_VALUE>)

None emptyvalue::

    >>> widget.attrs['emptyvalue'] = None
    >>> data = widget.extract({})
    >>> data.errors, data.extracted
    ([], <UNSET>)

    >>> data = widget.extract({'MYDATATYPEFIELD': ''})
    >>> data.errors, data.extracted
    ([], None)

UNSET emptyvalue::

    >>> widget.attrs['emptyvalue'] = UNSET
    >>> data = widget.extract({})
    >>> data.errors, data.extracted
    ([], <UNSET>)

    >>> data = widget.extract({'MYDATATYPEFIELD': ''})
    >>> data.errors, data.extracted
    ([], <UNSET>)

Int emptyvalue::

    >>> widget.attrs['emptyvalue'] = -1
    >>> data = widget.extract({})
    >>> data.errors, data.extracted
    ([], <UNSET>)

    >>> data = widget.extract({'MYDATATYPEFIELD': ''})
    >>> data.errors, data.extracted
    ([], -1L)

String emptyvalue. If convertable still fine::

    >>> widget.attrs['emptyvalue'] = '0'
    >>> data = widget.extract({})
    >>> data.errors, data.extracted
    ([], <UNSET>)

    >>> data = widget.extract({'MYDATATYPEFIELD': ''})
    >>> data.errors, data.extracted
    ([], 0L)

Test emptyvalue if ``float`` datatype set::

    >>> widget = factory(
    ...     'text',
    ...     name='MYDATATYPEFIELD',
    ...     value='',
    ...     props={
    ...         'datatype': 'float',
    ...     })

Default emptyvalue::

    >>> data = widget.extract({})
    >>> data.errors, data.extracted
    ([], <UNSET>)

    >>> data = widget.extract({'MYDATATYPEFIELD': ''})
    >>> data.errors, data.extracted
    ([], <EMPTY_VALUE>)

None emptyvalue::

    >>> widget.attrs['emptyvalue'] = None
    >>> data = widget.extract({})
    >>> data.errors, data.extracted
    ([], <UNSET>)

    >>> data = widget.extract({'MYDATATYPEFIELD': ''})
    >>> data.errors, data.extracted
    ([], None)

UNSET emptyvalue::

    >>> widget.attrs['emptyvalue'] = UNSET
    >>> data = widget.extract({})
    >>> data.errors, data.extracted
    ([], <UNSET>)

    >>> data = widget.extract({'MYDATATYPEFIELD': ''})
    >>> data.errors, data.extracted
    ([], <UNSET>)

Float emptyvalue::

    >>> widget.attrs['emptyvalue'] = 0.1
    >>> data = widget.extract({})
    >>> data.errors, data.extracted
    ([], <UNSET>)

    >>> data = widget.extract({'MYDATATYPEFIELD': ''})
    >>> data.errors, data.extracted
    ([], 0.1)

String emptyvalue. If convertable still fine::

    >>> widget.attrs['emptyvalue'] = '0,2'
    >>> data = widget.extract({})
    >>> data.errors, data.extracted
    ([], <UNSET>)

    >>> data = widget.extract({'MYDATATYPEFIELD': ''})
    >>> data.errors, data.extracted
    ([], 0.2)

Test emptyvalue if ``uuid`` datatype set::

    >>> widget = factory(
    ...     'text',
    ...     name='MYDATATYPEFIELD',
    ...     value='',
    ...     props={
    ...         'datatype': 'uuid',
    ...     })

Default emptyvalue::

    >>> data = widget.extract({})
    >>> data.errors, data.extracted
    ([], <UNSET>)

    >>> data = widget.extract({'MYDATATYPEFIELD': ''})
    >>> data.errors, data.extracted
    ([], <EMPTY_VALUE>)

None emptyvalue::

    >>> widget.attrs['emptyvalue'] = None
    >>> data = widget.extract({})
    >>> data.errors, data.extracted
    ([], <UNSET>)

    >>> data = widget.extract({'MYDATATYPEFIELD': ''})
    >>> data.errors, data.extracted
    ([], None)

UNSET emptyvalue::

    >>> widget.attrs['emptyvalue'] = UNSET
    >>> data = widget.extract({})
    >>> data.errors, data.extracted
    ([], <UNSET>)

    >>> data = widget.extract({'MYDATATYPEFIELD': ''})
    >>> data.errors, data.extracted
    ([], <UNSET>)

UUID emptyvalue::

    >>> widget.attrs['emptyvalue'] = uuid.uuid4()
    >>> data = widget.extract({})
    >>> data.errors, data.extracted
    ([], <UNSET>)

    >>> data = widget.extract({'MYDATATYPEFIELD': ''})
    >>> data.errors, data.extracted
    ([], UUID('...'))

String emptyvalue. If convertable still fine::

    >>> widget.attrs['emptyvalue'] = str(uuid.uuid4())
    >>> data = widget.extract({})
    >>> data.errors, data.extracted
    ([], <UNSET>)

    >>> data = widget.extract({'MYDATATYPEFIELD': ''})
    >>> data.errors, data.extracted
    ([], UUID('...'))

Integer datatype::

    >>> widget = factory(
    ...     'text',
    ...     name='MYDATATYPEFIELD',
    ...     value='',
    ...     props={
    ...         'datatype': 'int',
    ...     })
    >>> data = widget.extract({'MYDATATYPEFIELD': '1'})
    >>> data.errors, data.extracted
    ([], 1)

    >>> data = widget.extract({'MYDATATYPEFIELD': 'a'})
    >>> data.errors
    [ExtractionError('Input is not a valid integer.',)]

Float extraction::

    >>> widget = factory(
    ...     'text',
    ...     name='MYDATATYPEFIELD',
    ...     value='',
    ...     props={
    ...         'datatype': 'float',
    ...     })
    >>> data = widget.extract({'MYDATATYPEFIELD': '1.2'})
    >>> data.errors, data.extracted
    ([], 1.2)

    >>> data = widget.extract({'MYDATATYPEFIELD': 'a'})
    >>> data.errors
    [ExtractionError('Input is not a valid floating point number.',)]

UUID extraction::

    >>> widget = factory(
    ...     'text',
    ...     name='MYDATATYPEFIELD',
    ...     value='',
    ...     props={
    ...         'datatype': 'uuid',
    ...     })
    >>> data = widget.extract({
    ...     'MYDATATYPEFIELD': '3b8449f3-0456-4baa-a670-3066b0fcbda0'
    ... })
    >>> data.errors, data.extracted
    ([], UUID('3b8449f3-0456-4baa-a670-3066b0fcbda0'))

    >>> data = widget.extract({'MYDATATYPEFIELD': 'a'})
    >>> data.errors
    [ExtractionError('Input is not a valid UUID.',)]

Test ``datatype`` not allowed::

    >>> widget = factory(
    ...     'text',
    ...     name='MYDATATYPEFIELD',
    ...     value='',
    ...     props={
    ...         'datatype': 'uuid',
    ...         'allowed_datatypes': [int],
    ...     })

    >>> request = {
    ...     'MYDATATYPEFIELD': '3b8449f3-0456-4baa-a670-3066b0fcbda0'
    ... }
    >>> data = widget.extract(request)
    Traceback (most recent call last):
      ...
    ValueError: Datatype not allowed: "uuid"

Test ``datatype_message``::

    >>> widget = factory(
    ...     'text',
    ...     name='MYDATATYPEFIELD',
    ...     value='',
    ...     props={
    ...         'datatype': int,
    ...         'datatype_message': 'This did not work'
    ...     })
    >>> request = {
    ...     'MYDATATYPEFIELD': 'a'
    ... }
    >>> data = widget.extract(request)
    >>> data.errors, data.extracted
    ([ExtractionError('This did not work',)], 'a')

Test default error message if custom converter given but no
``datatype_message`` defined::

    >>> def custom_converter(val):
    ...     raise ValueError
    >>> widget = factory(
    ...     'text',
    ...     name='MYDATATYPEFIELD',
    ...     value='',
    ...     props={
    ...         'datatype': custom_converter,
    ...     })
    >>> request = {
    ...     'MYDATATYPEFIELD': 'a'
    ... }
    >>> data = widget.extract(request)
    >>> data.errors, data.extracted
    ([ExtractionError('Input conversion failed.',)], 'a')

Test unknown string ``datatype`` identifier::

    >>> widget = factory(
    ...     'text',
    ...     name='MYDATATYPEFIELD',
    ...     value='',
    ...     props={
    ...         'datatype': 'inexistent',
    ...     })
    >>> data = widget.extract({'MYDATATYPEFIELD': 'a'})
    Traceback (most recent call last):
      ...
    ValueError: Datatype unknown: "inexistent"


Checkbox
--------

A boolean checkbox widget (default)::

    >>> widget = factory(
    ...     'checkbox',
    ...     name='MYCHECKBOX')
    >>> wrapped_pxml(widget())
    <div>
      <input class="checkbox" id="input-MYCHECKBOX" name="MYCHECKBOX" 
        type="checkbox" value=""/>
      <input id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists" 
        type="hidden" value="checkboxexists"/>
    </div>
    <BLANKLINE>

    >>> widget.mode = 'display'
    >>> widget()
    u'<div class="display-checkbox" id="display-MYCHECKBOX">No</div>'

    >>> widget = factory(
    ...     'checkbox',
    ...     name='MYCHECKBOX',
    ...     value='True')
    >>> wrapped_pxml(widget())
    <div>
      <input checked="checked" class="checkbox" id="input-MYCHECKBOX" 
        name="MYCHECKBOX" type="checkbox" value=""/>
      <input id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists" 
        type="hidden" value="checkboxexists"/>
    </div>
    <BLANKLINE>

    >>> widget.mode = 'display'
    >>> widget()
    u'<div class="display-checkbox" id="display-MYCHECKBOX">Yes</div>'

A checkbox with label::

    >>> widget = factory(
    ...     'checkbox',
    ...     name='MYCHECKBOX',
    ...     props={
    ...         'with_label': True
    ...     })
    >>> widget()
    u'<input class="checkbox" id="input-MYCHECKBOX" name="MYCHECKBOX" 
    type="checkbox" value="" /><label class="checkbox_label" 
    for="input-MYCHECKBOX">&nbsp;</label><input id="checkboxexists-MYCHECKBOX" 
    name="MYCHECKBOX-exists" type="hidden" value="checkboxexists" />'

A checkbox widget with a value or an empty string::

    >>> widget = factory(
    ...     'checkbox',
    ...     name='MYCHECKBOX',
    ...     value='',
    ...     props={
    ...         'format': 'string'
    ...     })
    >>> wrapped_pxml(widget())
    <div>
      <input class="checkbox" id="input-MYCHECKBOX" name="MYCHECKBOX" 
      type="checkbox" value=""/>
      <input id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists" 
      type="hidden" value="checkboxexists"/>
    </div>
    <BLANKLINE>

    >>> widget.mode = 'display'
    >>> widget()
    u'<div class="display-checkbox" id="display-MYCHECKBOX">No</div>'

    >>> widget = factory(
    ...     'checkbox',
    ...     name='MYCHECKBOX',
    ...     value='Test Checkbox',
    ...     props={
    ...         'format': 'string'
    ...     })
    >>> wrapped_pxml(widget())
    <div>
      <input checked="checked" class="checkbox" id="input-MYCHECKBOX" 
      name="MYCHECKBOX" type="checkbox" value="Test Checkbox"/>
      <input id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists" 
      type="hidden" value="checkboxexists"/>
    </div>
    <BLANKLINE>

    >>> widget.mode = 'display'
    >>> widget()
    u'<div class="display-checkbox" id="display-MYCHECKBOX">Test Checkbox</div>'

    >>> widget.mode = 'edit'

Checkbox with manually set 'checked' attribute::

    >>> widget = factory(
    ...     'checkbox',
    ...     name='MYCHECKBOX',
    ...     value='',
    ...     props={
    ...         'format': 'string',
    ...         'checked': True,
    ...     })
    >>> wrapped_pxml(widget())
    <div>
      <input checked="checked" class="checkbox" id="input-MYCHECKBOX" 
      name="MYCHECKBOX" type="checkbox" value=""/>
      <input id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists" 
      type="hidden" value="checkboxexists"/>
    </div>
    <BLANKLINE>

    >>> widget = factory(
    ...     'checkbox',
    ...     name='MYCHECKBOX',
    ...     value='Test Checkbox',
    ...     props={
    ...         'format': 'string',
    ...         'checked': False,
    ...     })
    >>> wrapped_pxml(widget())
    <div>
      <input class="checkbox" id="input-MYCHECKBOX" name="MYCHECKBOX" 
      type="checkbox" value="Test Checkbox"/>
      <input id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists" 
      type="hidden" value="checkboxexists"/>
    </div>
    <BLANKLINE>

Checkbox extraction::

    >>> request = {
    ...     'MYCHECKBOX': '1',
    ...     'MYCHECKBOX-exists': 'checkboxexists'
    ... }
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData MYCHECKBOX, value='Test Checkbox', extracted='1' at ...>

    >>> request = {
    ...     'MYCHECKBOX': '',
    ...     'MYCHECKBOX-exists': 'checkboxexists'
    ... }
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData MYCHECKBOX, value='Test Checkbox', extracted='' at ...>

    >>> request = {
    ...     'MYCHECKBOX': 1,
    ... }
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData MYCHECKBOX, value='Test Checkbox', extracted=<UNSET> at ...>

    >>> model = dict()
    >>> data.persist_writer = write_mapping_writer
    >>> data.write(model)
    >>> model
    {'MYCHECKBOX': <UNSET>}

bool extraction::

    >>> widget = factory(
    ...     'checkbox',
    ...     name='MYCHECKBOX',
    ...     value='Test Checkbox',
    ...     props={
    ...         'format': 'bool'
    ...     })
    >>> request = {
    ...     'MYCHECKBOX': '',
    ...     'MYCHECKBOX-exists': 'checkboxexists'
    ... }
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData MYCHECKBOX, value='Test Checkbox', extracted=True at ...>

    >>> request = {
    ...     'MYCHECKBOX-exists': 'checkboxexists'
    ... }
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData MYCHECKBOX, value='Test Checkbox', extracted=False at ...>

    >>> model = dict()
    >>> data.persist_writer = write_mapping_writer
    >>> data.write(model)
    >>> model
    {'MYCHECKBOX': False}

invalid format::

    >>> widget = factory(
    ...     'checkbox',
    ...     name='MYCHECKBOX',
    ...     props={
    ...         'format': 'invalid'
    ...     })
    >>> request = {
    ...     'MYCHECKBOX': '',
    ...     'MYCHECKBOX-exists': 'checkboxexists'
    ... }
    >>> data = widget.extract(request)
    Traceback (most recent call last):
      ...
    ValueError: Checkbox widget has invalid format 'invalid' set

Render in display mode::

    >>> widget = factory(
    ...     'checkbox',
    ...     name='MYCHECKBOX',
    ...     value=False,
    ...     mode='display',
    ...     props={
    ...         'format': 'bool'
    ...     })
    >>> wrapped_pxml(widget())
    <div>
      <div class="display-checkbox" id="display-MYCHECKBOX">No</div>
    </div>
    <BLANKLINE>

    >>> widget = factory(
    ...     'checkbox',
    ...     name='MYCHECKBOX',
    ...     value=True,
    ...     mode='display',
    ...     props={
    ...         'format': 'bool'
    ...     })
    >>> wrapped_pxml(widget())
    <div>
      <div class="display-checkbox" id="display-MYCHECKBOX">Yes</div>
    </div>
    <BLANKLINE>

Display mode and display proxy bool format::

    >>> widget = factory(
    ...     'checkbox',
    ...     name='MYCHECKBOX',
    ...     value=True,
    ...     props={
    ...         'format': 'bool',
    ...         'display_proxy': True
    ...     },
    ...     mode='display')
    >>> widget()
    u'<div class="display-checkbox" id="display-MYCHECKBOX">Yes<input 
    class="checkbox" id="input-MYCHECKBOX" name="MYCHECKBOX" type="hidden" 
    value="" /><input id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists" 
    type="hidden" value="checkboxexists" /></div>'

    >>> data = widget.extract(request={'MYCHECKBOX-exists': 'checkboxexists'})
    >>> data
    <RuntimeData MYCHECKBOX, value=True, extracted=False at ...>

    >>> widget(data=data)
    u'<div class="display-checkbox" id="display-MYCHECKBOX">No<input 
    id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists" type="hidden" 
    value="checkboxexists" /></div>'

    >>> data = widget.extract(request={
    ...     'MYCHECKBOX-exists': 'checkboxexists',
    ...     'MYCHECKBOX': ''
    ... })
    >>> data
    <RuntimeData MYCHECKBOX, value=True, extracted=True at ...>

    >>> widget(data=data)
    u'<div class="display-checkbox" id="display-MYCHECKBOX">Yes<input 
    class="checkbox" id="input-MYCHECKBOX" name="MYCHECKBOX" 
    type="hidden" value="" /><input id="checkboxexists-MYCHECKBOX" 
    name="MYCHECKBOX-exists" type="hidden" value="checkboxexists" /></div>'

Display mode and display proxy string format::

    >>> widget = factory(
    ...     'checkbox',
    ...     name='MYCHECKBOX',
    ...     value='yes',
    ...     props={
    ...         'format': 'string',
    ...         'display_proxy': True
    ...     },
    ...     mode='display')
    >>> widget()
    u'<div class="display-checkbox" id="display-MYCHECKBOX">yes<input 
    class="checkbox" id="input-MYCHECKBOX" name="MYCHECKBOX" 
    type="hidden" value="yes" /><input id="checkboxexists-MYCHECKBOX" 
    name="MYCHECKBOX-exists" type="hidden" value="checkboxexists" /></div>'

    >>> data = widget.extract(request={'MYCHECKBOX-exists': 'checkboxexists'})
    >>> data
    <RuntimeData MYCHECKBOX, value='yes', extracted='' at ...>

    >>> widget(data=data)
    u'<div class="display-checkbox" id="display-MYCHECKBOX">No<input 
    class="checkbox" id="input-MYCHECKBOX" name="MYCHECKBOX" type="hidden" 
    value="" /><input id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists" 
    type="hidden" value="checkboxexists" /></div>'

    >>> data = widget.extract(request={
    ...     'MYCHECKBOX-exists': 'checkboxexists',
    ...     'MYCHECKBOX': ''
    ... })
    >>> data
    <RuntimeData MYCHECKBOX, value='yes', extracted='' at ...>

    >>> widget(data=data)
    u'<div class="display-checkbox" id="display-MYCHECKBOX">No<input 
    class="checkbox" id="input-MYCHECKBOX" name="MYCHECKBOX" type="hidden" 
    value="" /><input id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists" 
    type="hidden" value="checkboxexists" /></div>'

    >>> data = widget.extract(request={'MYCHECKBOX-exists': 'checkboxexists',
    ...                                'MYCHECKBOX': 'foo'})
    >>> data
    <RuntimeData MYCHECKBOX, value='yes', extracted='foo' at ...>

    >>> widget(data=data)
    u'<div class="display-checkbox" id="display-MYCHECKBOX">foo<input 
    class="checkbox" id="input-MYCHECKBOX" name="MYCHECKBOX" 
    type="hidden" value="foo" /><input id="checkboxexists-MYCHECKBOX" 
    name="MYCHECKBOX-exists" type="hidden" value="checkboxexists" /></div>'

Generic HTML5 Data::

    >>> widget = factory(
    ...     'checkbox',
    ...     name='MYCHECKBOX',
    ...     value='Test Checkbox',
    ...     props={
    ...         'data': {'foo': 'bar'}
    ...     })
    >>> widget()
    u'<input checked="checked" class="checkbox" data-foo=\'bar\' 
    id="input-MYCHECKBOX" name="MYCHECKBOX" type="checkbox" value="" /><input 
    id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists" type="hidden" 
    value="checkboxexists" />'


Textarea
--------

Textarea widget::

    >>> widget = factory(
    ...     'textarea',
    ...     name='MYTEXTAREA',
    ...     value=None)
    >>> widget()
    u'<textarea class="textarea" cols="80" id="input-MYTEXTAREA" 
    name="MYTEXTAREA" rows="25"></textarea>'

    >>> widget = factory(
    ...     'textarea',
    ...     name='MYTEXTAREA',
    ...     value=None,
    ...     props={
    ...         'data': {
    ...             'foo': 'bar'
    ...         },
    ...     })
    >>> widget()
    u'<textarea class="textarea" cols="80" data-foo=\'bar\' 
    id="input-MYTEXTAREA" name="MYTEXTAREA" rows="25"></textarea>'

    >>> widget.mode = 'display'
    >>> widget()
    u'<div class="display-textarea" data-foo=\'bar\' 
    id="display-MYTEXTAREA"></div>'

Emptyvalue::

    >>> widget = factory(
    ...     'textarea',
    ...     name='MYTEXTAREA',
    ...     props={
    ...         'emptyvalue': 'EMPTYVALUE',
    ...     })
    >>> widget.extract(request={'MYTEXTAREA': ''})
    <RuntimeData MYTEXTAREA, value=<UNSET>, extracted='EMPTYVALUE' at ...>

    >>> widget.extract(request={'MYTEXTAREA': 'NOEMPTY'})
    <RuntimeData MYTEXTAREA, value=<UNSET>, extracted='NOEMPTY' at ...>

Persist::

    >>> widget = factory(
    ...     'textarea',
    ...     name='MYTEXTAREA',
    ...     props={
    ...         'persist_writer': write_mapping_writer
    ...     })
    >>> data = widget.extract(request={'MYTEXTAREA': 'Text'})
    >>> model = dict()
    >>> data.write(model)
    >>> model
    {'MYTEXTAREA': 'Text'}


Lines
-----

Render empty::

    >>> widget = factory(
    ...     'lines',
    ...     name='MYLINES',
    ...     value=None)
    >>> widget()
    u'<textarea class="lines" cols="40" id="input-MYLINES" name="MYLINES" 
    rows="8"></textarea>'

Render with preset value, expected as list::

    >>> widget = factory(
    ...     'lines',
    ...     name='MYLINES',
    ...     value=['a', 'b', 'c'])
    >>> pxml(widget())
    <textarea class="lines" cols="40" id="input-MYLINES" name="MYLINES" 
    rows="8">a
    b
    c</textarea>
    <BLANKLINE>

Extract empty::

    >>> data = widget.extract({'MYLINES': ''})
    >>> data.extracted
    []

Extract with data::

    >>> data = widget.extract({'MYLINES': 'a\nb'})
    >>> data.extracted
    ['a', 'b']

Render with extracted data::

    >>> pxml(widget(data=data))
    <textarea class="lines" cols="40" id="input-MYLINES" name="MYLINES" 
    rows="8">a
    b</textarea>
    <BLANKLINE>

Display mode with preset value::

    >>> widget = factory(
    ...     'lines',
    ...     name='MYLINES',
    ...     value=['a', 'b', 'c'],
    ...     mode='display')
    >>> pxml(widget())
    <ul class="display-lines" id="display-MYLINES">
      <li>a</li>
      <li>b</li>
      <li>c</li>
    </ul>
    <BLANKLINE>

Display mode with empty preset value::

    >>> widget = factory(
    ...     'lines',
    ...     name='MYLINES',
    ...     value=[],
    ...     mode='display')
    >>> pxml(widget())
    <ul class="display-lines" id="display-MYLINES"/>
    <BLANKLINE>

Display mode with ``display_proxy``::

    >>> widget = factory(
    ...     'lines',
    ...     name='MYLINES',
    ...     value=['a', 'b', 'c'],
    ...     props={
    ...         'display_proxy': True,
    ...     },
    ...     mode='display')
    >>> wrapped_pxml(widget())
    <div>
      <ul class="display-lines" id="display-MYLINES">
        <li>a</li>
        <li>b</li>
        <li>c</li>
      </ul>
      <input class="lines" id="input-MYLINES" name="MYLINES" type="hidden" 
        value="a"/>
      <input class="lines" id="input-MYLINES" name="MYLINES" type="hidden" 
        value="b"/>
      <input class="lines" id="input-MYLINES" name="MYLINES" type="hidden" 
        value="c"/>
    </div>
    <BLANKLINE>

    >>> data = widget.extract({'MYLINES': 'a\nb'})
    >>> data
    <RuntimeData MYLINES, value=['a', 'b', 'c'], extracted=['a', 'b'] at ...>

    >>> wrapped_pxml(widget(data=data))
    <div>
      <ul class="display-lines" id="display-MYLINES">
        <li>a</li>
        <li>b</li>
      </ul>
      <input class="lines" id="input-MYLINES" name="MYLINES" type="hidden" 
        value="a"/>
      <input class="lines" id="input-MYLINES" name="MYLINES" type="hidden" 
        value="b"/>
    </div>
    <BLANKLINE>

Generic HTML5 Data::

    >>> widget = factory(
    ...     'lines',
    ...     name='MYLINES',
    ...     value=['a', 'b', 'c'],
    ...     props={
    ...         'data': {'foo': 'bar'}
    ...     })
    >>> pxml(widget())
    <textarea class="lines" cols="40" data-foo="bar" id="input-MYLINES" 
    name="MYLINES" rows="8">a
    b
    c</textarea>
    <BLANKLINE>

    >>> widget = factory(
    ...     'lines',
    ...     name='MYLINES',
    ...     value=['a', 'b', 'c'],
    ...     props={
    ...         'data': {'foo': 'bar'}
    ...     },
    ...     mode='display')
    >>> pxml(widget())
    <ul class="display-lines" data-foo="bar" id="display-MYLINES">
      <li>a</li>
      <li>b</li>
      <li>c</li>
    </ul>
    <BLANKLINE>

Emptyvalue::

    >>> widget = factory(
    ...     'lines',
    ...     name='MYLINES',
    ...     value=['a', 'b', 'c'],
    ...     props={
    ...         'emptyvalue': ['1']
    ...     })
    >>> widget.extract(request={'MYLINES': ''})
    <RuntimeData MYLINES, value=['a', 'b', 'c'], extracted=['1'] at ...>

    >>> widget.extract(request={'MYLINES': '1\n2'})
    <RuntimeData MYLINES, value=['a', 'b', 'c'], extracted=['1', '2'] at ...>

Datatype::

    >>> widget = factory(
    ...     'lines',
    ...     name='MYLINES',
    ...     props={
    ...         'emptyvalue': [1],
    ...         'datatype': int
    ...     })
    >>> widget.extract(request={'MYLINES': ''})
    <RuntimeData MYLINES, value=<UNSET>, extracted=[1] at ...>

    >>> widget.extract(request={'MYLINES': '1\n2'})
    <RuntimeData MYLINES, value=<UNSET>, extracted=[1, 2] at ...>

    >>> widget.attrs['emptyvalue'] = ['1']
    >>> widget.extract(request={'MYLINES': ''})
    <RuntimeData MYLINES, value=<UNSET>, extracted=[1] at ...>

Persist::

    >>> widget = factory(
    ...     'lines',
    ...     name='MYLINES',
    ...     props={
    ...         'persist_writer': write_mapping_writer
    ...     })
    >>> data = widget.extract(request={'MYLINES': '1\n2'})
    >>> model = dict()
    >>> data.write(model)
    >>> model
    {'MYLINES': ['1', '2']}


Selection
---------


Single Valued
.............

Default single value selection::

    >>> vocab = [
    ...     ('one','One'),
    ...     ('two', 'Two'),
    ...     ('three', 'Three'),
    ...     ('four', 'Four')
    ... ]
    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     value='one',
    ...     props={
    ...         'vocabulary': vocab
    ...     })
    >>> pxml(widget())
    <select class="select" id="input-MYSELECT" name="MYSELECT">
      <option id="input-MYSELECT-one" selected="selected" 
        value="one">One</option>
      <option id="input-MYSELECT-two" value="two">Two</option>
      <option id="input-MYSELECT-three" value="three">Three</option>
      <option id="input-MYSELECT-four" value="four">Four</option>
    </select>
    <BLANKLINE>

    >>> data = widget.extract({'MYSELECT': 'two'})
    >>> data.errors, data.extracted
    ([], 'two')

    >>> pxml(widget(data=data))
    <select class="select" id="input-MYSELECT" name="MYSELECT">
      <option id="input-MYSELECT-one" value="one">One</option>
      <option id="input-MYSELECT-two" selected="selected" 
        value="two">Two</option>
      <option id="input-MYSELECT-three" value="three">Three</option>
      <option id="input-MYSELECT-four" value="four">Four</option>
    </select>
    <BLANKLINE>

Single value selection completly disabled::

    >>> widget.attrs['disabled'] = True
    >>> pxml(widget())
    <select class="select" disabled="disabled" id="input-MYSELECT" 
      name="MYSELECT">
      <option id="input-MYSELECT-one" selected="selected" 
        value="one">One</option>
      <option id="input-MYSELECT-two" value="two">Two</option>
      <option id="input-MYSELECT-three" value="three">Three</option>
      <option id="input-MYSELECT-four" value="four">Four</option>
    </select>
    <BLANKLINE>

Single value selection with specific options disabled::

    >>> widget.attrs['disabled'] = ['two', 'four']
    >>> pxml(widget())
    <select class="select" id="input-MYSELECT" name="MYSELECT">
      <option id="input-MYSELECT-one" selected="selected" 
        value="one">One</option>
      <option disabled="disabled" id="input-MYSELECT-two" 
        value="two">Two</option>
      <option id="input-MYSELECT-three" value="three">Three</option>
      <option disabled="disabled" id="input-MYSELECT-four" 
        value="four">Four</option>
    </select>
    <BLANKLINE>

    >>> del widget.attrs['disabled']

Single value selection display mode::

    >>> widget.mode = 'display'
    >>> widget()
    u'<div class="display-select" id="display-MYSELECT">One</div>'

    >>> widget.attrs['display_proxy'] = True
    >>> wrapped_pxml(widget())
    <div>
      <div class="display-select" id="display-MYSELECT">One</div>
      <input class="select" id="input-MYSELECT" name="MYSELECT" type="hidden" 
        value="one"/>
    </div>
    <BLANKLINE>

    >>> data = widget.extract(request={'MYSELECT': 'two'})
    >>> data
    <RuntimeData MYSELECT, value='one', extracted='two' at ...>

    >>> wrapped_pxml(widget(data=data))
    <div>
      <div class="display-select" id="display-MYSELECT">Two</div>
      <input class="select" id="input-MYSELECT" name="MYSELECT" type="hidden" 
        value="two"/>
    </div>
    <BLANKLINE>

Single value selection with datatype set::

    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     props={
    ...         'datatype': uuid.UUID
    ...     })

Preselected values::

    >>> widget.getter = UNSET
    >>> widget.attrs['vocabulary'] = [
    ...     (UNSET, 'Empty value'),
    ...     (uuid.UUID('1b679ef8-9068-45f5-8bb8-4007264aa7f7'), 'One')
    ... ]
    >>> res = widget()
    >>> pxml(res)
    <select class="select" id="input-MYSELECT" name="MYSELECT">
      <option id="input-MYSELECT-" selected="selected" value="">Empty value</option>
      <option id="input-MYSELECT-1b679ef8-..." value="1b679ef8-...">One</option>
    </select>
    <BLANKLINE>

    >>> widget.getter = EMPTY_VALUE
    >>> widget.attrs['vocabulary'][0] = (EMPTY_VALUE, 'Empty value')
    >>> assert(res == widget())

    >>> widget.getter = None
    >>> widget.attrs['vocabulary'][0] = (None, 'Empty value')
    >>> assert(res == widget())

    >>> widget.getter = ''
    >>> widget.attrs['vocabulary'][0] = ('', 'Empty value')
    >>> assert(res == widget())

    >>> widget.getter = uuid.UUID('1b679ef8-9068-45f5-8bb8-4007264aa7f7')
    >>> res = widget()
    >>> pxml(res)
    <select class="select" id="input-MYSELECT" name="MYSELECT">
      <option id="input-MYSELECT-" value="">Empty value</option>
      <option id="input-MYSELECT-1b679ef8-..." selected="selected" value="1b679ef8-...">One</option>
    </select>
    <BLANKLINE>

Note, vocabulary keys are converted to ``datatype`` while widget value needs to
be of type defined in ``datatype`` or one from the valid empty values::

    >>> widget.attrs['vocabulary'] = [
    ...     (UNSET, 'Empty value'),
    ...     ('1b679ef8-9068-45f5-8bb8-4007264aa7f7', 'One')
    ... ]
    >>> res = widget()
    >>> assert(res == widget())

Test ``datatype`` extraction with selection::

    >>> vocab = [
    ...     (EMPTY_VALUE, 'Empty value'),
    ...     (1, 'One'),
    ...     (2, 'Two'),
    ... ]
    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     value=2,
    ...     props={
    ...         'vocabulary': vocab,
    ...         'datatype': 'int'
    ...     })
    >>> pxml(widget())
    <select class="select" id="input-MYSELECT" name="MYSELECT">
      <option id="input-MYSELECT-" value="">Empty value</option>
      <option id="input-MYSELECT-1" value="1">One</option>
      <option id="input-MYSELECT-2" selected="selected" value="2">Two</option>
    </select>
    <BLANKLINE>

    >>> data = widget.extract({'MYSELECT': ''})
    >>> assert(data.extracted == EMPTY_VALUE)

    >>> data = widget.extract({'MYSELECT': '1'})
    >>> assert(data.extracted == 1)

    >>> pxml(widget(data=data))
    <select class="select" id="input-MYSELECT" name="MYSELECT">
      <option id="input-MYSELECT-" value="">Empty value</option>
      <option id="input-MYSELECT-1" selected="selected"  value="1">One</option>
      <option id="input-MYSELECT-2" value="2">Two</option>
    </select>
    <BLANKLINE>

Test extraction with ``emptyvalue`` set::

    >>> widget.attrs['emptyvalue'] = UNSET
    >>> data = widget.extract({})
    >>> assert(data.extracted is UNSET)

    >>> data = widget.extract({'MYSELECT': ''})
    >>> assert(data.extracted is UNSET)

    >>> widget.attrs['emptyvalue'] = None
    >>> data = widget.extract({})
    >>> assert(data.extracted is UNSET)

    >>> data = widget.extract({'MYSELECT': ''})
    >>> assert(data.extracted is None)

    >>> widget.attrs['emptyvalue'] = 0
    >>> data = widget.extract({})
    >>> assert(data.extracted is UNSET)

    >>> data = widget.extract({'MYSELECT': ''})
    >>> assert(data.extracted  == 0)

Single value selection with ``datatype`` set completly disabled::

    >>> widget.attrs['disabled'] = True
    >>> pxml(widget())
    <select class="select" disabled="disabled" id="input-MYSELECT" 
      name="MYSELECT">
      <option id="input-MYSELECT-" value="">Empty value</option>
      <option id="input-MYSELECT-1" value="1">One</option>
      <option id="input-MYSELECT-2" selected="selected" value="2">Two</option>
    </select>
    <BLANKLINE>

Single value selection with ``datatype`` with specific options disabled::

    >>> widget.attrs['emptyvalue'] = None
    >>> widget.attrs['disabled'] = [None, 2]
    >>> rendered = widget()
    >>> pxml(rendered)
    <select class="select" id="input-MYSELECT" name="MYSELECT">
      <option disabled="disabled" id="input-MYSELECT-" value="">Empty value</option>
      <option id="input-MYSELECT-1" value="1">One</option>
      <option disabled="disabled" id="input-MYSELECT-2" selected="selected" value="2">Two</option>
    </select>
    <BLANKLINE>

    >>> widget.attrs['emptyvalue'] = UNSET
    >>> widget.attrs['disabled'] = [UNSET, 2]
    >>> assert(widget() == rendered)

    >>> widget.attrs['emptyvalue'] = EMPTY_VALUE
    >>> widget.attrs['disabled'] = [EMPTY_VALUE, 2]
    >>> assert(widget() == rendered)

    >>> widget.attrs['emptyvalue'] = 0
    >>> widget.attrs['disabled'] = [0, 2]
    >>> assert(widget() == rendered)

    >>> del widget.attrs['disabled']

Single value selection with datatype display mode::

    >>> widget.mode = 'display'
    >>> widget()
    u'<div class="display-select" id="display-MYSELECT">Two</div>'

    >>> widget.attrs['display_proxy'] = True
    >>> wrapped_pxml(widget())
    <div>
      <div class="display-select" id="display-MYSELECT">Two</div>
      <input class="select" id="input-MYSELECT" name="MYSELECT" type="hidden" 
        value="2"/>
    </div>
    <BLANKLINE>

    >>> data = widget.extract(request={'MYSELECT': '1'})
    >>> data
    <RuntimeData MYSELECT, value=2, extracted=1 at ...>

    >>> wrapped_pxml(widget(data=data))
    <div>
      <div class="display-select" id="display-MYSELECT">One</div>
      <input class="select" id="input-MYSELECT" name="MYSELECT" type="hidden" 
        value="1"/>
    </div>
    <BLANKLINE>

Generic HTML5 Data::

    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     value='one',
    ...     props={
    ...         'data': {'foo': 'bar'},
    ...         'vocabulary': [('one', 'One')]
    ...     })
    >>> pxml(widget())
    <select class="select" data-foo="bar" id="input-MYSELECT" name="MYSELECT">
      <option id="input-MYSELECT-one" selected="selected" 
        value="one">One</option>
    </select>
    <BLANKLINE>

    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     value='one',
    ...     props={
    ...         'data': {'foo': 'bar'},
    ...         'vocabulary': [('one', 'One')]
    ...     },
    ...     mode='display')
    >>> pxml(widget())
    <div class="display-select" data-foo="bar" id="display-MYSELECT">One</div>
    <BLANKLINE>

Persist::

    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     props={
    ...         'vocabulary': [('one', 'One')]
    ...     })
    >>> data = widget.extract({'MYSELECT': 'one'})
    >>> model = dict()
    >>> data.persist_writer = write_mapping_writer
    >>> data.write(model)
    >>> model
    {'MYSELECT': 'one'}


With Radio
..........

Render single selection as radio inputs::

    >>> vocab = [
    ...     ('one','One'),
    ...     ('two', 'Two'),
    ...     ('three', 'Three'),
    ...     ('four', 'Four')
    ... ]
    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     value='one',
    ...     props={
    ...         'vocabulary': vocab,
    ...         'format': 'single',
    ...         'listing_label_position': 'before'
    ...     })
    >>> wrapped_pxml(widget())
    <div>
      <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden" 
        value="exists"/>
      <div id="radio-MYSELECT-wrapper">
        <div id="radio-MYSELECT-one">
          <label for="input-MYSELECT-one">One</label>
          <input checked="checked" class="select" id="input-MYSELECT-one" 
            name="MYSELECT" type="radio" value="one"/>
        </div>
        <div id="radio-MYSELECT-two">
          <label for="input-MYSELECT-two">Two</label>
          <input class="select" id="input-MYSELECT-two" name="MYSELECT" 
            type="radio" value="two"/>
        </div>
        <div id="radio-MYSELECT-three">
          <label for="input-MYSELECT-three">Three</label>
          <input class="select" id="input-MYSELECT-three" name="MYSELECT" 
            type="radio" value="three"/>
        </div>
        <div id="radio-MYSELECT-four">
          <label for="input-MYSELECT-four">Four</label>
          <input class="select" id="input-MYSELECT-four" name="MYSELECT" 
            type="radio" value="four"/>
        </div>
      </div>
    </div>
    <BLANKLINE>

Render single selection as radio inputs, disables all::

    >>> widget.attrs['disabled'] = True
    >>> wrapped_pxml(widget())
    <div>
      <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden" 
        value="exists"/>
      <div id="radio-MYSELECT-wrapper">
        <div id="radio-MYSELECT-one">
          <label for="input-MYSELECT-one">One</label>
          <input checked="checked" class="select" disabled="disabled" 
            id="input-MYSELECT-one" name="MYSELECT" type="radio" value="one"/>
        </div>
        <div id="radio-MYSELECT-two">
          <label for="input-MYSELECT-two">Two</label>
          <input class="select" disabled="disabled" id="input-MYSELECT-two" 
            name="MYSELECT" type="radio" value="two"/>
        </div>
        <div id="radio-MYSELECT-three">
          <label for="input-MYSELECT-three">Three</label>
          <input class="select" disabled="disabled" id="input-MYSELECT-three" 
            name="MYSELECT" type="radio" value="three"/>
        </div>
        <div id="radio-MYSELECT-four">
          <label for="input-MYSELECT-four">Four</label>
          <input class="select" disabled="disabled" id="input-MYSELECT-four" 
            name="MYSELECT" type="radio" value="four"/>
        </div>
      </div>
    </div>
    <BLANKLINE>

Render single selection as radio inputs, disables some::

    >>> widget.attrs['disabled'] = ['one', 'three']
    >>> wrapped_pxml(widget())
    <div>
      <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden" 
        value="exists"/>
      <div id="radio-MYSELECT-wrapper">
        <div id="radio-MYSELECT-one">
          <label for="input-MYSELECT-one">One</label>
          <input checked="checked" class="select" disabled="disabled" 
            id="input-MYSELECT-one" name="MYSELECT" type="radio" value="one"/>
        </div>
        <div id="radio-MYSELECT-two">
          <label for="input-MYSELECT-two">Two</label>
          <input class="select" id="input-MYSELECT-two" name="MYSELECT" 
            type="radio" value="two"/>
        </div>
        <div id="radio-MYSELECT-three">
          <label for="input-MYSELECT-three">Three</label>
          <input class="select" disabled="disabled" id="input-MYSELECT-three" 
            name="MYSELECT" type="radio" value="three"/>
        </div>
        <div id="radio-MYSELECT-four">
          <label for="input-MYSELECT-four">Four</label>
          <input class="select" id="input-MYSELECT-four" name="MYSELECT" 
            type="radio" value="four"/>
        </div>
      </div>
    </div>
    <BLANKLINE>

    >>> del widget.attrs['disabled']

Radio single valued display mode::

    >>> widget.mode = 'display'
    >>> widget()
    u'<div class="display-select" id="display-MYSELECT">One</div>'

    >>> widget.attrs['display_proxy'] = True
    >>> wrapped_pxml(widget())
    <div>
      <div class="display-select" id="display-MYSELECT">One</div>
      <input class="select" id="input-MYSELECT" name="MYSELECT" type="hidden" 
        value="one"/>
    </div>
    <BLANKLINE>

    >>> data = widget.extract(request={'MYSELECT': 'two'})
    >>> data
    <RuntimeData MYSELECT, value='one', extracted='two' at ...>

    >>> wrapped_pxml(widget(data=data))
    <div>
      <div class="display-select" id="display-MYSELECT">Two</div>
      <input class="select" id="input-MYSELECT" name="MYSELECT" type="hidden" 
        value="two"/>
    </div>
    <BLANKLINE>

Radio single value selection with uuid datatype set::

    >>> vocab = [
    ...     ('3762033b-7118-4bad-89ed-7cb71f5ab6d1', 'One'),
    ...     ('74ef603d-29d0-4016-a003-334719dde835', 'Two'),
    ...     ('b1116392-4a80-496d-86f1-3a2c87e09c59', 'Three'),
    ...     ('e09471dc-625d-463b-be03-438d7089ec13', 'Four')
    ... ]
    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     value='b1116392-4a80-496d-86f1-3a2c87e09c59',
    ...     props={
    ...         'vocabulary': vocab,
    ...         'datatype': 'uuid',
    ...         'format': 'single',
    ...     })
    >>> wrapped_pxml(widget())
    <div>
      <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden" 
        value="exists"/>
      <div id="radio-MYSELECT-wrapper">
        <div id="radio-MYSELECT-3762033b-7118-4bad-89ed-7cb71f5ab6d1">
          <label 
            for="input-MYSELECT-3762033b-7118-4bad-89ed-7cb71f5ab6d1"><input 
              class="select" 
              id="input-MYSELECT-3762033b-7118-4bad-89ed-7cb71f5ab6d1" 
              name="MYSELECT" type="radio" 
              value="3762033b-7118-4bad-89ed-7cb71f5ab6d1"/>One</label>
        </div>
        <div id="radio-MYSELECT-74ef603d-29d0-4016-a003-334719dde835">
          <label 
            for="input-MYSELECT-74ef603d-29d0-4016-a003-334719dde835"><input 
              class="select" 
              id="input-MYSELECT-74ef603d-29d0-4016-a003-334719dde835" 
              name="MYSELECT" type="radio" 
              value="74ef603d-29d0-4016-a003-334719dde835"/>Two</label>
        </div>
        <div id="radio-MYSELECT-b1116392-4a80-496d-86f1-3a2c87e09c59">
          <label 
            for="input-MYSELECT-b1116392-4a80-496d-86f1-3a2c87e09c59"><input 
              checked="checked" 
              class="select" 
              id="input-MYSELECT-b1116392-4a80-496d-86f1-3a2c87e09c59" 
              name="MYSELECT" type="radio" 
              value="b1116392-4a80-496d-86f1-3a2c87e09c59"/>Three</label>
        </div>
        <div id="radio-MYSELECT-e09471dc-625d-463b-be03-438d7089ec13">
          <label 
            for="input-MYSELECT-e09471dc-625d-463b-be03-438d7089ec13"><input 
              class="select" 
              id="input-MYSELECT-e09471dc-625d-463b-be03-438d7089ec13" 
              name="MYSELECT" type="radio" 
              value="e09471dc-625d-463b-be03-438d7089ec13"/>Four</label>
        </div>
      </div>
    </div>
    <BLANKLINE>

    >>> data = widget.extract({
    ...     'MYSELECT': 'e09471dc-625d-463b-be03-438d7089ec13'
    ... })
    >>> data.extracted
    UUID('e09471dc-625d-463b-be03-438d7089ec13')

    >>> wrapped_pxml(widget(data=data))
    <div>
      <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden" 
        value="exists"/>
      <div id="radio-MYSELECT-wrapper">
        <div id="radio-MYSELECT-3762033b-7118-4bad-89ed-7cb71f5ab6d1">
          <label 
            for="input-MYSELECT-3762033b-7118-4bad-89ed-7cb71f5ab6d1"><input 
              class="select" 
              id="input-MYSELECT-3762033b-7118-4bad-89ed-7cb71f5ab6d1" 
              name="MYSELECT" type="radio" 
              value="3762033b-7118-4bad-89ed-7cb71f5ab6d1"/>One</label>
        </div>
        <div id="radio-MYSELECT-74ef603d-29d0-4016-a003-334719dde835">
          <label 
            for="input-MYSELECT-74ef603d-29d0-4016-a003-334719dde835"><input 
              class="select" 
              id="input-MYSELECT-74ef603d-29d0-4016-a003-334719dde835" 
              name="MYSELECT" type="radio" 
              value="74ef603d-29d0-4016-a003-334719dde835"/>Two</label>
        </div>
        <div id="radio-MYSELECT-b1116392-4a80-496d-86f1-3a2c87e09c59">
          <label 
            for="input-MYSELECT-b1116392-4a80-496d-86f1-3a2c87e09c59"><input 
              class="select" 
              id="input-MYSELECT-b1116392-4a80-496d-86f1-3a2c87e09c59" 
              name="MYSELECT" type="radio" 
              value="b1116392-4a80-496d-86f1-3a2c87e09c59"/>Three</label>
        </div>
        <div id="radio-MYSELECT-e09471dc-625d-463b-be03-438d7089ec13">
          <label 
            for="input-MYSELECT-e09471dc-625d-463b-be03-438d7089ec13"><input 
              checked="checked" class="select" 
              id="input-MYSELECT-e09471dc-625d-463b-be03-438d7089ec13" 
              name="MYSELECT" type="radio" 
              value="e09471dc-625d-463b-be03-438d7089ec13"/>Four</label>
        </div>
      </div>
    </div>
    <BLANKLINE>

Generic HTML5 Data::

    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     value='one',
    ...     props={
    ...         'vocabulary': [('one','One')],
    ...         'format': 'single',
    ...         'listing_label_position': 'before',
    ...         'data': {'foo': 'bar'}
    ...     })
    >>> wrapped_pxml(widget())
    <div>
      <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden" 
        value="exists"/>
      <div data-foo="bar" id="radio-MYSELECT-wrapper">
        <div id="radio-MYSELECT-one">
          <label for="input-MYSELECT-one">One</label>
          <input checked="checked" class="select" id="input-MYSELECT-one" 
            name="MYSELECT" type="radio" value="one"/>
        </div>
      </div>
    </div>
    <BLANKLINE>

    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     value='one',
    ...     props={
    ...         'vocabulary': [('one','One')],
    ...         'format': 'single',
    ...         'listing_label_position': 'before',
    ...         'data': {'foo': 'bar'}
    ...     },
    ...     mode='display')
    >>> wrapped_pxml(widget())
    <div>
      <div class="display-select" data-foo="bar" 
        id="display-MYSELECT">One</div>
    </div>
    <BLANKLINE>


Multi valued
............

Default multi valued::

    >>> vocab = [
    ...     ('one','One'),
    ...     ('two', 'Two'),
    ...     ('three', 'Three'),
    ...     ('four', 'Four')
    ... ]
    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     value=['one', 'two'],
    ...     props={
    ...         'multivalued': True,
    ...         'vocabulary': vocab
    ...     })
    >>> wrapped_pxml(widget())
    <div>
      <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden" 
        value="exists"/>
      <select class="select" id="input-MYSELECT" multiple="multiple" 
        name="MYSELECT">
        <option id="input-MYSELECT-one" selected="selected" 
          value="one">One</option>
        <option id="input-MYSELECT-two" selected="selected" 
          value="two">Two</option>
        <option id="input-MYSELECT-three" value="three">Three</option>
        <option id="input-MYSELECT-four" value="four">Four</option>
      </select>
    </div>
    <BLANKLINE>

Extract multi valued selection and render widget with extracted data::

    >>> data = widget.extract(request={'MYSELECT': ['one', 'four']})
    >>> data
    <RuntimeData MYSELECT, value=['one', 'two'], extracted=['one', 'four'] at ...>

    >>> wrapped_pxml(widget(data=data))
    <div>
      <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden" 
        value="exists"/>
      <select class="select" id="input-MYSELECT" multiple="multiple" 
        name="MYSELECT">
        <option id="input-MYSELECT-one" selected="selected" 
          value="one">One</option>
        <option id="input-MYSELECT-two" value="two">Two</option>
        <option id="input-MYSELECT-three" value="three">Three</option>
        <option id="input-MYSELECT-four" selected="selected" 
          value="four">Four</option>
      </select>
    </div>
    <BLANKLINE>

Multi selection display mode::

    >>> widget.mode = 'display'
    >>> pxml(widget())
    <ul class="display-select" id="display-MYSELECT">
      <li>One</li>
      <li>Two</li>
    </ul>
    <BLANKLINE>

Multi selection display mode with display proxy::

    >>> widget.attrs['display_proxy'] = True
    >>> wrapped_pxml(widget())
    <div>
      <ul class="display-select" id="display-MYSELECT">
        <li>One</li>
        <li>Two</li>
      </ul>
      <input class="select" id="input-MYSELECT" name="MYSELECT" type="hidden" 
        value="one"/>
      <input class="select" id="input-MYSELECT" name="MYSELECT" type="hidden" 
        value="two"/>
    </div>
    <BLANKLINE>

Multi selection display mode with display proxy and extracted data::

    >>> data = widget.extract(request={'MYSELECT': ['one']})
    >>> data
    <RuntimeData MYSELECT, value=['one', 'two'], extracted=['one'] at ...>

    >>> wrapped_pxml(widget(data=data))
    <div>
      <ul class="display-select" id="display-MYSELECT">
        <li>One</li>
      </ul>
      <input class="select" id="input-MYSELECT" name="MYSELECT" type="hidden" 
        value="one"/>
    </div>
    <BLANKLINE>

Multi selection display with empty values list::

    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     value=[],
    ...     props={
    ...         'vocabulary': [],
    ...         'multivalued': True
    ...     },
    ...     mode='display')
    >>> wrapped_pxml(widget())
    <div>
      <div class="display-select" id="display-MYSELECT"/>
    </div>
    <BLANKLINE>

Multi selection display with missing term in vocab::

    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     value=['one', 'two'],
    ...     props={
    ...         'multivalued': True,
    ...         'vocabulary': [('two', 'Two')]
    ...     },
    ...     mode='display')
    >>> pxml(widget())
    <ul class="display-select" id="display-MYSELECT">
      <li>one</li>
      <li>Two</li>
    </ul>
    <BLANKLINE>

Multiple values on single valued selection fails::

    >>> vocab = [
    ...     ('one','One'),
    ...     ('two', 'Two'),
    ...     ('three', 'Three'),
    ...     ('four', 'Four')
    ... ]
    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     value=['one', 'two'],
    ...     props={
    ...         'vocabulary': vocab
    ...     })
    >>> pxml(widget())
    Traceback (most recent call last):
      ...
    ValueError: Multiple values for single selection.

Multi value selection with float datatype set::

    >>> vocab = [
    ...     (1.0,'One'),
    ...     (2.0, 'Two'),
    ...     (3.0, 'Three'),
    ...     (4.0, 'Four')
    ... ]
    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     value=[1.0, 2.0],
    ...     props={
    ...         'datatype': 'float',
    ...         'multivalued': True,
    ...         'vocabulary': vocab,
    ...         'emptyvalue': []
    ...     })
    >>> wrapped_pxml(widget())
    <div>
      <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden" 
        value="exists"/>
      <select class="select" id="input-MYSELECT" multiple="multiple" 
        name="MYSELECT">
        <option id="input-MYSELECT-1.0" selected="selected" 
          value="1.0">One</option>
        <option id="input-MYSELECT-2.0" selected="selected" 
          value="2.0">Two</option>
        <option id="input-MYSELECT-3.0" value="3.0">Three</option>
        <option id="input-MYSELECT-4.0" value="4.0">Four</option>
      </select>
    </div>
    <BLANKLINE>

    >>> request = {
    ...     'MYSELECT': ['2.0', '3.0']
    ... }
    >>> data = widget.extract(request=request)
    >>> data.extracted
    [2.0, 3.0]

    >>> wrapped_pxml(widget(data=data))
    <div>
      <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden" 
        value="exists"/>
      <select class="select" id="input-MYSELECT" multiple="multiple" 
        name="MYSELECT">
        <option id="input-MYSELECT-1.0" value="1.0">One</option>
        <option id="input-MYSELECT-2.0" selected="selected" 
          value="2.0">Two</option>
        <option id="input-MYSELECT-3.0" selected="selected" 
          value="3.0">Three</option>
        <option id="input-MYSELECT-4.0" value="4.0">Four</option>
      </select>
    </div>
    <BLANKLINE>

    >>> request = {
    ...     'MYSELECT': '4.0'
    ... }
    >>> data = widget.extract(request=request)
    >>> data.extracted
    [4.0]

    >>> request = {
    ...     'MYSELECT': ''
    ... }
    >>> data = widget.extract(request=request)
    >>> data.extracted
    []

Generic HTML5 Data::

    >>> vocab = [
    ...     ('one','One'),
    ...     ('two', 'Two')
    ... ]
    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     value=['one', 'two'],
    ...     props={
    ...         'multivalued': True,
    ...         'data': {'foo': 'bar'},
    ...         'vocabulary': vocab
    ...     })
    >>> wrapped_pxml(widget())
    <div>
      <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden" 
        value="exists"/>
      <select class="select" data-foo="bar" id="input-MYSELECT" 
        multiple="multiple" name="MYSELECT">
        <option id="input-MYSELECT-one" selected="selected" 
          value="one">One</option>
        <option id="input-MYSELECT-two" selected="selected" 
          value="two">Two</option>
      </select>
    </div>
    <BLANKLINE>

    >>> widget.mode = 'display'
    >>> pxml(widget())
    <ul class="display-select" data-foo="bar" id="display-MYSELECT">
      <li>One</li>
      <li>Two</li>
    </ul>
    <BLANKLINE>

Persist::

    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     value=['one', 'two'],
    ...     props={
    ...         'multivalued': True,
    ...         'vocabulary': vocab
    ...     })
    >>> data = widget.extract({'MYSELECT': ['one', 'two', 'three']})
    >>> model = dict()
    >>> data.persist_writer = write_mapping_writer
    >>> data.write(model)
    >>> model
    {'MYSELECT': ['one', 'two', 'three']}


With Checkboxes
...............

Render multi selection as checkboxes::

    >>> vocab = [
    ...     ('one','One'),
    ...     ('two', 'Two'),
    ...     ('three', 'Three'),
    ...     ('four', 'Four')
    ... ]
    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     value='one',
    ...     props={
    ...         'multivalued': True,
    ...         'vocabulary': vocab,
    ...         'format': 'single'
    ...     })
    >>> wrapped_pxml(widget())
    <div>
      <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden" 
        value="exists"/>
      <div id="checkbox-MYSELECT-wrapper">
        <div id="checkbox-MYSELECT-one">
          <label for="input-MYSELECT-one"><input checked="checked" 
            class="select" id="input-MYSELECT-one" name="MYSELECT" 
            type="checkbox" value="one"/>One</label>
        </div>
        <div id="checkbox-MYSELECT-two">
          <label for="input-MYSELECT-two"><input class="select" 
            id="input-MYSELECT-two" name="MYSELECT" type="checkbox" 
            value="two"/>Two</label>
        </div>
        <div id="checkbox-MYSELECT-three">
          <label for="input-MYSELECT-three"><input class="select" 
            id="input-MYSELECT-three" name="MYSELECT" type="checkbox" 
            value="three"/>Three</label>
        </div>
        <div id="checkbox-MYSELECT-four">
          <label for="input-MYSELECT-four"><input class="select" 
            id="input-MYSELECT-four" name="MYSELECT" type="checkbox" 
            value="four"/>Four</label>
        </div>
      </div>
    </div>
    <BLANKLINE>

Checkbox multi selection display mode. Note, other as above, preset value for
multivalued widget is set as string, which is treaten as one item selected and
covered with the below tests::

    >>> widget.mode = 'display'
    >>> pxml(widget())
    <ul class="display-select" id="display-MYSELECT">
      <li>One</li>
    </ul>
    <BLANKLINE>

Checkbox multi selection display mode with display proxy::

    >>> widget.attrs['display_proxy'] = True
    >>> wrapped_pxml(widget())
    <div>
      <ul class="display-select" id="display-MYSELECT">
        <li>One</li>
      </ul>
      <input class="select" id="input-MYSELECT" name="MYSELECT" type="hidden" 
        value="one"/>
    </div>
    <BLANKLINE>

Checkbox multi selection display mode with display proxy and extracted data::

    >>> data = widget.extract(request={'MYSELECT': ['two']})
    >>> data
    <RuntimeData MYSELECT, value='one', extracted=['two'] at ...>
    
    >>> wrapped_pxml(widget(data=data))
    <div>
      <ul class="display-select" id="display-MYSELECT">
        <li>Two</li>
      </ul>
      <input class="select" id="input-MYSELECT" name="MYSELECT" type="hidden" 
        value="two"/>
    </div>
    <BLANKLINE>

Generic HTML5 Data::

    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     value='one',
    ...     props={
    ...         'multivalued': True,
    ...         'data': {'foo': 'bar'},
    ...         'vocabulary': [('one','One')],
    ...         'format': 'single'
    ...     })
    >>> wrapped_pxml(widget())
    <div>
      <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden" 
        value="exists"/>
      <div data-foo="bar" id="checkbox-MYSELECT-wrapper">
        <div id="checkbox-MYSELECT-one">
          <label for="input-MYSELECT-one"><input checked="checked" 
            class="select" id="input-MYSELECT-one" name="MYSELECT" 
            type="checkbox" value="one"/>One</label>
        </div>
      </div>
    </div>
    <BLANKLINE>

    >>> widget.mode = 'display'
    >>> pxml(widget())
    <ul class="display-select" data-foo="bar" id="display-MYSELECT">
      <li>One</li>
    </ul>
    <BLANKLINE>


Specials
........

Using 'ul' instead of 'div' for rendering radio or checkbox selections::

    >>> vocab = [
    ...     ('one','One'),
    ...     ('two', 'Two'),
    ...     ('three', 'Three'),
    ...     ('four', 'Four')
    ... ]
    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     value='one',
    ...     props={
    ...         'multivalued': True,
    ...         'vocabulary': vocab,
    ...         'format': 'single',
    ...         'listing_tag': 'ul'
    ...     })
    >>> wrapped_pxml(widget())
    <div>
      <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden" 
        value="exists"/>
      <ul id="checkbox-MYSELECT-wrapper">
        <li id="checkbox-MYSELECT-one">
          <label for="input-MYSELECT-one"><input checked="checked" 
            class="select" id="input-MYSELECT-one" name="MYSELECT" 
            type="checkbox" value="one"/>One</label>
        </li>
        <li id="checkbox-MYSELECT-two">
          <label for="input-MYSELECT-two"><input class="select" 
            id="input-MYSELECT-two" name="MYSELECT" type="checkbox" 
            value="two"/>Two</label>
        </li>
        <li id="checkbox-MYSELECT-three">
          <label for="input-MYSELECT-three"><input class="select" 
            id="input-MYSELECT-three" name="MYSELECT" type="checkbox" 
            value="three"/>Three</label>
        </li>
        <li id="checkbox-MYSELECT-four">
          <label for="input-MYSELECT-four"><input class="select" 
            id="input-MYSELECT-four" name="MYSELECT" type="checkbox" 
            value="four"/>Four</label>
        </li>
      </ul>
    </div>
    <BLANKLINE>

Render single format selection with label after input::

    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     value='one',
    ...     props={
    ...         'multivalued': True,
    ...         'vocabulary': [
    ...             ('one','One'),
    ...             ('two', 'Two'),
    ...         ],
    ...         'format': 'single',
    ...         'listing_tag': 'ul',
    ...         'listing_label_position': 'after'
    ...     })
    >>> wrapped_pxml(widget())
    <div>
      <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden" 
        value="exists"/>
      <ul id="checkbox-MYSELECT-wrapper">
        <li id="checkbox-MYSELECT-one">
          <input checked="checked" class="select" id="input-MYSELECT-one" 
            name="MYSELECT" type="checkbox" value="one"/>
          <label for="input-MYSELECT-one">One</label>
        </li>
        <li id="checkbox-MYSELECT-two">
          <input class="select" id="input-MYSELECT-two" name="MYSELECT" 
            type="checkbox" value="two"/>
          <label for="input-MYSELECT-two">Two</label>
        </li>
      </ul>
    </div>
    <BLANKLINE>

Render single format selection with input inside label before checkbox::

    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     value='one',
    ...     props={
    ...         'multivalued': True,
    ...         'vocabulary': [
    ...             ('one','One'),
    ...             ('two', 'Two'),
    ...         ],
    ...         'format': 'single',
    ...         'listing_tag': 'ul',
    ...         'listing_label_position': 'inner-before'
    ...     })
    >>> wrapped_pxml(widget())
    <div>
      <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden" 
        value="exists"/>
      <ul id="checkbox-MYSELECT-wrapper">
        <li id="checkbox-MYSELECT-one">
          <label for="input-MYSELECT-one">One<input checked="checked" 
            class="select" id="input-MYSELECT-one" name="MYSELECT" 
            type="checkbox" value="one"/></label>
        </li>
        <li id="checkbox-MYSELECT-two">
          <label for="input-MYSELECT-two">Two<input class="select" 
            id="input-MYSELECT-two" name="MYSELECT" type="checkbox" 
            value="two"/></label>
        </li>
      </ul>
    </div>
    <BLANKLINE>

Check BBB 'inner' for 'listing_label_position' which behaves like
'inner-after'::

    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     value='one',
    ...     props={
    ...         'vocabulary': [('one','One')],
    ...         'format': 'single',
    ...         'listing_label_position': 'inner'
    ...     })
    >>> wrapped_pxml(widget())
    <div>
      <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden" 
        value="exists"/>
      <div id="radio-MYSELECT-wrapper">
        <div id="radio-MYSELECT-one">
          <label for="input-MYSELECT-one"><input checked="checked" 
            class="select" id="input-MYSELECT-one" name="MYSELECT" 
            type="radio" value="one"/>One</label>
        </div>
      </div>
    </div>
    <BLANKLINE>

Check selection required::

    >>> vocab = [
    ...     ('one','One'),
    ...     ('two', 'Two'),
    ...     ('three', 'Three'),
    ...     ('four', 'Four')
    ... ]
    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     props={
    ...         'required': 'Selection required',
    ...         'vocabulary': vocab
    ...     })
    >>> pxml(widget())
    <select class="select" id="input-MYSELECT" name="MYSELECT" 
      required="required">
      <option id="input-MYSELECT-one" value="one">One</option>
      <option id="input-MYSELECT-two" value="two">Two</option>
      <option id="input-MYSELECT-three" value="three">Three</option>
      <option id="input-MYSELECT-four" value="four">Four</option>
    </select>
    <BLANKLINE>

    >>> data = widget.extract(request={'MYSELECT': ''})
    >>> data.printtree()
    <RuntimeData MYSELECT, value=<UNSET>, extracted='', 1 error(s) at ...>

    >>> vocab = [
    ...     ('one','One'),
    ...     ('two', 'Two'),
    ...     ('three', 'Three'),
    ...     ('four', 'Four')
    ... ]
    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     props={
    ...         'required': 'Selection required',
    ...         'multivalued': True,
    ...         'vocabulary': vocab
    ...     })
    >>> wrapped_pxml(widget())
    <div>
      <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden" 
        value="exists"/>
      <select class="select" id="input-MYSELECT" multiple="multiple" 
        name="MYSELECT" required="required">
        <option id="input-MYSELECT-one" value="one">One</option>
        <option id="input-MYSELECT-two" value="two">Two</option>
        <option id="input-MYSELECT-three" value="three">Three</option>
        <option id="input-MYSELECT-four" value="four">Four</option>
      </select>
    </div>
    <BLANKLINE>

    >>> data = widget.extract(request={'MYSELECT-exists': 'exists'})
    >>> data.printtree()
    <RuntimeData MYSELECT, value=<UNSET>, extracted=[], 1 error(s) at ...>

Check selection required with datatype set::

    >>> vocab = [
    ...     (1,'One'),
    ...     (2, 'Two'),
    ...     (3, 'Three'),
    ...     (4, 'Four')
    ... ]
    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     props={
    ...         'required': 'Selection required',
    ...         'multivalued': True,
    ...         'vocabulary': vocab,
    ...         'datatype': int,
    ...     })
    >>> data = widget.extract(request={'MYSELECT-exists': 'exists'})
    >>> data.printtree()
    <RuntimeData MYSELECT, value=<UNSET>, extracted=[], 1 error(s) at ...>

    >>> data = widget.extract(request={'MYSELECT': ['1', '2']})
    >>> data.printtree()
    <RuntimeData MYSELECT, value=<UNSET>, extracted=[1, 2] at ...>

Single selection extraction without value::

    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     props={
    ...         'vocabulary': [
    ...             ('one','One'),
    ...             ('two', 'Two')
    ...         ]
    ...     })
    >>> request = {
    ...     'MYSELECT': 'one',
    ...     'MYSELECT-exists': True,
    ... }
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData MYSELECT, value=<UNSET>, extracted='one' at ...>

Single selection extraction with value::

    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     value='two',
    ...     props={
    ...         'vocabulary': [
    ...             ('one','One'),
    ...             ('two', 'Two')
    ...         ]
    ...     })
    >>> request = {
    ...     'MYSELECT': 'one',
    ... }
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData MYSELECT, value='two', extracted='one' at ...>

Single selection extraction disabled (means browser does not post the value)
with value::

    >>> widget.attrs['disabled'] = True
    >>> data = widget.extract({'MYSELECT-exists': True})
    >>> data.printtree()
    <RuntimeData MYSELECT, value='two', extracted='two' at ...>

Disabled can be also the value itself::

    >>> widget.attrs['disabled'] = 'two'
    >>> data = widget.extract({'MYSELECT-exists': True})
    >>> data.printtree()
    <RuntimeData MYSELECT, value='two', extracted='two' at ...>

Single selection extraction required::

    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     value='two',
    ...     props={
    ...         'required': True,
    ...         'vocabulary': [
    ...             ('one','One'),
    ...             ('two', 'Two')
    ...         ]
    ...     })
    >>> request = {
    ...     'MYSELECT': '',
    ... }
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData MYSELECT, value='two', extracted='', 1 error(s) at ...>

A disabled and required returns value itself::

    >>> widget.attrs['disabled'] = True
    >>> data = widget.extract({'MYSELECT-exists': True})
    >>> data.printtree()
    <RuntimeData MYSELECT, value='two', extracted='two' at ...>

Multiple selection extraction without value::

    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     props={
    ...         'multivalued': True,
    ...         'vocabulary': [
    ...             ('one','One'),
    ...             ('two', 'Two')
    ...         ]
    ...     })
    >>> request = {
    ...     'MYSELECT': ['one', 'two'],
    ... }
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData MYSELECT, value=<UNSET>, extracted=['one', 'two'] at ...>

Multiple selection extraction with value::

    >>> vocab = [
    ...     ('one','One'),
    ...     ('two', 'Two'),
    ...     ('three', 'Three')
    ... ]
    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     value='three',
    ...     props={
    ...         'multivalued': True,
    ...         'vocabulary': vocab
    ...     })
    >>> request = {
    ...     'MYSELECT': 'one',
    ...     'MYSELECT-exists': True,
    ... }
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData MYSELECT, value='three', extracted=['one'] at ...>

Multiselection, completly disabled::

    >>> widget.attrs['disabled'] = True
    >>> data = widget.extract({'MYSELECT-exists': True})
    >>> data.printtree()
    <RuntimeData MYSELECT, value='three', extracted=['three'] at ...>

Multiselection, partly disabled, empty request::

    >>> vocab = [
    ...     ('one','One'),
    ...     ('two', 'Two'),
    ...     ('three', 'Three'),
    ...     ('four', 'Four')
    ... ]
    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     value=['one', 'three'],
    ...     props={
    ...         'multivalued': True,
    ...         'disabled': ['two', 'three'],
    ...         'vocabulary': vocab
    ...     })
    >>> data = widget.extract({})
    >>> data.printtree()
    <RuntimeData MYSELECT, value=['one', 'three'], extracted=<UNSET> at ...>

Multiselection, partly disabled, non-empty request::

    >>> vocab = [
    ...     ('one','One'),
    ...     ('two', 'Two'),
    ...     ('three', 'Three'),
    ...     ('four', 'Four'),
    ...     ('five', 'Five')
    ... ]
    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     value=['one', 'two', 'four'],
    ...     props={
    ...         'multivalued': True,
    ...         'disabled': ['two', 'three', 'four', 'five'],
    ...         'vocabulary': vocab,
    ...         'datatype': unicode,
    ...     })
    >>> request = {
    ...     'MYSELECT': ['one', 'two', 'five'],
    ...     'MYSELECT-exists': True,
    ... }

Explanation:

* one is a simple value as usal,
* two is disabled and in value, so it should be kept in.
* three is disabled and not in value, so it should kept out,
* four is disabled and in value, but someone removed it in the request, it
  should get recovered,
* five is disabled and not in value, but someone put it in the request. it
  should get removed.

Check extraction::

    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData MYSELECT, value=['one', 'two', 'four'], 
    extracted=[u'one', u'two', u'four'] at ...>

Single selection radio extraction::

    >>> vocab = [
    ...     ('one','One'),
    ...     ('two', 'Two'),
    ...     ('three', 'Three')
    ... ]
    >>> widget = factory(
    ...     'select',
    ...     'MYSELECT',
    ...     props={
    ...         'format': 'single',
    ...         'vocabulary': vocab
    ...     })

No exists marker in request. Extracts to UNSET::

    >>> request = {}
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData MYSELECT, value=<UNSET>, extracted=<UNSET> at ...>

Exists marker in request. Extracts to empty string::

    >>> request = {
    ...     'MYSELECT-exists': '1',
    ... }
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData MYSELECT, value=<UNSET>, extracted='' at ...>

Select value::

    >>> request = {
    ...     'MYSELECT-exists': '1',
    ...     'MYSELECT': 'one',
    ... }
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData MYSELECT, value=<UNSET>, extracted='one' at ...>

Multi selection radio extraction::

    >>> vocab = [
    ...     ('one','One'),
    ...     ('two', 'Two'),
    ...     ('three', 'Three')
    ... ]
    >>> widget = factory(
    ...     'select',
    ...     name='MYSELECT',
    ...     props={
    ...         'multivalued': True,
    ...         'format': 'single',
    ...         'vocabulary': vocab
    ...     })

No exists marker in request. Extracts to UNSET::

    >>> request = {
    ... }
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData MYSELECT, value=<UNSET>, extracted=<UNSET> at ...>

Exists marker in request. Extracts to empty list::

    >>> request = {
    ...     'MYSELECT-exists': '1',
    ... }
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData MYSELECT, value=<UNSET>, extracted=[] at ...>

Select values::

    >>> request = {
    ...     'MYSELECT-exists': '1',
    ...     'MYSELECT': ['one', 'two'],
    ... }
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData MYSELECT, value=<UNSET>, extracted=['one', 'two'] at ...>


File
----

Render file input::

    >>> widget = factory(
    ...     'file',
    ...     name='MYFILE')
    >>> widget()
    u'<input id="input-MYFILE" name="MYFILE" type="file" />'

Extract empty::

    >>> request = {}
    >>> data = widget.extract(request)
    >>> data.extracted
    <UNSET>

Extract ``new``::

    >>> request = {
    ...     'MYFILE': {'file': StringIO('123')},
    ... }
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData MYFILE, value=<UNSET>,
    extracted={'action': 'new', 'file': <StringIO.StringIO instance at ...>}
    at ...>

    >>> data.extracted['action']
    'new'

    >>> data.extracted['file'].read()
    '123'

File with value preset::

    >>> widget = factory(
    ...     'file',
    ...     name='MYFILE',
    ...     value={
    ...         'file': StringIO('321'),
    ...     })
    >>> wrapped_pxml(widget())
    <div>
      <input id="input-MYFILE" name="MYFILE" type="file"/>
      <div id="radio-MYFILE-keep">
        <input checked="checked" id="input-MYFILE-keep" name="MYFILE-action" 
          type="radio" value="keep"/>
        <span>Keep Existing file</span>
      </div>
      <div id="radio-MYFILE-replace">
        <input id="input-MYFILE-replace" name="MYFILE-action" type="radio" 
          value="replace"/>
        <span>Replace existing file</span>
      </div>
      <div id="radio-MYFILE-delete">
        <input id="input-MYFILE-delete" name="MYFILE-action" type="radio" 
          value="delete"/>
        <span>Delete existing file</span>
      </div>
    </div>
    <BLANKLINE>

Extract ``keep`` returns original value::

    >>> request = {
    ...     'MYFILE': {'file': StringIO('123')},
    ...     'MYFILE-action': 'keep'
    ... }
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData MYFILE,
    value={'action': 'keep', 'file': <StringIO.StringIO instance at ...>},
    extracted={'action': 'keep', 'file': <StringIO.StringIO instance at ...>}
    at ...>

    >>> data.extracted['file'].read()
    '321'

    >>> data.extracted['action']
    'keep'

Extract ``replace`` returns new value::

    >>> request['MYFILE-action'] = 'replace'
    >>> data = widget.extract(request)
    >>> data.extracted
    {'action': 'replace', 'file': <StringIO.StringIO instance at ...>}

    >>> data.extracted['file'].read()
    '123'

    >>> data.extracted['action']
    'replace'

Extract empty ``replace`` results in ``kepp action``::

    >>> request = {
    ...     'MYFILE': '',
    ...     'MYFILE-action': 'replace'
    ... }
    >>> data = widget.extract(request)
    >>> data.extracted
    {'action': 'keep', 
    'file': <StringIO.StringIO instance at ...>}

Extract ``delete`` returns UNSET::

    >>> request['MYFILE-action'] = 'delete'
    >>> data = widget.extract(request)
    >>> data.extracted
    {'action': 'delete', 'file': <UNSET>}

    >>> data.extracted['action']
    'delete'

    >>> wrapped_pxml(widget(request=request))
    <div>
      <input id="input-MYFILE" name="MYFILE" type="file"/>
      <div id="radio-MYFILE-keep">
        <input id="input-MYFILE-keep" name="MYFILE-action" type="radio" 
          value="keep"/>
        <span>Keep Existing file</span>
      </div>
      <div id="radio-MYFILE-replace">
        <input id="input-MYFILE-replace" name="MYFILE-action" type="radio" 
          value="replace"/>
        <span>Replace existing file</span>
      </div>
      <div id="radio-MYFILE-delete">
        <input checked="checked" id="input-MYFILE-delete" name="MYFILE-action" 
          type="radio" value="delete"/>
        <span>Delete existing file</span>
      </div>
    </div>
    <BLANKLINE>

    >>> widget = factory(
    ...     'file',
    ...     name='MYFILE',
    ...     props={
    ...         'accept': 'foo/bar'
    ...     })
    >>> widget()
    u'<input accept="foo/bar" id="input-MYFILE" name="MYFILE"
    type="file" />'

File display renderer::

    >>> convert_bytes(1 * 1024 * 1024 * 1024 * 1024)
    '1.00T'

    >>> convert_bytes(1 * 1024 * 1024 * 1024)
    '1.00G'

    >>> convert_bytes(1 * 1024 * 1024)
    '1.00M'

    >>> convert_bytes(1 * 1024)
    '1.00K'

    >>> convert_bytes(1)
    '1.00b'

    >>> widget = factory(
    ...     'file',
    ...     name='MYFILE',
    ...     mode='display')
    >>> pxml(widget())
    <div>No file</div>
    <BLANKLINE>

    >>> value = {
    ...     'file': StringIO('12345'),
    ...     'mimetype': 'text/plain',
    ...     'filename': 'foo.txt',
    ... }
    >>> widget = factory(
    ...     'file',
    ...     name='MYFILE',
    ...     value=value,
    ...     mode='display')
    >>> pxml(widget())
    <div>
      <ul>
        <li><strong>Filename: </strong>foo.txt</li>
        <li><strong>Mimetype: </strong>text/plain</li>
        <li><strong>Size: </strong>5.00b</li>
      </ul>
    </div>
    <BLANKLINE>

Generic HTML5 Data::

    >>> widget = factory(
    ...     'file',
    ...     name='MYFILE',
    ...     props={
    ...         'accept': 'foo/bar',
    ...         'data': {
    ...             'foo': 'bar'
    ...         }
    ...     })
    >>> widget()
    u'<input accept="foo/bar" data-foo=\'bar\' 
    id="input-MYFILE" name="MYFILE" type="file" />'

    >>> widget.mode = 'display'
    >>> widget()
    u"<div data-foo='bar'>No file</div>"


Submit(action)
--------------

Render submit button::

    >>> widget = factory(
    ...     'submit',
    ...     name='SAVE',
    ...     props={
    ...         'action': True,
    ...         'label': 'Action name',
    ...     })
    >>> widget()
    u'<input id="input-SAVE" name="action.SAVE" type="submit" 
    value="Action name" />'

If expression is or evaluates to False, skip rendering::

    >>> widget = factory(
    ...     'submit',
    ...     name='SAVE',
    ...     props={
    ...         'action': True,
    ...         'label': 'Action name',
    ...         'expression': False,
    ...     })
    >>> widget()
    u''

    >>> widget = factory(
    ...     'submit',
    ...     name='SAVE',
    ...     props={
    ...         'action': True,
    ...         'label': 'Action name',
    ...         'expression': lambda: False,
    ...     })
    >>> widget()
    u''

Generic HTML5 Data::

    >>> widget = factory(
    ...     'submit',
    ...     name='SAVE',
    ...     props={
    ...         'action': True,
    ...         'label': 'Action name',
    ...         'data': {'foo': 'bar'},
    ...     })
    >>> widget()
    u'<input data-foo=\'bar\' id="input-SAVE" name="action.SAVE" 
    type="submit" value="Action name" />'


Proxy
-----

Used to pass hidden arguments out of form namespace::

    >>> widget = factory(
    ...     'proxy',
    ...     name='PROXY',
    ...     value='1')
    >>> widget()
    u'<input id="input-PROXY" name="PROXY" type="hidden" value="1" />'

    >>> widget(request={'PROXY': '2'})
    u'<input id="input-PROXY" name="PROXY" type="hidden" value="2" />'

Emptyvalue::

    >>> widget = factory(
    ...     'proxy',
    ...     name='PROXY',
    ...     value='',
    ...     props={
    ...         'emptyvalue': '1.0'
    ...     })
    >>> widget.extract(request={'PROXY': ''})
    <RuntimeData PROXY, value='', extracted='1.0' at ...>

Datatype::

    >>> widget = factory(
    ...     'proxy',
    ...     name='PROXY',
    ...     value='',
    ...     props={
    ...         'emptyvalue': '1.0',
    ...         'datatype': float
    ...     })
    >>> widget.extract(request={'PROXY': '2.0'})
    <RuntimeData PROXY, value='', extracted=2.0 at ...>

    >>> widget.extract(request={'PROXY': ''})
    <RuntimeData PROXY, value='', extracted=1.0 at ...>

Default emptyvalue extraction::

    >>> del widget.attrs['emptyvalue']
    >>> widget.extract(request={'PROXY': ''})
    <RuntimeData PROXY, value='', extracted=<EMPTY_VALUE> at ...>

Persist defaults to false::

    >>> widget = factory(
    ...     'proxy',
    ...     name='PROXY',
    ...     props={
    ...         'persist_writer': write_mapping_writer
    ...     })
    >>> data = widget.extract(request={'PROXY': '10'})
    >>> model = dict()
    >>> data.write(model)
    >>> model
    {}

If proxy widgets really need to be persisted, ``persist`` property needs to be
set explicitely::

    >>> widget.attrs['persist'] = True
    >>> data = widget.extract(request={'PROXY': '10'})
    >>> data.write(model)
    >>> model
    {'PROXY': '10'}


Label
-----

Default::

    >>> widget = factory(
    ...     'label:file',
    ...     name='MYFILE',
    ...     props={
    ...         'label': 'MY FILE'
    ...     })
    >>> wrapped_pxml(widget())
    <div>
      <label for="input-MYFILE">MY FILE</label>
      <input id="input-MYFILE" name="MYFILE" type="file"/>
    </div>
    <BLANKLINE>

Label after widget::

    >>> widget = factory(
    ...     'label:file',
    ...     name='MYFILE',
    ...     props={
    ...         'label': 'MY FILE',
    ...         'label.position': 'after'
    ...     })
    >>> wrapped_pxml(widget())
    <div>
      <input id="input-MYFILE" name="MYFILE" type="file"/>
      <label for="input-MYFILE">MY FILE</label>
    </div>
    <BLANKLINE>

Same with inner label::

    >>> widget = factory(
    ...     'label:file',
    ...     name='MYFILE',
    ...     props={
    ...         'label': 'MY FILE',
    ...         'label.position': 'inner'
    ...     })
    >>> wrapped_pxml(widget())
    <div>
      <label for="input-MYFILE">MY FILE<input id="input-MYFILE" name="MYFILE" 
        type="file"/></label>
    </div>
    <BLANKLINE>

Invalid position::

    >>> widget = factory(
    ...     'label:file',
    ...     name='MYFILE',
    ...     props={
    ...         'label': 'MY FILE',
    ...         'label.position': 'inexistent'
    ...     })
    >>> wrapped_pxml(widget())
    Traceback (most recent call last):
      ...
    ValueError: Invalid value for position "inexistent"

Render with title attribute::

    >>> widget = factory(
    ...     'label',
    ...     name='MYFILE', \
    ...     props={
    ...         'title': 'My awesome title',
    ...     })
    >>> widget()
    u'<label for="input-MYFILE" title="My awesome title">MYFILE</label>'

Label Text can be a callable::

    >>> widget = factory(
    ...     'label',
    ...     name='MYFILE', \
    ...     props={
    ...         'label': lambda: 'Fooo',
    ...     })
    >>> widget()
    u'<label for="input-MYFILE">Fooo</label>'

Position can be callable::

    >>> widget = factory(
    ...     'label',
    ...     name='MYFILE', \
    ...     props={
    ...         'label': 'Fooo',
    ...         'position': lambda x, y: 'inner',
    ...     })
    >>> widget()
    u'<label for="input-MYFILE">Fooo</label>'


Field
-----

Chained file inside field with label::

    >>> widget = factory(
    ...     'field:label:file',
    ...     name='MYFILE',
    ...     props={
    ...         'label': 'MY FILE'
    ...     })
    >>> pxml(widget())
    <div class="field" id="field-MYFILE">
      <label for="input-MYFILE">MY FILE</label>
      <input id="input-MYFILE" name="MYFILE" type="file"/>
    </div>
    <BLANKLINE>

Render error class directly on field::

    >>> widget = factory(
    ...     'field:text',
    ...     name='MYFIELD',
    ...     props={
    ...         'required': True,
    ...         'witherror': 'fielderrorclass'
    ...     })
    >>> data = widget.extract({'MYFIELD': ''})
    >>> data.printtree()
    <RuntimeData MYFIELD, value=<UNSET>, extracted='', 1 error(s) at ...>

    >>> pxml(widget(data))
    <div class="field fielderrorclass" id="field-MYFIELD">
      <input class="required text" id="input-MYFIELD" name="MYFIELD" 
        required="required" type="text" value=""/>
    </div>
    <BLANKLINE>


Password
--------

Password widget has some additional properties, ``strength``, ``minlength``
and ``ascii``.

Use in add forms, no password set yet::

    >>> widget = factory(
    ...     'password',
    ...     name='PWD')
    >>> widget()
    u'<input class="password" id="input-PWD" name="PWD" type="password" 
    value="" />'

    >>> data = widget.extract({})
    >>> data.extracted
    <UNSET>

    >>> data = widget.extract({'PWD': 'xx'})
    >>> data.extracted
    'xx'

    >>> widget.mode = 'display'
    >>> widget()
    u''

Use in edit forms. note that password is never shown up in markup, but a
placeholder is used when a password is already set. Thus, if a extracted
password value is UNSET, this means that password was not changed::

    >>> widget = factory(
    ...     'password',
    ...     name='PASSWORD',
    ...     value='secret')
    >>> widget()
    u'<input class="password" id="input-PASSWORD" name="PASSWORD" 
    type="password" value="_NOCHANGE_" />'

    >>> data = widget.extract({'PASSWORD': '_NOCHANGE_'})
    >>> data.extracted
    <UNSET>

    >>> data = widget.extract({'PASSWORD': 'foo'})
    >>> data.extracted
    'foo'

    >>> widget(data=data)
    u'<input class="password" id="input-PASSWORD" name="PASSWORD" 
    type="password" value="foo" />'

    >>> widget.mode = 'display'
    >>> widget()
    u'********'

Password validation::

    >>> widget = factory(
    ...     'password',
    ...     name='PWD',
    ...     props={
    ...         'strength': 5, # max 4, does not matter, max is used
    ...     })
    >>> data = widget.extract({'PWD': ''})
    >>> data.errors
    [ExtractionError('Password too weak',)]

    >>> data = widget.extract({'PWD': 'A0*'})
    >>> data.errors
    [ExtractionError('Password too weak',)]

    >>> data = widget.extract({'PWD': 'a0*'})
    >>> data.errors
    [ExtractionError('Password too weak',)]

    >>> data = widget.extract({'PWD': 'aA*'})
    >>> data.errors
    [ExtractionError('Password too weak',)]

    >>> data = widget.extract({'PWD': 'aA0'})
    >>> data.errors
    [ExtractionError('Password too weak',)]

    >>> data = widget.extract({'PWD': 'aA0*'})
    >>> data.errors
    []

Minlength validation::

    >>> widget = factory(
    ...     'password',
    ...     name='PWD',
    ...     props={
    ...         'minlength': 3,
    ...     })
    >>> data = widget.extract({'PWD': 'xx'})
    >>> data.errors
    [ExtractionError('Input must have at least 3 characters.',)]

    >>> data = widget.extract({'PWD': 'xxx'})
    >>> data.errors
    []

Ascii validation::

    >>> widget = factory(
    ...     'password',
    ...     name='PWD',
    ...     props={
    ...         'ascii': True,
    ...     })
    >>> data = widget.extract({'PWD': u'äää'})
    >>> data.errors
    [ExtractionError('Input contains illegal characters.',)]

    >>> data = widget.extract({'PWD': u'xx'})
    >>> data.errors
    []

Combine all validations::

    >>> widget = factory(
    ...     'password',
    ...     name='PWD',
    ...     props={
    ...         'required': 'No Password given',
    ...         'minlength': 6,
    ...         'ascii': True,
    ...         'strength': 4,
    ...     })
    >>> data = widget.extract({'PWD': u''})
    >>> data.errors
    [ExtractionError('No Password given',)]

    >>> data = widget.extract({'PWD': u'xxxxx'})
    >>> data.errors
    [ExtractionError('Input must have at least 6 characters.',)]

    >>> data = widget.extract({'PWD': u'xxxxxä'})
    >>> data.errors
    [ExtractionError('Input contains illegal characters.',)]

    >>> data = widget.extract({'PWD': u'xxxxxx'})
    >>> data.errors
    [ExtractionError('Password too weak',)]

    >>> data = widget.extract({'PWD': u'xX1*00'})
    >>> data.errors
    []

Emptyvalue::

    >>> widget = factory(
    ...     'password',
    ...     name='PWD',
    ...     props={
    ...         'emptyvalue': 'DEFAULTPWD',  # <- not a good idea, but works
    ...     })
    >>> widget.extract(request={'PWD': ''})
    <RuntimeData PWD, value=<UNSET>, extracted='DEFAULTPWD' at ...>

    >>> widget.extract(request={'PWD': 'NOEMPTY'})
    <RuntimeData PWD, value=<UNSET>, extracted='NOEMPTY' at ...>

Persist::

    >>> widget = factory(
    ...     'password',
    ...     name='PWD',
    ...     props={
    ...         'persist_writer': write_mapping_writer
    ...     })
    >>> data = widget.extract(request={'PWD': '1234'})
    >>> model = dict()
    >>> data.write(model)
    >>> model
    {'PWD': '1234'}


Error
-----

Chained password inside error inside field::

    >>> widget = factory(
    ...     'field:error:password',
    ...     name='PASSWORD',
    ...     props={
    ...         'label': 'Password',
    ...         'required': 'No password given!'
    ...     })
    >>> data = widget.extract({'PASSWORD': ''})
    >>> pxml(widget(data=data))
    <div class="field" id="field-PASSWORD">
      <div class="error">
        <div class="errormessage">No password given!</div>
        <input class="password required" id="input-PASSWORD" name="PASSWORD" 
          required="required" type="password" value=""/>
      </div>
    </div>
    <BLANKLINE>

    >>> data = widget.extract({'PASSWORD': 'secret'})
    >>> pxml(widget(data=data))
    <div class="field" id="field-PASSWORD">
      <input class="password required" id="input-PASSWORD" name="PASSWORD" 
        required="required" type="password" value="secret"/>
    </div>
    <BLANKLINE>

    >>> widget = factory(
    ...     'error:text',
    ...     name='MYDISPLAY',
    ...     value='somevalue',
    ...     mode='display')
    >>> widget()
    u'<div class="display-text" id="display-MYDISPLAY">somevalue</div>'

Error wrapping in div element can be suppressed::

    >>> widget = factory(
    ...     'field:error:password',
    ...     name='PASSWORD',
    ...     props={
    ...         'label': 'Password',
    ...         'required': 'No password given!',
    ...         'message_tag': None
    ...     })
    >>> data = widget.extract({'PASSWORD': ''})
    >>> pxml(widget(data=data))
    <div class="field" id="field-PASSWORD">
      <div class="error">No password given!<input class="password required" 
        id="input-PASSWORD" name="PASSWORD" required="required" 
        type="password" value=""/></div>
    </div>
    <BLANKLINE>


Help
----

Render some additional help text::

    >>> widget = factory(
    ...     'field:help:text',
    ...     name='HELPEXAMPLE',
    ...     props={
    ...         'label': 'Help',
    ...         'help': 'Shout out loud here'
    ...     })
    >>> pxml(widget())
    <div class="field" id="field-HELPEXAMPLE">
      <div class="help">Shout out loud here</div>
      <input class="text" id="input-HELPEXAMPLE" name="HELPEXAMPLE" 
        type="text" value=""/>
    </div>
    <BLANKLINE>

Render empty (WHAT'S THIS GOOD FOR?)::

    >>> widget = factory(
    ...     'field:help:text',
    ...     name='HELPEXAMPLE',
    ...     props={
    ...         'label': 'Help',
    ...         'help': False,
    ...         'render_empty': False
    ...     })
    >>> pxml(widget())
    <div class="field" id="field-HELPEXAMPLE">
      <input class="text" id="input-HELPEXAMPLE" name="HELPEXAMPLE" 
        type="text" value=""/>
    </div>
    <BLANKLINE>


E-Mail
------

Render email input field::

    >>> widget = factory(
    ...     'email',
    ...     name='EMAIL')
    >>> pxml(widget())
    <input class="email" id="input-EMAIL" name="EMAIL" type="email" value=""/>

Extract not required and empty::

    >>> data = widget.extract({'EMAIL': ''})
    >>> data.errors
    []

Extract invalid email input::

    >>> data = widget.extract({'EMAIL': 'foo@bar'})
    >>> data.errors
    [ExtractionError('Input not a valid email address.',)]

    >>> data = widget.extract({'EMAIL': '@bar.com'})
    >>> data.errors
    [ExtractionError('Input not a valid email address.',)]

Extract valid email input::

    >>> data = widget.extract({'EMAIL': 'foo@bar.com'})
    >>> data.errors
    []

Extract required email input::

    >>> widget = factory(
    ...     'email',
    ...     name='EMAIL',
    ...     props={
    ...         'required': 'E-Mail Address is required'
    ...     })
    >>> data = widget.extract({'EMAIL': ''})
    >>> data.errors
    [ExtractionError('E-Mail Address is required',)]

    >>> data = widget.extract({'EMAIL': 'foo@bar.com'})
    >>> data.errors
    []

Emptyvalue::

    >>> widget = factory(
    ...     'email',
    ...     name='EMAIL',
    ...     props={
    ...         'emptyvalue': 'foo@bar.baz',
    ...     })
    >>> widget.extract(request={'EMAIL': ''})
    <RuntimeData EMAIL, value=<UNSET>, extracted='foo@bar.baz' at ...>

    >>> widget.extract(request={'EMAIL': 'foo@baz.bam'})
    <RuntimeData EMAIL, value=<UNSET>, extracted='foo@baz.bam' at ...>

Datatype::

    >>> widget = factory(
    ...     'email',
    ...     name='EMAIL',
    ...     props={
    ...         'datatype': unicode
    ...     })
    >>> widget.extract(request={'EMAIL': 'foo@example.com'})
    <RuntimeData EMAIL, value=<UNSET>, extracted=u'foo@example.com' at ...>

    >>> widget = factory(
    ...     'email',
    ...     name='EMAIL',
    ...     props={
    ...         'datatype': str
    ...     })
    >>> widget.extract(request={'EMAIL': u'foo@example.com'})
    <RuntimeData EMAIL, value=<UNSET>, extracted='foo@example.com' at ...>

Persist::

    >>> widget = factory(
    ...     'email',
    ...     name='EMAIL')
    >>> data = widget.extract({'EMAIL': 'foo@bar.baz'})
    >>> model = dict()
    >>> data.persist_writer = write_mapping_writer
    >>> data.write(model)
    >>> model
    {'EMAIL': 'foo@bar.baz'}


URL
---

Render URL input field::

    >>> widget = factory(
    ...     'url',
    ...     name='URL')
    >>> pxml(widget())
    <input class="url" id="input-URL" name="URL" type="url" value=""/>

Extract not required and empty::

    >>> data = widget.extract({'URL': ''})
    >>> data.errors
    []

Extract invalid URL input::

    >>> data = widget.extract({'URL': 'htt:/bla'})
    >>> data.errors
    [ExtractionError('Input not a valid web address.',)]

    >>> data = widget.extract({'URL': 'invalid'})
    >>> data.errors
    [ExtractionError('Input not a valid web address.',)]

Extract value URL input::

    >>> data = widget.extract({
    ...     'URL': 'http://www.foo.bar.com:8080/bla#fasel?blubber=bla&bla=fasel'
    ... })
    >>> data.errors
    []

Emptyvalue::

    >>> widget = factory(
    ...     'url',
    ...     name='URL',
    ...     props={
    ...         'emptyvalue': 'http://www.example.com',
    ...     })
    >>> widget.extract(request={'URL': ''})
    <RuntimeData URL, value=<UNSET>, extracted='http://www.example.com' at ...>

    >>> widget.extract(request={'URL': 'http://www.example.org'})
    <RuntimeData URL, value=<UNSET>, extracted='http://www.example.org' at ...>

Persist::

    >>> widget = factory(
    ...     'url',
    ...     name='URL')
    >>> data = widget.extract({'URL': 'http://www.example.org'})
    >>> model = dict()
    >>> data.persist_writer = write_mapping_writer
    >>> data.write(model)
    >>> model
    {'URL': 'http://www.example.org'}


Search
------

Render search input field::

    >>> widget = factory(
    ...     'search',
    ...     name='SEARCH')
    >>> pxml(widget())
    <input class="search" id="input-SEARCH" name="SEARCH" 
    type="search" value=""/>

Extract not required and empty::

    >>> data = widget.extract({'SEARCH': ''})
    >>> data.errors
    []

Extract required empty::

    >>> widget.attrs['required'] = True
    >>> widget.extract({'SEARCH': ''})
    <RuntimeData SEARCH, value=<UNSET>, extracted='', 1 error(s) at ...>

    >>> del widget.attrs['required']

Emptyvalue::

    >>> widget.attrs['emptyvalue'] = 'defaultsearch'
    >>> widget.extract(request={'SEARCH': ''})
    <RuntimeData SEARCH, value=<UNSET>, extracted='defaultsearch' at ...>

    >>> widget.extract(request={'SEARCH': 'searchstr'})
    <RuntimeData SEARCH, value=<UNSET>, extracted='searchstr' at ...>


Number
------

Display renderer::

    >>> widget = factory(
    ...     'number',
    ...     name='NUMBER',
    ...     value=3,
    ...     mode='display')
    >>> pxml(widget())
    <div class="display-number" id="display-NUMBER">3</div>
    <BLANKLINE>

Render number input::

    >>> widget = factory(
    ...     'number',
    ...     name='NUMBER',
    ...     value=lambda w,d:3)
    >>> pxml(widget())
    <input class="number" id="input-NUMBER" 
    name="NUMBER" type="number" value="3"/>
    <BLANKLINE>

Extract unset::

    >>> data = widget.extract({})
    >>> data.errors, data.extracted
    ([], <UNSET>)

    >>> data.printtree()
    <RuntimeData NUMBER, value=3, extracted=<UNSET> at ...>

Extract not required and empty::

    >>> data = widget.extract({'NUMBER': ''})
    >>> data.errors, data.extracted
    ([], <UNSET>)

Extract invalid floating point input::

    >>> data = widget.extract({'NUMBER': 'abc'})
    >>> data.errors
    [ExtractionError('Input is not a valid floating point number.',)]

Extract valid floating point input::

    >>> data = widget.extract({'NUMBER': '10'})
    >>> data.errors, data.extracted
    ([], 10.0)

    >>> data = widget.extract({'NUMBER': '10.0'})
    >>> data.errors, data.extracted
    ([], 10.0)

    >>> data = widget.extract({'NUMBER': '10,0'})
    >>> data.errors, data.extracted
    ([], 10.0)

Instanciate with invalid datatype::

    >>> widget = factory(
    ...     'number',
    ...     name='NUMBER',
    ...     props={
    ...         'datatype': 'invalid'
    ...     })
    >>> widget.extract({'NUMBER': '10.0'})
    Traceback (most recent call last):
      ...
    ValueError: Datatype not allowed: "invalid"

Extract invalid integer input::

    >>> widget = factory(
    ...     'number',
    ...     name='NUMBER',
    ...     props={
    ...         'datatype': 'integer'
    ...     })
    >>> data = widget.extract({'NUMBER': '10.0'})
    >>> data.errors
    [ExtractionError('Input is not a valid integer.',)]

Extract with min value set::

    >>> widget = factory(
    ...     'number',
    ...     name='NUMBER',
    ...     props={
    ...         'min': 10
    ...     })
    >>> data = widget.extract({'NUMBER': '9'})
    >>> data.errors
    [ExtractionError('Value has to be at minimum 10.',)]

    >>> data = widget.extract({'NUMBER': '10'})
    >>> data.errors
    []

    >>> data = widget.extract({'NUMBER': '11'})
    >>> data.errors
    []

Extract min value 0::

    >>> widget = factory(
    ...     'number',
    ...     name='NUMBER',
    ...     props={
    ...         'min': 0
    ...     })
    >>> data = widget.extract({'NUMBER': '-1'})
    >>> data.errors
    [ExtractionError('Value has to be at minimum 0.',)]

    >>> data = widget.extract({'NUMBER': '0'})
    >>> data.errors
    []

Extract with max value set::

    >>> widget = factory(
    ...     'number',
    ...     name='NUMBER',
    ...     props={
    ...         'max': lambda w,d: 10
    ...     })
    >>> data = widget.extract({'NUMBER': '9'})
    >>> data.errors
    []

    >>> data = widget.extract({'NUMBER': '10'})
    >>> data.errors
    []

    >>> data = widget.extract({'NUMBER': '11'})
    >>> data.errors
    [ExtractionError('Value has to be at maximum 10.',)]

Extract max value 0::

    >>> widget = factory(
    ...     'number',
    ...     name='NUMBER',
    ...     props={
    ...         'max': 0
    ...     })
    >>> data = widget.extract({'NUMBER': '1'})
    >>> data.errors
    [ExtractionError('Value has to be at maximum 0.',)]

    >>> data = widget.extract({'NUMBER': '0'})
    >>> data.errors
    []

Extract with step set::

    >>> widget = factory(
    ...     'number',
    ...     name='NUMBER',
    ...     props={
    ...         'step': 2
    ...     })
    >>> data = widget.extract({'NUMBER': '9'})
    >>> data.errors
    [ExtractionError('Value 9.0 has to be in stepping of 2',)]

    >>> data = widget.extract({'NUMBER': '6'})
    >>> data.errors
    []

Extract with step and min value set::

    >>> widget = factory(
    ...     'number',
    ...     name='NUMBER',
    ...     props={
    ...         'step': 2,
    ...         'min': 3
    ...     })
    >>> data = widget.extract({'NUMBER': '7'})
    >>> data.errors
    []

    >>> data = widget.extract({'NUMBER': '6'})
    >>> data.errors
    [ExtractionError('Value 6.0 has to be in stepping of 2 based on a 
    floor value of 3',)]

Extract 0 value::

    >>> widget = factory(
    ...     'number',
    ...     name='NUMBER')
    >>> data = widget.extract({'NUMBER': '0'})
    >>> data.extracted
    0.0

    >>> widget = factory(
    ...     'number',
    ...     name='NUMBER',
    ...     props={
    ...         'datatype': 'int'
    ...     })
    >>> data = widget.extract({'NUMBER': '0'})
    >>> data.extracted
    0

Persist::

    >>> widget = factory(
    ...     'number',
    ...     name='NUMBER',
    ...     props={
    ...         'datatype': 'int'
    ...     })
    >>> data = widget.extract({'NUMBER': '0'})
    >>> model = dict()
    >>> data.persist_writer = write_mapping_writer
    >>> data.write(model)
    >>> model
    {'NUMBER': 0}
