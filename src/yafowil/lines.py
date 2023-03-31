# -*- coding: utf-8 -*-
from yafowil.base import factory
from yafowil.base import fetch_value
from yafowil.common import display_proxy_renderer
from yafowil.common import generic_extractor
from yafowil.common import generic_required_extractor
from yafowil.compat import ITER_TYPES
from yafowil.datatypes import generic_datatype_extractor
from yafowil.datatypes import generic_emptyvalue_extractor
from yafowil.textarea import textarea_attributes
from yafowil.textarea import textarea_managed_props
from yafowil.tsf import _
from yafowil.utils import as_data_attrs
from yafowil.utils import attr_value
from yafowil.utils import cssid
from yafowil.utils import managedprops


###############################################################################
# lines
###############################################################################

def lines_extractor(widget, data):
    """Extract textarea value as list of lines.
    """
    extracted = data.extracted
    if not extracted:
        return list()
    return extracted.split('\n')


@managedprops(*textarea_managed_props)
def lines_edit_renderer(widget, data):
    """Renders text area with list value as lines.
    """
    tag = data.tag
    area_attrs = textarea_attributes(widget, data)
    value = fetch_value(widget, data)
    if value is None:
        value = u''
    else:
        value = u'\n'.join(value)
    return tag('textarea', value, **area_attrs)


@managedprops('class', 'data')
def lines_display_renderer(widget, data):
    value = fetch_value(widget, data)
    if type(value) in ITER_TYPES and not value:
        value = u''
    attrs = {
        'id': cssid(widget, 'display'),
        'class_': 'display-{0}'.format(attr_value('class', widget, data))
    }
    attrs.update(as_data_attrs(attr_value('data', widget, data)))
    content = u''
    for line in value:
        content += data.tag('li', line)
    return data.tag('ul', content, **attrs)


factory.register(
    'lines',
    extractors=[
        generic_extractor,
        generic_required_extractor,
        lines_extractor,
        generic_emptyvalue_extractor,
        generic_datatype_extractor,
    ],
    edit_renderers=[lines_edit_renderer],
    display_renderers=[
        lines_display_renderer,
        display_proxy_renderer
    ]
)

factory.doc['blueprint']['lines'] = """\
Lines blueprint. Renders a textarea and extracts lines as list.
"""

factory.defaults['lines.default'] = ''

factory.defaults['lines.class'] = 'lines'

factory.defaults['lines.wrap'] = None
factory.doc['props']['lines.wrap'] = """\
Either ``soft``, ``hard``, ``virtual``, ``physical`` or  ``off``.
"""

factory.defaults['lines.cols'] = 40
factory.doc['props']['lines.cols'] = """\
Number of characters.
"""

factory.defaults['lines.rows'] = 8
factory.doc['props']['lines.rows'] = """\
Number of lines.
"""

factory.defaults['lines.readonly'] = None
factory.doc['props']['lines.readonly'] = """\
Flag textarea is readonly.
"""

factory.defaults['lines.persist'] = True
