# -*- coding: utf-8 -*-
from node.utils import UNSET
from yafowil.base import factory
from yafowil.common import empty_display_renderer
from yafowil.common import generic_positional_rendering_helper
from yafowil.utils import attr_value
from yafowil.utils import css_managed_props
from yafowil.utils import cssclasses
from yafowil.utils import cssid
from yafowil.utils import managedprops


###############################################################################
# field
###############################################################################

@managedprops('witherror', *css_managed_props)
def field_renderer(widget, data):
    tag = data.tag
    div_attrs = {
        'id': cssid(widget, 'field'),
        'class_': cssclasses(widget, data)
    }
    witherror = attr_value('witherror', widget, data)
    if witherror and data.errors:
        div_attrs['class_'] += u' {0}'.format(witherror)
    return tag('div', data.rendered, **div_attrs)


factory.register(
    'field',
    edit_renderers=[field_renderer],
    display_renderers=[field_renderer]
)

factory.doc['blueprint']['field'] = """\
Renders a div with an class field around the prior rendered output. This is
supposed to be used for styling and grouping purposes.
"""

factory.defaults['field.class'] = 'field'

factory.defaults['field.witherror'] = None
factory.doc['props']['field.witherror'] = """\
Put the class given with this property on the div if an error happened.
"""


###############################################################################
# label
###############################################################################

@managedprops('position', 'label', 'for', *css_managed_props)
def label_renderer(widget, data):
    tag = data.tag
    label_text = attr_value('label', widget, data, widget.name)
    label_attrs = {
        'class_': cssclasses(widget, data)
    }
    if data.mode == 'edit':
        for_path = attr_value('for', widget, data)
        if for_path:
            for_widget = widget.root
            for name in for_path.split('.'):
                for_widget = for_widget[name]
            label_attrs['for_'] = cssid(for_widget, 'input')
        else:
            label_attrs['for_'] = cssid(widget, 'input')
        title = attr_value('title', widget, data)
        if title:
            label_attrs['title'] = title
    pos = attr_value('position', widget, data)
    if pos == 'inner':
        # deprecated, use explicit inner-after or inner-before
        pos = 'inner-before'
    rendered = data.rendered is not UNSET and data.rendered or u''
    return generic_positional_rendering_helper(
        'label', label_text, label_attrs, rendered, pos, tag
    )


factory.register(
    'label',
    edit_renderers=[label_renderer],
    display_renderers=[label_renderer]
)

factory.doc['blueprint']['label'] = """\
Label blueprint.
"""

factory.defaults['label.position'] = 'before'
factory.doc['props']['label.position'] = """\
Label can be rendered at 3 different positions: ``before`` or ``after`` the
prior rendered output or with ``inner`` it puts the prior rendered output
inside the label tag.
"""

factory.doc['props']['label.label'] = """\
Text to be displayed as a label.
"""

factory.defaults['label.for'] = None
factory.doc['props']['label.for'] = """\
Optional dottedpath of widget to be labled
"""


###############################################################################
# help
###############################################################################

@managedprops('tag', 'help', 'position', 'render_empty', *css_managed_props)
def help_renderer(widget, data):
    render_empty = attr_value('render_empty', widget, data)
    help_val = attr_value('help', widget, data)
    if not render_empty and not help_val:
        return data.rendered
    tag = data.tag
    attrs = dict(class_=cssclasses(widget, data))
    elem_tag = attr_value('tag', widget, data)
    position = attr_value('position', widget, data)
    return generic_positional_rendering_helper(
        elem_tag, help_val, attrs, data.rendered, position, tag
    )


factory.register(
    'help',
    edit_renderers=[help_renderer],
    display_renderers=[empty_display_renderer]
)

factory.doc['blueprint']['help'] = """\
Renders a tag with an help-message and the prior rendered output.
"""

factory.defaults['help.class'] = 'help'

factory.defaults['help.tag'] = 'div'
factory.doc['props']['help.tag'] = """\
HTML tag to use to enclose all help messages.
"""

factory.defaults['help.help'] = ''
factory.doc['props']['help.help'] = """\
Help text.
"""

factory.defaults['help.render_empty'] = False
factory.doc['props']['help.render_empty'] = """\
Render tag even if there is no help message.
"""

factory.defaults['help.position'] = 'before'
factory.doc['props']['help.position'] = """\
Help can be rendered at 3 different positions: ``before``/ ``after`` the
prior rendered output or with ``inner-before``/ ``inner-after``  it puts the
prior rendered output inside the tag used for the help message (beofre or
after the message.
"""


###############################################################################
# error
###############################################################################

@managedprops(
    'tag',
    'message_tag',
    'message_class',
    'position',
    'render_empty',
    *css_managed_props)
def error_renderer(widget, data):
    if not data.errors and not attr_value('render_empty', widget, data):
        return data.rendered
    tag = data.tag
    msgs = u''
    for error in data.errors:
        message_tag = attr_value('message_tag', widget, data)
        if message_tag:
            msgs += tag(
                message_tag,
                error.msg,
                class_=attr_value('message_class', widget, data)
            )
        else:
            msgs += tag.translate(error.msg)
    attrs = dict(class_=cssclasses(widget, data))
    elem_tag = attr_value('tag', widget, data)
    position = attr_value('position', widget, data)
    return generic_positional_rendering_helper(
        elem_tag, msgs, attrs, data.rendered, position, tag
    )


factory.register(
    'error',
    edit_renderers=[error_renderer],
    display_renderers=[empty_display_renderer]
)

factory.doc['blueprint']['error'] = """\
Renders a tag with an error-message and the prior rendered output.
"""

factory.defaults['error.class'] = 'error'

factory.defaults['error.tag'] = 'div'
factory.doc['props']['error.tag'] = """\
HTML tag to use to enclose all error messages.
"""

factory.defaults['error.render_empty'] = False
factory.doc['props']['error.render_empty'] = """\
Render tag even if there is no error message.
"""

factory.defaults['error.message_tag'] = 'div'
factory.doc['props']['error.message_tag'] = """\
HTML tag to use to enclose each error message.
"""

factory.defaults['error.message_class'] = 'errormessage'
factory.doc['props']['error.message_class'] = """\
CSS class to apply to inner message-tag.
"""

factory.defaults['error.position'] = 'inner-before'
factory.doc['props']['error.position'] = """\
Error can be rendered at 3 different positions: ``before``/ ``after`` the
prior rendered output or with ``inner-before``/ ``inner-after``  it puts the
prior rendered output inside the tag used for the error message (beofre or
after the message.
"""
