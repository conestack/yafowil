import re
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


@managedprops('type', 'size', 'disabled', 'autofocus', 'placeholder', 
              'autocomplete', *css_managed_props)
def input_generic_renderer(widget, data):
    """Generic HTML ``input`` tag render.
    """
    input_attrs = {
        'type': widget.attrs['type'],
        'value': fetch_value(widget, data),
        'name_': widget.dottedpath,
        'id': cssid(widget, 'input'),    
        'class_': cssclasses(widget, data),
        'size': widget.attrs.get('size'),
        'placeholder': widget.attrs.get('placeholder') or None,
        'autofocus': widget.attrs.get('autofocus') and 'autofocus' or None,
        'disabled': bool(widget.attrs.get('disabled')) and 'disabled' or None,
        'autocomplete': widget.attrs.get('autocomplete'),
    }
    input_attrs['required'] = \
        widget.attrs.get('required') and 'required' or None
    if widget.attrs['type'] in ['range', 'number']:
        input_attrs['min'] = widget.attrs.get('min') or None
        input_attrs['max'] = widget.attrs.get('min') or None
        input_attrs['step'] = widget.attrs.get('step') or None
    return data.tag('input', **input_attrs)


@managedprops('template', 'class')
def generic_display_renderer(widget, data):
    """Generic display renderer to render a value.
    """
    if callable(widget.attrs['template']):
        content = widget.attrs['template'](widget, data)
    else:
        value = fetch_value(widget, data)
        if value is None:
            value = u''
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


###############################################################################
# text
###############################################################################

factory.register(
    'text', 
    extractors=[generic_extractor, generic_required_extractor], 
    edit_renderers=[input_generic_renderer],
    display_renderers=[generic_display_renderer])

factory.doc['blueprint']['text'] = \
"""Text input blueprint.
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
"""Used to pass hidden arguments out of form namespace.
"""

factory.defaults['proxy.class'] = None


###############################################################################
# textarea
###############################################################################

def textarea_attributes(widget, data):
    return {
        'name_': widget.dottedpath,
        'id': cssid(widget, 'input'),
        'class_': cssclasses(widget, data),            
        'wrap': widget.attrs['wrap'],
        'cols': widget.attrs['cols'],
        'rows': widget.attrs['rows'],
        'readonly': widget.attrs['readonly'] and 'readonly',
        'placeholder': widget.attrs.get('placeholder') or None,
        'autofocus': widget.attrs.get('autofocus') and 'autofocus' or None,
        'required': widget.attrs.get('required') and 'required' or None,        
    }


@managedprops('wrap', 'cols', 'rows', 'readonly', 'autofocus', 'placeholder', 
              *css_managed_props)
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
    display_renderers=[generic_display_renderer])

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
"""Flag  textarea is readonly.
"""


###############################################################################
# lines
###############################################################################

@managedprops('wrap', 'cols', 'rows', 'readonly', 'autofocus', 'placeholder', 
              *css_managed_props)
def lines_renderer(widget, data):
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


def lines_extractor(widget, data):
    """Extract textarea value as list of lines.
    """
    extracted = data.extracted
    if not extracted:
        return list()
    return extracted.split('\n')


factory.register(
    'lines', 
    extractors=[generic_extractor, generic_required_extractor, lines_extractor], 
    edit_renderers=[lines_renderer],
    display_renderers=[generic_display_renderer])

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
"""Flag  textarea is readonly.
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
    value = _pwd_value(widget, data)
    input_attrs = {
        'type': 'password',
        'value':  value,
        'name_': widget.dottedpath,
        'id': cssid(widget, 'input'),    
        'class_': cssclasses(widget, data),
        'size': widget.attrs.get('size'),
        'placeholder': widget.attrs.get('placeholder') or None,
        'autofocus': widget.attrs.get('autofocus') and 'autofocus' or None,      
        'disabled': widget.attrs.get('disabled'),
    }
    input_attrs['required'] = \
        widget.attrs.get('required') and 'required' or None
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
"""Flag  ascii check should performed.
"""

