# -*- coding: utf-8 -*-

Common Blueprints
=================

This test creates widgets from ist blueprints with different properties.


Prepare
-------

Trigger registry by importing module::

    >>> import yafowil.common

Helper::

    >>> from yafowil.utils import Tag
    >>> tag = Tag(lambda msg: msg)


Hidden
------

::
    >>> from yafowil.base import factory
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


Generic tag
-----------
::
    >>> widget = factory('tag', name='MYTAG', props={
    ...     'tag': 'h3',
    ...     'text': 'A Headline',
    ...     'class': 'form_heading'})
    >>> widget()
    u'<h3 class="form_heading" id="tag-MYTAG">A Headline</h3>'


Text Input
----------
::
    >>> widget = factory(
    ...     'text',
    ...     name='MYTEXT',
    ...     value='Test Text')
    >>> widget()
    u'<input class="text" id="input-MYTEXT" name="MYTEXT" type="text"
    value="Test Text" />'

    >>> widget.mode = 'display'
    >>> widget()
    u'<div class="display-text" id="display-MYTEXT">Test Text</div>'


Render with title attribute::

    >>> widget = factory(
    ...     'text',
    ...     name='MYTEXT',
    ...     value='ja ha!',
    ...     props={
    ...         'title': 'My awesome title'})
    >>> widget()
    u'<input class="text" id="input-MYTEXT" name="MYTEXT" title="My awesome title" type="text" value="ja ha!" />'



Autofocus Text Input
--------------------
::
    >>> widget = factory(
    ...     'text',
    ...     name='AUTOFOCUS',
    ...     value='',
    ...     props={
    ...         'autofocus': True})
    >>> widget()
    u'<input autofocus="autofocus" class="text" id="input-AUTOFOCUS"
    name="AUTOFOCUS" type="text" value="" />'


Placeholder Text Input
----------------------
::
    >>> widget = factory(
    ...     'text',
    ...     name='PLACEHOLDER',
    ...     value='',
    ...     props={
    ...         'placeholder': 'This is a placeholder.'})
    >>> widget()
    u'<input class="text" id="input-PLACEHOLDER" name="PLACEHOLDER"
    placeholder="This is a placeholder." type="text" value="" />'


Required Input
--------------
::
    >>> widget = factory(
    ...     'text',
    ...     name='REQUIRED',
    ...     value='',
    ...     props={
    ...         'required': True,
    ...         'error_class': True})
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
    ...         'error_class': True})
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
    ...         'required': 'You fool, fill in a value!'})
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
    ...         'required': required_callback})
    >>> data = widget.extract({'REQUIRED': ''})
    >>> data.errors
    [ExtractionError('Foooo',)]

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
    ...     props=dict(template='%0.3f'))
    >>> widget()
        u'<div class="display-text" id="display-DISPLAY">123.457</div>'

    >>> def mytemplate(widget, data):
    ...     return '<TEMPLATE>%s</TEMPLATE>' % data.value
    >>> widget = factory(
    ...     'text',
    ...     name='DISPLAY',
    ...     value='lorem ipsum',
    ...     mode='display',
    ...     props=dict(template=mytemplate))
    >>> widget()
    u'<div class="display-text" id="display-DISPLAY"><TEMPLATE>lorem
    ipsum</TEMPLATE></div>'

``display_proxy`` can be used if mode is 'display' to proxy the value in a
hidden field::

    >>> widget = factory(
    ...     'text',
    ...     name='DISPLAY',
    ...     value='lorem ipsum',
    ...     mode='display',
    ...     props={'display_proxy': True})
    >>> widget()
    u'<div class="display-text" id="display-DISPLAY">lorem ipsum</div><input 
    class="text" id="input-DISPLAY" name="DISPLAY" type="hidden" 
    value="lorem ipsum" />'

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


Checkbox
--------

A boolean checkbox widget (default)::

    >>> widget = factory('checkbox', 'MYCHECKBOX')
    >>> widget()
    u'<input id="input-MYCHECKBOX" name="MYCHECKBOX"
    type="checkbox" value="" /><input id="checkboxexists-MYCHECKBOX"
    name="MYCHECKBOX-exists" type="hidden" value="checkboxexists" />'

    >>> widget.mode = 'display'
    >>> widget()
    u'<div class="display-None" id="display-MYCHECKBOX">no</div>'

    >>> widget = factory('checkbox', 'MYCHECKBOX', value='True')
    >>> widget()
    u'<input checked="checked" id="input-MYCHECKBOX" name="MYCHECKBOX"
    type="checkbox" value="" /><input id="checkboxexists-MYCHECKBOX"
    name="MYCHECKBOX-exists" type="hidden" value="checkboxexists" />'

    >>> widget.mode = 'display'
    >>> widget()
    u'<div class="display-None" id="display-MYCHECKBOX">yes</div>'

A checkbox widget with a value or an empty string::

    >>> widget = factory(
    ...     'checkbox',
    ...     'MYCHECKBOX',
    ...     value='',
    ...     props={'format': 'string'})
    >>> pxml('<div>'+widget()+'</div>')
    <div>
      <input id="input-MYCHECKBOX" name="MYCHECKBOX" type="checkbox" value=""/>
      <input id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists"
      type="hidden" value="checkboxexists"/>
    </div>

    >>> widget.mode = 'display'
    >>> widget()
    u'<div class="display-None" id="display-MYCHECKBOX">no</div>'

    >>> widget = factory(
    ...     'checkbox',
    ...     'MYCHECKBOX',
    ...     value='Test Checkbox',
    ...     props={'format': 'string'})
    >>> pxml('<div>'+widget()+'</div>')
    <div>
      <input checked="checked" id="input-MYCHECKBOX" name="MYCHECKBOX"
      type="checkbox" value="Test Checkbox"/>
      <input id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists"
      type="hidden" value="checkboxexists"/>
    </div>
    <BLANKLINE>

    >>> widget.mode = 'display'
    >>> widget()
    u'<div class="display-None" id="display-MYCHECKBOX">Test Checkbox</div>'

    >>> widget.mode = 'edit'

Checkbox with manually set 'checked' attribute::

    >>> widget = factory(
    ...     'checkbox',
    ...     'MYCHECKBOX',
    ...     value='',
    ...     props={
    ...         'format': 'string',
    ...         'checked': True,
    ...     })
    >>> pxml('<div>'+widget()+'</div>')
    <div>
      <input checked="checked" id="input-MYCHECKBOX" name="MYCHECKBOX"
      type="checkbox" value=""/>
      <input id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists"
      type="hidden" value="checkboxexists"/>
    </div>
    <BLANKLINE>

    >>> widget = factory(
    ...     'checkbox',
    ...     'MYCHECKBOX',
    ...     value='Test Checkbox',
    ...     props={
    ...         'format': 'string',
    ...         'checked': False,
    ...     })
    >>> pxml('<div>'+widget()+'</div>')
    <div>
      <input id="input-MYCHECKBOX" name="MYCHECKBOX" type="checkbox"
      value="Test Checkbox"/>
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

bool extraction::

    >>> widget = factory(
    ...     'checkbox',
    ...     'MYCHECKBOX',
    ...     value='Test Checkbox',
    ...     props={'format': 'bool'})
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

