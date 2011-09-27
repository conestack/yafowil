Compound
--------

Preparation::

    >>> import yafowil.common
    >>> import yafowil.compound
    >>> from yafowil.base import factory
    >>> from yafowil.utils import Tag
    >>> tag = Tag(lambda msg: msg)           

Render Compound with values set via compound widget::

    >>> value = {
    ...     'inner': 'Value 1 from parent',
    ...     'inner2': 'Value 2 from parent',
    ... }
    >>> compound = factory('compound', name='COMPOUND', value=value)
    >>> compound['inner']  = factory('text')
    >>> compound['inner2'] = factory('text', 
    ...                              props={'required': True})
    >>> pxml(tag('div', compound()))
    <div>
      <input class="text" id="input-COMPOUND-inner" name="COMPOUND.inner" type="text" value="Value 1 from parent"/>
      <input class="required text" id="input-COMPOUND-inner2" name="COMPOUND.inner2" required="required" type="text" value="Value 2 from parent"/>
    </div>
    <BLANKLINE>

ValueError if value for a compound member is defined both::

    >>> value = {'inner': 'Value 1 from parent'}
    >>> compound = factory('compound', name='COMPOUND', value=value)
    >>> compound['inner']  = factory('text', value='value1')
    >>> pxml(tag('div', compound()))
    Traceback (most recent call last):
      ...
    ValueError: Both compound and compound member provide a value for 'inner'

Render Compound with values set via compound members::

    >>> compound = factory('compound', name='COMPOUND')
    >>> compound['inner']  = factory('text', value='value1')
    >>> compound['inner2'] = factory('text', value='value2', 
    ...                              props={'required': True})
    >>> pxml(tag('div', compound()))
    <div>
      <input class="text" id="input-COMPOUND-inner" name="COMPOUND.inner" type="text" value="value1"/>
      <input class="required text" id="input-COMPOUND-inner2" name="COMPOUND.inner2" required="required" type="text" value="value2"/>
    </div>
    <BLANKLINE>

Extract Compound empty::    

    >>> data = compound.extract({})
    >>> data 
    <RuntimeData COMPOUND, value=<UNSET>, 
    extracted=odict([('inner', <UNSET>), ('inner2', <UNSET>)]) at ...> 

    >>> data['inner']
    <RuntimeData COMPOUND.inner, value='value1', extracted=<UNSET> at ...>    

Extract with a value in request::

    >>> data = compound.extract({'COMPOUND.inner': 'newvalue'})
    >>> data['inner']
    <RuntimeData COMPOUND.inner, value='value1', extracted='newvalue' at ...>    

Extract with empty required, error should be there::

    >>> data = compound.extract({'COMPOUND.inner2': ''})
    >>> data['inner2']
    <RuntimeData COMPOUND.inner2, value='value2', extracted='', 
    1 error(s) at ...>

Compound display renderers, same as edit renderers::

    >>> compound = factory('compound', name='COMPOUND', mode='display')
    >>> pxml(tag('div', compound()))
    <div/>
    <BLANKLINE>


Wrapped compound
----------------

::

    >>> wrapped_compound = factory('div', name='WRAPPED_COMPOUND')
    >>> wrapped_compound['inner']  = factory('text', value='value1')
    >>> wrapped_compound['inner2'] = factory('text', value='value2', 
    ...                                      props={'required': True})
    >>> pxml(wrapped_compound())
    <div>
      <input class="text" id="input-WRAPPED_COMPOUND-inner" name="WRAPPED_COMPOUND.inner" type="text" value="value1"/>
      <input class="required text" id="input-WRAPPED_COMPOUND-inner2" name="WRAPPED_COMPOUND.inner2" required="required" type="text" value="value2"/>
    </div>
    <BLANKLINE>
    
    >>> wrapped_compound = factory(
    ...     'div',
    ...     name='WRAPPED_COMPOUND',
    ...     props={'class': 'foo'},
    ...     mode='display')
    >>> pxml(wrapped_compound())
    <div class="foo"/>
    <BLANKLINE>


Fieldset
--------

::

    >>> compound = factory('fieldset', 
    ...                    'COMPOUND',
    ...                    props={'legend': 'Some Test'})
    >>> compound['inner'] = factory('text', 'inner', 'value')
    >>> compound['inner2'] = factory('text', 'inner2', 'value2')
    >>> pxml(compound())
    <fieldset id="fieldset-COMPOUND">
      <legend>Some Test</legend>
      <input class="text" id="input-COMPOUND-inner" name="COMPOUND.inner" type="text" value="value"/>
      <input class="text" id="input-COMPOUND-inner2" name="COMPOUND.inner2" type="text" value="value2"/>
    </fieldset>
    <BLANKLINE>

Fieldset display renderers are the same as fieldset edit renderers::

    >>> compound = factory('fieldset', 
    ...                    'COMPOUND',
    ...                    props={'legend': 'Some Test'},
    ...                    mode='display')
    >>> pxml(compound())
    <fieldset id="fieldset-COMPOUND">
      <legend>Some Test</legend>
    </fieldset>
    <BLANKLINE>

Test Form::

    >>> form = factory('form',
    ...                name = 'FORM',
    ...                props={'action': 'http://fubar.com'})
    >>> form()
    u'<form action="http://fubar.com" enctype="multipart/form-data" id="form-FORM" method="post" novalidate="novalidate"></form>'

Form display renderer::

    >>> form = factory('form',
    ...                name = 'FORM',
    ...                props={'action': 'http://fubar.com'},
    ...                mode='display')
    >>> form()
    u'<div></div>'

  
Form
----

::

    >>> from yafowil.base import factory
    >>> from yafowil.controller import Controller
    
Create a form::
    
    >>> form = factory('form', name='myform', 
    ...     props={'action': 'http://www.domain.tld/someform'})
    >>> form['someinput'] = factory('label:text', 
    ...     props={'label': 'Your Text'})
    
    >>> def formaction(widget, data):
    ...     data.printtree()

    >>> def formnext(request):
    ...     return 'http://www.domain.tld/result'
    
    >>> form['submit'] = factory('submit', 
    ...     props={'handler': formaction, 'next': formnext, 'action': True})
    
Render an empty form::

    >>> pxml(form())
    <form action="http://www.domain.tld/someform" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <label for="input-myform-someinput">Your Text</label>
      <input class="text" id="input-myform-someinput" name="myform.someinput" type="text" value=""/>
      <input id="input-myform-submit" name="action.myform.submit" type="submit" value="submit"/>
    </form>
    <BLANKLINE>

Get form data out of request (request is expected dict-like)::

    >>> request = {'myform.someinput': 'Hello World', 
    ...            'action.myform.submit': 'submit'}
    >>> controller = Controller(form, request)
    <RuntimeData myform, value=<UNSET>, extracted=odict([('someinput', 'Hello World'), ('submit', <UNSET>)]) at ...>
      <RuntimeData myform.someinput, value=<UNSET>, extracted='Hello World' at ...>
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
    ...         'action': 'action'})
    >>> form['label'] = factory(
    ...     'label',
    ...     props={
    ...         'label': 'Foo',
    ...         'for': 'field'})
    >>> form['field'] = factory('text')
    >>> form()
    u'<form action="action" enctype="multipart/form-data" id="form-form" 
    method="post" novalidate="novalidate"><label 
    for="input-form-field">Foo</label><input 
    class="text" id="input-form-field" name="form.field" type="text" 
    value="" /></form>'
