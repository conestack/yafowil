from odict import odict
from yafowil.base import (
    factory,
    tag,
)

def compound_extractor(widget, data):
    result = dict()    
    for childname in widget:
        result[childname] = widget[childname].extract(data['request'])
    return result

def compound_renderer(widget, data):
    result = u''
    for childname in widget:
        kw = dict() 
        if data['extracted']: 
            kw['data'] = data['extracted'][0][childname] # XXX First Extracted!?!? looks like a hack
        result += widget[childname](**kw)
    return result

def compound_preprocessor(widget, data):
    if widget.attributes.get('delegation', False):
        for childname in widget:
            widget[childname].getter = data['value'].get(childname, None)
    return data
        
factory.register('compound', 
                 [compound_extractor], 
                 [compound_renderer],
                 [compound_preprocessor])

def fieldset_renderer(uname, data, properties):
    fieldset_id = properties.get('id',{}).get('fieldset', cssid(uname, 'fieldset'))
    class_ = properties.get('class',{}).get('fieldset', None)
    rendered = data.last_rendered
    if properties.get('legend', False):
        rendered = tag('legend', properties.get('legend')) + rendered
    return tag('fieldset', rendered, id=fieldset_id, class_=class_)   

factory.register('fieldset', 
                 factory.extractors('compound'), 
                 factory.renderers('compound')+[fieldset_renderer],
                 factory.preprocessors('compound'))

# XXX outdated, controller takes over here
def form_renderer(uname, data, properties):
    method = properties.get('method', None)
    enctype_default = method == 'post' and 'multipart/form-data' or None
    form_attrs = {
        'action': properties['action'],
        'method': method,
        'enctype': properties.get('enctype', enctype_default),
        'class_': properties.get('class', {}).get('form', None),
        'id': properties.get('id', {}).get('form', 'form-%s' % uname),
    }
    return tag('form', data.last_rendered, **form_attrs)

factory.register('form', 
                 factory.extractors('compound'), 
                 factory.renderers('compound')+[form_renderer],
                 factory.preprocessors('compound'))