invalid format::

    >>> widget = factory(
    ...     'checkbox',
    ...     'MYCHECKBOX',
    ...     props={'format': 'invalid'})
    >>> request = {
    ...     'MYCHECKBOX': '',
    ...     'MYCHECKBOX-exists': 'checkboxexists'
    ... }
    >>> data = widget.extract(request)
    Traceback (most recent call last):
      ...
    ValueError: Checkbox widget has invalid format 'invalid' set

Render in display mode::

    >>> widget = factory('checkbox', 'MYCHECKBOX', value=False, mode='display',
    ...     props={
    ...         'format': 'bool'})
    >>> pxml('<div>' + widget() + '</div>')
    <div>
      <div class="display-None" id="display-MYCHECKBOX">no</div>
    </div>
    <BLANKLINE>
    
    >>> widget = factory('checkbox', 'MYCHECKBOX', value=True, mode='display',
    ...     props={
    ...         'format': 'bool'})
    >>> pxml('<div>' + widget() + '</div>')
    <div>
      <div class="display-None" id="display-MYCHECKBOX">yes</div>
    </div>
    <BLANKLINE>

Display mode and display proxy bool format::

    >>> widget = factory('checkbox', 'MYCHECKBOX', value=True, mode='display',
    ...     props={
    ...         'format': 'bool',
    ...         'display_proxy': True})
    >>> widget()
    u'<div class="display-None" id="display-MYCHECKBOX">yes<input 
    id="input-MYCHECKBOX" name="MYCHECKBOX" type="hidden" value="" /><input 
    id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists" type="hidden" 
    value="checkboxexists" /></div>'
    
    >>> data = widget.extract(request={'MYCHECKBOX-exists': 'checkboxexists'})
    >>> data
    <RuntimeData MYCHECKBOX, value=True, extracted=False at ...>
    
    >>> widget(data=data)
    u'<div class="display-None" id="display-MYCHECKBOX">no<input 
    id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists" type="hidden" 
    value="checkboxexists" /></div>'
    
    >>> data = widget.extract(request={'MYCHECKBOX-exists': 'checkboxexists',
    ...                                'MYCHECKBOX': ''})
    >>> data
    <RuntimeData MYCHECKBOX, value=True, extracted=True at ...>
    
    >>> widget(data=data)
    u'<div class="display-None" id="display-MYCHECKBOX">yes<input 
    id="input-MYCHECKBOX" name="MYCHECKBOX" type="hidden" value="" /><input 
    id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists" type="hidden" 
    value="checkboxexists" /></div>'

Display mode and display proxy string format::

    >>> widget = factory('checkbox', 'MYCHECKBOX', value='yes', mode='display',
    ...     props={
    ...         'format': 'string',
    ...         'display_proxy': True})
    >>> widget()
    u'<div class="display-None" id="display-MYCHECKBOX">yes<input 
    id="input-MYCHECKBOX" name="MYCHECKBOX" type="hidden" value="yes" /><input 
    id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists" type="hidden" 
    value="checkboxexists" /></div>'
    
    >>> data = widget.extract(request={'MYCHECKBOX-exists': 'checkboxexists'})
    >>> data
    <RuntimeData MYCHECKBOX, value='yes', extracted='' at ...>
    
    >>> widget(data=data)
    u'<div class="display-None" id="display-MYCHECKBOX">no<input 
    id="input-MYCHECKBOX" name="MYCHECKBOX" type="hidden" value="" /><input 
    id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists" type="hidden" 
    value="checkboxexists" /></div>'
    
    >>> data = widget.extract(request={'MYCHECKBOX-exists': 'checkboxexists',
    ...                                'MYCHECKBOX': ''})
    >>> data
    <RuntimeData MYCHECKBOX, value='yes', extracted='' at ...>
    
    >>> widget(data=data)
    u'<div class="display-None" id="display-MYCHECKBOX">no<input 
    id="input-MYCHECKBOX" name="MYCHECKBOX" type="hidden" value="" /><input 
    id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists" type="hidden" 
    value="checkboxexists" /></div>'
    
    >>> data = widget.extract(request={'MYCHECKBOX-exists': 'checkboxexists',
    ...                                'MYCHECKBOX': 'foo'})
    >>> data
    <RuntimeData MYCHECKBOX, value='yes', extracted='foo' at ...>
    
    >>> widget(data=data)
    u'<div class="display-None" id="display-MYCHECKBOX">foo<input 
    id="input-MYCHECKBOX" name="MYCHECKBOX" type="hidden" value="foo" /><input 
    id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists" type="hidden" 
    value="checkboxexists" /></div>'


Textarea
--------
::
    >>> widget = factory(
    ...     'textarea',
    ...     'MYTEXTAREA',
    ...     value=None,
    ...     props={
    ...         'label': 'Test Textarea Widget',
    ...         'id': {
    ...             'label': 'TestLabelId'
    ...         },
    ...     })

    >>> widget()
    u'<textarea cols="80" id="input-MYTEXTAREA" name="MYTEXTAREA" rows="25"></textarea>'

    >>> widget.mode = 'display'
    >>> widget()
    u'<div class="display-None" id="display-MYTEXTAREA"></div>'

    >>> widget = factory(
    ...     'textarea',
    ...     'MYTEXTAREA',
    ...     value='Test Textarea',
    ...     props={
    ...         'label': 'Test Textarea Widget',
    ...         'id': {
    ...             'label': 'TestLabelId'
    ...         },
    ...     })
    >>> widget()
    u'<textarea cols="80" id="input-MYTEXTAREA" name="MYTEXTAREA"
    rows="25">Test Textarea</textarea>'


Lines
-----

Render empty::

    >>> widget = factory('lines', 'MYLINES', value=None)
    >>> widget()
    u'<textarea cols="40" id="input-MYLINES" name="MYLINES" rows="8"></textarea>'

Render with preset value, expected as list::

    >>> widget = factory('lines', 'MYLINES', value=['a', 'b', 'c'])
    >>> pxml(widget())
    <textarea cols="40" id="input-MYLINES" name="MYLINES" rows="8">a
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
    <textarea cols="40" id="input-MYLINES" name="MYLINES" rows="8">a
    b</textarea>
    <BLANKLINE>

Display mode with preset value::

    >>> widget = factory('lines', 'MYLINES', value=['a', 'b', 'c'],
    ...                  mode='display')
    >>> pxml(widget())
    <ul class="display-None" id="display-MYLINES">
      <li>a</li>
      <li>b</li>
      <li>c</li>
    </ul>
    <BLANKLINE>

Display mode with empty preset value::

    >>> widget = factory('lines', 'MYLINES', value=[], mode='display')
    >>> pxml(widget())
    <ul class="display-None" id="display-MYLINES"/>
    <BLANKLINE>

