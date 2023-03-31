# -*- coding: utf-8 -*-
from yafowil.base import factory
from yafowil.common import display_proxy_renderer
from yafowil.common import generic_display_renderer
from yafowil.common import generic_extractor
from yafowil.common import generic_required_extractor
from yafowil.common import input_generic_renderer
from yafowil.datatypes import generic_emptyvalue_extractor


###############################################################################
# search
###############################################################################

factory.register(
    'search',
    extractors=[
        generic_extractor,
        generic_required_extractor,
        generic_emptyvalue_extractor,
    ],
    edit_renderers=[input_generic_renderer],
    display_renderers=[
        generic_display_renderer,
        display_proxy_renderer
    ]
)

factory.doc['blueprint']['search'] = """\
Search blueprint (HTML5).
"""

factory.defaults['search.type'] = 'search'

factory.defaults['search.default'] = ''

factory.defaults['search.required_class'] = 'required'

factory.defaults['search.class'] = 'search'
