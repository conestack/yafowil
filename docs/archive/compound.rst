Compound
--------

Preparation::

    >>> from yafowil.base import factory
    >>> from yafowil.controller import Controller
    >>> from yafowil.utils import Tag
    >>> import yafowil.common
    >>> import yafowil.compound

    >>> tag = Tag(lambda msg: msg)           

Render Compound with values set via compound widget::

    >>> value = {
    ...     'inner': 'Value 1 from parent',
    ...     'inner2': 'Value 2 from parent',
    ... }
    >>> compound = factory(
    ...     'compound',
    ...     name='COMPOUND',
    ...     value=value)
    >>> compound['inner']  = factory('text')
    >>> compound['inner2'] = factory(
    ...     'text',
    ...     props={
    ...         'required': True
    ...     })
    >>> pxml(tag('div', compound()))
    <div>
      <input class="text" id="input-COMPOUND-inner" name="COMPOUND.inner" 
        type="text" value="Value 1 from parent"/>
      <input class="required text" id="input-COMPOUND-inner2" 
        name="COMPOUND.inner2" required="required" type="text" 
        value="Value 2 from parent"/>
    </div>
    <BLANKLINE>

ValueError if value for a compound member is defined both::

    >>> value = {'inner': 'Value 1 from parent'}
    >>> compound = factory(
    ...     'compound',
    ...     name='COMPOUND',
    ...     value=value)
    >>> compound['inner']  = factory(
    ...     'text',
    ...     value='value1')
    >>> pxml(tag('div', compound()))
    Traceback (most recent call last):
      ...
    ValueError: Both compound and compound member provide a value for 'inner'

Render Compound with values set via compound members::

    >>> compound = factory(
    ...     'compound',
    ...     name='COMPOUND')
    >>> compound['inner']  = factory(
    ...     'text',
    ...     value='value1')
    >>> compound['inner2'] = factory(
    ...     'error:text',
    ...     value='value2',
    ...     props={
    ...         'required': True
    ...     })
    >>> pxml(tag('div', compound()))
    <div>
      <input class="text" id="input-COMPOUND-inner" name="COMPOUND.inner" 
        type="text" value="value1"/>
      <input class="required text" id="input-COMPOUND-inner2" 
        name="COMPOUND.inner2" required="required" type="text" value="value2"/>
    </div>
    <BLANKLINE>

Extract Compound with empty request::

    >>> data = compound.extract({})
    >>> data
    <RuntimeData COMPOUND, value=<UNSET>, 
    extracted=odict([('inner', <UNSET>), ('inner2', <UNSET>)]) at ...> 

    >>> data['inner']
    <RuntimeData COMPOUND.inner, value='value1', extracted=<UNSET> at ...>

    >>> data.extracted
    odict([('inner', <UNSET>), ('inner2', <UNSET>)])

Extract with a value in request::

    >>> request = {
    ...     'COMPOUND.inner': 'newvalue',
    ...     'COMPOUND.inner2': '',
    ... }
    >>> data = compound.extract(request)
    >>> data['inner']
    <RuntimeData COMPOUND.inner, value='value1', extracted='newvalue' at ...> 

    >>> data['inner2']
    <RuntimeData COMPOUND.inner2, value='value2', extracted='', 
      1 error(s) at ...>

    >>> data.extracted
    odict([('inner', 'newvalue'), ('inner2', '')])

    >>> pxml('<div>' + compound(data=data) + '</div>')
    <div>
      <input class="text" id="input-COMPOUND-inner" name="COMPOUND.inner" 
        type="text" value="newvalue"/>
      <div class="error">
        <div class="errormessage">Mandatory field was empty</div>
        <input class="required text" id="input-COMPOUND-inner2" 
          name="COMPOUND.inner2" required="required" type="text" value=""/>
      </div>
    </div>
    <BLANKLINE>

Compound display renderers, same as edit renderers::

    >>> compound = factory(
    ...     'compound',
    ...     name='COMPOUND',
    ...     mode='display')
    >>> pxml(tag('div', compound()))
    <div/>
    <BLANKLINE>

