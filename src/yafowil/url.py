# -*- coding: utf-8 -*-
from node.utils import UNSET
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.common import display_proxy_renderer
from yafowil.common import generic_display_renderer
from yafowil.common import generic_extractor
from yafowil.common import generic_required_extractor
from yafowil.common import input_generic_renderer
from yafowil.datatypes import generic_emptyvalue_extractor
from yafowil.tsf import _
import re


###############################################################################
# url
###############################################################################

URL_RE = r'^(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:'
URL_RE += r'.?+=&%@!\-\/]))?$'


def url_extractor(widget, data):
    val = data.extracted
    if not val:
        return val
    if not re.match(URL_RE, val is not UNSET and val or ''):
        message = _('web_address_not_valid',
                    default=u'Input not a valid web address.')
        raise ExtractionError(message)
    return val


factory.register(
    'url',
    extractors=[
        generic_extractor,
        generic_required_extractor,
        generic_emptyvalue_extractor,
        url_extractor
    ],
    edit_renderers=[input_generic_renderer],
    display_renderers=[
        generic_display_renderer,
        display_proxy_renderer
    ]
)

factory.doc['blueprint']['url'] = """\
URL aka web address (HTML5) input blueprint.
"""

factory.defaults['url.type'] = 'url'

factory.defaults['url.default'] = ''

factory.defaults['url.required_class'] = 'required'

factory.defaults['url.class'] = 'url'

factory.defaults['url.persist'] = True