factory.defaults['password.strength'] = -1
factory.doc['props']['password.strength'] = \
"""Integer value <= 4. Define how many rules must apply to consider a password
valid.
"""

factory.defaults['weak_password_message'] = u'Password too weak'
factory.doc['props']['password.strength'] = \
"""Message shown if password is not strong enough.
"""
factory.defaults['password.displayplaceholder'] = u'*'*8
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
    format = widget.attrs['format']
    if format == 'bool':
        return widget.dottedpath in data.request
    elif format == 'string':
        return data.request.get(widget.dottedpath, '')
    raise ValueError, "Checkbox widget has invalid format '%s' set" % format


@managedprops('format', 'disabled', 'checked', *css_managed_props)
def checkbox_edit_renderer(widget, data):
    tag = data.tag
    value = fetch_value(widget, data)
    input_attrs = {
        'type': 'checkbox',
        'value': value,
        'name_': widget.dottedpath,
        'id': cssid(widget, 'input'),    
        'class_': cssclasses(widget, data),
        'disabled': bool(widget.attrs.get('disabled')) and 'disabled' or None,            
    }
    if widget.attrs['checked'] is not None:
        if widget.attrs['checked']:
            input_attrs['checked'] = 'checked'
    else:
        input_attrs['checked'] = value and 'checked' or None
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


@managedprops('bool', 'vocabulary')
def checkbox_display_renderer(widget, data):
    """Generic display renderer to render a value.
    """
    value = fetch_value(widget, data)
    if widget.attrs['format'] == 'string' and bool(value):
        content = value
    else:
        vocab = dict(vocabulary(widget.attrs.get('vocabulary', [])))
        content = vocab[bool(value)]

    attrs = {
        'id': cssid(widget, 'display'),
        'class_': 'display-%s' % widget.attrs['class'] or 'generic'
    }
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

factory.defaults['checkbox.vocabulary'] = { True:'yes', False: 'no', 
                                            UNSET: 'not set' }
factory.doc['props']['checkbox.vocabulary'] = """\
In display mode and if ```bool``` is set to ```True``` this mapping will be used
for display of the value. Expected keys are ```True```, ```False``` and 
```UNSET```.
"""

factory.defaults['checkbox.required_class'] = 'required'


###############################################################################
# selection
###############################################################################

@managedprops('format', 'multivalued', 'disabled')
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
        listing_tag = widget.attrs['listing_tag']
        item_tag = listing_tag == 'div' and 'div' or 'li'
        if widget.attrs['multivalued']:
            tagtype = 'checkbox'
        else:
            tagtype = 'radio'
        for key, term in vocabulary(widget.attrs.get('vocabulary', [])):
            attrs = {
                'type': tagtype,
                'value':  key,
                'checked': (key in value) and 'checked' or None,
                'name_': widget.dottedpath,
                'id': cssid(widget, 'input', key),    
                'class_': cssclasses(widget, data),
            }
            if (disabled and disabled is not True and key in disabled) \
               or disabled is True:
                attrs['disabled'] = 'disabled'                                 
            
            input = tag('input', **attrs)
            if label_pos == 'inner':
                item = tag('label', term, input, for_=attrs['id'])
            elif label_pos == 'after':
                item = input + tag('label', term, for_=attrs['id'])
            else:
                item = tag('label', term, for_=attrs['id']) + input
            tags.append(tag(item_tag, item,
                            **{'id': cssid(widget, tagtype, key)}))
        return select_exists_marker(widget, data) + \
            tag(listing_tag, *tags, **{'id': cssid(widget, tagtype, 'wrapper')})


