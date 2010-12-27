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

factory.defaults['required'] = False
factory.doc['props']['required'] = \
"""Wether this value is required or not.
"""

factory.defaults['required_message'] = u'Mandatory field was empty'          
factory.doc['props']['required_message'] = \
"""Message to be shown if required condition was not met.
""" 
            
factory.defaults['required_class'] = None
factory.doc['props']['required_class'] = \
"""CSS-class to put on in case if required condition was not met.
"""

factory.defaults['required_class_default'] = 'required'
factory.doc['props']['required_class_default'] = \
"""CSS-class to put on in case if required condition was not met if no specific 
class was given.
"""

###############################################################################
# generic
###############################################################################

def _value(widget, data):
    """BBB
    """
    logging.warn("Deprecated usage of 'yafowil.common._value', please use "+\
                 "'yafowil.common.fetch_value' instead.") 
    return fetch_value(widget, data)   
    
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
        Define wether value is required ot not. Either basestring instance or
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

@managedprops('type', 'size', 'disabled', *css_managed_props)
def input_generic_renderer(widget, data):
    """Generic HTML ``input`` tag render.
    
    Properties:
    
    ``type``
        Type of this input tag.
    
    ``size``
        Size of input tag.
    
    ``disabled``
        Bool evaluating value, if evaluates to True, sets disabled="disabled" 
        on input tag.
    """
    tag = data.tag
    input_attrs = {
        'type': widget.attrs['type'],
        'value': fetch_value(widget, data),
        'name_': widget.dottedpath,
        'id': cssid(widget, 'input'),    
        'class_': cssclasses(widget, data),
        'size': widget.attrs.get('size'),
        'disabled': bool(widget.attrs.get('disabled')) and 'disabled' or None,
    }
    return tag('input', **input_attrs)

###############################################################################
# text
###############################################################################

factory.register('text', 
                 [generic_extractor, generic_required_extractor], 
                 [input_generic_renderer])
factory.doc['widget']['text'] = \
"""Text input widget.
"""

factory.defaults['text.type'] = 'text'
factory.doc['props']['text.type'] = \
"""Type of input tag.
"""

factory.defaults['text.required_class'] = 'required'

factory.defaults['text.default'] = ''

factory.defaults['text.class'] = 'text'

factory.defaults['text.size'] = None
factory.doc['props']['text.size'] = \
"""Allowed input size.
"""

factory.defaults['text.disabled'] = False
factory.doc['props']['text.disabled'] = \
"""Flag wether input field is disabled.
"""

###############################################################################
# hidden
###############################################################################

factory.register('hidden', 
                 [generic_extractor], 
                 [input_generic_renderer])