Display mode with ``display_proxy``::

    >>> widget = factory('lines', 'MYLINES', value=['a', 'b', 'c'],
    ...     mode='display', props={
    ...         'display_proxy': True,
    ...     })
    >>> pxml('<div>' + widget() + '</div>')
    <div>
      <ul class="display-None" id="display-MYLINES">
        <li>a</li>
        <li>b</li>
        <li>c</li>
      </ul>
      <input id="input-MYLINES" name="MYLINES" type="hidden" value="a"/>
      <input id="input-MYLINES" name="MYLINES" type="hidden" value="b"/>
      <input id="input-MYLINES" name="MYLINES" type="hidden" value="c"/>
    </div>
    <BLANKLINE>
    
    >>> data = widget.extract({'MYLINES': 'a\nb'})
    >>> data
    <RuntimeData MYLINES, value=['a', 'b', 'c'], extracted=['a', 'b'] at ...>
    
    >>> pxml('<div>' + widget(data=data) + '</div>')
    <div>
      <ul class="display-None" id="display-MYLINES">
        <li>a</li>
        <li>b</li>
      </ul>
      <input id="input-MYLINES" name="MYLINES" type="hidden" value="a"/>
      <input id="input-MYLINES" name="MYLINES" type="hidden" value="b"/>
    </div>
    <BLANKLINE>


Selection
---------


Single Valued
.............
::
    >>> widget = factory(
    ...     'select',
    ...     'MYSELECT',
    ...     value='one',
    ...     props={
    ...         'vocabulary': [
    ...             ('one','One'),
    ...             ('two', 'Two'),
    ...             ('three', 'Three'),
    ...             ('four', 'Four')]})
    >>> pxml(widget())
    <select class="select" id="input-MYSELECT" name="MYSELECT">
      <option id="input-MYSELECT-one" selected="selected" value="one">One</option>
      <option id="input-MYSELECT-two" value="two">Two</option>
      <option id="input-MYSELECT-three" value="three">Three</option>
      <option id="input-MYSELECT-four" value="four">Four</option>
    </select>
    <BLANKLINE>

    >>> data = widget.extract({'MYSELECT': 'two'})
    >>> pxml(widget(data=data))
    <select class="select" id="input-MYSELECT" name="MYSELECT">
      <option id="input-MYSELECT-one" value="one">One</option>
      <option id="input-MYSELECT-two" selected="selected" value="two">Two</option>
      <option id="input-MYSELECT-three" value="three">Three</option>
      <option id="input-MYSELECT-four" value="four">Four</option>
    </select>
    <BLANKLINE>

Single valued set to completly disabled::

    >>> widget.attrs['disabled'] = True
    >>> pxml(widget())
    <select class="select" disabled="disabled" id="input-MYSELECT" name="MYSELECT">
      <option id="input-MYSELECT-one" selected="selected" value="one">One</option>
      <option id="input-MYSELECT-two" value="two">Two</option>
      <option id="input-MYSELECT-three" value="three">Three</option>
      <option id="input-MYSELECT-four" value="four">Four</option>
    </select>
    <BLANKLINE>

Single valued with specific options disabled::

    >>> widget.attrs['disabled'] = ['two', 'four']
    >>> pxml(widget())
    <select class="select" id="input-MYSELECT" name="MYSELECT">
      <option id="input-MYSELECT-one" selected="selected" value="one">One</option>
      <option disabled="disabled" id="input-MYSELECT-two" value="two">Two</option>
      <option id="input-MYSELECT-three" value="three">Three</option>
      <option disabled="disabled" id="input-MYSELECT-four" value="four">Four</option>
    </select>
    <BLANKLINE>
    
    >>> del widget.attrs['disabled']

Single valued display mode::

    >>> widget.mode = 'display'
    >>> widget()
    u'<div class="display-select" id="display-MYSELECT">One</div>'
    
    >>> widget.attrs['display_proxy'] = True
    >>> widget()
    u'<div class="display-select" id="display-MYSELECT">One</div><input 
    class="select" id="input-MYSELECT" name="MYSELECT" 
    type="hidden" value="one" />'
    
    >>> data = widget.extract(request={'MYSELECT': 'two'})
    >>> data
    <RuntimeData MYSELECT, value='one', extracted='two' at ...>
    
    >>> pxml('<div>' + widget(data=data) + '</div>')
    <div>
      <div class="display-select" id="display-MYSELECT">Two</div>
      <input class="select" id="input-MYSELECT" name="MYSELECT" type="hidden" value="two"/>
    </div>
    <BLANKLINE>


With Radio
..........

Render single selection as radio inputs::

    >>> widget = factory(
    ...     'select',
    ...     'MYSELECT',
    ...     value='one',
    ...     props={
    ...         'vocabulary': [
    ...             ('one','One'),
    ...             ('two', 'Two'),
    ...             ('three', 'Three'),
    ...             ('four', 'Four')],
    ...         'format': 'single',
    ...         'listing_label_position': 'before'})
    >>> pxml('<div>'+widget()+'</div>')
    <div>
      <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden" value="exists"/>
      <div id="radio-MYSELECT-wrapper">
        <div id="radio-MYSELECT-one">
          <label for="input-MYSELECT-one">One</label>
          <input checked="checked" class="select" id="input-MYSELECT-one" name="MYSELECT" type="radio" value="one"/>
        </div>
        <div id="radio-MYSELECT-two">
          <label for="input-MYSELECT-two">Two</label>
          <input class="select" id="input-MYSELECT-two" name="MYSELECT" type="radio" value="two"/>
        </div>
        <div id="radio-MYSELECT-three">
          <label for="input-MYSELECT-three">Three</label>
          <input class="select" id="input-MYSELECT-three" name="MYSELECT" type="radio" value="three"/>
        </div>
        <div id="radio-MYSELECT-four">
          <label for="input-MYSELECT-four">Four</label>
          <input class="select" id="input-MYSELECT-four" name="MYSELECT" type="radio" value="four"/>
        </div>
      </div>
    </div>
    <BLANKLINE>

Render single selection as radio inputs, disables all::

    >>> widget.attrs['disabled'] = True
    >>> pxml('<div>'+widget()+'</div>')
    <div>
      <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden" value="exists"/>
      <div id="radio-MYSELECT-wrapper">
        <div id="radio-MYSELECT-one">
          <label for="input-MYSELECT-one">One</label>
          <input checked="checked" class="select" disabled="disabled" id="input-MYSELECT-one" name="MYSELECT" type="radio" value="one"/>
        </div>
        <div id="radio-MYSELECT-two">
          <label for="input-MYSELECT-two">Two</label>
          <input class="select" disabled="disabled" id="input-MYSELECT-two" name="MYSELECT" type="radio" value="two"/>
        </div>
        <div id="radio-MYSELECT-three">
          <label for="input-MYSELECT-three">Three</label>
          <input class="select" disabled="disabled" id="input-MYSELECT-three" name="MYSELECT" type="radio" value="three"/>
        </div>
        <div id="radio-MYSELECT-four">
          <label for="input-MYSELECT-four">Four</label>
          <input class="select" disabled="disabled" id="input-MYSELECT-four" name="MYSELECT" type="radio" value="four"/>
        </div>
      </div>
    </div>
    <BLANKLINE>