@managedprops('template', 'class', 'multivalued')
def select_display_renderer(widget, data):
    value = fetch_value(widget, data)
    if not widget.attrs['multivalued'] or not value:
        return generic_display_renderer(widget, data)
    attrs = {
        'id': cssid(widget, 'display'),
        'class_': 'display-%s' % widget.attrs['class'] or 'generic'
    }
    content = u''
    vocab = dict(vocabulary(widget.attrs.get('vocabulary', [])))
    for key in value:
        content += data.tag('li', vocab[key])
    return data.tag('ul', content, **attrs)
        

factory.register(
    'select',
    extractors=[select_extractor, generic_required_extractor], 
    edit_renderers=[select_edit_renderer],
    display_renderers=[select_display_renderer])

factory.doc['blueprint']['select'] = """\
Selection Blueprint. Single selection as dropdown or radio-buttons. Multiple 
selection as selection-list or as checkboxes. 
"""
    
factory.defaults['select.multivalued'] = None

factory.defaults['select.size'] = None

factory.defaults['select.default'] = []

factory.defaults['select.format'] = 'block'

factory.defaults['select.class'] = 'select'

factory.defaults['select.listing_tag'] = 'div'
factory.doc['props']['select.listing_tag'] = """\
Desired rendering tag for selection if selection format is 'single'. Valid
values are 'div' and 'ul'.
"""

factory.defaults['select.listing_label_position'] = 'before'
factory.doc['props']['select.listing_label_position'] = """\
Label position if format is 'single'. Behaves the same way as label widget
position property.
"""

factory.doc['props']['select.vocabulary'] = """\
Vocabulary to be used for the selection list. Expects a dict-like or an iterable 
or a callable which returns one of both first. An iterable can consist out of 
strings or out of tuples with ``(key, value)``.   
"""

factory.doc['props']['select.disabled'] = """\
Disables the whole widget or single selections. To disable the whole widget just
set the value to 'True'. To disable single selection pass a iterable of keys to 
disable, i.e. ``['foo', 'baz']``. Defaults to False.
"""


###############################################################################
# file
###############################################################################

def file_extractor(widget, data):
    name = widget.dottedpath
    if name not in data.request:
        return UNSET
    if '%s-action' % name in data.request:
        option = data.request.get('%s-action' % name, 'keep')
        if option == 'keep':
            return data.value
        elif option == 'delete':
            return UNSET
    return data.request[name]


@managedprops('accept', 'placeholder', 'autofocus', 
              'required', *css_managed_props)
def input_file_edit_renderer(widget, data):
    tag = data.tag
    input_attrs = {
        'name_': widget.dottedpath,
        'id': cssid(widget, 'input'),
        'class_': cssclasses(widget, data),            
        'type': 'file',
        'value':  '',
        'placeholder': widget.attrs.get('placeholder') or None,
        'autofocus': widget.attrs.get('autofocus') and 'autofocus' or None,
        'required': widget.attrs.get('required') and 'required' or None,        
    }
    if widget.attrs.get('accept'):
        input_attrs['accept'] = widget.attrs['accept']
    return tag('input', **input_attrs)


