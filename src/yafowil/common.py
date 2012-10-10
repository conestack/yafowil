import re
import types
import logging
from yafowil.base import (
    factory,
    ExtractionError,
    fetch_value
)
from utils import (
    UNSET,
    cssclasses,
    css_managed_props,
    cssid,
    managedprops,
    vocabulary,
)


###############################################################################
# common defaults
###############################################################################

factory.defaults['default'] = UNSET
factory.doc['props']['default'] = \
"""Default value.
"""

factory.defaults['class'] = None
factory.doc['props']['class'] = \
"""Common CSS-class to put on.
"""

factory.defaults['class_add'] = None
factory.doc['props']['class_add'] = \
"""Additional CSS-class to put on.
"""

factory.defaults['error_class'] = None
factory.doc['props']['error_class'] = \
"""CSS-class to put on in case of error.
"""

factory.defaults['error_class_default'] = 'error'
factory.doc['props']['error_class_default'] = \
"""Fallback CSS-class to put on in case of error if no specific class was
 given.
"""

factory.defaults['autofocus'] = None
factory.doc['props']['autofocus'] = \
"""Whether this field gets the focus automatically or not (if browser supports
 it).
"""

factory.defaults['autocomplete'] = None
factory.doc['props']['autocomplete'] = \
"""Switch autocomplete explizit to ``on`` or ``off``.
"""

factory.defaults['placeholder'] = None
factory.doc['props']['placeholder'] = \
"""Whether this input has a placeholder value or not (if browser supports it).
"""

factory.defaults['required'] = False
factory.doc['props']['required'] = \
"""Whether this value is required or not.
"""

factory.defaults['required_message'] = u'Mandatory field was empty'
factory.doc['props']['required_message'] = \
"""Message to be shown if required condition was not met.
"""

factory.defaults['required_class'] = None
factory.doc['props']['required_class'] = \
"""CSS-class to put on in case if required condition was not met.
"""

factory.defaults['type'] = None
factory.doc['props']['type'] = \
"""HTML type attribute.
"""

factory.defaults['size'] = None
factory.doc['props']['size'] = \
"""Allowed input size.
"""

factory.defaults['disabled'] = None
factory.doc['props']['disabled'] = \
"""Disables input.
"""

factory.defaults['required_class_default'] = 'required'
factory.doc['props']['required_class_default'] = \
"""CSS-class to apply if required condition was not met - if no specific class
was given.
"""

factory.defaults['template'] = '%s'
factory.doc['props']['template'] = \
"""Format string with pythons built-in string format template. If a callable
is given it will be used instead and is called with ``widget`` and ``data`` as
parameters.
"""

factory.defaults['title'] = None
factory.doc['props']['title'] = """\
Optional help text to be rendered in the title attribute.
"""

factory.defaults['display_proxy'] = False
factory.doc['props']['display_proxy'] = """\
If 'True' and widget mode 'display', widget value gets rendered as hidden input.
"""


###############################################################################
# generic
###############################################################################

def generic_extractor(widget, data):
    """Extract raw data from request by ``widget.dottedpath``.
    """
    __managed_props = []
    if widget.dottedpath not in data.request:
        return UNSET
    return data.request[widget.dottedpath]


@managedprops('required', 'required_message')
def generic_required_extractor(widget, data):
    """Validate required.

    If required is set and some value was extracted,
    so ``data.extracted`` is not ``UNSET``, then we evaluate ``data.extracted``
    to boolean. Raise ``ExtractionError`` if result is ``False``.

    Properties:

    ``required``
        Define  value is required ot not. Either basestring instance or
        callable returning basestring is expected.

    ``required_message``
        Default required message as basestring instance.
    """
    required = widget.attrs.get('required')
    if callable(required):
        required = required(widget, data)
    if not required \
       or bool(data.extracted) \
       or data.extracted is UNSET:
        return data.extracted
    if isinstance(required, basestring):
        raise ExtractionError(required)
    raise ExtractionError(widget.attrs['required_message'])