Render single selection as radio inputs, disables some::

    >>> widget.attrs['disabled'] = ['one', 'three']
    >>> pxml('<div>'+widget()+'</div>')
    <div>
      <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden" value="exists"/>
      <div id="radio-MYSELECT-wrapper">
        <div id="radio-MYSELECT-one">
          <label for="input-MYSELECT-one">One</label>
          <input checked="checked" class="select" disabled="disabled" id="input-MYSELECT-one" name="MYSELECT" type="radio" value="one"/>
        </div>
        <div id="radio-MYSELECT-two">
          <label for="input-MYSELECT-two">Two</label>
          <input class="select" id="input-MYSELECT-two" name="MYSELECT" type="radio" value="two"/>
        </div>
        <div id="radio-MYSELECT-three">
          <label for="input-MYSELECT-three">Three</label>
          <input class="select" disabled="disabled" id="input-MYSELECT-three" name="MYSELECT" type="radio" value="three"/>
        </div>
        <div id="radio-MYSELECT-four">
          <label for="input-MYSELECT-four">Four</label>
          <input class="select" id="input-MYSELECT-four" name="MYSELECT" type="radio" value="four"/>
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
    >>> widget()
    u'<div class="display-select" id="display-MYSELECT">One</div><input 
    class="select" id="input-MYSELECT" name="MYSELECT" 
    type="hidden" value="one" />'
    
    >>> data = widget.extract(request={'MYSELECT': 'two'})
    >>> data
    <RuntimeData MYSELECT, value='one', extracted='two' at ...>
    
    >>> pxml('<div>' + widget(data=data) + '</div>')
    <div>
      <div class="display-select" id="display-MYSELECT">Two</div>
      <input class="select" id="input-MYSELECT" name="MYSELECT" type="hidden" value="two"/>
    </div>
    <BLANKLINE>


Multi valued
............
::
    >>> widget = factory(
    ...     'select',
    ...     'MYSELECT',
    ...     value=['one', 'two'],
    ...     props={
    ...         'multivalued': True,
    ...         'vocabulary': [
    ...             ('one','One'),
    ...             ('two', 'Two'),
    ...             ('three', 'Three'),
    ...             ('four', 'Four')]})
    >>> pxml('<div>' + widget() + '</div>')
    <div>
      <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden" value="exists"/>
      <select class="select" id="input-MYSELECT" multiple="multiple" name="MYSELECT">
        <option id="input-MYSELECT-one" selected="selected" value="one">One</option>
        <option id="input-MYSELECT-two" selected="selected" value="two">Two</option>
        <option id="input-MYSELECT-three" value="three">Three</option>
        <option id="input-MYSELECT-four" value="four">Four</option>
      </select>
    </div>
    <BLANKLINE>

Extract multi valued selection and render widget with extracted data::

    >>> data = widget.extract(request={'MYSELECT': ['one', 'four']})
    >>> data
    <RuntimeData MYSELECT, value=['one', 'two'], extracted=['one', 'four'] at ...>
    
    >>> pxml('<div>' + widget(data=data) + '</div>')
    <div>
      <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden" value="exists"/>
      <select class="select" id="input-MYSELECT" multiple="multiple" name="MYSELECT">
        <option id="input-MYSELECT-one" selected="selected" value="one">One</option>
        <option id="input-MYSELECT-two" value="two">Two</option>
        <option id="input-MYSELECT-three" value="three">Three</option>
        <option id="input-MYSELECT-four" selected="selected" value="four">Four</option>
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
    >>> pxml('<div>' + widget() + '</div>')
    <div>
      <ul class="display-select" id="display-MYSELECT">
        <li>One</li>
        <li>Two</li>
      </ul>
      <input class="select" id="input-MYSELECT" name="MYSELECT" type="hidden" value="one"/>
      <input class="select" id="input-MYSELECT" name="MYSELECT" type="hidden" value="two"/>
    </div>
    <BLANKLINE>

Multi selection display mode with display proxy and extracted data::
    
    >>> data = widget.extract(request={'MYSELECT': ['one']})
    >>> data
    <RuntimeData MYSELECT, value=['one', 'two'], extracted=['one'] at ...>
    
    >>> pxml('<div>' + widget(data=data) + '</div>')
    <div>
      <ul class="display-select" id="display-MYSELECT">
        <li>One</li>
      </ul>
      <input class="select" id="input-MYSELECT" name="MYSELECT" type="hidden" value="one"/>
    </div>
    <BLANKLINE>

Multiple values on single valued selection fails::

    >>> widget = factory(
    ...     'select',
    ...     'MYSELECT',
    ...     value=['one', 'two'],
    ...     props={
    ...         'vocabulary': [
    ...             ('one','One'),
    ...             ('two', 'Two'),
    ...             ('three', 'Three'),
    ...             ('four', 'Four')]})
    >>> pxml(widget())
    Traceback (most recent call last):
      ...
    ValueError: Multiple values for single selection.


With Checkboxes
...............

Render multi selection as checkboxes::

    >>> widget = factory(
    ...     'select',
    ...     'MYSELECT',
    ...     value='one',
    ...     props={
    ...         'multivalued': True,
    ...         'vocabulary': [
    ...             ('one','One'),
    ...             ('two', 'Two'),
    ...             ('three', 'Three'),
    ...             ('four', 'Four')],
    ...         'format': 'single'})
    >>> pxml('<div>' + widget() + '</div>')
    <div>
      <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden" value="exists"/>
      <div id="checkbox-MYSELECT-wrapper">
        <div id="checkbox-MYSELECT-one">
          <label for="input-MYSELECT-one"><input checked="checked" class="select" id="input-MYSELECT-one" name="MYSELECT" type="checkbox" value="one"/>One</label>
        </div>
        <div id="checkbox-MYSELECT-two">
          <label for="input-MYSELECT-two"><input class="select" id="input-MYSELECT-two" name="MYSELECT" type="checkbox" value="two"/>Two</label>
        </div>
        <div id="checkbox-MYSELECT-three">
          <label for="input-MYSELECT-three"><input class="select" id="input-MYSELECT-three" name="MYSELECT" type="checkbox" value="three"/>Three</label>
        </div>
        <div id="checkbox-MYSELECT-four">
          <label for="input-MYSELECT-four"><input class="select" id="input-MYSELECT-four" name="MYSELECT" type="checkbox" value="four"/>Four</label>
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
    >>> pxml('<div>' + widget() + '</div>')
    <div>
      <ul class="display-select" id="display-MYSELECT">
        <li>One</li>
      </ul>
      <input class="select" id="input-MYSELECT" name="MYSELECT" type="hidden" value="one"/>
    </div>
    <BLANKLINE>

Checkbox multi selection display mode with display proxy and extracted data::
    
    >>> data = widget.extract(request={'MYSELECT': ['two']})
    >>> data
    <RuntimeData MYSELECT, value='one', extracted=['two'] at ...>
    
    >>> pxml('<div>' + widget(data=data) + '</div>')
    <div>
      <ul class="display-select" id="display-MYSELECT">
        <li>Two</li>
      </ul>
      <input class="select" id="input-MYSELECT" name="MYSELECT" type="hidden" value="two"/>
    </div>
    <BLANKLINE>


Specials
........

