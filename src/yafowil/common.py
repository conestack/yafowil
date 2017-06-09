# -*- coding: utf-8 -*-
from node.utils import UNSET
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.base import fetch_value
from yafowil.tsf import _
from yafowil.utils import EMPTY_VALUE
from yafowil.utils import attr_value
from yafowil.utils import convert_value_to_datatype
from yafowil.utils import convert_values_to_datatype
from yafowil.utils import css_managed_props
from yafowil.utils import cssclasses
from yafowil.utils import cssid
from yafowil.utils import generic_html5_attrs
from yafowil.utils import managedprops
from yafowil.utils import vocabulary
import re
import types
import uuid


###############################################################################
# common defaults
###############################################################################

factory.defaults['default'] = UNSET
factory.doc['props']['default'] = """\
Default value for rendering.
"""

factory.defaults['class'] = None
factory.doc['props']['class'] = """\
Common CSS-class to put on.
"""

factory.defaults['class_add'] = None
factory.doc['props']['class_add'] = """\
Additional CSS-class to put on.
"""

factory.defaults['error_class'] = None
factory.doc['props']['error_class'] = """\
CSS-class to put on in case of error.
"""

factory.defaults['error_class_default'] = 'error'
factory.doc['props']['error_class_default'] = """\
Fallback CSS-class to put on in case of error if no specific class was
given.
"""

factory.defaults['autofocus'] = None
factory.doc['props']['autofocus'] = """\
Whether this field gets the focus automatically or not (if browser supports
it).
"""

factory.defaults['autocomplete'] = None
factory.doc['props']['autocomplete'] = """\
Switch autocomplete explizit to ``on`` or ``off``.
"""

factory.defaults['placeholder'] = None
factory.doc['props']['placeholder'] = """\
Whether this input has a placeholder value or not (if browser supports it).
"""

factory.doc['props']['emptyvalue'] = """\
If configured and received value in request is empty, return as extracted
value.
"""

factory.defaults['datatype'] = None
factory.doc['props']['datatype'] = """\
Callable for converting extracted value to output datatype.

``datatype`` can also be defined as string with value out of ``'str'``,
``'unicode'``, ``'int'``, ``'integer'``, ``'long'``, ``'float'`` or
``'uuid'``.

Custom converter callables must raise one out of the following exceptions if
conversion fails:
    * ``ValueError``
    * ``UnicodeDecodeError``
    * ``UnicodeEncodeError``
"""

factory.defaults['allowed_datatypes'] = UNSET
factory.doc['props']['allowed_datatypes'] = """\
List of allowed datatypes. If ``UNSET``, datatype converters are not
restricted.
"""

factory.defaults['datatype_message'] = None
factory.doc['props']['datatype_message'] = """\
Custom extraction error message if ``datatype`` conversion fails.
"""

factory.defaults['required'] = False
factory.doc['props']['required'] = """\
Whether this value is required or not.
"""

factory.defaults['required_message'] = _(
    'required_message', default=u'Mandatory field was empty')
factory.doc['props']['required_message'] = """\
Message to be shown if required condition was not met.
"""

factory.defaults['required_class'] = None
factory.doc['props']['required_class'] = """\
CSS-class to put on in case if required condition was not met.
"""

factory.defaults['type'] = None
factory.doc['props']['type'] = """\
HTML type attribute.
"""

factory.defaults['size'] = None
factory.doc['props']['size'] = """\
Allowed input size.
"""

factory.defaults['maxlength'] = None
factory.doc['props']['maxlength'] = """\
Input maxlength.
"""

factory.defaults['disabled'] = None
factory.doc['props']['disabled'] = """\
Disables input.
"""

factory.defaults['required_class_default'] = 'required'
factory.doc['props']['required_class_default'] = """\
CSS-class to apply if required condition was not met - if no specific class
was given.
"""

factory.defaults['template'] = '%s'
factory.doc['props']['template'] = """\
Format string with pythons built-in string format template. If a callable
is given it will be used instead and is called with ``widget`` and ``data`` as
parameters.
"""

factory.defaults['title'] = None
factory.doc['props']['title'] = """\
Optional help text to be rendered in the title attribute.
"""

factory.defaults['data'] = dict()
factory.doc['props']['data'] = """\
Additional data rendered as HTML5 data attributes on DOM Element.
"""

factory.defaults['display_proxy'] = False
factory.doc['props']['display_proxy'] = """\
If 'True' and widget mode 'display', widget value gets rendered as hidden
input.
"""


###############################################################################
# generic
###############################################################################

def generic_extractor(widget, data):
    """Extract raw value from request by ``widget.dottedpath``.

    Return ``UNSET`` if widget not present in request.
    """
    __managed_props = []  # noqa
    try:
        return data.request[widget.dottedpath]
    except KeyError:
        return UNSET


@managedprops('required', 'required_message')
def generic_required_extractor(widget, data):
    """Validate required.

    If ``required`` is set and some raw value has been extracted,
    evaluate ``data.extracted`` to boolean. Raise ``ExtractionError`` if
    ``False``.
    """
    required = attr_value('required', widget, data)
    if not required or bool(data.extracted) or data.extracted is UNSET:
        return data.extracted
    if isinstance(required, basestring):
        raise ExtractionError(required)
    raise ExtractionError(attr_value('required_message', widget, data))


@managedprops('emptyvalue')
def generic_emptyvalue_extractor(widget, data):
    """Return emptyvalue if widget present in request and raw value is empty.
    """
    try:
        if not data.request[widget.dottedpath]:
            return attr_value('emptyvalue', widget, data, data.extracted)
    except KeyError:
        pass
    return data.extracted