def input_attributes_common(widget, data, excludes=list(), value=None):
    if value is None:
        value = fetch_value(widget, data)
    input_attrs = {
        'autofocus': widget.attrs.get('autofocus') and 'autofocus' or None,
        'class_': cssclasses(widget, data),
        'disabled': bool(widget.attrs.get('disabled')) and 'disabled' or None,
        'id': cssid(widget, 'input'),
        'name_': widget.dottedpath,
        'placeholder': widget.attrs.get('placeholder') or None,
        'required': widget.attrs.get('required') and 'required' or None,
        'size': widget.attrs.get('size'),
        'title': widget.attrs.get('title') or None,
        'type': widget.attrs.get('type') or None,
        'value': value,
    }
    for attr_name in excludes:
        del input_attrs[attr_name]
    return input_attrs


def input_attributes_full(widget, data, value=None):
    input_attrs = input_attributes_common(widget, data, value=value)
    input_attrs['autocomplete'] = widget.attrs.get('autocomplete')
    if widget.attrs['type'] in ['range', 'number']:
        input_attrs['min'] = widget.attrs.get('min') or None
        input_attrs['max'] = widget.attrs.get('min') or None
        input_attrs['step'] = widget.attrs.get('step') or None
    return input_attrs


@managedprops('type', 'size', 'disabled', 'autofocus', 'placeholder',
              'autocomplete', *css_managed_props)
def input_generic_renderer(widget, data):
    """Generic HTML ``input`` tag render.
    """
    input_attrs = input_attributes_full(widget, data)
    return data.tag('input', **input_attrs)


# multivalued is not documented, because its only valid for specific blueprints
@managedprops('display_proxy', 'type')
def display_proxy_renderer(widget, data):
    rendered = data.rendered
    if widget.attrs['display_proxy']:
        orgin_type = widget.attrs.get('type')
        widget.attrs['type'] = 'hidden'
        value = fetch_value(widget, data)
        multivalued = widget.attrs.get('multivalued')
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
        if not value:
            value = u''
        content = widget.attrs['template'] % value
    else:
        content = widget.attrs['template'] % value
    attrs = {
        'id': cssid(widget, 'display'),
        'class_': 'display-%s' % widget.attrs['class'] or 'generic'
    }
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
        raise ValueError('Invalid value for position "%s"' % pos)
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

@managedprops('tag', 'text', *css_managed_props)
def tag_renderer(widget, data):
    """Renderer for HTML tags.
    """
    attrs = {
        'id': cssid(widget, 'tag'),
        'class_': cssclasses(widget, data),
    }
    return data.tag(widget.attrs['tag'], widget.attrs['text'], **attrs)


factory.register(
    'tag',
    edit_renderers=[tag_renderer],
    display_renderers=[tag_renderer])

factory.doc['blueprint']['tag'] = \
"""Render HTML tags with text. Useful for rendering headings etc.
"""

factory.doc['props']['tag.tag'] = \
"""HTML tag name.
"""

factory.doc['props']['tag.text'] = \
"""Tag contents.
"""


###############################################################################
# text
###############################################################################

factory.register(
    'text',
    extractors=[generic_extractor, generic_required_extractor],
    edit_renderers=[input_generic_renderer],
    display_renderers=[generic_display_renderer, display_proxy_renderer])

factory.doc['blueprint']['text'] = \
"""One line text input blueprint.
"""

factory.defaults['text.type'] = 'text'
factory.doc['props']['text.type'] = \
"""Type of input tag.
"""

factory.defaults['text.required_class'] = 'required'

factory.defaults['text.default'] = ''

factory.defaults['text.class'] = 'text'

factory.defaults['text.disabled'] = False
factory.doc['props']['text.disabled'] = \
"""Flag  input field is disabled.
"""


###############################################################################
# hidden
###############################################################################

factory.register(
     'hidden',
     extractors=[generic_extractor],
     edit_renderers=[input_generic_renderer],
     display_renderers=[empty_display_renderer])

factory.doc['blueprint']['hidden'] = \
"""Hidden input blueprint.
"""

factory.defaults['hidden.type'] = 'hidden'
factory.doc['props']['hidden.type'] = \
"""Type of input tag.
"""

factory.defaults['hidden.default'] = ''

factory.defaults['hidden.class'] = 'hidden'


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
    if data.request is not UNSET:
        if data.request.get(widget.__name__):
            value = data.request.get(widget.__name__)
    input_attrs = {
        'type': 'hidden',
        'value':  value,
        'name_': widget.__name__,
        'id': cssid(widget, 'input'),
        'class_': cssclasses(widget, data),
    }
    return tag('input', **input_attrs)