Compound with structural compound as child::

    >>> value = {
    ...     'inner': 'Value 1 from parent',
    ...     'inner2': 'Value 2 from parent',
    ... }
    >>> compound = factory(
    ...     'compound',
    ...     name='COMPOUND',
    ...     value=value)
    >>> structural = compound['STRUCTURAL'] = factory(
    ...     'compound',
    ...     props={
    ...         'structural': True
    ...     })
    >>> structural['inner']  = factory('text')
    >>> structural['inner2'] = factory(
    ...     'text',
    ...     props={
    ...         'required': True
    ...     })
    >>> pxml(tag('div', compound()))
    <div>
      <input class="text" id="input-COMPOUND-inner" name="COMPOUND.inner" 
        type="text" value="Value 1 from parent"/>
      <input class="required text" id="input-COMPOUND-inner2" 
        name="COMPOUND.inner2" required="required" type="text" 
          value="Value 2 from parent"/>
    </div>
    <BLANKLINE>

    >>> compound.printtree()
    <class 'yafowil.base.Widget'>: COMPOUND
      <class 'yafowil.base.Widget'>: STRUCTURAL
        <class 'yafowil.base.Widget'>: inner
        <class 'yafowil.base.Widget'>: inner2

    >>> data = compound.extract({
    ...     'COMPOUND.inner': 'newvalue',
    ...     'COMPOUND.inner2': '',
    ... })
    >>> data.printtree()
    <RuntimeData COMPOUND, 
      value={'inner2': 'Value 2 from parent', 'inner': 'Value 1 from parent'}, 
      extracted=odict([('inner', 'newvalue'), ('inner2', '')]) at ...>
      <RuntimeData COMPOUND.inner, value='Value 1 from parent', 
        extracted='newvalue' at ...>
      <RuntimeData COMPOUND.inner2, value='Value 2 from parent', 
        extracted='', 1 error(s) at ...>

    >>> data.extracted
    odict([('inner', 'newvalue'), ('inner2', '')])

Compound with compound as child::

    >>> value = {
    ...     'CHILD_COMPOUND': {
    ...         'inner': 'Value 1 from parent',
    ...         'inner2': 'Value 2 from parent',
    ...     }
    ... }
    >>> compound = factory(
    ...     'compound',
    ...     name='COMPOUND',
    ...     value=value)
    >>> child_compound = compound['CHILD_COMPOUND'] = factory('compound')
    >>> child_compound['inner'] = factory('text')
    >>> child_compound['inner2'] = factory(
    ...     'text',
    ...     props={
    ...         'required': True
    ...     })
    >>> pxml(tag('div', compound()))
    <div>
      <input class="text" id="input-COMPOUND-CHILD_COMPOUND-inner" 
        name="COMPOUND.CHILD_COMPOUND.inner" type="text" 
        value="Value 1 from parent"/>
      <input class="required text" id="input-COMPOUND-CHILD_COMPOUND-inner2" 
        name="COMPOUND.CHILD_COMPOUND.inner2" required="required" type="text" 
        value="Value 2 from parent"/>
    </div>
    <BLANKLINE>

    >>> compound.printtree()
    <class 'yafowil.base.Widget'>: COMPOUND
      <class 'yafowil.base.Widget'>: CHILD_COMPOUND
        <class 'yafowil.base.Widget'>: inner
        <class 'yafowil.base.Widget'>: inner2

    >>> data = compound.extract({
    ...     'COMPOUND.CHILD_COMPOUND.inner': 'newvalue',
    ...     'COMPOUND.CHILD_COMPOUND.inner2': 'newvalue2',
    ... })
    >>> data.printtree()
    <RuntimeData COMPOUND, value={'CHILD_COMPOUND': 
      {'inner2': 'Value 2 from parent', 'inner': 'Value 1 from parent'}}, 
      extracted=odict([('CHILD_COMPOUND', odict([('inner', 'newvalue'), 
      ('inner2', 'newvalue2')]))]) at ...>
      <RuntimeData COMPOUND.CHILD_COMPOUND, 
        value={'inner2': 'Value 2 from parent', 
        'inner': 'Value 1 from parent'}, 
        extracted=odict([('inner', 'newvalue'), 
        ('inner2', 'newvalue2')]) at ...>
        <RuntimeData COMPOUND.CHILD_COMPOUND.inner, 
          value='Value 1 from parent', extracted='newvalue' at ...>
        <RuntimeData COMPOUND.CHILD_COMPOUND.inner2, 
          value='Value 2 from parent', extracted='newvalue2' at ...>

    >>> data.extracted
    odict([('CHILD_COMPOUND', 
    odict([('inner', 'newvalue'), 
    ('inner2', 'newvalue2')]))])