Using 'ul' instead of 'div' for rendering radio or checkbox selections::

    >>> widget = factory(
    ...     'select',
    ...     'MYSELECT',
    ...     value='one',
    ...     props={
    ...         'multivalued': True,
    ...         'vocabulary': [
    ...             ('one','One'),
    ...             ('two', 'Two'),
    ...             ('three', 'Three'),
    ...             ('four', 'Four')],
    ...         'format': 'single',
    ...         'listing_tag': 'ul'})
    >>> pxml('<div>'+widget()+'</div>')
    <div>
      <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden" value="exists"/>
      <ul id="checkbox-MYSELECT-wrapper">
        <li id="checkbox-MYSELECT-one">
          <label for="input-MYSELECT-one"><input checked="checked" class="select" id="input-MYSELECT-one" name="MYSELECT" type="checkbox" value="one"/>One</label>
        </li>
        <li id="checkbox-MYSELECT-two">
          <label for="input-MYSELECT-two"><input class="select" id="input-MYSELECT-two" name="MYSELECT" type="checkbox" value="two"/>Two</label>
        </li>
        <li id="checkbox-MYSELECT-three">
          <label for="input-MYSELECT-three"><input class="select" id="input-MYSELECT-three" name="MYSELECT" type="checkbox" value="three"/>Three</label>
        </li>
        <li id="checkbox-MYSELECT-four">
          <label for="input-MYSELECT-four"><input class="select" id="input-MYSELECT-four" name="MYSELECT" type="checkbox" value="four"/>Four</label>
        </li>
      </ul>
    </div>
    <BLANKLINE>

Render single format selection with label after input::

    >>> widget = factory(
    ...     'select',
    ...     'MYSELECT',
    ...     value='one',
    ...     props={
    ...         'multivalued': True,
    ...         'vocabulary': [
    ...             ('one','One'),
    ...             ('two', 'Two'),
    ...         ],
    ...         'format': 'single',
    ...         'listing_tag': 'ul',
    ...         'listing_label_position': 'after'})
    >>> pxml('<div>'+widget()+'</div>')
    <div>
      <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden" value="exists"/>
      <ul id="checkbox-MYSELECT-wrapper">
        <li id="checkbox-MYSELECT-one">
          <input checked="checked" class="select" id="input-MYSELECT-one" name="MYSELECT" type="checkbox" value="one"/>
          <label for="input-MYSELECT-one">One</label>
        </li>
        <li id="checkbox-MYSELECT-two">
          <input class="select" id="input-MYSELECT-two" name="MYSELECT" type="checkbox" value="two"/>
          <label for="input-MYSELECT-two">Two</label>
        </li>
      </ul>
    </div>
    <BLANKLINE>

Render single format selection with input inside label before checkbox::

    >>> widget = factory(
    ...     'select',
    ...     'MYSELECT',
    ...     value='one',
    ...     props={
    ...         'multivalued': True,
    ...         'vocabulary': [
    ...             ('one','One'),
    ...             ('two', 'Two'),
    ...         ],
    ...         'format': 'single',
    ...         'listing_tag': 'ul',
    ...         'listing_label_position': 'inner-before'})
    >>> pxml('<div>'+widget()+'</div>')
    <div>
      <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden" value="exists"/>
      <ul id="checkbox-MYSELECT-wrapper">
        <li id="checkbox-MYSELECT-one">
          <label for="input-MYSELECT-one">One<input checked="checked" class="select" id="input-MYSELECT-one" name="MYSELECT" type="checkbox" value="one"/></label>
        </li>
        <li id="checkbox-MYSELECT-two">
          <label for="input-MYSELECT-two">Two<input class="select" id="input-MYSELECT-two" name="MYSELECT" type="checkbox" value="two"/></label>
        </li>
      </ul>
    </div>
    <BLANKLINE>

Check BBB 'inner' for 'listing_label_position' which behaves like
'inner-after'::

    >>> widget = factory(
    ...     'select',
    ...     'MYSELECT',
    ...     value='one',
    ...     props={
    ...         'vocabulary': [('one','One')],
    ...         'format': 'single',
    ...         'listing_label_position': 'inner'})
    >>> pxml('<div>'+widget()+'</div>')
    <div>
      <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden" value="exists"/>
      <div id="radio-MYSELECT-wrapper">
        <div id="radio-MYSELECT-one">
          <label for="input-MYSELECT-one"><input checked="checked" class="select" id="input-MYSELECT-one" name="MYSELECT" type="radio" value="one"/>One</label>
        </div>
      </div>
    </div>
    <BLANKLINE>

Check selection required::

    >>> widget = factory(
    ...     'select',
    ...     'reqselect',
    ...     props={
    ...         'required': 'Selection required',
    ...         'vocabulary': [
    ...             ('one','One'),
    ...             ('two', 'Two'),
    ...             ('three', 'Three'),
    ...             ('four', 'Four')]})
    >>> pxml(widget())
    <select class="select" id="input-reqselect" name="reqselect" required="required">
      <option id="input-reqselect-one" value="one">One</option>
      <option id="input-reqselect-two" value="two">Two</option>
      <option id="input-reqselect-three" value="three">Three</option>
      <option id="input-reqselect-four" value="four">Four</option>
    </select>
    <BLANKLINE>

    >>> data = widget.extract(request={'reqselect': ''})
    >>> data.printtree()
    <RuntimeData reqselect, value=<UNSET>, extracted='', 1 error(s) at ...>

    >>> widget = factory(
    ...     'select',
    ...     'reqselect',
    ...     props={
    ...         'required': 'Selection required',
    ...         'multivalued': True,
    ...         'vocabulary': [
    ...             ('one','One'),
    ...             ('two', 'Two'),
    ...             ('three', 'Three'),
    ...             ('four', 'Four')]})
    >>> pxml('<div>' + widget() + '</div>')
    <div>
      <input id="exists-reqselect" name="reqselect-exists" type="hidden" value="exists"/>
      <select class="select" id="input-reqselect" multiple="multiple" name="reqselect" required="required">
        <option id="input-reqselect-one" value="one">One</option>
        <option id="input-reqselect-two" value="two">Two</option>
        <option id="input-reqselect-three" value="three">Three</option>
        <option id="input-reqselect-four" value="four">Four</option>
      </select>
    </div>
    <BLANKLINE>

    >>> data = widget.extract(request={'reqselect-exists': 'exists'})
    >>> data.printtree()
    <RuntimeData reqselect, value=<UNSET>, extracted=[], 1 error(s) at ...>

Single selection extraction without value::

    >>> widget = factory(
    ...     'select',
    ...     'myselect',
    ...     props={
    ...         'vocabulary': [
    ...             ('one','One'),
    ...             ('two', 'Two')]})

    >>> request = {
    ...     'myselect': 'one',
    ...     'myselect-exists': True,
    ... }
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData myselect, value=<UNSET>, extracted='one' at ...>

Single selection extraction with value::

    >>> widget = factory(
    ...     'select',
    ...     'myselect',
    ...     value='two',
    ...     props={
    ...         'vocabulary': [
    ...             ('one','One'),
    ...             ('two', 'Two')]})

    >>> request = {
    ...     'myselect': 'one',
    ... }
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData myselect, value='two', extracted='one' at ...>