DATATYPE_LABELS = {
    str: _('datatype_str', default='string'),
    unicode: _('datatype_unicode', default='unicode'),
    int: _('datatype_integer', default='integer'),
    long: _('datatype_long', default='long integer'),
    float: _('datatype_float', default='floating point number'),
    uuid.UUID: _('datatype_uuid', default='UUID')
}
# B/C
DATATYPE_LABELS['str'] = DATATYPE_LABELS[str]
DATATYPE_LABELS['unicode'] = DATATYPE_LABELS[unicode]
DATATYPE_LABELS['int'] = DATATYPE_LABELS[int]
DATATYPE_LABELS['integer'] = DATATYPE_LABELS[int]
DATATYPE_LABELS['long'] = DATATYPE_LABELS[long]
DATATYPE_LABELS['float'] = DATATYPE_LABELS[float]
DATATYPE_LABELS['uuid'] = DATATYPE_LABELS[uuid.UUID]


@managedprops('datatype', 'allowed_datatypes',
              'datatype_message', 'emptyvalue')
def generic_datatype_extractor(widget, data):
    """Convert extracted value to ``datatype``.

    If extracted value is ``UNSET`` return ``UNSET``.
    If no ``datatype`` given, return extracted value.
    Otherwise try to convert value to given ``datatype`` and return the
    converted value or raise an ``ExtractionError`` if conversion fails.
    Extraction error message can be customized with ``datatype_message``
    property. Value can also be a list, then all items inside the list are
    converted.
    """
    extracted = data.extracted
    if extracted is UNSET:
        return extracted
    datatype = attr_value('datatype', widget, data)
    if not datatype:
        return extracted
    allowed_datatypes = attr_value('allowed_datatypes', widget, data)
    if allowed_datatypes and datatype not in allowed_datatypes:
        raise ValueError('Datatype not allowed: "{0}"'.format(datatype))
    try:
        emptyvalue = attr_value('emptyvalue', widget, data, EMPTY_VALUE)
        return convert_values_to_datatype(
            extracted,
            datatype,
            empty_value=emptyvalue
        )
    except KeyError:
        raise ValueError('Datatype unknown: "{0}"'.format(datatype))
    except (ValueError, UnicodeEncodeError, UnicodeDecodeError):
        datatype_message = attr_value('datatype_message', widget, data)
        if not datatype_message:
            datatype_label = DATATYPE_LABELS.get(datatype)
            if not datatype_label:
                datatype_message = _(
                    'generic_datatype_message',
                    default=u'Input conversion failed.'
                )
            else:
                datatype_message = _(
                    'standard_datatype_message',
                    default=u'Input is not a valid ${datatype}.',
                    mapping={
                        'datatype': datatype_label
                    }
                )
        raise ExtractionError(datatype_message)


def input_attributes_common(widget, data, excludes=list(), value=None):
    if value is None:
        value = fetch_value(widget, data)
    if isinstance(value, basestring):
        value = value.replace('"', '&quot;')
    autofocus = attr_value('autofocus', widget, data) and 'autofocus' or None
    disabled = attr_value('disabled', widget, data)
    disabled = bool(disabled) and 'disabled' or None
    required = attr_value('required', widget, data) and 'required' or None
    input_attrs = {
        'autofocus': autofocus,
        'class_': cssclasses(widget, data),
        'disabled': disabled,
        'id': cssid(widget, 'input'),
        'name_': widget.dottedpath,
        'placeholder': attr_value('placeholder', widget, data),
        'required': required,
        'size': attr_value('size', widget, data),
        'maxlength': attr_value('maxlength', widget, data),
        'title': attr_value('title', widget, data),
        'type': attr_value('type', widget, data),
        'value': value,
    }
    input_attrs.update(generic_html5_attrs(attr_value('data', widget, data)))
    for attr_name in excludes:
        del input_attrs[attr_name]
    return input_attrs


def input_attributes_full(widget, data, value=None):
    input_attrs = input_attributes_common(widget, data, value=value)
    input_attrs['autocomplete'] = attr_value(
        'autocomplete', widget, data)
    if attr_value('type', widget, data) in ['range', 'number']:
        input_attrs['min'] = attr_value('min', widget, data)
        input_attrs['max'] = attr_value('max', widget, data)
        input_attrs['step'] = attr_value('step', widget, data)
    return input_attrs


@managedprops(*css_managed_props)
def input_generic_renderer(widget, data, custom_attrs={}):
    """Generic HTML ``input`` tag render.
    """
    input_attrs = input_attributes_full(widget, data)
    input_attrs.update(custom_attrs)
    return data.tag('input', **input_attrs)


# multivalued is not documented, because its only valid for specific blueprints
@managedprops('display_proxy')
def display_proxy_renderer(widget, data):
    rendered = data.rendered
    if attr_value('display_proxy', widget, data):
        orgin_type = attr_value('type', widget, data)
        widget.attrs['type'] = 'hidden'
        value = fetch_value(widget, data)
        multivalued = attr_value('multivalued', widget, data)
        if multivalued and isinstance(value, basestring):
            value = [value]
        if multivalued or type(value) in [types.ListType, types.TupleType]:
            for val in value:
                input_attrs = input_attributes_full(widget, data, value=val)
                rendered += data.tag('input', **input_attrs)
        else:
            rendered += input_generic_renderer(widget, data)
        if orgin_type:
            widget.attrs['type'] = orgin_type
        else:
            del widget.attrs['type']
    return rendered