factory.doc['widget']['hidden'] = \
"""Hidden input widget.
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

factory.register('proxy', 
                 [generic_extractor], 
                 [input_proxy_renderer])
factory.doc['widget']['proxy'] = \
"""Used to pass hidden arguments out of form namespace.
"""

factory.defaults['proxy.class'] = None

###############################################################################
# textarea
###############################################################################

@managedprops('wrap', 'cols', 'rows', 'readonly', *css_managed_props)
def textarea_renderer(widget, data):
    """Renders text area.
    """
    tag = data.tag
    area_attrs = {
        'name_': widget.dottedpath,
        'id': cssid(widget, 'input'),
        'class_': cssclasses(widget, data),            
        'wrap': widget.attrs['wrap'],
        'cols': widget.attrs['cols'],
        'rows': widget.attrs['rows'],
        'readonly': widget.attrs['readonly'] and 'readonly',
    }
    return tag('textarea', fetch_value(widget, data), **area_attrs)

factory.register('textarea', 
                 [generic_extractor, generic_required_extractor], 
                 [textarea_renderer])
factory.doc['widget']['textarea'] = \
"""HTML textarea widget.
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
"""Flag wether textarea is readonly.
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
        Flag wether ascii check should perform.
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
    if not required_strength:
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

@managedprops('size', 'disabled', *css_managed_props)
def password_renderer(widget, data):
    """Render password widget.
    
    The password is never rendered to markup, instead
    ``yafowil.common.PASSWORD_NOCHANGE_VALUE`` is set as ``value`` property on
    dom element. See ``yafowil.common.password_extractor`` for details on
    password extraction.
    
    Properties:
    
    ``size``
        Maximum size of password.
    
    ``disabled``
        Bool evaluating value, if evaluates to True, set disabled="disabled" on
        password input tag.
    """
    tag = data.tag
    def pwd_value(widget, data):
        if data.extracted is not UNSET:
            return data.extracted
        if data.value is not UNSET \
          and data.value is not None:
            return PASSWORD_NOCHANGE_VALUE
        return widget.attrs['default']
    value = pwd_value(widget, data) 
    input_attrs = {
        'type': 'password',
        'value':  value,
        'name_': widget.dottedpath,
        'id': cssid(widget, 'input'),    
        'class_': cssclasses(widget, data),
        'size': widget.attrs.get('size'),
        'disabled': widget.attrs.get('disabled'),
    }
    return tag('input', **input_attrs)

factory.register('password', 
                 [generic_extractor, generic_required_extractor,
                  minlength_extractor, ascii_extractor, password_extractor],
                 [password_renderer],
                 [])
factory.doc['widget']['password'] = \
"""Password widget.
"""

factory.defaults['password.required_class'] = 'required'

factory.defaults['password.default'] = ''
factory.defaults['password.class'] = 'password'

factory.defaults['password.minlength'] = -1
factory.doc['props']['password.minlength'] = \
"""Minlength of password.
"""

factory.defaults['password.ascii'] = False
factory.doc['props']['password.ascii'] = \
"""Flag wether ascii check should performed.
"""

factory.defaults['password.strength'] = 'strength'
factory.defaults['password.strength'] = -1
factory.doc['props']['password.strength'] = \
"""Integer value <= 4. Define how many rules must apply to consider a password
valid.
"""

factory.defaults['weak_password_message'] = u'Password too weak'
factory.doc['props']['password.strength'] = \
"""Message shown if password is not strong enough.
"""

###############################################################################
# checkbox
###############################################################################

@managedprops('format')
def input_checkbox_extractor(widget, data):
    """Extracts data from a single input with type checkbox.
    """
    if '%s-exists' % widget.dottedpath not in data.request:
        return UNSET
    format = widget.attrs['format']
    if format == 'bool':
        return widget.dottedpath in data.request
    elif format == 'string':
        return data.request.get(widget.dottedpath, '')
    raise ValueError, 'Checkbox widget has invalid format % s set' % format

@managedprops('format', *css_managed_props)
def input_checkbox_renderer(widget, data):
    tag = data.tag
    value = fetch_value(widget, data)
    input_attrs = {
        'type': 'checkbox',
        'checked':  value and 'checked' or None,
        'value': value,
        'name_': widget.dottedpath,
        'id': cssid(widget, 'input'),    
        'class_': cssclasses(widget, data),    
    }
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

factory.defaults['checkbox.default'] = False
factory.defaults['checkbox.format'] = 'bool'
factory.defaults['checkbox.required_class'] = 'required'
factory.register('checkbox', 
                 [input_checkbox_extractor, generic_required_extractor], 
                 [input_checkbox_renderer])

###############################################################################
# selection
###############################################################################

@managedprops('format', 'multivalued')
def select_extractor(widget, data):
    extracted = generic_extractor(widget, data)
    if extracted is UNSET \
       and widget.attrs['format'] != 'block' \
       and '%s-exists' % widget.dottedpath in data.request:
        if widget.attrs['multivalued']:
            extracted = []
        else:
            extracted = ''
    return extracted 

@managedprops('format', 'vocabulary', 'multivalued', *css_managed_props)
def select_renderer(widget, data):
    tag = data.tag
    value = fetch_value(widget, data)
    if value is UNSET:
        value = []
    if isinstance(value, basestring) or not hasattr(value, '__iter__'):
        value = [value]
    if widget.attrs['format'] == 'block':
        optiontags = []
        for key, term in vocabulary(widget.attrs.get('vocabulary', [])):
            attrs = {
                'selected': (key in value) and 'selected' or None,
                'value': key,
                'id': cssid(widget, 'input', key),
            }
            optiontags.append(tag('option', term, **attrs))
        select_attrs = {
            'name_': widget.dottedpath,
            'id': cssid(widget, 'input'),
            'class_': cssclasses(widget, data),                        
            'multiple': widget.attrs['multivalued'] and 'multiple' or None,
        }
        return tag('select', *optiontags, **select_attrs)
    else:
        tags = []
        for key, term in vocabulary(widget.attrs.get('vocabulary', [])):
            if widget.attrs['multivalued']:
                tagtype = 'checkbox'
            else:
                tagtype = 'radio'
            attrs = {
                'type': tagtype,
                'value':  key,
                'checked': (key in value) and 'checked' or None,
                'name_': widget.dottedpath,
                'id': cssid(widget, 'input', key),    
                'class_': cssclasses(widget, data),    
            }
            input = tag('input', **attrs)
            text = tag('span', term)
            tags.append(tag('div', input, text, 
                            **{'id': cssid(widget, 'radio', key)}))
        attrs = {
            'type': 'hidden',
            'value':  'exists',
            'name_': "%s-exists" % widget.dottedpath,
            'id': cssid(widget, 'exists'),    
        }
        exists_marker = tag('input', **attrs)            
        return exists_marker + u''.join(tags)
        
factory.defaults['select.multivalued'] = None
factory.defaults['select.default'] = []
factory.defaults['select.format'] = 'block'
factory.register('select', 
                 [select_extractor], 
                 [select_renderer])

###############################################################################
# file
###############################################################################

def file_extracor(widget, data):
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

@managedprops('accept',*css_managed_props)
def input_file_renderer(widget, data):
    tag = data.tag
    input_attrs = {
        'name_': widget.dottedpath,
        'id': cssid(widget, 'input'),
        'class_': cssclasses(widget, data),            
        'type': 'file',
        'value':  '',
    }
    if widget.attrs.get('accept'):
        input_attrs['accept'] = widget.attrs['accept']
    return tag('input', **input_attrs)

@managedprops('vocabulary', *css_managed_props)
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
    
factory.defaults['file.multivalued'] = False
factory.defaults['file.vocabulary'] = [
    ('keep', 'Keep Existing file'),
    ('replace', 'Replace existing file'),
    ('delete', 'Delete existing file'),
]
factory.register('file',
                 [file_extracor, generic_required_extractor],
                 [input_file_renderer, file_options_renderer])

###############################################################################
# submit
###############################################################################

@managedprops('label', 'class', 'action')
def submit_renderer(widget, data):
    tag = data.tag
    input_attrs = {
        'name': widget.attrs['action'] and 'action.%s' % widget.dottedpath,
        'id': cssid(widget, 'input'),
        'class_': widget.attrs.get('class'),
        'type': 'submit',
        'value': widget.attrs.get('label', widget.__name__),
    }
    return tag('input', **input_attrs)

factory.defaults['submit.action'] = None
factory.register('submit', [], [submit_renderer])

###############################################################################
# email
###############################################################################

EMAIL_RE = u'^[a-zA-Z0-9\._\-]+@[a-zA-Z0-9\._\-]+.[a-zA-Z0-9]{2,6}$'

def email_extractor(widget, data):
    val = data.extracted
    if not re.match(EMAIL_RE, val is not UNSET and val or ''):
        raise ExtractionError(u'Input not a valid email address.')
    return val

factory.defaults['email.type'] = 'text'
factory.defaults['email.default'] = ''
factory.defaults['email.required_class'] = 'required'
factory.defaults['email.class'] = 'email'
factory.defaults['email.size'] = None
factory.defaults['email.disabled'] = False
factory.register('email', 
                 [generic_extractor, generic_required_extractor,
                  email_extractor],
                 [input_generic_renderer])

###############################################################################
# label
###############################################################################

@managedprops('position', 'label', 'help', 'help_class', *css_managed_props)
def label_renderer(widget, data):
    tag = data.tag
    label_text = widget.attrs.get('label', widget.__name__)
    label_attrs = {
        'for_': cssid(widget, 'input'),
        'class_': cssclasses(widget, data)
    }
    help = u''
    if widget.attrs['help']:
        help_attrs = {'class_': widget.attrs['help_class']}
        help = tag('div', widget.attrs['help'], help_attrs)
    pos = widget.attrs['position']
    if pos == 'inner':
        return tag('label', label_text, help, data.rendered, **label_attrs)
    elif pos == 'after':
        return data.rendered + tag('label', label_text, help, **label_attrs)
    return tag('label', label_text, help, **label_attrs) + data.rendered

factory.defaults['label.position'] = 'before'
factory.defaults['label.help'] = None
factory.defaults['label.help_class'] = 'help'
factory.register('label', [], [label_renderer])

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

factory.defaults['field.class'] = 'field'
factory.defaults['field.witherror'] = None
factory.register('field', [], [field_renderer])

###############################################################################
# error
###############################################################################

@managedprops('message_class', *css_managed_props)
def error_renderer(widget, data):
    if not data.errors:
        return data.rendered
    tag = data.tag
    msgs = u''
    for error in data.errors:
        msgs += tag('div', str(error), class_=widget.attrs['message_class'])
    return tag('div', msgs, data.rendered, class_=cssclasses(widget, data))

factory.defaults['error.error_class'] = 'error'
factory.defaults['error.message_class'] = 'errormessage'
factory.register('error', [], [error_renderer])