Required imports::

    >>> import yafowil.common
    >>> import yafowil.compound
    >>> from yafowil.base import factory
    >>> from yafowil.controller import Controller

Dummy context::

    >>> class Context(object):
    ...     value = 'hello world'    
    >>> context = Context()

Dummy getter::

    >>> def getter(widget, data):
    ...     return data.request.context.value

Create Widget tree::

    >>> form = factory(
    ...     u'form',
    ...     name='testform',
    ...     props={
    ...         'action': 'http://fubar.com'
    ...     })
    >>> form['field1'] = factory(
    ...     'text',
    ...     value=getter)
    >>> form['field2'] = factory(
    ...     'text',
    ...     value='',
    ...     props={
    ...         'required': True
    ...     })

Define action ``handler``::

    >>> def handler(widget, data):
    ...     print 'handler called "%s"' % '.'.join(widget.path)

Define action ``next``::

    >>> def next(request):
    ...     return 'next return value'

Indicate widget to be an ``action`` definition by setting ``action`` attribute
to widget properties. ``expression``, ``handler`` and ``next`` are action
referring properties::

    >>> props = {
    ...     'action': 'save',
    ...     'expression': True,
    ...     'handler': handler,
    ...     'next': next,
    ...     'label': 'Save',
    ...     'skip': False,
    ... }

Add save action::

    >>> form['save'] = factory('submit', props=props)

Add cancel action. In this case we want the form processing to be skipped and
just the next action to be performed::

    >>> props = {
    ...     'action': 'cancel',
    ...     'expression': True,
    ...     'handler': None,
    ...     'next': next,
    ...     'label': 'Cancel',
    ...     'skip': True,
    ... }
    >>> form['cancel'] = factory('submit', props=props)

Check widget tree::

    >>> form.printtree()
    <class 'yafowil.base.Widget'>: testform
      <class 'yafowil.base.Widget'>: field1
      <class 'yafowil.base.Widget'>: field2
      <class 'yafowil.base.Widget'>: save
      <class 'yafowil.base.Widget'>: cancel

Dummy request::

    >>> class Request(dict):
    ...     context = context
    >>> request = Request()

Render form with empty request::

    >>> data = form.extract(request)
    >>> pxml(form(data))
    <form action="http://fubar.com" enctype="multipart/form-data" 
      id="form-testform" method="post" novalidate="novalidate">
      <input class="text" id="input-testform-field1" name="testform.field1" 
        type="text" value="hello world"/>
      <input class="required text" id="input-testform-field2" 
        name="testform.field2" required="required" type="text" value=""/>
      <input id="input-testform-save" name="action.testform.save" 
        type="submit" value="Save"/>
      <input id="input-testform-cancel" name="action.testform.cancel" 
        type="submit" value="Cancel"/>
    </form>
    <BLANKLINE>

Create controller for form::

    >>> controller = Controller(form, request)

If action is not triggered, or ``action['next']`` is not set,
``Controller.next`` is ``None``::

    >>> controller.next

An empty request does not trigger validation failures::

    >>> controller.error
    False

Provide empty required field and it fails!::

    >>> request['testform.field2'] = ''
    >>> controller = Controller(form, request)
    >>> controller.error
    True

Provide required field and all is fine::

    >>> request['testform.field2'] = '1'
    >>> controller = Controller(form, request)
    >>> controller.error
    False

Trigger save action without required field::

    >>> request['testform.field2'] = ''
    >>> request['action.testform.save'] = '1'
    >>> controller = Controller(form, request)
    >>> controller.error
    True

    >>> controller.performed
    True

Trigger save action with valid input::

    >>> request['testform.field2'] = '1'
    >>> controller = Controller(form, request)
    handler called "testform"

    >>> controller.next
    'next return value'

    >>> controller.error
    False

    >>> controller.performed
    True

Render the form performed::

    >>> pxml(controller.rendered)
    <form action="http://fubar.com" enctype="multipart/form-data" 
      id="form-testform" method="post" novalidate="novalidate">
      <input class="text" id="input-testform-field1" name="testform.field1" 
        type="text" value="hello world"/>
      <input class="required text" id="input-testform-field2" 
        name="testform.field2" required="required" type="text" value="1"/>
      <input id="input-testform-save" name="action.testform.save" 
        type="submit" value="Save"/>
      <input id="input-testform-cancel" name="action.testform.cancel" 
        type="submit" value="Cancel"/>
    </form>
    <BLANKLINE>

Trigger cancel action. performing is skipped::

    >>> del request['action.testform.save']
    >>> request['action.testform.cancel'] = '1'
    >>> controller = Controller(form, request)

    >>> controller.next
    'next return value'

    >>> controller.performed
    False

Render form not performed::

    >>> pxml(controller.rendered)
    <form action="http://fubar.com" enctype="multipart/form-data" 
      id="form-testform" method="post" novalidate="novalidate">
      <input class="text" id="input-testform-field1" name="testform.field1" 
        type="text" value="hello world"/>
      <input class="required text" id="input-testform-field2" 
        name="testform.field2" required="required" type="text" value=""/>
      <input id="input-testform-save" name="action.testform.save" 
        type="submit" value="Save"/>
      <input id="input-testform-cancel" name="action.testform.cancel" 
        type="submit" value="Cancel"/>
    </form>
    <BLANKLINE>

Try recursive lookup of actions::

    >>> form = factory(
    ...     u'form',
    ...     name='testform',
    ...     props={
    ...         'action': 'http://fubar.com'
    ...     })
    >>> form['level1'] = factory(
    ...     'submit',
    ...     props={
    ...         'action': 'l1action'
    ...     })
    >>> form['fieldset'] = factory('fieldset')
    >>> form['fieldset']['level2'] = factory(
    ...     'submit',
    ...     props={
    ...         'action': 'l2action'
    ...     })
    >>> form['fieldset']['subset'] = factory('fieldset')
    >>> form['fieldset']['subset']['level3'] = factory(
    ...     'submit',
    ...     props={
    ...         'action': 'l3action'
    ...     })
    >>> controller = Controller(form, {})
    >>> controller.actions
    [<Widget object 'level1' at ...>, 
    <Widget object 'level2' at ...>, 
    <Widget object 'level3' at ...>]