@managedprops('template', 'class')
def generic_display_renderer(widget, data, value=None):
    """Generic display renderer to render a value.
    """
    if callable(widget.attrs['template']):
        content = widget.attrs['template'](widget, data)
    elif value is None:
        value = fetch_value(widget, data)
        if value in [UNSET, None]:
            value = u''
        content = widget.attrs['template'] % value
    else:
        content = widget.attrs['template'] % value
    attrs = {
        'id': cssid(widget, 'display'),
        'class_': 'display-{0}'.format(
            attr_value('class', widget, data) or 'generic'
        )
    }
    attrs.update(generic_html5_attrs(attr_value('data', widget, data)))
    return data.tag('div', content, **attrs)


def empty_display_renderer(widget, data):
    """Display renderer which renders an empty string.
    """
    return data.rendered or u''


def generic_positional_rendering_helper(tagname, message, attrs, rendered, pos,
                                        tag):
    """returns new tag with rendered content dependent on position

    tagname
        name of new tag, ie. div, p, label and so on

    message
        text included in new tag

    attrs
        attributes on new tag

    rendered
        prior rendered text

    pos
        position how to place the newtag relative to the prior rendered:
        'before'='<newtag>message</newtag>rendered',
        'after' ='<newtag>message</newtag>'
        'inner-before'= <newtag>message rendered</newtag>
        'inner-after'= <newtag>rendered message</newtag>
    """
    if pos not in ['before', 'after', 'inner-before', 'inner-after']:
        raise ValueError('Invalid value for position "{0}"'.format(pos))
    if pos.startswith('inner'):
        if pos.endswith('before'):
            inner = message, rendered
        else:
            inner = rendered, message
        return tag(tagname, *inner, **attrs)
    else:
        newtag = tag(tagname, message, **attrs)
        if pos == 'before':
            return newtag + rendered
        return rendered + newtag


###############################################################################
# tag
###############################################################################

@managedprops('tag', 'text', 'data', *css_managed_props)
def tag_renderer(widget, data):
    """Renderer for HTML tags.
    """
    attrs = {
        'id': cssid(widget, 'tag'),
        'class_': cssclasses(widget, data),
    }
    attrs.update(generic_html5_attrs(attr_value('data', widget, data)))
    tag = attr_value('tag', widget, data)
    text = attr_value('text', widget, data)
    return data.tag(tag, text, **attrs)


factory.register(
    'tag',
    edit_renderers=[tag_renderer],
    display_renderers=[tag_renderer])

factory.doc['blueprint']['tag'] = """\
Render HTML tags with text. Useful for rendering headings etc.
"""

factory.doc['props']['tag.tag'] = """\
HTML tag name.
"""

factory.doc['props']['tag.text'] = """\
Tag contents.
"""


###############################################################################
# text
###############################################################################

@managedprops('data', 'title', 'size', 'disabled', 'autofocus',
              'placeholder', 'autocomplete', *css_managed_props)
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
    ])

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
    display_renderers=[empty_display_renderer])

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
    display_renderers=[empty_display_renderer])

factory.doc['blueprint']['proxy'] = """\
Bypass arguments out of form namespace using a hidden field.
"""

factory.defaults['proxy.class'] = None

factory.defaults['proxy.persist'] = True


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
    ta_attrs.update(generic_html5_attrs(attr_value('data', widget, data)))
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
    ])

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
    if type(value) in [types.ListType, types.TupleType] and not value:
        value = u''
    attrs = {
        'id': cssid(widget, 'display'),
        'class_': 'display-{0}'.format(attr_value('class', widget, data))
    }
    attrs.update(generic_html5_attrs(attr_value('data', widget, data)))
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
    ])

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
            message = _('minlength_extraction_error',
                        default=u'Input must have at least ${len} characters.',
                        mapping={'len': minlength})
            raise ExtractionError(message)
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
        str(val)
    except UnicodeEncodeError:
        message = _(u'ascii_extractor_error',
                    default=u'Input contains illegal characters.')
        raise ExtractionError(message)
    return val


LOWER_CASE_RE = '(?=.*[a-z])'
UPPER_CASE_RE = '(?=.*[A-Z])'
DIGIT_RE = '(?=.*[\d])'
SPECIAL_CHAR_RE = '(?=.*[\W])'
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


@managedprops('data', 'title', 'size', 'disabled', 'autofocus',
              'placeholder', 'autocomplete', *css_managed_props)
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
    display_renderers=[password_display_renderer])

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


@managedprops('data', 'title', 'size', 'disabled', 'autofocus',
              'format', 'disabled', 'checked', *css_managed_props)
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
    with_label = attr_value('with_label', widget, data)
    if with_label:
        label = tag('label',
                    '&nbsp;',
                    for_=cssid(widget, 'input'),
                    class_='checkbox_label')
        checkbox = tag('input', **input_attrs) + label
    else:
        checkbox = tag('input', **input_attrs)
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
    display_renderers=[checkbox_display_renderer])

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


###############################################################################
# select
###############################################################################

@managedprops('multivalued', 'disabled')
def select_extractor(widget, data):
    extracted = generic_extractor(widget, data)
    multivalued = attr_value('multivalued', widget, data)
    exists_marker = '{0}-exists'.format(widget.dottedpath)
    if extracted is UNSET and exists_marker in data.request:
        if multivalued:
            extracted = []
        else:
            extracted = ''
    if extracted is UNSET:
        return extracted
    if multivalued and isinstance(extracted, basestring):
        extracted = [extracted]
    disabled = widget.attrs.get('disabled', False)
    if not disabled:
        return extracted
    if not multivalued:
        return data.value
    disabled_items = disabled is True and data.value or disabled
    if isinstance(disabled_items, basestring):
        disabled_items = [disabled_items]
    for item in disabled_items:
        if item in extracted and item not in data.value:
            extracted.remove(item)
        elif item not in extracted and item in data.value:
            extracted.append(item)
    return extracted