Single selection extraction disabled (means browser does not post the value)
with value::

    >>> widget.attrs['disabled'] = True
    >>> data = widget.extract({'myselect-exists': True})
    >>> data.printtree()
    <RuntimeData myselect, value='two', extracted='two' at ...>

Disabled can be also the value itself::

    >>> widget.attrs['disabled'] = 'two'
    >>> data = widget.extract({'myselect-exists': True})
    >>> data.printtree()
    <RuntimeData myselect, value='two', extracted='two' at ...>

Single selection extraction required::

    >>> widget = factory(
    ...     'select',
    ...     'myselect',
    ...     value='two',
    ...     props={
    ...         'required': True,
    ...         'vocabulary': [
    ...             ('one','One'),
    ...             ('two', 'Two')]})

    >>> request = {
    ...     'myselect':'',
    ... }
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData myselect, value='two', extracted='', 1 error(s) at ...>

A disabled and required returns value itself::

    >>> widget.attrs['disabled'] = True
    >>> data = widget.extract({'myselect-exists': True})
    >>> data.printtree()
    <RuntimeData myselect, value='two', extracted='two' at ...>

Multiple selection extraction without value::

    >>> widget = factory(
    ...     'select',
    ...     'myselect',
    ...     props={
    ...         'multivalued': True,
    ...         'vocabulary': [
    ...             ('one','One'),
    ...             ('two', 'Two')]})

    >>> request = {
    ...     'myselect': ['one', 'two'],
    ... }
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData myselect, value=<UNSET>, extracted=['one', 'two'] at ...>

Multiple selection extraction with value::

    >>> widget = factory(
    ...     'select',
    ...     'myselect',
    ...     value='three',
    ...     props={
    ...         'multivalued': True,
    ...         'vocabulary': [
    ...             ('one','One'),
    ...             ('two', 'Two'),
    ...             ('three', 'Three')]})

    >>> request = {
    ...     'myselect': 'one',
    ...     'myselect-exists': True,
    ... }
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData myselect, value='three', extracted=['one'] at ...>

Multiselection, completly disabled::

    >>> widget.attrs['disabled'] = True
    >>> data = widget.extract({'myselect-exists': True})
    >>> data.printtree()
    <RuntimeData myselect, value='three', extracted=['three'] at ...>

Multiselection, partly disabled, empty request::

    >>> widget = factory(
    ...     'select',
    ...     'myselect',
    ...     value=['one', 'three'],
    ...     props={
    ...         'multivalued': True,
    ...         'disabled': ['two', 'three'],
    ...         'vocabulary': [
    ...             ('one','One'),
    ...             ('two', 'Two'),
    ...             ('three', 'Three'),
    ...             ('four', 'Four')]})

    >>> data = widget.extract({})
    >>> data.printtree()
    <RuntimeData myselect, value=['one', 'three'], extracted=<UNSET> at ...>

Multiselection, partly disabled, non-empty request::

    >>> widget = factory(
    ...     'select',
    ...     'myselect',
    ...     value=['one', 'two', 'four'],
    ...     props={
    ...         'multivalued': True,
    ...         'disabled': ['two', 'three', 'four', 'five'],
    ...         'vocabulary': [
    ...             ('one','One'),
    ...             ('two', 'Two'),
    ...             ('three', 'Three'),
    ...             ('four', 'Four'),
    ...             ('five', 'Five')]})
    >>> request = {
    ...     'myselect': ['one', 'two', 'five'],
    ...     'myselect-exists': True,
    ... }

Explanation:
* one is a simple value as usal,
* two is disabled and in value, so it should be kept in.
* three is disabled and not in value, so it should kept out,
* four is disabled and in value, but someone removed it in the request, it
  should get recovered,
* five is disabled and not in value, but someone put it in the request. it
  should get removed.

::
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData myselect, value=['one', 'two', 'four'],
    extracted=['one', 'two', 'four'] at ...>

Single selection radio extraction::

    >>> widget = factory(
    ...     'select',
    ...     'myselect',
    ...     props={
    ...         'format': 'single',
    ...         'vocabulary': [
    ...             ('one','One'),
    ...             ('two', 'Two'),
    ...             ('three', 'Three')]})

No exists marker in request. Extracts to UNSET::

    >>> request = {
    ... }
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData myselect, value=<UNSET>, extracted=<UNSET> at ...>

Exists marker in request. Extracts to empty string::

    >>> request = {
    ...     'myselect-exists': '1',
    ... }
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData myselect, value=<UNSET>, extracted='' at ...>

Select value::

    >>> request = {
    ...     'myselect-exists': '1',
    ...     'myselect': 'one',
    ... }
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData myselect, value=<UNSET>, extracted='one' at ...>

Multi selection radio extraction::

    >>> widget = factory(
    ...     'select',
    ...     'myselect',
    ...     props={
    ...         'multivalued': True,
    ...         'format': 'single',
    ...         'vocabulary': [
    ...             ('one','One'),
    ...             ('two', 'Two'),
    ...             ('three', 'Three')]})

No exists marker in request. Extracts to UNSET::

    >>> request = {
    ... }
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData myselect, value=<UNSET>, extracted=<UNSET> at ...>

Exists marker in request. Extracts to empty list::

    >>> request = {
    ...     'myselect-exists': '1',
    ... }
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData myselect, value=<UNSET>, extracted=[] at ...>

Select values::

    >>> request = {
    ...     'myselect-exists': '1',
    ...     'myselect': ['one', 'two'],
    ... }
    >>> data = widget.extract(request)
    >>> data.printtree()
    <RuntimeData myselect, value=<UNSET>, extracted=['one', 'two'] at ...>


File
----
::
    >>> widget = factory('file', 'MYFILE')
    >>> widget()
    u'<input id="input-MYFILE" name="MYFILE" type="file" />'

Extract empty::

    >>> request = {
    ... }
    >>> data = widget.extract(request)
    >>> data.extracted
    <UNSET>

Extract ``new``::

    >>> from StringIO import StringIO
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
    ...     'MYFILE',
    ...     value={
    ...         'file': StringIO('321'),
    ...     })
    >>> pxml('<div>' + widget() + '</div>')
    <div>
      <input id="input-MYFILE" name="MYFILE" type="file"/>
      <div id="radio-MYFILE-keep">
        <input checked="checked" id="input-MYFILE-keep" name="MYFILE-action" type="radio" value="keep"/>
        <span>Keep Existing file</span>
      </div>
      <div id="radio-MYFILE-replace">
        <input id="input-MYFILE-replace" name="MYFILE-action" type="radio" value="replace"/>
        <span>Replace existing file</span>
      </div>
      <div id="radio-MYFILE-delete">
        <input id="input-MYFILE-delete" name="MYFILE-action" type="radio" value="delete"/>
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

    >>> pxml('<div>' + widget(request=request) + '</div>')
    <div>
      <input id="input-MYFILE" name="MYFILE" type="file"/>
      <div id="radio-MYFILE-keep">
        <input id="input-MYFILE-keep" name="MYFILE-action" type="radio" value="keep"/>
        <span>Keep Existing file</span>
      </div>
      <div id="radio-MYFILE-replace">
        <input id="input-MYFILE-replace" name="MYFILE-action" type="radio" value="replace"/>
        <span>Replace existing file</span>
      </div>
      <div id="radio-MYFILE-delete">
        <input checked="checked" id="input-MYFILE-delete" name="MYFILE-action" type="radio" value="delete"/>
        <span>Delete existing file</span>
      </div>
    </div>
    <BLANKLINE>

    >>> widget = factory('file', 'MYFILE', props={'accept': 'foo/bar'})
    >>> widget()
    u'<input accept="foo/bar" id="input-MYFILE" name="MYFILE"
    type="file" />'

