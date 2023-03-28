# -*- coding: utf-8 -*-
from node.utils import UNSET
from yafowil.base import factory
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