def select_exists_marker(widget, data):
    tag = data.tag
    attrs = {
        'type': 'hidden',
        'value': 'exists',
        'name_': "{0}-exists".format(widget.dottedpath),
        'id': cssid(widget, 'exists'),
    }
    return tag('input', **attrs)


def select_edit_renderer_props(widget, data):
    value = fetch_value(widget, data)
    multivalued = attr_value('multivalued', widget, data)
    if isinstance(value, basestring) or not hasattr(value, '__iter__'):
        value = [value]
    datatype = attr_value('datatype', widget, data)
    if datatype:
        value = convert_values_to_datatype(value, datatype)
    emptyvalue = attr_value('emptyvalue', widget, data, EMPTY_VALUE)
    if not multivalued and len(value) > 1:
        raise ValueError(u'Multiple values for single selection.')
    disabled = attr_value('disabled', widget, data, False)
    return value, multivalued, datatype, emptyvalue, disabled


def select_block_edit_renderer(widget, data, custom_attrs={}):
    value, multivalued, datatype, emptyvalue, disabled = \
        select_edit_renderer_props(widget, data)
    optiontags = []
    vocab = attr_value('vocabulary', widget, data, [])
    for key, term in vocabulary(vocab):
        vval = key
        if datatype:
            vval = convert_value_to_datatype(
                key,
                datatype,
                empty_value=emptyvalue
            )
        key = '' if key in [None, UNSET] else key
        attrs = {
            'selected': 'selected' if vval in value else None,
            'value': key,
            'id': cssid(widget, 'input', key),
        }
        if disabled and disabled is not True and vval in disabled:
            attrs['disabled'] = 'disabled'
        optiontags.append(data.tag('option', term, **attrs))
    autofocus = \
        attr_value('autofocus', widget, data) and 'autofocus' or None
    required = attr_value('required', widget, data) and 'required' or None
    block_class = attr_value('block_class', widget, data)
    select_attrs = {
        'name_': widget.dottedpath,
        'id': cssid(widget, 'input'),
        'title': attr_value('title', widget, data) or None,
        'class_': cssclasses(widget, data, additional=[block_class]),
        'multiple': multivalued and 'multiple' or None,
        'size': attr_value('size', widget, data) or None,
        'placeholder': attr_value('placeholder', widget, data) or None,
        'autofocus': autofocus,
        'required': required,
    }
    select_attrs.update(
        generic_html5_attrs(
            attr_value('data', widget, data)))
    select_attrs.update(custom_attrs)
    if disabled is True:
        select_attrs['disabled'] = 'disabled'
    rendered = data.tag('select', *optiontags, **select_attrs)
    if multivalued:
        attrs = {
            'type': 'hidden',
            'value': 'exists',
            'name_': '{0}-exists'.format(widget.dottedpath),
            'id': cssid(widget, 'exists'),
        }
        rendered = select_exists_marker(widget, data) + rendered
    return rendered


def select_cb_edit_renderer(widget, data, custom_attrs={}):
    value, multivalued, datatype, emptyvalue, disabled = \
        select_edit_renderer_props(widget, data)
    tags = []
    label_pos = attr_value('listing_label_position', widget, data)
    if label_pos == 'inner':
        # deprecated, use explicit inner-after or inner-before
        label_pos = 'inner-after'
    listing_tag = attr_value('listing_tag', widget, data)
    item_tag = listing_tag == 'div' and 'div' or 'li'
    if multivalued:
        tagtype = 'checkbox'
        wrapper_class = attr_value('checkbox_wrapper_class', widget, data)
        label_class = attr_value('checkbox_label_class', widget, data)
        # B/C deprecated as of yafowil 2.2
        if not label_class:
            label_class = attr_value('label_checkbox_class', widget, data)
    else:
        tagtype = 'radio'
        wrapper_class = attr_value('radio_wrapper_class', widget, data)
        label_class = attr_value('radio_label_class', widget, data)
        # B/C deprecated as of yafowil 2.2
        if not label_class:
            label_class = attr_value('label_radio_class', widget, data)
    vocab = attr_value('vocabulary', widget, data, [])
    for key, term in vocabulary(vocab):
        vval = key
        if datatype:
            vval = convert_value_to_datatype(
                key,
                datatype,
                empty_value=emptyvalue
            )
        key = '' if key in [None, UNSET] else key
        input_attrs = {
            'type': tagtype,
            'value': key,
            'checked': 'checked' if vval in value else None,
            'name_': widget.dottedpath,
            'id': cssid(widget, 'input', key),
            'class_': cssclasses(widget, data),
        }
        if (disabled and disabled is not True and vval in disabled) \
           or disabled is True:
            input_attrs['disabled'] = 'disabled'
        inputtag = data.tag('input', **input_attrs)
        label_attrs = dict(for_=input_attrs['id'], _class=label_class)
        item = generic_positional_rendering_helper(
            'label', term, label_attrs, inputtag, label_pos, data.tag)
        item_wrapper = data.tag(item_tag, item, **{
            'id': cssid(widget, tagtype, key),
            'class': wrapper_class,
        })
        tags.append(item_wrapper)
    wrapper_attrs = {'id': cssid(widget, tagtype, 'wrapper')}
    wrapper_attrs.update(
        generic_html5_attrs(
            attr_value('data', widget, data)))
    wrapper_attrs.update(custom_attrs)
    taglisting = data.tag(listing_tag, *tags, **wrapper_attrs)
    return select_exists_marker(widget, data) + taglisting