factory.register(
    'proxy',
    extractors=[generic_extractor],
    edit_renderers=[input_proxy_renderer],
    display_renderers=[empty_display_renderer])

factory.doc['blueprint']['proxy'] = \
"""Bypass arguments out of form namespace using a hidden field.
"""

factory.defaults['proxy.class'] = None


###############################################################################
# textarea
###############################################################################

def textarea_attributes(widget, data):
    return {
        'autofocus': widget.attrs.get('autofocus') and 'autofocus' or None,
        'class_': cssclasses(widget, data),
        'cols': widget.attrs['cols'],
        'disabled': widget.attrs.get('disabled') and 'disabled' or None,
        'id': cssid(widget, 'input'),
        'name_': widget.dottedpath,
        'placeholder': widget.attrs.get('placeholder') or None,
        'readonly': widget.attrs['readonly'] and 'readonly',
        'required': widget.attrs.get('required') and 'required' or None,
        'rows': widget.attrs['rows'],
        'wrap': widget.attrs['wrap'],
    }
textarea_managed_props = ['autofocus', 'cols', 'disabled', 'placeholder',
                          'readonly', 'required', 'rows', 'wrap'] + \
                          css_managed_props

@managedprops(*textarea_managed_props)
def textarea_renderer(widget, data):
    """Renders text area.
    """
    tag = data.tag
    area_attrs = textarea_attributes(widget, data)
    value = fetch_value(widget, data)
    if value is None:
        value = ''
    return tag('textarea', value, **area_attrs)


factory.register(
    'textarea',
    extractors=[generic_extractor, generic_required_extractor],
    edit_renderers=[textarea_renderer],
    display_renderers=[generic_display_renderer, display_proxy_renderer])

factory.doc['blueprint']['textarea'] = \
"""HTML textarea blueprint.
"""

factory.defaults['textarea.default'] = ''
factory.defaults['textarea.wrap'] = None
factory.doc['props']['textarea.wrap'] = \
"""Either ``soft``, ``hard``, ``virtual``, ``physical`` or  ``off``.
"""

factory.defaults['textarea.cols'] = 80
factory.doc['props']['textarea.cols'] = \
"""Number of characters.
"""

factory.defaults['textarea.rows'] = 25
factory.doc['props']['textarea.rows'] = \
"""Number of lines.
"""

factory.defaults['textarea.readonly'] = None
factory.doc['props']['textarea.readonly'] = \
"""Flag textarea is readonly.
"""


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


@managedprops(*css_managed_props)
def lines_display_renderer(widget, data):
    value = fetch_value(widget, data)
    if type(value) in [types.ListType, types.TupleType] and not value:
        value = u''
    attrs = {
        'id': cssid(widget, 'display'),
        'class_': 'display-%s' % widget.attrs['class'] or 'generic'
    }
    content = u''
    for line in value:
        content += data.tag('li', line)
    return data.tag('ul', content, **attrs)


factory.register(
    'lines',
    extractors=[generic_extractor,
                generic_required_extractor,
                lines_extractor],
    edit_renderers=[lines_edit_renderer],
    display_renderers=[lines_display_renderer, display_proxy_renderer])

factory.doc['blueprint']['lines'] = \
"""Lines blueprint. Renders a textarea and extracts lines as list.
"""

factory.defaults['lines.default'] = ''
factory.defaults['lines.wrap'] = None
factory.doc['props']['lines.wrap'] = \
"""Either ``soft``, ``hard``, ``virtual``, ``physical`` or  ``off``.
"""

factory.defaults['lines.cols'] = 40
factory.doc['props']['lines.cols'] = \
"""Number of characters.
"""

factory.defaults['lines.rows'] = 8
factory.doc['props']['lines.rows'] = \
"""Number of lines.
"""

