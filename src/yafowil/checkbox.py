# -*- coding: utf-8 -*-
from node.utils import UNSET
from yafowil.base import factory
from yafowil.base import fetch_value
from yafowil.common import generic_required_extractor
from yafowil.common import input_attributes_common
from yafowil.tsf import _
from yafowil.utils import attr_value
from yafowil.utils import css_managed_props
from yafowil.utils import cssid
from yafowil.utils import managedprops
from yafowil.utils import vocabulary


###############################################################################
# checkbox
###############################################################################

@managedprops('format')
def checkbox_extractor(widget, data):
    """Extracts data from a single input with type checkbox.
    """
    if '{0}-exists'.format(widget.dottedpath) not in data.request:
        return UNSET
    fmt = attr_value('format', widget, data)
    if fmt == 'bool':
        return widget.dottedpath in data.request
    elif fmt == 'string':
        return data.request.get(widget.dottedpath, '')
    raise ValueError(
        "Checkbox widget has invalid format '{0}' set".format(fmt)
    )


@managedprops(
    'data',
    'title',
    'size',
    'disabled',
    'autofocus',
    'format',
    'disabled',
    'checked',
    'with_label',
    *css_managed_props)
def checkbox_edit_renderer(widget, data):
    tag = data.tag
    input_attrs = input_attributes_common(widget, data)
    input_attrs['type'] = 'checkbox'
    checked = attr_value('checked', widget, data)
    if checked is not None:
        if checked:
            input_attrs['checked'] = 'checked'
    else:
        input_attrs['checked'] = input_attrs['value'] and 'checked' or None
    if attr_value('format', widget, data) == 'bool':
        input_attrs['value'] = ''
    checkbox = tag('input', **input_attrs)
    if attr_value('with_label', widget, data):
        checkbox += tag(
            'label',
            '&nbsp;',
            for_=cssid(widget, 'input'),
            class_='checkbox_label'
        )
    input_attrs = {
        'type': 'hidden',
        'value': 'checkboxexists',
        'name_': "{0}-exists".format(widget.dottedpath),
        'id': cssid(widget, 'checkboxexists'),
    }
    exists_marker = tag('input', **input_attrs)
    return checkbox + exists_marker


@managedprops('class', 'format', 'vocabulary', 'display_proxy')
def checkbox_display_renderer(widget, data):
    """Generic display renderer to render a value.
    """
    value = fetch_value(widget, data)
    fmt = attr_value('format', widget, data)
    if fmt == 'string' and bool(value):
        content = value
    else:
        vocab = dict(vocabulary(attr_value('vocabulary', widget, data, [])))
        # XXX: value might be 'True' Looks odd.
        content = vocab[bool(value)]
        if data.tag.translate:
            content = data.tag.translate(content)
    attrs = {
        'id': cssid(widget, 'display'),
        'class_': 'display-{0}'.format(attr_value('class', widget, data))
    }
    if attr_value('display_proxy', widget, data):
        widget.attrs['type'] = 'hidden'
        if fmt == 'string':
            input_attrs = input_attributes_common(widget, data, value=value)
            content += data.tag('input', **input_attrs)
        elif bool(value):
            input_attrs = input_attributes_common(widget, data, value='')
            content += data.tag('input', **input_attrs)
        del widget.attrs['type']
        input_attrs = {
            'type': 'hidden',
            'value': 'checkboxexists',
            'name_': "{0}-exists".format(widget.dottedpath),
            'id': cssid(widget, 'checkboxexists'),
        }
        content += data.tag('input', **input_attrs)
    return data.tag('div', content, **attrs)


factory.register(
    'checkbox',
    extractors=[
        checkbox_extractor,
        generic_required_extractor
    ],
    edit_renderers=[checkbox_edit_renderer],
    display_renderers=[checkbox_display_renderer]
)

factory.doc['blueprint']['checkbox'] = """\
Single checkbox blueprint.
"""

factory.defaults['checkbox.default'] = False

factory.defaults['checkbox.format'] = 'bool'
factory.doc['props']['checkbox.format'] = """\
Data-type of the extracted value. One out of ``bool`` or ``string``.
"""

factory.defaults['checkbox.class'] = 'checkbox'

factory.defaults['checkbox.disabled'] = False
factory.doc['props']['checkbox.disabled'] = """\
Flag whether checkbox is disabled.
"""

factory.defaults['checkbox.checked'] = None
factory.doc['props']['checkbox.checked'] = """\
Set 'checked' attribute explicit. If not given, compute by value.
"""

factory.defaults['checkbox.vocabulary'] = {
    True: _('yes', default=u'Yes'),
    False: _('no', default=u'No'),
    UNSET: _('unset', default=u'Unset'),  # XXX: never used right now?
}

factory.doc['props']['checkbox.vocabulary'] = """\
In display mode and if ```bool``` is set to ```True``` this mapping will be
used for display of the value. Expected keys are ```True```, ```False``` and
```UNSET```.
"""

factory.defaults['checkbox.with_label'] = False
factory.doc['props']['checkbox.with_label'] = """\
Render empty label tag after visible checkbox in order to make checkbox UI
customizable via CSS like so::

    input.large_checkbox {
        display: none;
    }
    input.large_checkbox + label {
        width: 59px;
        height: 60px;
        background: url('/checkbox_large.png');
    }
    input.large_checkbox:checked + label {
        background: url('/checkbox_large_selected.png');
    }
"""

factory.defaults['checkbox.required_class'] = 'required'

factory.defaults['checkbox.persist'] = True