File display renderer::

    >>> from yafowil.common import convert_bytes
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
    ...     'MYFILE',
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
    ...     'MYFILE',
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


Submit(action)
--------------
::
    >>> props = {
    ...     'action': True,
    ...     'label': 'Action name',
    ... }
    >>> widget = factory('submit', name='save', props=props)
    >>> widget()
    u'<input id="input-save" name="action.save" type="submit" value="Action name" />'

    >>> props = {
    ...     'action': True,
    ...     'label': 'Action name',
    ...     'expression': False,
    ... }
    >>> widget = factory('submit', name='save', props=props)
    >>> widget()
    u''

    >>> props = {
    ...     'action': True,
    ...     'label': 'Action name',
    ...     'expression': lambda: False,
    ... }
    >>> widget = factory('submit', name='save', props=props)
    >>> widget()
    u''


Proxy
-----

Used to pass hidden arguments out of form namespace::

    >>> widget = factory('proxy', name='proxy', value='1')
    >>> widget()
    u'<input id="input-proxy" name="proxy" type="hidden" value="1" />'

    >>> widget(request={'proxy': '2'})
    u'<input id="input-proxy" name="proxy" type="hidden" value="2" />'


Label
-----

Default::

    >>> widget = factory('label:file', name='MYFILE', \
    ...                   props={'label': 'MY FILE'})
    >>> pxml(tag('div', widget()))
    <div>
      <label for="input-MYFILE">MY FILE</label>
      <input id="input-MYFILE" name="MYFILE" type="file"/>
    </div>
    <BLANKLINE>

Label after widget::

    >>> widget = factory('label:file', name='MYFILE', \
    ...                   props={'label': 'MY FILE',
    ...                          'label.position': 'after'})
    >>> pxml(tag('div', widget()))
    <div>
      <input id="input-MYFILE" name="MYFILE" type="file"/>
      <label for="input-MYFILE">MY FILE</label>
    </div>
    <BLANKLINE>

Same with inner label::

    >>> widget = factory('label:file', name='MYFILE', \
    ...                   props={'label': 'MY FILE',
    ...                          'label.position': 'inner'})
    >>> pxml(tag('div', widget()))
    <div>
      <label for="input-MYFILE">MY FILE<input id="input-MYFILE" name="MYFILE" type="file"/></label>
    </div>
    <BLANKLINE>

Invalid position::

    >>> widget = factory('label:file', name='MYFILE', \
    ...                   props={'label': 'MY FILE',
    ...                          'label.position': 'inexistent'})
    >>> pxml(tag('div', widget()))
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
    ...     props={'label': 'MY FILE'})
    >>> pxml(widget())
    <div class="field" id="field-MYFILE">
      <label for="input-MYFILE">MY FILE</label>
      <input id="input-MYFILE" name="MYFILE" type="file"/>
    </div>
    <BLANKLINE>

Render error class directly on field::

    >>> widget = factory(
    ...     'field:text',
    ...     name='myfield',
    ...     props={
    ...         'required': True,
    ...         'witherror': 'fielderrorclass'})
    >>> data = widget.extract({'myfield': ''})
    >>> data.printtree()
    <RuntimeData myfield, value=<UNSET>, extracted='', 1 error(s) at ...>

    >>> pxml(widget(data))
    <div class="field fielderrorclass" id="field-myfield">
      <input class="required text" id="input-myfield" name="myfield" required="required" type="text" value=""/>
    </div>
    <BLANKLINE>


Password
--------

Password widget has some additional properties, ``strength``, ``minlength``
and ``ascii``.

Use in add forms, no password set yet::

    >>> widget = factory(
    ...     'password',
    ...     name='pwd',
    ...     props={
    ...     })
    >>> widget()
    u'<input class="password" id="input-pwd" name="pwd" type="password" value="" />'

    >>> data = widget.extract({})
    >>> data.extracted
    <UNSET>

    >>> data = widget.extract({'pwd': 'xx'})
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
    ...     name='password',
    ...     value='secret',
    ...     props={
    ...     })
    >>> widget()
    u'<input class="password" id="input-password" name="password" type="password" value="_NOCHANGE_" />'

    >>> data = widget.extract({'password': '_NOCHANGE_'})
    >>> data.extracted
    <UNSET>

    >>> data = widget.extract({'password': 'foo'})
    >>> data.extracted
    'foo'

    >>> widget(data=data)
    u'<input class="password" id="input-password" name="password" type="password" value="foo" />'

    >>> widget.mode = 'display'
    >>> widget()
    u'********'

Password validation::

    >>> widget = factory(
    ...     'password',
    ...     name='pwd',
    ...     props={
    ...         'strength': 5, # max 4, does not matter, max is used
    ...     })
    >>> data = widget.extract({'pwd': ''})
    >>> data.errors
    [ExtractionError('Password too weak',)]

    >>> data = widget.extract({'pwd': 'A0*'})
    >>> data.errors
    [ExtractionError('Password too weak',)]

    >>> data = widget.extract({'pwd': 'a0*'})
    >>> data.errors
    [ExtractionError('Password too weak',)]

    >>> data = widget.extract({'pwd': 'aA*'})
    >>> data.errors
    [ExtractionError('Password too weak',)]

    >>> data = widget.extract({'pwd': 'aA0'})
    >>> data.errors
    [ExtractionError('Password too weak',)]

    >>> data = widget.extract({'pwd': 'aA0*'})
    >>> data.errors
    []

Minlength validation::

    >>> widget = factory(
    ...     'password',
    ...     name='pwd',
    ...     props={
    ...         'minlength': 3,
    ...     })
    >>> data = widget.extract({'pwd': 'xx'})
    >>> data.errors
    [ExtractionError('Input must have at least 3 characters.',)]

    >>> data = widget.extract({'pwd': 'xxx'})
    >>> data.errors
    []

Ascii validation::

    >>> widget = factory(
    ...     'password',
    ...     name='pwd',
    ...     props={
    ...         'ascii': True,
    ...     })
    >>> data = widget.extract({'pwd': u'äää'})
    >>> data.errors
    [ExtractionError('Input contains illegal characters.',)]

    >>> data = widget.extract({'pwd': u'xx'})
    >>> data.errors
    []