@managedprops('data', 'title', 'format', 'vocabulary', 'multivalued',
              'disabled', 'listing_label_position', 'listing_tag', 'size',
              'label_checkbox_class', 'label_radio_class', 'block_class',
              'autofocus', 'placeholder', 'datatype', 'emptyvalue',
              *css_managed_props)
def select_edit_renderer(widget, data, custom_attrs={}):
    if attr_value('format', widget, data) == 'block':
        return select_block_edit_renderer(
            widget,
            data,
            custom_attrs=custom_attrs
        )
    return select_cb_edit_renderer(widget, data, custom_attrs=custom_attrs)


@managedprops('data', 'template', 'class', 'multivalued')
def select_display_renderer(widget, data):
    value = fetch_value(widget, data)
    if type(value) in [types.ListType, types.TupleType] and not value:
        value = u''
    multivalued = attr_value('multivalued', widget, data)
    vocab = dict(attr_value('vocabulary', widget, data, []))
    if not multivalued or not value:
        value = vocab.get(value, value)
        if data.tag.translate:
            value = data.tag.translate(value)
        return generic_display_renderer(widget, data, value=value)
    attrs = {
        'id': cssid(widget, 'display'),
        'class_': 'display-{0}'.format(attr_value('class', widget, data))
    }
    attrs.update(generic_html5_attrs(attr_value('data', widget, data)))
    content = u''
    if multivalued and isinstance(value, basestring):
        value = [value]
    for key in value:
        content += data.tag('li', vocab[key])
    return data.tag('ul', content, **attrs)


factory.register(
    'select',
    extractors=[
        select_extractor,
        generic_required_extractor,
        generic_emptyvalue_extractor,
        generic_datatype_extractor,
    ],
    edit_renderers=[select_edit_renderer],
    display_renderers=[
        select_display_renderer,
        display_proxy_renderer
    ])

factory.doc['blueprint']['select'] = """\
Selection Blueprint. Single selection as dropdown or radio-buttons. Multiple
selection as selection-list or as checkboxes.
"""

factory.defaults['select.multivalued'] = None
factory.doc['props']['select.multivalued'] = """\
Flag whether multiple items can be selected.
"""

factory.defaults['select.size'] = None
factory.doc['props']['select.size'] = """\
Size of input if multivalued and format 'block'.
"""

# maybe callable returning '' for single select and [] for multi select
factory.defaults['select.default'] = UNSET

factory.defaults['select.format'] = 'block'
factory.doc['props']['select.format'] = """\
Every value except 'block' results in either a list of radio buttons or
checkboxes depending on the 'multivalued' property.
"""

factory.defaults['select.class'] = 'select'

factory.defaults['select.block_class'] = None
factory.doc['props']['select.block_class'] = """\
CSS class to render on selection if block format.
"""

factory.defaults['select.checkbox_wrapper_class'] = None
factory.doc['props']['select.checkbox_wrapper_class'] = """\
CSS class to render on checkbox wrapper.
"""

factory.defaults['select.checkbox_label_class'] = None
factory.doc['props']['select.checkbox_label_class'] = """\
CSS class to render on checkbox labels.
"""

factory.defaults['select.label_checkbox_class'] = None
factory.doc['props']['select.label_checkbox_class'] = """\
CSS class to render on checkbox labels.

This property is deprecated and will be remove as of yafowil 2.2. Use
``checkbox_label_class`` instead.
"""

factory.defaults['select.radio_wrapper_class'] = None
factory.doc['props']['select.radio_wrapper_class'] = """\
CSS class to render on radio button wrapper.
"""

factory.defaults['select.radio_label_class'] = None
factory.doc['props']['select.radio_label_class'] = """\
CSS class to render on radio button labels.
"""

factory.defaults['select.label_radio_class'] = None
factory.doc['props']['select.label_radio_class'] = """\
CSS class to render on radio button labels.

This property is deprecated and will be remove as of yafowil 2.2. Use
``radio_label_class`` instead.
"""

factory.defaults['select.listing_tag'] = 'div'
factory.doc['props']['select.listing_tag'] = """\
Desired rendering tag for selection if selection format is 'single'. Valid
values are 'div' and 'ul'.
"""

factory.defaults['select.listing_label_position'] = 'inner-after'
factory.doc['props']['select.listing_label_position'] = """\
Label position if format is 'single'. Behaves the same way as label widget
position property.
"""

factory.doc['props']['select.vocabulary'] = """\
Vocabulary to be used for the selection list. Expects a dict-like or an
iterable or a callable which returns one of both first. An iterable can consist
out of strings or out of tuples with ``(key, value)``. The items in the result
list are in the same order like the vocabulary.
"""

factory.doc['props']['select.disabled'] = """\
Disables the whole widget or single selections. To disable the whole widget
set the value to 'True'. To disable single selection pass a iterable of keys to
disable, i.e. ``['foo', 'baz']``. Defaults to False.
"""

factory.defaults['select.persist'] = True


###############################################################################
# file
###############################################################################