Compound with structural compound with compound as children::

    >>> value = {
    ...     'CHILD_COMPOUND': {
    ...         'inner': 'Value 1 from parent',
    ...         'inner2': 'Value 2 from parent',
    ...     }
    ... }
    >>> compound = factory(
    ...     'compound',
    ...     name='COMPOUND',
    ...     value=value)
    >>> structural = compound['STRUCTURAL'] = factory(
    ...     'compound',
    ...     props={
    ...         'structural': True
    ...     })
    >>> child_compound = structural['CHILD_COMPOUND'] = factory('compound')
    >>> child_compound['inner'] = factory('text')
    >>> child_compound['inner2'] = factory(
    ...     'text',
    ...     props={
    ...         'required': True
    ...     })
    >>> pxml(tag('div', compound()))
    <div>
      <input class="text" id="input-COMPOUND-CHILD_COMPOUND-inner" 
        name="COMPOUND.CHILD_COMPOUND.inner" type="text" 
        value="Value 1 from parent"/>
      <input class="required text" id="input-COMPOUND-CHILD_COMPOUND-inner2" 
        name="COMPOUND.CHILD_COMPOUND.inner2" required="required" type="text" 
        value="Value 2 from parent"/>
    </div>
    <BLANKLINE>

    >>> compound.printtree()
    <class 'yafowil.base.Widget'>: COMPOUND
      <class 'yafowil.base.Widget'>: STRUCTURAL
        <class 'yafowil.base.Widget'>: CHILD_COMPOUND
          <class 'yafowil.base.Widget'>: inner
          <class 'yafowil.base.Widget'>: inner2

    >>> compound['STRUCTURAL'].attrs
    {'structural': True}

    >>> compound['STRUCTURAL']['CHILD_COMPOUND'].attrs
    {}

    >>> data = compound.extract({
    ...     'COMPOUND.CHILD_COMPOUND.inner': 'newvalue',
    ...     'COMPOUND.CHILD_COMPOUND.inner2': 'newvalue2',
    ... })

    >>> data.printtree()
    <RuntimeData COMPOUND, value={'CHILD_COMPOUND': 
      {'inner2': 'Value 2 from parent', 'inner': 'Value 1 from parent'}}, 
      extracted=odict([('CHILD_COMPOUND', odict([('inner', 'newvalue'), 
      ('inner2', 'newvalue2')]))]) at ...>
      <RuntimeData COMPOUND.CHILD_COMPOUND, 
        value={'inner2': 'Value 2 from parent', 
        'inner': 'Value 1 from parent'}, 
        extracted=odict([('inner', 'newvalue'), 
        ('inner2', 'newvalue2')]) at ...>
        <RuntimeData COMPOUND.CHILD_COMPOUND.inner, 
          value='Value 1 from parent', extracted='newvalue' at ...>
        <RuntimeData COMPOUND.CHILD_COMPOUND.inner2, 
          value='Value 2 from parent', extracted='newvalue2' at ...>

    >>> data.extracted
    odict([('CHILD_COMPOUND', 
    odict([('inner', 'newvalue'), 
    ('inner2', 'newvalue2')]))])

