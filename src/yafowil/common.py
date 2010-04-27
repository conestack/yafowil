from yafowil.base import (
    factory,
    UNSET,
    ExtractionError,
)
from utils import (
    cssid,
    cssclasses,
    tag,
    vocabulary,)

def generic_extractor(widget, data):    
    return data['request'].get('.'.join(widget.path), 
                               widget.attrs.get('default', UNSET))               

def generic_required_extractor(widget, data):
    extracted = data.last_extracted
    if widget.attrs.get('required', False) \
       and (extracted is UNSET or not bool(extracted)):
        if isinstance(widget.attributes['required'], basestring):
            raise ExtractionError(widget.attributes['required'])
        raise ExtractionError('Mandatory field was empty')
    return extracted

def input_generic_renderer(widget, data):
    input_attrs = {
        'type': data.get('input_field_type', 0) or \
                widget.attrs.get('type', None),
        'value':  data['extracted'] and data.last_extracted \
                  or data['value'] or '',
        'name_': '.'.join(widget.path),
        'id': cssid(widget, 'input'),    
        'class_': cssclasses(widget, data),    
    }
    return tag('input', **input_attrs)
    
class InputGenericPreprocessor(object):
    
    def __init__(self, inputtype):
        self.inputtype = inputtype
        
    def __call__(self, widget, data):
        data['input_field_type'] = self.inputtype   
        return data 
    
def register_generic_input(subtype):
    factory.register(subtype, 
                     [generic_extractor, generic_required_extractor], 
                     [input_generic_renderer],
                     [InputGenericPreprocessor(subtype)])

register_generic_input('text')
register_generic_input('password')
register_generic_input('hidden')
register_generic_input('radio')
register_generic_input('checkbox')

def input_file_renderer(widget, data):
    input_attrs = {
        'type': 'file',
        'value':  '',
        'name_': '.'.join(widget.path),
        'accept': widget.attrs.get('accept', None),
        'id': cssid(widget, 'input'),
    }
    return tag('input', **input_attrs)
    
factory.register('file', 
                 [generic_extractor, generic_required_extractor], 
                 [input_file_renderer])

def select_renderer(widget, data):
    optiontags = [] 
    attr = widget.attributes
    value = data['extracted'] and data.last_extracted or data['value'] or []
    if isinstance(value, basestring) and attr.get('multiple', False):
        value = [value]
    for key, term in vocabulary(attr.get('vocabulary', [])):
        option_attrs = {
            'selected': (key in value) and 'selected' or None,
            'value': key,
            'id': cssid(widget, 'input', key),
        }
        optiontags.append(tag('option', term, **option_attrs))
    select_attrs = {
        'name_': '.'.join(widget.path),
        'class_': cssclasses(widget, data),
        'id': cssid(widget, 'input'),
        'multiple': attr.get('multiple', None) and 'multiple',
    }
    return tag('select', *optiontags, **select_attrs)

factory.register('select', 
                 [generic_extractor], 
                 [select_renderer])

def textarea_renderer(widget, data):
    attr = widget.attributes
    area_attrs = {
        'name_': '.'.join(widget.path),
        'class_': cssclasses(widget, data),        
        'id': cssid(widget, 'input'),
        'wrap': attr.get('wrap', None),
        'cols': attr.get('cols', 80),
        'rows': attr.get('rows', 25),
        'readonly': attr.get('readonly', None) and 'readonly',
    }
    value = data['extracted'] and data.last_extracted or data['value'] or ''
    return tag('textarea', value, **area_attrs)

factory.register('textarea', 
                 [generic_extractor, generic_required_extractor], 
                 [textarea_renderer])

def submit_renderer(widget, data):
    attrs = widget.attributes
    input_attrs = {
        'id': cssid(widget, 'input'),
        'type': 'submit',
        'class_': attrs.get('class_', ''),
        'value': attrs['label'],
    }
    if attrs.get('action'):
        input_attrs['name_'] = 'action.%s' % '.'.join(widget.path)
    return tag('input', **input_attrs)

factory.register('submit', [], [submit_renderer])

def label_renderer(widget, data):
    label_text = widget.attributes.get('label', widget.__name__)
    label_attrs = {
        'id': cssid(widget, 'label'),
        'for_': cssid(widget, 'input'),
    }
    pos = widget.attributes.get('labelpos') # default rendering 'before'
    if pos == 'inner':
        return tag('label', label_text, data.last_rendered, **label_attrs)
    elif pos == 'after':
        return data.last_rendered + tag('label', label_text, **label_attrs)
    return tag('label', label_text, **label_attrs) + data.last_rendered

factory.register('label', [], [label_renderer])

def field_renderer(widget, data):
    div_attrs = {
        'id': cssid(widget, 'field'),
    }
    return tag('div', data.last_rendered, **div_attrs)

factory.register('field', [], [field_renderer])

def error_renderer(widget, data):
    content = list()
    for error in data['errors']:
        content.append(tag('div', str(error), class_='errormessage'))
    if not content:
        return data.last_rendered
    content += [data.last_rendered]
    return tag('div', *content, class_='error')

factory.register('error', [], [error_renderer])