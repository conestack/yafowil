from yafowil.base import (
    factory,
    tag,
    cssid,
    vocabulary,
    UNSET,
    ExtractionError,
)

def generic_extractor(uname, data, properties):    
    return data['request'].get(uname, properties.get('default', UNSET))                

def generic_required_extractor(uname, data, properties):
    extracted = data.last_extracted     
    if properties.get('required', False) \
       and extracted is not UNSET \
       and not bool(extracted):
        raise ExtractionError('Mandatory field was empty')
    return extracted

def cssclasses(data, properties, specific, additional=[]):
    _classes = list()
    if properties.get('class', {}).get(specific, False):
        _classes.append(properties['class'][specific])    
    if data.get('class', {}).get(specific, False):
        _classes.append(data['class'][specific])    
    if data['errors']:
        _classes.append('error')
    if properties.get('required', None):
        _classes.append('required')        
    if additional:
        _classes += additional
    return _classes and ' '.join(sorted(_classes)) or None

def input_generic_renderer(uname, data, properties):
    itype = data.get('input_field_type', 0) or properties.get('type', None)
    input_attrs = {
        'type': itype,
        'class_': cssclasses(data, properties, 'input'),
        'value':  data['extracted'] and data.last_extracted \
                  or data['value'] or '',
        'name_': uname,
        'id': properties.get('id', {}).get('input', cssid(uname, 'input')),        
    }
    return tag('input', **input_attrs)
    
class InputGenericPreprocessor(object):
    
    def __init__(self, inputtype):
        self.inputtype = inputtype
        
    def __call__(self, uname, data, properties):
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

def input_file_renderer(uname, data, properties):
    input_attrs = {
        'type': 'file',              
        'class_': cssclasses(data, properties, 'input'),
        'value':  '',
        'name_': uname,
        'accept': properties.get('accept', None),
        'id': properties.get('id', {}).get('input', cssid(uname, 'input')),        
    }
    return tag('input', **input_attrs)
    
factory.register('file', 
                 [generic_extractor, generic_required_extractor], 
                 [input_file_renderer])

def select_renderer(uname, data, properties):
    optiontags = [] 
    value = data['extracted'] and data.last_extracted or data['value'] or []
    if isinstance(value, basestring) \
       and properties.get('multiple', False):
        value = [value]
    for key, term in vocabulary(properties.get('vocabulary', [])):
        option_attrs = {
            'class_': properties.get('class', {}).get('option', None),
            'selected': (key in value) and 'selected' or None,
            'value': key,
            'id': cssid('%s-%s' % (uname, key), 'input'),
        }
        optiontags.append(tag('option', term, **option_attrs))
    select_attrs = {
        'class_': cssclasses(data, properties, 'input'),
        'name_': uname,
        'id': properties.get('id', {}).get('input', cssid(uname, 'input')),
        'multiple': properties.get('multiple', None) and 'multiple',
    }
    return tag('select', *optiontags, **select_attrs)

factory.register('select', 
                 [generic_extractor], 
                 [select_renderer])

def textarea_renderer(uname, data, properties):
    area_attrs = {
        'class_': cssclasses(data, properties, 'input'),
        'name_': uname,
        'id': properties.get('id', {}).get('input', cssid(uname, 'input')),
        'wrap': properties.get('wrap', None),
        'cols': properties.get('cols', 80),
        'rows': properties.get('rows', 25),
        'readonly': properties.get('readonly', None) and 'readonly',
    }
    value = data['extracted'] and data.last_extracted or data['value'] or ''
    return tag('textarea', value, **area_attrs)

factory.register('textarea', 
                 [generic_extractor, generic_required_extractor], 
                 [textarea_renderer])    

def submit_renderer(uname, data, properties):
    input_attrs = {
        'type': 'submit',
        'class_': properties.get('class',{}).get('input', None),
        'value': properties.get('label', uname),
        'name_': uname, 
        'id': properties.get('id',{}).get('input', cssid(uname, 'action')),
    }
    return tag('input', **input_attrs)      

factory.register('submit', 
                 [generic_extractor], 
                 [submit_renderer])
