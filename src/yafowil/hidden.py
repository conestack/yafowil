# -*- coding: utf-8 -*-
from yafowil.base import factory
from yafowil.common import empty_display_renderer
from yafowil.common import generic_extractor
from yafowil.common import input_generic_renderer
from yafowil.datatypes import generic_datatype_extractor
from yafowil.datatypes import generic_emptyvalue_extractor


###############################################################################
# hidden
###############################################################################

factory.register(
    'hidden',
    extractors=[
        generic_extractor,
        generic_emptyvalue_extractor,
        generic_datatype_extractor
    ],
    edit_renderers=[input_generic_renderer],
    display_renderers=[empty_display_renderer]
)

factory.doc['blueprint']['hidden'] = """\
Hidden input blueprint.
"""

factory.defaults['hidden.type'] = 'hidden'
factory.doc['props']['hidden.type'] = """\
Type of input tag.
"""

factory.defaults['hidden.default'] = ''

factory.defaults['hidden.class'] = 'hidden'

factory.defaults['hidden.persist'] = True