def file_extractor(widget, data):
    """Return a dict with following keys:

    mimetype
        Mimetype of file.
    headers
        rfc822.Message instance.
    original
        Original file handle from underlying framework.
    file
        File descriptor containing the data.
    filename
        File name.
    action
        widget flags 'new', 'keep', 'replace', 'delete'
    """
    name = widget.dottedpath
    if name not in data.request:
        return UNSET
    if not '{0}-action'.format(name) in data.request:
        value = data.request[name]
        if value:
            value['action'] = 'new'
        return value
    value = data.value
    action = value['action'] = data.request.get(
        '{0}-action'.format(name),
        'keep'
    )
    if action == 'delete':
        value['file'] = UNSET
    elif action == 'replace':
        new_val = data.request[name]
        if new_val:
            value = new_val
            value['action'] = 'replace'
        else:
            value['action'] = 'keep'
    return value


@managedprops('accept', 'placeholder', 'autofocus',
              'required', *css_managed_props)
def input_file_edit_renderer(widget, data):
    tag = data.tag
    input_attrs = input_attributes_common(widget, data, excludes=['value'])
    input_attrs['type'] = 'file'
    if attr_value('accept', widget, data):
        input_attrs['accept'] = attr_value('accept', widget, data)
    return tag('input', **input_attrs)


def convert_bytes(value):
    value = float(value)
    if value >= 1099511627776:
        terabytes = value / 1099511627776
        size = '{0:.2f}T'.format(terabytes)
    elif value >= 1073741824:
        gigabytes = value / 1073741824
        size = '{0:.2f}G'.format(gigabytes)
    elif value >= 1048576:
        megabytes = value / 1048576
        size = '{0:.2f}M'.format(megabytes)
    elif value >= 1024:
        kilobytes = value / 1024
        size = '{0:.2f}K'.format(kilobytes)
    else:
        size = '{0:.2f}b'.format(value)
    return size


def input_file_display_renderer(widget, data):
    tag = data.tag
    value = data.value
    attrs = {
        'class': cssclasses(widget, data),
    }
    attrs.update(generic_html5_attrs(attr_value('data', widget, data)))
    if not value:
        no_file_message = _('no_file', default=u'No file')
        return tag('div', no_file_message, **attrs)
    file_val = value['file']
    size = convert_bytes(len(file_val.read()))
    file_val.seek(0)
    unknown_message = _('unknown', default=u'Unknown')
    filename_message = _('filename', default=u'Filename: ')
    mimetype_message = _('mimetype', default=u'Mimetype: ')
    size_message = _('size', default=u'Size: ')
    filename = value.get('filename', unknown_message)
    mimetype = value.get('mimetype', unknown_message)
    return tag('div',
               tag('ul',
                   tag('li', tag('strong', filename_message), filename),
                   tag('li', tag('strong', mimetype_message), mimetype),
                   tag('li', tag('strong', size_message), size)),
               **attrs)


@managedprops(*css_managed_props)
def file_options_renderer(widget, data):
    if data.value in [None, UNSET, '']:
        return data.rendered
    tag = data.tag
    if data.request:
        value = [
            data.request.get('{0}-action'.format(widget.dottedpath), 'keep')
        ]
    else:
        value = ['keep']
    tags = []
    vocab = attr_value('vocabulary', widget, data, [])
    for key, term in vocabulary(vocab):
        attrs = {
            'type': 'radio',
            'value': key,
            'checked': (key in value) and 'checked' or None,
            'name_': '{0}-action'.format(widget.dottedpath),
            'id': cssid(widget, 'input', key),
            'class_': cssclasses(widget, data),
        }
        taginput = tag('input', **attrs)
        text = tag('span', term)
        tags.append(tag('div', taginput, text,
                        **{'id': cssid(widget, 'radio', key)}))
    return data.rendered + u''.join(tags)


factory.register(
    'file',
    extractors=[
        file_extractor,
        generic_required_extractor
    ],
    edit_renderers=[
        input_file_edit_renderer,
        file_options_renderer
    ],
    display_renderers=[input_file_display_renderer])

factory.doc['blueprint']['file'] = """\
A basic file upload blueprint.
"""

factory.defaults['file.accept'] = None
factory.doc['props']['file.accept'] = """\
Accepted mimetype.
"""

factory.defaults['file.vocabulary'] = [
    ('keep', _('file_keep', default=u'Keep Existing file')),
    ('replace', _('file_replace', default=u'Replace existing file')),
    ('delete', _('file_delete', default=u'Delete existing file')),
]


###############################################################################
# submit
###############################################################################

@managedprops('label', 'class', 'action', 'handler',
              'next', 'skip', 'expression')
def submit_renderer(widget, data):
    expression = attr_value('expression', widget, data)
    if not expression:
        return u''
    tag = data.tag
    input_attrs = input_attributes_common(widget, data)
    input_attrs['type'] = 'submit'
    input_attrs['name_'] = attr_value('action', widget, data) \
        and 'action.{0}'.format(widget.dottedpath)
    input_attrs['value'] = attr_value('label', widget, data, widget.name)
    return tag('input', **input_attrs)


factory.register(
    'submit',
    edit_renderers=[submit_renderer],
    display_renderers=[empty_display_renderer])

factory.doc['blueprint']['submit'] = """\
Submit action inside the form
"""

factory.doc['props']['submit.label'] = """\
Label of the submit.
"""

factory.defaults['submit.expression'] = True
factory.doc['props']['submit.expression'] = """\
Flag or expression callable whether this action is available to the user
or not.
"""

factory.defaults['submit.action'] = True
factory.doc['props']['submit.action'] = """\
Marks this widget as an action. One out of ``True`` or ``False``.
"""

factory.defaults['submit.skip'] = False
factory.doc['props']['submit.skip'] = """\
Skips action and only perform next. One out of ``True`` or ``False``.
"""

