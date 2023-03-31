# -*- coding: utf-8 -*-
from yafowil.base import factory
from yafowil.common import display_proxy_renderer
from yafowil.common import generic_display_renderer
from yafowil.common import generic_extractor
from yafowil.common import generic_required_extractor
from yafowil.common import input_generic_renderer
from yafowil.datatypes import generic_datatype_extractor
from yafowil.datatypes import generic_emptyvalue_extractor
from yafowil.utils import css_managed_props
from yafowil.utils import managedprops


###############################################################################
# text
###############################################################################

@managedprops(
    'data',
    'title',
    'size',
    'disabled',
    'autofocus',
    'placeholder',
    'autocomplete',
    *css_managed_props)
def text_edit_renderer(widget, data):
    return input_generic_renderer(widget, data)


factory.register(
    'text',
    extractors=[
        generic_extractor,
        generic_required_extractor,
        generic_emptyvalue_extractor,
        generic_datatype_extractor,
    ],
    edit_renderers=[text_edit_renderer],
    display_renderers=[
        generic_display_renderer,
        display_proxy_renderer
    ]
)

factory.doc['blueprint']['text'] = """\
One line text input blueprint.
"""

factory.defaults['text.type'] = 'text'
factory.doc['props']['text.type'] = """\
Type of input tag.
"""

factory.defaults['text.required_class'] = 'required'

factory.defaults['text.default'] = ''

factory.defaults['text.class'] = 'text'

factory.defaults['text.disabled'] = False
factory.doc['props']['text.disabled'] = """\
Flag  input field is disabled.
"""

factory.defaults['text.persist'] = True