Address different compounds with value on parent::

    >>> value = {
    ...     'c1': {
    ...         'f1': 'Foo',
    ...     },
    ...     'c2': {
    ...         'f2': 'Bar',
    ...         'f3': 'Baz',
    ...     },
    ... }
    >>> compound = factory(
    ...     'compound',
    ...     'comp',
    ...     value=value)
    >>> compound['c1'] = factory('compound')
    >>> compound['c1']['f1'] = factory('text')
    >>> compound['c2'] = factory('compound')
    >>> compound['c2']['f2'] = factory('text')
    >>> compound['c2']['f3'] = factory('text')
    >>> compound['c3'] = factory('compound')
    >>> compound['c3']['f4'] = factory('text')

    >>> pxml(tag('div', compound()))
    <div>
      <input class="text" id="input-comp-c1-f1" name="comp.c1.f1" type="text" 
        value="Foo"/>
      <input class="text" id="input-comp-c2-f2" name="comp.c2.f2" type="text" 
        value="Bar"/>
      <input class="text" id="input-comp-c2-f3" name="comp.c2.f3" type="text" 
        value="Baz"/>
      <input class="text" id="input-comp-c3-f4" name="comp.c3.f4" type="text" 
        value=""/>
    </div>
    <BLANKLINE>

    >>> compound.printtree()
    <class 'yafowil.base.Widget'>: comp
      <class 'yafowil.base.Widget'>: c1
        <class 'yafowil.base.Widget'>: f1
      <class 'yafowil.base.Widget'>: c2
        <class 'yafowil.base.Widget'>: f2
        <class 'yafowil.base.Widget'>: f3
      <class 'yafowil.base.Widget'>: c3
        <class 'yafowil.base.Widget'>: f4

    >>> data = compound.extract({
    ...     'comp.c1.f1': 'Foo 1',
    ...     'comp.c2.f2': 'Bar 2',
    ...     'comp.c2.f3': 'Baz 1',
    ... })

    >>> data.printtree()
    <RuntimeData comp, 
      value={'c2': {'f2': 'Bar', 'f3': 'Baz'}, 'c1': {'f1': 'Foo'}}, 
      extracted=odict([('c1', odict([('f1', 'Foo 1')])), 
      ('c2', odict([('f2', 'Bar 2'), ('f3', 'Baz 1')])), 
      ('c3', odict([('f4', <UNSET>)]))]) at ...>
      <RuntimeData comp.c1, value={'f1': 'Foo'}, 
        extracted=odict([('f1', 'Foo 1')]) at ...>
        <RuntimeData comp.c1.f1, value='Foo', extracted='Foo 1' at ...>
      <RuntimeData comp.c2, value={'f2': 'Bar', 'f3': 'Baz'}, 
        extracted=odict([('f2', 'Bar 2'), ('f3', 'Baz 1')]) at ...>
        <RuntimeData comp.c2.f2, value='Bar', extracted='Bar 2' at ...>
        <RuntimeData comp.c2.f3, value='Baz', extracted='Baz 1' at ...>
      <RuntimeData comp.c3, value=<UNSET>, 
        extracted=odict([('f4', <UNSET>)]) at ...>
        <RuntimeData comp.c3.f4, value=<UNSET>, extracted=<UNSET> at ...>

Check compound with value callbacks::

    >>> def val(widget, data):
    ...     return 'val F1'
    >>> value = {
    ...     'f1': val,
    ... }
    >>> compound = factory(
    ...     'compound',
    ...     'comp',
    ...     value=value)
    >>> compound['f1'] = factory('text')
    >>> compound()
    u'<input class="text" id="input-comp-f1" name="comp.f1" type="text" 
    value="val F1" />'

    >>> data = compound.extract({'comp.f1': 'New val 1'})
    >>> data.printtree()
    <RuntimeData comp, value={'f1': <function val at ...>}, 
      extracted=odict([('f1', 'New val 1')]) at ...>
      <RuntimeData comp.f1, value='val F1', extracted='New val 1' at ...>

    >>> def value(widget, data):
    ...     return {
    ...         'f1': 'F1 Val'
    ...     }
    >>> compound = factory(
    ...     'compound',
    ...     'comp',
    ...     value=value)
    >>> compound['f1'] = factory('text')
    >>> compound()
    u'<input class="text" id="input-comp-f1" name="comp.f1" type="text" 
    value="F1 Val" />'
    
    >>> data = compound.extract({'comp.f1': 'New val 1'})
    >>> data.printtree()
    <RuntimeData comp, value={'f1': 'F1 Val'}, 
      extracted=odict([('f1', 'New val 1')]) at ...>
      <RuntimeData comp.f1, value='F1 Val', extracted='New val 1' at ...>


Div
---