def input_file_display_renderer(widget, data):
    tag = data.tag
    # XXX TODO
    return tag('div', 'DISPLAY FILE TODO')


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
        input = tag('input', **attrs)
        text = tag('span', term)
        tags.append(tag('div', input, text, 
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

factory.defaults['file.multivalued'] = False

factory.defaults['file.accept'] = None
factory.doc['props']['file.accept'] = """\
Content type sto accept.
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
    input_attrs = {
        'name': widget.attrs['action'] and 'action.%s' % widget.dottedpath,
        'id': cssid(widget, 'input'),
        'class_': widget.attrs.get('class'),
        'type': 'submit',
        'value': widget.attrs.get('label', widget.__name__),
    }
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
    extractors=[generic_extractor, generic_required_extractor, email_extractor],
    edit_renderers=[input_generic_renderer],
    display_renderers=[generic_display_renderer])

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

URL_RE = u'^(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:'+\
         u'.?+=&%@!\-\/]))?$'


def url_extractor(widget, data):
    val = data.extracted
    if not re.match(URL_RE, val is not UNSET and val or ''):
        raise ExtractionError(u'Input not a valid web address.')
    return val


factory.register(
    'url',
    extractors=[generic_extractor, generic_required_extractor, url_extractor],
    edit_renderers=[input_generic_renderer],
    display_renderers=[generic_display_renderer])

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
    display_renderers=[generic_display_renderer])

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

def number_extractor(widget, data):
    val = data.extracted
    if val is UNSET or val == '':
        return val
    if widget.attrs.get('datatype') == 'integer':
        convert = int
    elif widget.attrs.get('datatype') == 'float':
        convert = float
    else:
        raise ValueError, 'Output datatype must be integer or float'
    try:
        val = convert(val)
    except ValueError:
        raise ExtractionError(u'Input is not a valid number (%s).' % \
                              widget.attrs.get('datatype'))
    if widget.attrs.get('min') and val <  _callable_attr('min', widget, data):
            raise ExtractionError(u'Value has to be at minimum %s.' % 
                                  _callable_attr('min', widget, data))
    if widget.attrs.get('max') and val > _callable_attr('max', widget, data):
        raise ExtractionError(u'Value has to be at maximum %s.' %
                              _callable_attr('max', widget, data))
    if widget.attrs.get('step'):
        step =  _callable_attr('step', widget, data)
        min = _callable_attr('min', widget, data) or 0
        if (val - min) % step:
            msg = u'Value %s has to be in stepping of %s' % (val, step)
            if min:
                msg += ' based on a floor value of %s' % min
            raise ExtractionError(msg)
    return val


factory.register(
    'number', 
    extractors=[generic_extractor, generic_required_extractor,
                number_extractor],
    edit_renderers=[input_generic_renderer],
    display_renderers=[generic_display_renderer])

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

factory.defaults['number.max'] = None

factory.defaults['number.step'] = None

factory.defaults['number.required_class'] = 'required'

factory.defaults['number.class'] = 'number'


###############################################################################
# label
###############################################################################

@managedprops('position', 'label', 'for', 'help', 'help_class',
              *css_managed_props)
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
    help = u''
    if widget.attrs['help']:
        help_attrs = {'class_': widget.attrs['help_class']}
        help = tag('div', widget.attrs['help'], **help_attrs)
    pos = widget.attrs['position']
    rendered = data.rendered is not UNSET and data.rendered or u''
    if pos == 'inner':
        return tag('label', label_text, help, rendered, **label_attrs)
    elif pos == 'after':
        return rendered + tag('label', label_text, help, **label_attrs)
    return tag('label', label_text, help, **label_attrs) + rendered


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
prior rendered output or with ``inner`` it puts the prior rendered output inside
the label tag.
"""

factory.doc['props']['label.label'] = """\
Text to be displayed as a label.
"""

factory.defaults['label.for'] = None
factory.doc['props']['label.for'] = """\
Optional dottedpath of widget to be labled
"""

factory.defaults['label.help'] = None
factory.doc['props']['label.help'] = """\
Optional help text (alternative description) to be rendered inside a div after
the label.
"""

factory.defaults['label.help_class'] = 'help'


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

@managedprops('message_class', 'error_class', 'error', *css_managed_props)
def error_renderer(widget, data):
    if not data.errors:
        return data.rendered
    tag = data.tag
    msgs = u''
    for error in data.errors:
        msgs += tag('div', error.message, class_=widget.attrs['message_class'])
    return tag('div', msgs, data.rendered, class_=cssclasses(widget, data))


factory.register(
    'error',
    edit_renderers=[error_renderer],
    display_renderers=[empty_display_renderer])

factory.doc['blueprint']['error'] = """\
Renders a div with an errormessage around the prior rendered output.
"""

factory.defaults['error.error_class'] = 'error'

factory.defaults['error.message_class'] = 'errormessage'