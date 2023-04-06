# -*- coding: utf-8 -*-
from yafowil.base import factory
from yafowil.common import empty_display_renderer
from yafowil.common import input_attributes_common
from yafowil.tsf import _
from yafowil.utils import attr_value
from yafowil.utils import managedprops


###############################################################################
# submit
###############################################################################

@managedprops(
    'tag_type',
    'label',
    'class',
    'action',
    'handler',
    'next',
    'skip',
    'expression')
def submit_renderer(widget, data):
    expression = attr_value('expression', widget, data)
    if not expression:
        return u''
    tag = data.tag
    input_attrs = input_attributes_common(widget, data)
    input_attrs['type'] = 'submit'
    input_attrs['name_'] = attr_value('action', widget, data) \
        and 'action.{0}'.format(widget.dottedpath)
    input_attrs['value'] = attr_value('label', widget, data, widget.name)
    return tag(attr_value('tag_type', widget, data), **input_attrs)


factory.register(
    'submit',
    edit_renderers=[submit_renderer],
    display_renderers=[empty_display_renderer]
)

factory.doc['blueprint']['submit'] = """\
Submit action inside the form
"""

factory.doc['props']['submit.label'] = """\
Label of the submit.
"""

factory.defaults['submit.tag_type'] = 'input'
factory.doc['props']['submit.tag_type'] = """\
Define the type of tag that will be rendered.
"""

factory.defaults['submit.expression'] = True
factory.doc['props']['submit.expression'] = """\
Flag or expression callable whether this action is available to the user
or not.
"""

factory.defaults['submit.action'] = True
factory.doc['props']['submit.action'] = """\
Marks this widget as an action. One out of ``True`` or ``False``.
"""

factory.defaults['submit.skip'] = False
factory.doc['props']['submit.skip'] = """\
Skips action and only perform next. One out of ``True`` or ``False``.
"""

factory.doc['props']['submit.handler'] = """\
Handler is a callable which get called if this action performs. It expects two
parameters: ``widget``, ``data``.
"""

factory.doc['props']['submit.next'] = """\
Next is a callable expected to return the web address. It expects a request as
the only parameter.
"""

factory.defaults['submit.disabled'] = False
factory.doc['props']['submit.disabled'] = """\
Flag the submit field as disabled.
"""


###############################################################################
# button
###############################################################################

@managedprops(
    'text',
    'action',
    'handler',
    'next',
    'skip',
    'type',
    'expression',
    'form',
    'formaction',
    'formenctype',
    'formmethod',
    'formnovalidate',
    'formtarget',
    'autofocus',
    'disabled',
    'class',
    'class_add',
    'accesskey')
def button_renderer(widget, data):
    expression = attr_value('expression', widget, data)
    if not expression:
        return u''
    tag = data.tag
    input_attrs = input_attributes_common(widget, data)
    input_attrs['type'] = attr_value('type', widget, data)
    input_attrs['form'] = attr_value('form', widget, data)
    input_attrs['formaction'] = attr_value('formaction', widget, data)
    input_attrs['formenctype'] = attr_value('formenctype', widget, data)
    input_attrs['formmethod'] = attr_value('formmethod', widget, data)
    input_attrs['formnovalidate'] = attr_value('formnovalidate', widget, data)
    input_attrs['formtarget'] = attr_value('formtarget', widget, data)
    input_attrs['accesskey'] = attr_value('accesskey', widget, data)
    if input_attrs['type'] == 'submit':
        # only 'submit' type sends data to the server
        if attr_value('action', widget, data):
            # only if an server side action is set this makes sense:
            input_attrs['name_'] = 'action.{0}'.format(widget.dottedpath)
        else:
            # otherwise check for a custom name
            input_attrs['name_'] = attr_value('name', widget, data)
    text = attr_value('text', widget, data)
    return tag("button", text, **input_attrs)


factory.register(
    'button',
    edit_renderers=[button_renderer],
    display_renderers=[empty_display_renderer]
)

factory.defaults['button.type'] = 'submit'