Div blueprint as compound::

    >>> div = factory(
    ...     'div',
    ...     name='WRAPPED_COMPOUND')
    >>> div['inner']  = factory(
    ...     'text',
    ...     value='value1')
    >>> div['inner2'] = factory(
    ...     'text',
    ...     value='value2',
    ...     props={
    ...         'required': True
    ...     })
    >>> pxml(div())
    <div>
      <input class="text" id="input-WRAPPED_COMPOUND-inner" 
        name="WRAPPED_COMPOUND.inner" type="text" value="value1"/>
      <input class="required text" id="input-WRAPPED_COMPOUND-inner2" 
        name="WRAPPED_COMPOUND.inner2" required="required" type="text" 
        value="value2"/>
    </div>
    <BLANKLINE>

    >>> data = div.extract({
    ...     'WRAPPED_COMPOUND.inner': '1',
    ...     'WRAPPED_COMPOUND.inner2': '2',
    ... })
    >>> data.printtree()
    <RuntimeData WRAPPED_COMPOUND, value=<UNSET>, 
      extracted=odict([('inner', '1'), ('inner2', '2')]) at ...>
      <RuntimeData WRAPPED_COMPOUND.inner, value='value1', 
        extracted='1' at ...>
      <RuntimeData WRAPPED_COMPOUND.inner2, value='value2', 
        extracted='2' at ...>

Dic blueprint as compound, but with ``leaf`` property set. Causes
``hybrid_renderer`` and ``hybrid_extractor`` to skip auto delegating to
``compound_renderer`` and ``compound_extractor``::

    >>> div = factory(
    ...     'div',
    ...     name='WRAPPED_COMPOUND',
    ...     props={
    ...         'leaf': True
    ...     })
    >>> div['inner']  = factory(
    ...     'text',
    ...     value='value1')
    >>> div['inner2'] = factory(
    ...     'text',
    ...     value='value2',
    ...     props={
    ...         'required': True
    ...     })
    >>> pxml(div())
    <div/>
    <BLANKLINE>

    >>> data = div.extract({
    ...     'WRAPPED_COMPOUND.inner': '1',
    ...     'WRAPPED_COMPOUND.inner2': '2',
    ... })
    >>> data.printtree()
    <RuntimeData WRAPPED_COMPOUND, value=<UNSET>, extracted=<UNSET> at ...>

Div blueprint as leaf::

    >>> input = factory(
    ...     'div:text',
    ...     'field',
    ...     value='1')
    >>> pxml(input())
    <div>
      <input class="text" id="input-field" name="field" type="text" value="1"/>
    </div>
    <BLANKLINE>

    >>> data = input.extract({
    ...     'field': '2',
    ... })
    >>> data.printtree()
    <RuntimeData field, value='1', extracted='2' at ...>

Empty div::

    >>> input = factory(
    ...     'div',
    ...     'field')
    >>> pxml(input())
    <div/>
    <BLANKLINE>

Div with data attributes::

    >>> input = factory(
    ...     'div',
    ...     'field',
    ...     props={
    ...         'data': {
    ...             'foo': 'bar'
    ...         }
    ...     })
    >>> pxml(input())
    <div data-foo="bar"/>
    <BLANKLINE>

Display mode::

    >>> div = factory(
    ...     'div',
    ...     name='WRAPPED_COMPOUND',
    ...     props={
    ...         'class': 'foo'
    ...     },
    ...     mode='display')
    >>> pxml(div())
    <div class="foo"/>
    <BLANKLINE>

    >>> input = factory(
    ...     'div:text',
    ...     'field',
    ...     value='1',
    ...     mode='display')
    >>> pxml(input())
    <div>
      <div class="display-text" id="display-field">1</div>
    </div>
    <BLANKLINE>


Fieldset
--------

::

    >>> compound = factory(
    ...     'fieldset',
    ...     'COMPOUND',
    ...     props={
    ...         'legend': 'Some Test'
    ...     })
    >>> compound['inner'] = factory('text', 'inner', 'value')
    >>> compound['inner2'] = factory('text', 'inner2', 'value2')
    >>> pxml(compound())
    <fieldset id="fieldset-COMPOUND">
      <legend>Some Test</legend>
      <input class="text" id="input-COMPOUND-inner" name="COMPOUND.inner" 
        type="text" value="value"/>
      <input class="text" id="input-COMPOUND-inner2" name="COMPOUND.inner2" 
        type="text" value="value2"/>
    </fieldset>
    <BLANKLINE>