factory.doc['props']['submit.handler'] = """\
Handler is a callable which get called if this action performs. It expects two
parameters: ``widget``, ``data``.
"""

factory.doc['props']['submit.next'] = """\
Next is a callable expected to return the web address. It expects a request as
the only parameter.
"""

factory.defaults['text.disabled'] = False
factory.doc['props']['text.disabled'] = """\
Flag  input field is disabled.
"""


###############################################################################
# email
###############################################################################

EMAIL_RE = u'^[a-zA-Z0-9\._\-]+@[a-zA-Z0-9\._\-]+.[a-zA-Z0-9]{2,6}$'


def email_extractor(widget, data):
    val = data.extracted
    if not val:
        return val
    if not re.match(EMAIL_RE, val):
        message = _('email_address_not_valid',
                    default=u'Input not a valid email address.')
        raise ExtractionError(message)
    return val


factory.register(
    'email',
    extractors=[
        generic_extractor,
        generic_required_extractor,
        generic_emptyvalue_extractor,
        email_extractor
    ],
    edit_renderers=[input_generic_renderer],
    display_renderers=[
        generic_display_renderer,
        display_proxy_renderer
    ])

factory.doc['blueprint']['email'] = """\
Email (HTML5) input blueprint.
"""

factory.defaults['email.type'] = 'email'

factory.defaults['email.default'] = ''

factory.defaults['email.required_class'] = 'required'

factory.defaults['email.class'] = 'email'

factory.defaults['email.persist'] = True


###############################################################################
# url
###############################################################################

URL_RE = u'^(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:'
URL_RE += u'.?+=&%@!\-\/]))?$'


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
    ])

factory.doc['blueprint']['url'] = """\
URL aka web address (HTML5) input blueprint.
"""

factory.defaults['url.type'] = 'url'

factory.defaults['url.default'] = ''

factory.defaults['url.required_class'] = 'required'

factory.defaults['url.class'] = 'url'

factory.defaults['url.persist'] = True


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
    ])

factory.doc['blueprint']['search'] = """\
Search blueprint (HTML5).
"""

factory.defaults['search.type'] = 'search'

factory.defaults['search.default'] = ''

factory.defaults['search.required_class'] = 'required'

factory.defaults['search.class'] = 'search'


###############################################################################
# number
###############################################################################

@managedprops('min', 'max', 'step')
def number_extractor(widget, data):
    val = data.extracted
    if val is UNSET:
        return val
    min_val = attr_value('min', widget, data)
    if min_val is not None and val < min_val:
        message = _('input_number_minimum_value',
                    default=u'Value has to be at minimum ${min}.',
                    mapping={'min': min_val})
        raise ExtractionError(message)
    max_val = attr_value('max', widget, data)
    if max_val is not None and val > max_val:
        message = _('input_number_maximum_value',
                    default=u'Value has to be at maximum ${max}.',
                    mapping={'max': max_val})
        raise ExtractionError(message)
    step = attr_value('step', widget, data)
    if step:
        minimum = min_val or 0
        if (val - minimum) % step:
            if minimum:
                message = _(
                    'input_number_step_and_minimum_value',
                    default=u'Value ${val} has to be in stepping of ${step} '
                            u'based on a floor value of ${minimum}',
                    mapping={
                        'val': val,
                        'step': step,
                        'minimum': minimum,
                    })
            else:
                message = _(
                    'input_number_step_value',
                    default=u'Value ${val} has to be in stepping of ${step}',
                    mapping={
                        'val': val,
                        'step': step,
                    })
            raise ExtractionError(message)
    return val


factory.register(
    'number',
    extractors=[
        generic_extractor,
        generic_required_extractor,
        generic_emptyvalue_extractor,
        generic_datatype_extractor,
        number_extractor,
    ],
    edit_renderers=[input_generic_renderer],
    display_renderers=[
        generic_display_renderer,
        display_proxy_renderer
    ])

factory.doc['blueprint']['number'] = """\
Number blueprint (HTML5).
"""

factory.defaults['number.type'] = 'number'

factory.defaults['number.default'] = ''

factory.defaults['number.emptyvalue'] = UNSET

factory.defaults['number.datatype'] = float
factory.doc['props']['number.datatype'] = """\
Callable for converting extracted value to output datatype. Allowed datatypes
are ``int`` and ``float``

``datatype`` can also be defined as string with value out of `'int'``,
``'integer'`` or ``'float'``.
"""

factory.defaults['number.allowed_datatypes'] = [
    int, float,
    # B/C
    'int', 'integer', 'float'
]

factory.defaults['number.min'] = None
factory.doc['props']['number.min'] = """\
Minimum value.
"""

factory.defaults['number.max'] = None
factory.doc['props']['number.max'] = """\
Maximum value.
"""

factory.defaults['number.step'] = None
factory.doc['props']['number.step'] = """\
Stepping value must be in.
"""

factory.defaults['number.required_class'] = 'required'

factory.defaults['number.class'] = 'number'

factory.defaults['number.persist'] = True


###############################################################################
# label
###############################################################################

@managedprops('position', 'label', 'for', *css_managed_props)
def label_renderer(widget, data):
    tag = data.tag
    label_text = attr_value('label', widget, data, widget.name)
    label_attrs = {
        'class_': cssclasses(widget, data)
    }
    if data.mode == 'edit':
        for_path = attr_value('for', widget, data)
        if for_path:
            for_widget = widget.root
            for name in for_path.split('.'):
                for_widget = for_widget[name]
            label_attrs['for_'] = cssid(for_widget, 'input')
        else:
            label_attrs['for_'] = cssid(widget, 'input')
        title = attr_value('title', widget, data)
        if title:
            label_attrs['title'] = title
    pos = attr_value('position', widget, data)
    if pos == 'inner':
        # deprecated, use explicit inner-after or inner-before
        pos = 'inner-before'
    rendered = data.rendered is not UNSET and data.rendered or u''
    return generic_positional_rendering_helper('label', label_text,
                                               label_attrs, rendered, pos, tag)


