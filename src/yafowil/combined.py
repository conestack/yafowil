import yafowil.standard
import yafowil.compound
from yafowil.base import (
    factory,
    UNSET,
)

def select_or_add_preprocessor(uname, data, properties):
    data['value'] = dict(existing=data['value'])
    widgets = list()
    props = dict(vocabulary=properties['vocabulary'])
    props.update(properties.get('existing', {}))
    props['multiple'] = properties.get('multiple', None)
    widgets.append(factory('select', 'existing', None, props))
    if properties.get('multiple', False):
        widgets.append(factory('textarea', 'new', '', 
                               properties.get('new', {})))
    else:
        widgets.append(factory('text', 'new', None, properties.get('new', {})))
    data['widgets'] = widgets
    data['delegate'] = True
    return data
    
def select_or_add_extractor(uname, data, properties):
    result = list()
    if data.last_extracted['existing']:
        existing = data.last_extracted['existing'].last_extracted
        if existing is not UNSET:
            if not hasattr(existing, '__iter__'):
                existing = [existing]   
            result += existing
    new = data.last_extracted['new'].last_extracted
    if new:
        if properties.get('multiple', False):
            new = new.split('\n')
        if isinstance(new, basestring):
            new = [new]
        [result.append(_) for _ in new if _ not in result]                
    return result

factory.register('select_or_add', 
                 factory.extractors('compound') + 
                    [select_or_add_extractor,
                     yafowil.standard.generic_required_extractor], 
                 factory.renderers('compound'),
                 [select_or_add_preprocessor]+factory.preprocessors('compound'))