Combine all validations::

    >>> widget = factory(
    ...     'password',
    ...     name='pwd',
    ...     props={
    ...         'required': 'No Password given',
    ...         'minlength': 6,
    ...         'ascii': True,
    ...         'strength': 4,
    ...     })
    >>> data = widget.extract({'pwd': u''})
    >>> data.errors
    [ExtractionError('No Password given',)]

    >>> data = widget.extract({'pwd': u'xxxxx'})
    >>> data.errors
    [ExtractionError('Input must have at least 6 characters.',)]

    >>> data = widget.extract({'pwd': u'xxxxxä'})
    >>> data.errors
    [ExtractionError('Input contains illegal characters.',)]

    >>> data = widget.extract({'pwd': u'xxxxxx'})
    >>> data.errors
    [ExtractionError('Password too weak',)]

    >>> data = widget.extract({'pwd': u'xX1*00'})
    >>> data.errors
    []


Error
-----

Chained password inside error inside field::

    >>> widget = factory('field:error:password', name='password',
    ...                  props={'label': 'Password',
    ...                         'required': 'No password given!'})
    >>> data = widget.extract({'password': ''})
    >>> pxml(widget(data=data))
    <div class="field" id="field-password">
      <div class="error">
        <div class="errormessage">No password given!</div>
        <input class="password required" id="input-password" name="password" required="required" type="password" value=""/>
      </div>
    </div>
    <BLANKLINE>

    >>> data = widget.extract({'password': 'secret'})
    >>> pxml(widget(data=data))
    <div class="field" id="field-password">
      <input class="password required" id="input-password" name="password" required="required" type="password" value="secret"/>
    </div>
    <BLANKLINE>

    >>> widget = factory('error:text', name='mydisplay',
    ...                  value='somevalue',
    ...                  mode='display')
    >>> widget()
    u'<div class="display-text" id="display-mydisplay">somevalue</div>'

Error wrapping in div element can be suppressed::

    >>> widget = factory('field:error:password', name='password',
    ...                  props={'label': 'Password',
    ...                         'required': 'No password given!',
    ...                         'message_tag': None})
    >>> data = widget.extract({'password': ''})
    >>> pxml(widget(data=data))
    <div class="field" id="field-password">
      <div class="error">No password given!<input class="password required" id="input-password" name="password" required="required" type="password" value=""/></div>
    </div>
    <BLANKLINE>


Help
----

Render some additional help text::

    >>> widget = factory('field:help:text', name='helpexample',
    ...                  props={'label': 'Help',
    ...                         'help': 'Shout out loud here'})
    >>> pxml(widget())
    <div class="field" id="field-helpexample">
      <div class="help">Shout out loud here</div>
      <input class="text" id="input-helpexample" name="helpexample" type="text" value=""/>
    </div>
    <BLANKLINE>

Render empty (WHAT'S THIS GOOD FOR?)::

    >>> widget = factory('field:help:text', name='helpexample',
    ...                  props={'label': 'Help',
    ...                         'help': False,
    ...                         'render_empty': False})
    >>> pxml(widget())
    <div class="field" id="field-helpexample">
      <input class="text" id="input-helpexample" name="helpexample" type="text" value=""/>
    </div>
    <BLANKLINE>


e-mail
------

::
    >>> widget = factory(
    ...     'email',
    ...     name='email')
    >>> pxml(widget())
    <input class="email" id="input-email" name="email" type="email" value=""/>

    >>> data = widget.extract({'email': 'foo@bar'})
    >>> data.errors
    [ExtractionError('Input not a valid email address.',)]

    >>> data = widget.extract({'email': '@bar.com'})
    >>> data.errors
    [ExtractionError('Input not a valid email address.',)]

    >>> data = widget.extract({'email': 'foo@bar.com'})
    >>> data.errors
    []


URL
---

::
    >>> widget = factory(
    ...     'url',
    ...     name='url')
    >>> pxml(widget())
    <input class="url" id="input-url" name="url" type="url" value=""/>

    >>> data = widget.extract({'url': 'htt:/bla'})
    >>> data.errors
    [ExtractionError('Input not a valid web address.',)]

    >>> data = widget.extract({'url': 'invalid'})
    >>> data.errors
    [ExtractionError('Input not a valid web address.',)]

    >>> data = widget.extract({'url': 'http://www.foo.bar.com:8080/bla#fasel?blubber=bla&bla=fasel'})
    >>> data.errors
    []


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

Default behaviour::

    >>> widget = factory(
    ...     'number',
    ...     name='NUMBER',
    ...     value=lambda w,d:3)
    >>> pxml(widget())
    <input class="number" id="input-NUMBER" name="NUMBER" type="number" value="3"/>
    <BLANKLINE>

    >>> data = widget.extract({})
    >>> data.printtree()
    <RuntimeData NUMBER, value=3, extracted=<UNSET> at ...>

    >>> data = widget.extract({'NUMBER': 'abc'})
    >>> data.errors
    [ExtractionError('Input is not a valid number (float).',)]

    >>> data = widget.extract({'NUMBER': '10'})
    >>> data.errors
    []

    >>> data = widget.extract({'NUMBER': '10.0'})
    >>> data.errors
    []

    >>> widget = factory(
    ...     'number',
    ...     name='NUMBER',
    ...     props={'datatype': 'invalid'})
    >>> widget.extract({'NUMBER': '10.0'})
    Traceback (most recent call last):
      ...
    ValueError: Output datatype must be integer or float

With integer datatype::

    >>> widget = factory(
    ...     'number',
    ...     name='NUMBER',
    ...     props={'datatype': "integer"})

    >>> data = widget.extract({'NUMBER': '10.0'})
    >>> data.errors
    [ExtractionError('Input is not a valid number (integer).',)]

With min set::

    >>> widget = factory(
    ...     'number',
    ...     name='NUMBER',
    ...     props={'min': 10})

    >>> data = widget.extract({'NUMBER': '9'})
    >>> data.errors
    [ExtractionError('Value has to be at minimum 10.',)]

    >>> data = widget.extract({'NUMBER': '10'})
    >>> data.errors
    []

    >>> data = widget.extract({'NUMBER': '11'})
    >>> data.errors
    []

With max set::

    >>> widget = factory(
    ...     'number',
    ...     name='NUMBER',
    ...     props={'max': lambda w,d: 10})

    >>> data = widget.extract({'NUMBER': '9'})
    >>> data.errors
    []

    >>> data = widget.extract({'NUMBER': '10'})
    >>> data.errors
    []

    >>> data = widget.extract({'NUMBER': '11'})
    >>> data.errors
    [ExtractionError('Value has to be at maximum 10.',)]

With step set::

    >>> widget = factory(
    ...     'number',
    ...     name='NUMBER',
    ...     props={'step': 2})

    >>> data = widget.extract({'NUMBER': '9'})
    >>> data.errors
    [ExtractionError('Value 9.0 has to be in stepping of 2',)]

    >>> data = widget.extract({'NUMBER': '6'})
    >>> data.errors
    []

With step and min set::

    >>> widget = factory(
    ...     'number',
    ...     name='NUMBER',
    ...     props={'step': 2, 'min': 3})

    >>> data = widget.extract({'NUMBER': '7'})
    >>> data.errors
    []

    >>> data = widget.extract({'NUMBER': '6'})
    >>> data.errors
    [ExtractionError('Value 6.0 has to be in stepping of 2 based on a floor value of 3',)]
