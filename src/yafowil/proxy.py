# -*- coding: utf-8 -*-
from node.utils import UNSET
from yafowil.base import factory
from yafowil.common import empty_display_renderer
from yafowil.common import generic_extractor
from yafowil.datatypes import generic_datatype_extractor
from yafowil.datatypes import generic_emptyvalue_extractor
from yafowil.utils import css_managed_props
from yafowil.utils import cssclasses
from yafowil.utils import cssid
from yafowil.utils import managedprops


###############################################################################
# proxy
###############################################################################

@managedprops(*css_managed_props)
def input_proxy_renderer(widget, data):
    """Render hidden input ignoring ``widget.dottedpath``, just using widget
    name.
    """
    tag = data.tag
    value = data.value
    if data.request is not UNSET and data.request.get(widget.__name__):
        value = data.request.get(widget.__name__)
    input_attrs = {
        'type': 'hidden',
        'value': value,
        'name_': widget.__name__,
        'id': cssid(widget, 'input'),
        'class_': cssclasses(widget, data),
    }
    return tag('input', **input_attrs)


factory.register(
    'proxy',
    extractors=[
        generic_extractor,
        generic_emptyvalue_extractor,
        generic_datatype_extractor
    ],
    edit_renderers=[input_proxy_renderer],
    display_renderers=[empty_display_renderer]
)

factory.doc['blueprint']['proxy'] = """\
Bypass arguments out of form namespace using a hidden field.
"""

factory.defaults['proxy.class'] = None
