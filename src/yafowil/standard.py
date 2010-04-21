from yafowil.base import (
    factory,
    tag,
    vocabulary,
    UNSET,
    ExtractionError,
)
from utils import (
    cssclasses,
    cssid,
)

def generic_extractor(widget, data):    
    return data['request'].get(widget.uname, 
                               widget.attributes.get('default', UNSET))               

def generic_required_extractor(widget, data):
    extracted = data.last_extracted     
    if widget.attributes.get('required', False) \
       and extracted is not UNSET \
       and not bool(extracted):
        raise ExtractionError('Mandatory field was empty')
    return extracted

def input_generic_renderer(widget, data):
    attr = widget.attributes
    itype = data.get('input_field_type', 0) or attr.get('type', None)
    input_attrs = {
        'type': itype,
        'class_': cssclasses(widget, data, 'input'),
        'value':  data['extracted'] and data.last_extracted \
                  or data['value'] or '',
        'name_': widget.uname,
        'id': attr.get('id', {}).get('input', cssid(widget.uname, 'input')),        
    }
    return tag('input', **input_attrs)
    
class InputGenericPreprocessor(object):
    
    def __init__(self, inputtype):
        self.inputtype = inputtype
        
    def __call__(self, widget, data):
        data['input_field_type'] = self.inputtype   
        return data 

factory.register('text', 
                 [generic_extractor, generic_required_extractor], 
                 [input_generic_renderer],
                 [InputGenericPreprocessor('text')])

factory.register('hidden', 
                 [generic_extractor, generic_required_extractor], 
                 [input_generic_renderer],
                 [InputGenericPreprocessor('hidden')])

factory.register('radio', 
                 [generic_extractor, generic_required_extractor], 
                 [input_generic_renderer],
                 [InputGenericPreprocessor('radio')])

factory.register('checkbox', 
                 [generic_extractor, generic_required_extractor], 
                 [input_generic_renderer],
                 [InputGenericPreprocessor('checkbox')])

def input_file_renderer(widget, data):
    input_attrs = {
        'type': 'file',              
        'class_': cssclasses(widget, data, 'input'),
        'value':  '',
        'name_': widget.uname,
        'accept': widget.attributes.get('accept', None),
        'id': widget.attributes.get('id', {}).get('input', cssid(widget.uname, 
                                                                 'input')),        
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
            'class_': attr.get('class', {}).get('option', None),
            'selected': (key in value) and 'selected' or None,
            'value': key,
            'id': cssid('%s-%s' % (widget.uname, key), 'input'),
        }
        optiontags.append(tag('option', term, **option_attrs))
    select_attrs = {
        'class_': cssclasses(widget, data, 'input'),
        'name_': widget.uname,
        'id': attr.get('id', {}).get('input', cssid(widget.uname, 'input')),
        'multiple': attr.get('multiple', None) and 'multiple',
    }
    return tag('select', *optiontags, **select_attrs)

factory.register('select', 
                 [generic_extractor], 
                 [select_renderer])

def textarea_renderer(widget, data):
    attr = widget.attributes
    area_attrs = {
        'class_': cssclasses(widget, data, 'input'),
        'name_': widget.uname,
        'id': attr.get('id', {}).get('input', cssid(widget.uname, 'input')),
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
    attr = widget.attributes
    input_attrs = {
        'type': 'submit',
        'class_': attr.get('class',{}).get('input', None),
        'value': attr.get('label', widget.__name__),
        'name_': widget.uname, 
        'id': attr.get('id',{}).get('input', cssid(widget.uname, 'action')),
    }
    return tag('input', **input_attrs)      

factory.register('submit', 
                 [generic_extractor], 
                 [submit_renderer])