factory.register(
    'label',
    edit_renderers=[label_renderer],
    display_renderers=[label_renderer])

factory.doc['blueprint']['label'] = """\
Label blueprint.
"""

factory.defaults['label.position'] = 'before'
factory.doc['props']['label.position'] = """\
Label can be rendered at 3 different positions: ``before`` or ``after`` the
prior rendered output or with ``inner`` it puts the prior rendered output
inside the label tag.
"""

factory.doc['props']['label.label'] = """\
Text to be displayed as a label.
"""

factory.defaults['label.for'] = None
factory.doc['props']['label.for'] = """\
Optional dottedpath of widget to be labled
"""


###############################################################################
# field
###############################################################################

@managedprops('witherror', *css_managed_props)
def field_renderer(widget, data):
    tag = data.tag
    div_attrs = {
        'id': cssid(widget, 'field'),
        'class_': cssclasses(widget, data)
    }
    witherror = attr_value('witherror', widget, data)
    if witherror and data.errors:
        div_attrs['class_'] += u' {0}'.format(witherror)
    return tag('div', data.rendered, **div_attrs)


factory.register(
    'field',
    edit_renderers=[field_renderer],
    display_renderers=[field_renderer])

factory.doc['blueprint']['field'] = """\
Renders a div with an class field around the prior rendered output. This is
supposed to be used for styling and grouping purposes.
"""

factory.defaults['field.class'] = 'field'

factory.defaults['field.witherror'] = None
factory.doc['props']['field.witherror'] = """\
Put the class given with this property on the div if an error happened.
"""


###############################################################################
# error
###############################################################################

@managedprops('tag', 'message_tag', 'message_class', 'position',
              'render_empty', *css_managed_props)
def error_renderer(widget, data):
    if not data.errors and not attr_value('render_empty', widget, data):
        return data.rendered
    tag = data.tag
    msgs = u''
    for error in data.errors:
        message_tag = attr_value('message_tag', widget, data)
        if message_tag:
            msgs += tag(message_tag, error.message,
                        class_=attr_value('message_class', widget, data))
        else:
            msgs += error.message
    attrs = dict(class_=cssclasses(widget, data))
    elem_tag = attr_value('tag', widget, data)
    position = attr_value('position', widget, data)
    return generic_positional_rendering_helper(elem_tag, msgs,
                                               attrs, data.rendered,
                                               position, tag)


factory.register(
    'error',
    edit_renderers=[error_renderer],
    display_renderers=[empty_display_renderer])

factory.doc['blueprint']['error'] = """\
Renders a tag with an error-message and the prior rendered output.
"""

factory.defaults['error.class'] = 'error'

factory.defaults['error.tag'] = 'div'
factory.doc['props']['error.tag'] = """\
HTML tag to use to enclose all error messages.
"""

factory.defaults['error.render_empty'] = False
factory.doc['props']['error.render_empty'] = """\
Render tag even if there is no error message.
"""

factory.defaults['error.message_tag'] = 'div'
factory.doc['props']['error.message_tag'] = """\
HTML tag to use to enclose each error message.
"""

factory.defaults['error.message_class'] = 'errormessage'
factory.doc['props']['error.message_class'] = """\
CSS class to apply to inner message-tag.
"""

factory.defaults['error.position'] = 'inner-before'
factory.doc['props']['error.position'] = """\
Error can be rendered at 3 different positions: ``before``/ ``after`` the
prior rendered output or with ``inner-before``/ ``inner-after``  it puts the
prior rendered output inside the tag used for the error message (beofre or
after the message.
"""


###############################################################################
# help
###############################################################################

@managedprops('tag', 'help', 'position', 'render_empty', *css_managed_props)
def help_renderer(widget, data):
    render_empty = attr_value('render_empty', widget, data)
    help_val = attr_value('help', widget, data)
    if not render_empty and not help_val:
        return data.rendered
    tag = data.tag
    attrs = dict(class_=cssclasses(widget, data))
    elem_tag = attr_value('tag', widget, data)
    position = attr_value('position', widget, data)
    return generic_positional_rendering_helper(
        elem_tag, help_val, attrs, data.rendered, position, tag)


factory.register(
    'help',
    edit_renderers=[help_renderer],
    display_renderers=[empty_display_renderer])

factory.doc['blueprint']['help'] = """\
Renders a tag with an help-message and the prior rendered output.
"""

factory.defaults['help.class'] = 'help'

factory.defaults['help.tag'] = 'div'
factory.doc['props']['help.tag'] = """\
HTML tag to use to enclose all help messages.
"""

factory.defaults['help.help'] = ''
factory.doc['props']['help.help'] = """\
Help text.
"""

factory.defaults['help.render_empty'] = False
factory.doc['props']['help.render_empty'] = """\
Render tag even if there is no help message.
"""

factory.defaults['help.position'] = 'before'
factory.doc['props']['help.position'] = """\
Help can be rendered at 3 different positions: ``before``/ ``after`` the
prior rendered output or with ``inner-before``/ ``inner-after``  it puts the
prior rendered output inside the tag used for the help message (beofre or
after the message.
"""
