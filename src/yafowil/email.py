# -*- coding: utf-8 -*-
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.common import display_proxy_renderer
from yafowil.common import generic_display_renderer
from yafowil.common import generic_extractor
from yafowil.common import generic_required_extractor
from yafowil.common import input_generic_renderer
from yafowil.compat import BYTES_TYPE
from yafowil.compat import UNICODE_TYPE
from yafowil.datatypes import generic_datatype_extractor
from yafowil.datatypes import generic_emptyvalue_extractor
from yafowil.tsf import _
import re


###############################################################################
# email
###############################################################################

EMAIL_RE = r'^[a-zA-Z0-9\._\-]+@[a-zA-Z0-9\._\-]+.[a-zA-Z0-9]{2,6}$'


def email_extractor(widget, data):
    val = data.extracted
    if not val:
        return val
    email_re = EMAIL_RE \
        if isinstance(val, UNICODE_TYPE) \
        else EMAIL_RE.encode()
    if not re.match(email_re, val):
        raise ExtractionError(_(
            'email_address_not_valid',
            default=u'Input not a valid email address.'
        ))
    return val


factory.register(
    'email',
    extractors=[
        generic_extractor,
        generic_required_extractor,
        generic_emptyvalue_extractor,
        generic_datatype_extractor,
        email_extractor
    ],
    edit_renderers=[input_generic_renderer],
    display_renderers=[
        generic_display_renderer,
        display_proxy_renderer
    ]
)

factory.doc['blueprint']['email'] = """\
Email (HTML5) input blueprint.
"""

factory.defaults['email.type'] = 'email'

factory.defaults['email.default'] = ''

factory.defaults['email.required_class'] = 'required'

factory.defaults['email.class'] = 'email'

factory.defaults['email.persist'] = True

factory.defaults['email.allowed_datatypes'] = [
    BYTES_TYPE, UNICODE_TYPE,
]