Structural fieldset renders without id attribute::

    >>> compound = factory(
    ...     'fieldset',
    ...     'COMPOUND',
    ...     props={
    ...         'structural': True
    ...     })
    >>> pxml(compound())
    <fieldset/>
    <BLANKLINE>
 
Fieldset display renderers are the same as fieldset edit renderers::

    >>> compound = factory(
    ...     'fieldset',
    ...     'COMPOUND',
    ...     props={
    ...         'legend': 'Some Test'
    ...     },
    ...     mode='display')
    >>> pxml(compound())
    <fieldset id="fieldset-COMPOUND">
      <legend>Some Test</legend>
    </fieldset>
    <BLANKLINE>


Form
----

Test Form::

    >>> form = factory(
    ...     'form',
    ...     name = 'FORM',
    ...     props={
    ...         'action': 'http://fubar.com'
    ...     })
    >>> form()
    u'<form action="http://fubar.com" enctype="multipart/form-data" 
    id="form-FORM" method="post" novalidate="novalidate"></form>'

Form action as callable::

    >>> def action(widget, data):
    ...     return 'http://fubar.com'

    >>> form = factory(
    ...     'form',
    ...     name = 'FORM',
    ...     props={
    ...         'action': action
    ...     })
    >>> form()
    u'<form action="http://fubar.com" enctype="multipart/form-data" 
    id="form-FORM" method="post" novalidate="novalidate"></form>'

Form display renderer::

    >>> form = factory(
    ...     'form',
    ...     name = 'FORM',
    ...     props={
    ...         'action': 'http://fubar.com'
    ...     },
    ...     mode='display')
    >>> form()
    u'<div></div>'

Create a form with some children::

    >>> form = factory(
    ...     'form',
    ...     name='myform',
    ...     props={
    ...         'action': 'http://www.domain.tld/someform'
    ...     })
    >>> form['someinput'] = factory(
    ...     'label:text',
    ...     props={
    ...         'label': 'Your Text'
    ...     })

    >>> def formaction(widget, data):
    ...     data.printtree()

    >>> def formnext(request):
    ...     return 'http://www.domain.tld/result'

    >>> form['submit'] = factory(
    ...     'submit',
    ...     props={
    ...         'handler': formaction,
    ...         'next': formnext,
    ...         'action': True
    ...     })

Render an empty form::

    >>> pxml(form())
    <form action="http://www.domain.tld/someform" 
      enctype="multipart/form-data" id="form-myform" method="post" 
      novalidate="novalidate">
      <label for="input-myform-someinput">Your Text</label>
      <input class="text" id="input-myform-someinput" name="myform.someinput" 
        type="text" value=""/>
      <input id="input-myform-submit" name="action.myform.submit" 
        type="submit" value="submit"/>
    </form>
    <BLANKLINE>

Get form data out of request (request is expected dict-like)::

    >>> request = {
    ...     'myform.someinput': 'Hello World',
    ...     'action.myform.submit': 'submit'
    ... }
    >>> controller = Controller(form, request)
    <RuntimeData myform, value=<UNSET>, 
      extracted=odict([('someinput', 'Hello World'), 
      ('submit', <UNSET>)]) at ...>
      <RuntimeData myform.someinput, value=<UNSET>, 
        extracted='Hello World' at ...>
      <RuntimeData myform.submit, value=<UNSET>, extracted=<UNSET> at ...>

Form action property can be callable::

    >>> def action(widget, data):
    ...     return 'actionfromcall'

    >>> form = factory(
    ...     'form',
    ...     name='form',
    ...     props={
    ...         'action':action,
    ...     })
    >>> form()
    u'<form action="actionfromcall" enctype="multipart/form-data" 
    id="form-form" method="post" novalidate="novalidate"></form>'

Create label for field in other compound::

    >>> form = factory(
    ...     'form',
    ...     name = 'form',
    ...     props = {
    ...         'action': 'action'
    ...     })
    >>> form['label'] = factory(
    ...     'label',
    ...     props={
    ...         'label': 'Foo',
    ...         'for': 'field'
    ...     })
    >>> form['field'] = factory('text')
    >>> form()
    u'<form action="action" enctype="multipart/form-data" id="form-form" 
    method="post" novalidate="novalidate"><label 
    for="input-form-field">Foo</label><input 
    class="text" id="input-form-field" name="form.field" type="text" 
    value="" /></form>'