factory.doc['blueprint']['button'] = """\
Represents a clickable button, used to submit forms or anywhere in a document for
accessible, standard button functionality.
"""

factory.doc['props']['button.text'] = """\
The content of the button element.
"""

# parts of the docs are copied over from
# https://developer.mozilla.org/de/docs/Web/HTML/Element/button

factory.doc['props']['button.form'] = """\
The <form> element to associate the button with (its form owner).
The value of this attribute must be the id of a <form> in the same document.
(If this attribute is not set, the <button> is associated with its ancestor
<form> element, if any.)
"""

factory.doc['props']['button.formaction'] = """\
The URL that processes the information submitted by the button.
Overrides the action attribute of the button's form owner.
Does nothing if there is no form owner.
"""

factory.doc['props']['button.formenctype'] = """\
If the button is a submit button (it's inside/associated with a <form> and
doesn't have type="button"), specifies how to encode the form data that is
submitted. Possible values:

application/x-www-form-urlencoded: The default if the attribute is not used.

multipart/form-data: Use to submit <input> elements with their type attributes
set to file.

text/plain: Specified as a debugging aid; shouldn’t be used for real form
submission.

If this attribute is specified, it overrides the enctype attribute of the
button's form owner.
"""

factory.doc['props']['button.formmethod'] = """\
If the button is a submit button (it's inside/associated with a <form> and
doesn't have type="button"), this attribute specifies the HTTP method used
to submit the form. Possible values: POST or GET. If specified, this
attribute overrides the method attribute of the button's form owner.
"""

factory.doc['props']['button.formnovalidate'] = """\
If the button is a submit button, this Boolean attribute specifies that the
form is not to be validated when it is submitted. If this attribute is
specified, it overrides the novalidate attribute of the button's form owner.
"""

factory.doc['props']['button.formtarget'] = """\
If the button is a submit button, this attribute is a author-defined name or
standardized, underscore-prefixed keyword indicating where to display the
response from submitting the form. This is the name of, or keyword for,
a browsing context (a tab, window, or <iframe>). If this attribute is
specified, it overrides the target attribute of the button's form owner.
The following keywords have special meanings:

_self: Load the response into the same browsing context as the current one.
This is the default if the attribute is not specified.

_blank: Load the response into a new unnamed browsing context — usually a new
tab or window, depending on the user’s browser settings.

_parent: Load the response into the parent browsing context of the current one.
If there is no parent, this option behaves the same way as _self.

_top: Load the response into the top-level browsing context (that is, the
browsing context that is an ancestor of the current one, and has no parent).
If there is no parent, this option behaves the same way as _self.
"""

factory.defaults['button.expression'] = True
factory.doc['props']['button.expression'] = """\
Flag or expression callable whether this action is available to the user
or not.
"""

factory.defaults['button.action'] = True
factory.doc['props']['button.action'] = """\
Marks this widget as an action. One out of ``True`` or ``False``.
"""

factory.defaults['button.skip'] = False
factory.doc['props']['button.skip'] = """\
Skips action and only perform next. One out of ``True`` or ``False``.
"""

factory.doc['props']['button.handler'] = """\
Handler is a callable which get called if this action performs. It expects two
parameters: ``widget``, ``data``.
"""

factory.doc['props']['button.next'] = """\
Next is a callable expected to return the web address. It expects a request as
the only parameter.
"""

factory.defaults['button.disabled'] = False
factory.doc['props']['button.disabled'] = """\
Flag the button field as disabled.
"""

factory.defaults['button.autofocus'] = False
factory.doc['props']['button.autofocus'] = """\
Boolean attribute specifies that the button should have input focus when the
page loads. Only one element in a document can have this attribute.
"""

factory.defaults['button.autocomplete'] = False
factory.doc['props']['button.autocomplete'] = """\
This attribute on a <button> is nonstandard and Firefox-specific.
Unlike other browsers, Firefox persists the dynamic disabled state of a
<button> across page loads. Setting autocomplete="off" on the button
disables this feature
"""
