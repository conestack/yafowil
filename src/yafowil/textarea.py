# -*- coding: utf-8 -*-
from yafowil.base import factory
from yafowil.base import fetch_value
from yafowil.common import display_proxy_renderer
from yafowil.common import generic_display_renderer
from yafowil.common import generic_extractor
from yafowil.common import generic_required_extractor
from yafowil.datatypes import generic_emptyvalue_extractor
from yafowil.utils import as_data_attrs
from yafowil.utils import attr_value
from yafowil.utils import css_managed_props
from yafowil.utils import cssclasses
from yafowil.utils import cssid
from yafowil.utils import managedprops


###############################################################################
# textarea
###############################################################################

def textarea_attributes(widget, data):
    autofocus = attr_value('autofocus', widget, data) and 'autofocus' or None
    disabled = attr_value('disabled', widget, data) and 'disabled' or None
    readonly = attr_value('readonly', widget, data) and 'readonly' or None
    required = attr_value('required', widget, data) and 'required' or None
    ta_attrs = {
        'autofocus': autofocus,
        'class_': cssclasses(widget, data),
        'cols': attr_value('cols', widget, data),
        'disabled': disabled,
        'id': cssid(widget, 'input'),
        'title': attr_value('title', widget, data),
        'name_': widget.dottedpath,
        'placeholder': attr_value('placeholder', widget, data),
        'readonly': readonly,
        'required': required,
        'rows': attr_value('rows', widget, data),
        'wrap': attr_value('wrap', widget, data),
    }
    ta_attrs.update(as_data_attrs(attr_value('data', widget, data)))
    return ta_attrs


textarea_managed_props = [
    'data', 'title', 'autofocus', 'cols', 'disabled',
    'placeholder', 'readonly', 'required', 'rows', 'wrap',
] + css_managed_props


@managedprops(*textarea_managed_props)
def textarea_renderer(widget, data, custom_attrs={}):
    """Renders text area.
    """
    tag = data.tag
    area_attrs = textarea_attributes(widget, data)
    area_attrs.update(custom_attrs)
    value = fetch_value(widget, data)
    if value is None:
        value = ''
    return tag('textarea', value, **area_attrs)


factory.register(
    'textarea',
    extractors=[
        generic_extractor,
        generic_required_extractor,
        generic_emptyvalue_extractor
    ],
    edit_renderers=[textarea_renderer],
    display_renderers=[
        generic_display_renderer,
        display_proxy_renderer
    ]
)

factory.doc['blueprint']['textarea'] = """\
HTML textarea blueprint.
"""

factory.defaults['textarea.default'] = ''

factory.defaults['textarea.wrap'] = None
factory.doc['props']['textarea.wrap'] = """\
Either ``soft``, ``hard``, ``virtual``, ``physical`` or  ``off``.
"""

factory.defaults['textarea.class'] = 'textarea'

factory.defaults['textarea.cols'] = 80
factory.doc['props']['textarea.cols'] = """\
Number of characters.
"""

factory.defaults['textarea.rows'] = 25
factory.doc['props']['textarea.rows'] = """\
Number of lines.
"""

factory.defaults['textarea.readonly'] = None
factory.doc['props']['textarea.readonly'] = """\
Flag textarea is readonly.
"""

factory.defaults['textarea.persist'] = True