factory.defaults['lines.readonly'] = None
factory.doc['props']['lines.readonly'] = \
"""Flag textarea is readonly.
"""


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
    minlength = widget.attrs.get('minlength', -1)
    if minlength != -1:
        if len(val) < minlength:
            message = u'Input must have at least %i characters.' % minlength
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
    if not widget.attrs.get('ascii', False):
        return val
    try:
        str(val)
    except UnicodeEncodeError:
        raise ExtractionError(u'Input contains illegal characters.')
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
    required_strength = widget.attrs.get('strength', 0)
    if required_strength <= 0:
        return val
    if required_strength > len(RE_PASSWORD_ALL):
        required_strength = len(RE_PASSWORD_ALL)
    strength = 0
    for reg_exp in RE_PASSWORD_ALL:
        if re.match(reg_exp, val):
            strength += 1
    if strength < required_strength:
        raise ExtractionError(widget.attrs.get('weak_password_message'))
    return val


def _pwd_value(widget, data):
    if data.extracted is not UNSET:
        return data.extracted
    if data.value is not UNSET \
      and data.value is not None:
        return PASSWORD_NOCHANGE_VALUE
    return widget.attrs['default']


@managedprops('size', 'disabled', 'placeholder', 'autofocus', 'required',
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
        return widget.attrs['displayplaceholder']
    return u''


factory.register(
    'password',
    extractors=[generic_extractor, generic_required_extractor,
                minlength_extractor, ascii_extractor, password_extractor],
    edit_renderers=[password_edit_renderer],
    display_renderers=[password_display_renderer])

factory.doc['blueprint']['password'] = \
"""Password blueprint.

The password is never rendered to markup, instead
``yafowil.common.PASSWORD_NOCHANGE_VALUE`` is set as ``value`` property on
dom element. See ``yafowil.common.password_extractor`` for details on
password extraction.
"""

factory.defaults['password.required_class'] = 'required'

factory.defaults['password.default'] = ''

factory.defaults['password.class'] = 'password'

factory.defaults['password.minlength'] = -1
factory.doc['props']['password.size'] = \
"""Maximum length of password.
"""

factory.doc['props']['password.minlength'] = \
"""Minimum length of password.
"""

factory.defaults['password.ascii'] = False
factory.doc['props']['password.ascii'] = \
"""Flag ascii check should performed.
"""

factory.defaults['password.strength'] = -1
factory.doc['props']['password.strength'] = \
"""Integer value <= 4. Define how many rules must apply to consider a password
valid.
"""

factory.defaults['weak_password_message'] = u'Password too weak'
factory.doc['props']['password.weak_password_message'] = \
"""Message shown if password is not strong enough.
"""

factory.defaults['password.displayplaceholder'] = u'*' * 8
factory.doc['props']['password.displayplaceholder'] = \
"""Placeholder shown in display mode if password was set.
"""


###############################################################################
# checkbox
###############################################################################

@managedprops('format')
def checkbox_extractor(widget, data):
    """Extracts data from a single input with type checkbox.
    """
    if '%s-exists' % widget.dottedpath not in data.request:
        return UNSET
    fmt = widget.attrs['format']
    if fmt == 'bool':
        return widget.dottedpath in data.request
    elif fmt == 'string':
        return data.request.get(widget.dottedpath, '')
    raise ValueError("Checkbox widget has invalid format '%s' set" % fmt)


@managedprops('format', 'disabled', 'checked', *css_managed_props)
def checkbox_edit_renderer(widget, data):
    tag = data.tag
    input_attrs = input_attributes_common(widget, data)
    input_attrs['type'] = 'checkbox'
    if widget.attrs['checked'] is not None:
        if widget.attrs['checked']:
            input_attrs['checked'] = 'checked'
    else:
        input_attrs['checked'] = input_attrs['value'] and 'checked' or None
    if widget.attrs['format'] == 'bool':
        input_attrs['value'] = ''
    checkbox = tag('input', **input_attrs)
    input_attrs = {
        'type': 'hidden',
        'value':  'checkboxexists',
        'name_': "%s-exists" % widget.dottedpath,
        'id': cssid(widget, 'checkboxexists'),
    }
    exists_marker = tag('input', **input_attrs)
    return checkbox + exists_marker


@managedprops('format', 'vocabulary')
def checkbox_display_renderer(widget, data):
    """Generic display renderer to render a value.
    """
    value = fetch_value(widget, data)
    if widget.attrs['format'] == 'string' and bool(value):
        content = value
    else:
        vocab = dict(vocabulary(widget.attrs.get('vocabulary', [])))
        content = vocab[bool(value)]
        if data.tag.translate:
            content = data.tag.translate(content)
    attrs = {
        'id': cssid(widget, 'display'),
        'class_': 'display-%s' % widget.attrs['class'] or 'generic'
    }
    if widget.attrs['display_proxy']:
        widget.attrs['type'] = 'hidden'
        if widget.attrs['format'] == 'string':
            input_attrs = input_attributes_common(widget, data, value=value)
            content += data.tag('input', **input_attrs)
        elif bool(value):
            input_attrs = input_attributes_common(widget, data, value='')
            content += data.tag('input', **input_attrs)
        del widget.attrs['type']
        input_attrs = {
            'type': 'hidden',
            'value':  'checkboxexists',
            'name_': "%s-exists" % widget.dottedpath,
            'id': cssid(widget, 'checkboxexists'),
        }
        content += data.tag('input', **input_attrs)
    return data.tag('div', content, **attrs)


factory.register(
    'checkbox',
    extractors=[checkbox_extractor, generic_required_extractor],
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

factory.defaults['checkbox.disabled'] = False
factory.doc['props']['checkbox.disabled'] = """\
Flag whether checkbox is disabled.
"""

factory.defaults['checkbox.checked'] = None
factory.doc['props']['checkbox.checked'] = """\
Set 'checked' attribute explicit. If not given, compute by value.
"""

factory.defaults['checkbox.vocabulary'] = {
    True: 'yes',
    False: 'no',
    UNSET: 'not set',
}

factory.doc['props']['checkbox.vocabulary'] = """\
In display mode and if ```bool``` is set to ```True``` this mapping will be
used for display of the value. Expected keys are ```True```, ```False``` and
```UNSET```.
"""

factory.defaults['checkbox.required_class'] = 'required'


###############################################################################
# selection
###############################################################################

@managedprops('multivalued', 'disabled')
def select_extractor(widget, data):
    extracted = generic_extractor(widget, data)
    if extracted is UNSET \
       and '%s-exists' % widget.dottedpath in data.request:
        if widget.attrs['multivalued']:
            extracted = []
        else:
            extracted = ''
    if extracted is UNSET:
        return extracted
    if widget.attrs['multivalued'] and isinstance(extracted, basestring):
        extracted = [extracted]
    disabled = widget.attrs.get('disabled', False)
    if not disabled:
        return extracted
    if not widget.attrs['multivalued']:
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
        'value':  'exists',
        'name_': "%s-exists" % widget.dottedpath,
        'id': cssid(widget, 'exists'),
    }
    return tag('input', **attrs)


@managedprops('format', 'vocabulary', 'multivalued', 'disabled',
              'listing_label_position', 'listing_tag', 'size',
              'label_checkbox_class', 'label_radio_class',
              *css_managed_props)
def select_edit_renderer(widget, data):
    tag = data.tag
    value = fetch_value(widget, data)
    if isinstance(value, basestring) or not hasattr(value, '__iter__'):
        value = [value]
    if not widget.attrs['multivalued'] and len(value) > 1:
        raise ValueError(u"Multiple values for single selection.")
    disabled = widget.attrs.get('disabled', False)
    if widget.attrs['format'] == 'block':
        optiontags = []
        for key, term in vocabulary(widget.attrs.get('vocabulary', [])):
            attrs = {
                'selected': (key in value) and 'selected' or None,
                'value': key,
                'id': cssid(widget, 'input', key),
            }
            if disabled and disabled is not True and key in disabled:
                attrs['disabled'] = 'disabled'
            optiontags.append(tag('option', term, **attrs))
        select_attrs = {
            'name_': widget.dottedpath,
            'id': cssid(widget, 'input'),
            'class_': cssclasses(widget, data),
            'multiple': widget.attrs['multivalued'] and 'multiple' or None,
            'size': widget.attrs['size'] or None,
            'placeholder': widget.attrs.get('placeholder') or None,
            'autofocus': widget.attrs.get('autofocus') and 'autofocus' or None,
            'required': widget.attrs.get('required') and 'required' or None,
        }
        if disabled is True:
            select_attrs['disabled'] = 'disabled'
        rendered = tag('select', *optiontags, **select_attrs)
        if widget.attrs['multivalued']:
            attrs = {
                'type': 'hidden',
                'value':  'exists',
                'name_': "%s-exists" % widget.dottedpath,
                'id': cssid(widget, 'exists'),
            }
            rendered = select_exists_marker(widget, data) + rendered
        return rendered
    else:
        tags = []
        label_pos = widget.attrs['listing_label_position']
        if label_pos == 'inner':
            # deprecated, use explicit inner-after or inner-before
            label_pos = 'inner-after'
        listing_tag = widget.attrs['listing_tag']
        item_tag = listing_tag == 'div' and 'div' or 'li'
        if widget.attrs['multivalued']:
            tagtype = 'checkbox'
            tagclass = widget.attrs['label_checkbox_class']
        else:
            tagtype = 'radio'
            tagclass = widget.attrs['label_radio_class']
        for key, term in vocabulary(widget.attrs.get('vocabulary', [])):
            input_attrs = {
                'type': tagtype,
                'value':  key,
                'checked': (key in value) and 'checked' or None,
                'name_': widget.dottedpath,
                'id': cssid(widget, 'input', key),
                'class_': cssclasses(widget, data),
            }
            if (disabled and disabled is not True and key in disabled) \
               or disabled is True:
                input_attrs['disabled'] = 'disabled'
            inputtag = tag('input', **input_attrs)
            label_attrs = dict(for_=input_attrs['id'], _class=tagclass)
            item = generic_positional_rendering_helper('label', term,
                                                       label_attrs, inputtag,
                                                       label_pos, tag)
            tags.append(tag(item_tag, item,
                            **{'id': cssid(widget, tagtype, key)}))
        taglisting = tag(listing_tag,
                         *tags,
                         **{'id': cssid(widget, tagtype, 'wrapper')})
        return select_exists_marker(widget, data) + taglisting


@managedprops('template', 'class', 'multivalued')
def select_display_renderer(widget, data):
    value = fetch_value(widget, data)
    if type(value) in [types.ListType, types.TupleType] and not value:
        value = u''
    if not widget.attrs['multivalued'] or not value:
        vocab = dict(vocabulary(widget.attrs.get('vocabulary', [])))
        value = vocab.get(value, value)
        if data.tag.translate:
            value = data.tag.translate(value)
        return generic_display_renderer(widget, data, value=value)
    attrs = {
        'id': cssid(widget, 'display'),
        'class_': 'display-%s' % widget.attrs['class'] or 'generic'
    }
    content = u''
    vocab = dict(vocabulary(widget.attrs.get('vocabulary', [])))
    if widget.attrs['multivalued'] and isinstance(value, basestring):
        value = [value]
    for key in value:
        content += data.tag('li', vocab[key])
    return data.tag('ul', content, **attrs)


factory.register(
    'select',
    extractors=[select_extractor, generic_required_extractor],
    edit_renderers=[select_edit_renderer],
    display_renderers=[select_display_renderer, display_proxy_renderer])

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

factory.defaults['select.default'] = []

factory.defaults['select.format'] = 'block'
factory.doc['props']['select.format'] = """\
Every value except 'block' results in either a list of radio buttons or
checkboxes depending on the 'multivalued' property.
"""

factory.defaults['select.class'] = 'select'

factory.defaults['select.label_checkbox_class'] = None
factory.doc['props']['select.label_checkbox_class'] = """\
CSS class to render on checkbox labels.
"""

factory.defaults['select.label_radio_class'] = None
factory.doc['props']['select.label_radio_class'] = """\
CSS class to render on radio button labels.
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
    if not '%s-action' % name in data.request:
        value = data.request[name]
        if value:
            value['action'] = 'new'
        return value
    value = data.value
    action = value['action'] = data.request.get('%s-action' % name, 'keep')
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
    if widget.attrs.get('accept'):
        input_attrs['accept'] = widget.attrs['accept']
    return tag('input', **input_attrs)


def convert_bytes(bytes):
    bytes = float(bytes)
    if bytes >= 1099511627776:
        terabytes = bytes / 1099511627776
        size = '%.2fT' % terabytes
    elif bytes >= 1073741824:
        gigabytes = bytes / 1073741824
        size = '%.2fG' % gigabytes
    elif bytes >= 1048576:
        megabytes = bytes / 1048576
        size = '%.2fM' % megabytes
    elif bytes >= 1024:
        kilobytes = bytes / 1024
        size = '%.2fK' % kilobytes
    else:
        size = '%.2fb' % bytes
    return size


def input_file_display_renderer(widget, data):
    tag = data.tag
    value = data.value
    if not value:
        return tag('div', 'No file')
    file = value['file']
    size = convert_bytes(len(file.read()))
    file.seek(0)
    filename = value.get('filename', 'Unknown')
    mimetype = value.get('mimetype', 'Unknown')
    return tag('div',
               tag('ul',
                   tag('li', tag('strong', 'Filename: '), filename),
                   tag('li', tag('strong', 'Mimetype: '), mimetype),
                   tag('li', tag('strong', 'Size: '), size)),
               class_=cssclasses(widget, data))


@managedprops(*css_managed_props)
def file_options_renderer(widget, data):
    if data.value in [None, UNSET, '']:
        return data.rendered
    tag = data.tag
    if data.request:
        value = [data.request.get('%s-action' % widget.dottedpath, 'keep')]
    else:
        value = ['keep']
    tags = []
    for key, term in vocabulary(widget.attrs.get('vocabulary', [])):
        attrs = {
            'type': 'radio',
            'value':  key,
            'checked': (key in value) and 'checked' or None,
            'name_': '%s-action' % widget.dottedpath,
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
    extractors=[file_extractor, generic_required_extractor],
    edit_renderers=[input_file_edit_renderer, file_options_renderer],
    display_renderers=[input_file_display_renderer])

factory.doc['blueprint']['file'] = """\
A basic file upload blueprint.
"""

factory.defaults['file.accept'] = None
factory.doc['props']['file.accept'] = """\
Accepted mimetype.
"""

factory.defaults['file.vocabulary'] = [
    ('keep', u'Keep Existing file'),
    ('replace', u'Replace existing file'),
    ('delete', u'Delete existing file'),
]


###############################################################################
# submit
###############################################################################

@managedprops('label', 'class', 'action', 'handler',
              'next', 'skip', 'expression')
def submit_renderer(widget, data):
    expression = widget.attrs['expression']
    if callable(expression):
        expression = expression()
    if not expression:
        return u''
    tag = data.tag
    input_attrs = input_attributes_common(widget, data)
    input_attrs['type'] = 'submit'
    input_attrs['name_'] = widget.attrs['action'] and\
                          'action.%s' % widget.dottedpath
    input_attrs['value'] = widget.attrs.get('label', widget.__name__)
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
factory.doc['props']['text.disabled'] = \
"""Flag  input field is disabled.
"""


###############################################################################
# email
###############################################################################

EMAIL_RE = u'^[a-zA-Z0-9\._\-]+@[a-zA-Z0-9\._\-]+.[a-zA-Z0-9]{2,6}$'


def email_extractor(widget, data):
    val = data.extracted
    if not re.match(EMAIL_RE, val is not UNSET and val or ''):
        raise ExtractionError(u'Input not a valid email address.')
    return val


factory.register(
    'email',
    extractors=[generic_extractor,
                generic_required_extractor,
                email_extractor],
    edit_renderers=[input_generic_renderer],
    display_renderers=[generic_display_renderer, display_proxy_renderer])

factory.doc['blueprint']['email'] = \
"""E-mail (HTML5) input blueprint.
"""

factory.defaults['email.type'] = 'email'

factory.defaults['email.default'] = ''

factory.defaults['email.required_class'] = 'required'

factory.defaults['email.class'] = 'email'


###############################################################################
# url
###############################################################################

URL_RE = u'^(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:'
URL_RE += u'.?+=&%@!\-\/]))?$'


def url_extractor(widget, data):
    val = data.extracted
    if not re.match(URL_RE, val is not UNSET and val or ''):
        raise ExtractionError(u'Input not a valid web address.')
    return val


factory.register(
    'url',
    extractors=[generic_extractor, generic_required_extractor, url_extractor],
    edit_renderers=[input_generic_renderer],
    display_renderers=[generic_display_renderer, display_proxy_renderer])

factory.doc['blueprint']['url'] = \
"""URL aka web address (HTML5) input blueprint.
"""

factory.defaults['url.type'] = 'url'

factory.defaults['url.default'] = ''

factory.defaults['url.required_class'] = 'required'

factory.defaults['url.class'] = 'url'


###############################################################################
# search
###############################################################################

factory.register(
    'search',
    extractors=[generic_extractor, generic_required_extractor],
    edit_renderers=[input_generic_renderer],
    display_renderers=[generic_display_renderer, display_proxy_renderer])

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

def _callable_attr(key, widget, data):
    # helper, make me generic
    value = widget.attrs.get(key)
    if callable(value):
        return value(widget, data)
    return value


@managedprops('datatype', 'min', 'max', 'step')
def number_extractor(widget, data):
    val = data.extracted
    if val is UNSET or val == '':
        return val
    if widget.attrs.get('datatype') == 'integer':
        convert = int
    elif widget.attrs.get('datatype') == 'float':
        convert = float
    else:
        raise ValueError('Output datatype must be integer or float')
    try:
        val = convert(val)
    except ValueError:
        raise ExtractionError(u'Input is not a valid number (%s).' % \
                              widget.attrs.get('datatype'))
    if widget.attrs.get('min') and val < _callable_attr('min', widget, data):
            raise ExtractionError(u'Value has to be at minimum %s.' %
                                  _callable_attr('min', widget, data))
    if widget.attrs.get('max') and val > _callable_attr('max', widget, data):
        raise ExtractionError(u'Value has to be at maximum %s.' %
                              _callable_attr('max', widget, data))
    if widget.attrs.get('step'):
        step = _callable_attr('step', widget, data)
        minimum = _callable_attr('min', widget, data) or 0
        if (val - minimum) % step:
            msg = u'Value %s has to be in stepping of %s' % (val, step)
            if minimum:
                msg += ' based on a floor value of %s' % minimum
            raise ExtractionError(msg)
    return val


factory.register(
    'number',
    extractors=[generic_extractor, generic_required_extractor,
                number_extractor],
    edit_renderers=[input_generic_renderer],
    display_renderers=[generic_display_renderer, display_proxy_renderer])

factory.doc['blueprint']['number'] = """\
Number blueprint (HTML5).
"""

factory.defaults['number.type'] = 'number'

factory.defaults['number.datatype'] = 'float'
factory.doc['props']['number.datatype'] = """\
Output datatype, one out of ``integer`` or ``float``.
"""

factory.defaults['number.default'] = ''

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


###############################################################################
# label
###############################################################################

@managedprops('position', 'label', 'for', *css_managed_props)
def label_renderer(widget, data):
    tag = data.tag
    label_text = widget.attrs.get('label', widget.__name__)
    if callable(label_text):
        label_text = label_text()
    label_attrs = {
        'class_': cssclasses(widget, data)
    }
    if data.mode == 'edit':
        for_path = widget.attrs['for']
        if for_path:
            for_widget = widget.root
            for name in for_path.split('.'):
                for_widget = for_widget[name]
            label_attrs['for_'] = cssid(for_widget, 'input')
        else:
            label_attrs['for_'] = cssid(widget, 'input')
        if widget.attrs['title']:
            label_attrs['title'] = widget.attrs['title']
    pos = widget.attrs['position']
    if callable(pos):
        pos = pos(widget, data)
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
    if widget.attrs['witherror'] and data.errors:
        div_attrs['class_'] += u' %s' % widget.attrs['witherror']
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
    if not data.errors and not widget.attrs.get('render_empty'):
        return data.rendered
    tag = data.tag
    msgs = u''
    for error in data.errors:
        if widget.attrs.get('message_tag'):
            msgs += tag(widget.attrs['message_tag'],
                        error.message,
                        class_=widget.attrs['message_class'])
        else:
            msgs += error.message
    attrs = dict(class_=cssclasses(widget, data))
    return generic_positional_rendering_helper(widget.attrs['tag'], msgs,
                                               attrs, data.rendered,
                                               widget.attrs['position'], tag)

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
    if not widget.attrs.get('render_empty') and not widget.attrs.get('help'):
        return data.rendered
    tag = data.tag
    attrs = dict(class_=cssclasses(widget, data))
    return generic_positional_rendering_helper(widget.attrs['tag'],
                                               widget.attrs['help'],
                                               attrs, data.rendered,
                                               widget.attrs['position'], tag)

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
