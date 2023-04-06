# -*- coding: utf-8 -*-
from node.utils import UNSET
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.common import generic_extractor
from yafowil.common import generic_required_extractor
from yafowil.common import input_attributes_common
from yafowil.datatypes import generic_emptyvalue_extractor
from yafowil.tsf import _
from yafowil.utils import attr_value
from yafowil.utils import css_managed_props
from yafowil.utils import managedprops
import re


###############################################################################
# password
###############################################################################

@managedprops('minlength')
def minlength_extractor(widget, data):
    """Validate minlength of a string input.

    Only perform if ``minlength`` property is set.

    Properties:

    ``minlength``
        Minimum length of string as int.
    """
    val = data.extracted
    if val is UNSET:
        return val
    minlength = attr_value('minlength', widget, data, -1)
    if minlength != -1:
        if len(val) < minlength:
            raise ExtractionError(_(
                'minlength_extraction_error',
                default=u'Input must have at least ${len} characters.',
                mapping={'len': minlength}
            ))
    return val


@managedprops('ascii')
def ascii_extractor(widget, data):
    """Validate if a string is ASCII encoding.

    Only perform if ``ascii`` property evaludates to True.

    Properties:

    ``ascii``
        Flag  ascii check should perform.
    """
    val = data.extracted
    if val is UNSET:
        return val
    if not attr_value('ascii', widget, data, False):
        return val
    try:
        val.encode('ascii')
    except UnicodeEncodeError:
        raise ExtractionError(_(
            u'ascii_extractor_error',
            default=u'Input contains illegal characters.'
        ))
    return val


LOWER_CASE_RE = r'(?=.*[a-z])'
UPPER_CASE_RE = r'(?=.*[A-Z])'
DIGIT_RE = r'(?=.*[\d])'
SPECIAL_CHAR_RE = r'(?=.*[\W])'
RE_PASSWORD_ALL = [
    LOWER_CASE_RE,
    UPPER_CASE_RE,
    DIGIT_RE,
    SPECIAL_CHAR_RE]
PASSWORD_NOCHANGE_VALUE = '_NOCHANGE_'


@managedprops('strength', 'weak_password_message')
def password_extractor(widget, data):
    """Extract and validate password input.

    If extracted password is unchanged, return ``UNSET``. Consider this when
    reading from password widgets!

    This extractor provides a strength check. It only performs if ``strenght``
    property is set. Strength check is done by four rules:
        - input contains lowercase character
        - input contains uppercase character
        - input contains digit
        - input contains special character.

    Properties:

    ``strength``
        Integer value <= 4. Define how many rules must apply to consider a
        password valid.
    """
    val = data.extracted
    if val == PASSWORD_NOCHANGE_VALUE:
        return UNSET
    if val is UNSET:
        return val
    required_strength = attr_value('strength', widget, data, 0)
    if required_strength <= 0:
        return val
    if required_strength > len(RE_PASSWORD_ALL):
        required_strength = len(RE_PASSWORD_ALL)
    strength = 0
    for reg_exp in RE_PASSWORD_ALL:
        if re.match(reg_exp, val):
            strength += 1
    if strength < required_strength:
        error = attr_value('weak_password_message', widget, data)
        raise ExtractionError(error)
    return val


def _pwd_value(widget, data):
    if data.extracted is not UNSET:
        return data.extracted
    if data.value is not UNSET \
       and data.value is not None:
        return PASSWORD_NOCHANGE_VALUE
    return attr_value('default', widget, data)


@managedprops(
    'data',
    'title',
    'size',
    'disabled',
    'autofocus',
    'placeholder',
    'autocomplete',
    *css_managed_props)
def password_edit_renderer(widget, data):
    """Render password widget.
    """
    tag = data.tag
    input_attrs = input_attributes_common(widget, data)
    input_attrs['type'] = 'password'
    input_attrs['value'] = _pwd_value(widget, data)
    return tag('input', **input_attrs)


@managedprops('displayplaceholder')
def password_display_renderer(widget, data):
    value = _pwd_value(widget, data)
    if value == PASSWORD_NOCHANGE_VALUE:
        return attr_value('displayplaceholder', widget, data)
    return u''


factory.register(
    'password',
    extractors=[
        generic_extractor,
        generic_required_extractor,
        generic_emptyvalue_extractor,
        minlength_extractor,
        ascii_extractor,
        password_extractor
    ],
    edit_renderers=[password_edit_renderer],
    display_renderers=[password_display_renderer]
)

factory.doc['blueprint']['password'] = """\
Password blueprint.

The password is never rendered to markup, instead
``yafowil.common.PASSWORD_NOCHANGE_VALUE`` is set as ``value`` property on
dom element. See ``yafowil.common.password_extractor`` for details on
password extraction.
"""

factory.defaults['password.required_class'] = 'required'

factory.defaults['password.default'] = ''

factory.defaults['password.class'] = 'password'

factory.defaults['password.minlength'] = -1
factory.doc['props']['password.size'] = """\
Maximum length of password.
"""

factory.doc['props']['password.minlength'] = """\
Minimum length of password.
"""

factory.defaults['password.ascii'] = False
factory.doc['props']['password.ascii'] = """\
Flag ascii check should performed.
"""

factory.defaults['password.strength'] = -1
factory.doc['props']['password.strength'] = """\
Integer value <= 4. Define how many rules must apply to consider a password
valid.
"""

factory.defaults['weak_password_message'] = _('weak_password_message',
                                              default=u'Password too weak')
factory.doc['props']['password.weak_password_message'] = """\
Message shown if password is not strong enough.
"""

factory.defaults['password.displayplaceholder'] = u'*' * 8
factory.doc['props']['password.displayplaceholder'] = """\
Placeholder shown in display mode if password was set.
"""

factory.defaults['password.persist'] = True