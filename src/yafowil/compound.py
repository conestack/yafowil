from odict import odict
from yafowil.base import (
    factory,
)
from yafowil.utils import (
    cssid, 
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
            # XXX First Extracted!?!? looks like a hack
            kw['data'] = data['extracted'][0][childname]
        kw['request'] = data['request']
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

def fieldset_renderer(widget, data):
    fieldset_id = widget.attributes.get('id',{}).get('fieldset', 
                                                     cssid(widget.uname, 
                                                           'fieldset'))
    class_ = widget.attributes.get('class',{}).get('fieldset', None)
    rendered = data.last_rendered
    if widget.attributes.get('legend', False):
        rendered = tag('legend', widget.attributes['legend']) + rendered
    return tag('fieldset', rendered, id=fieldset_id, class_=class_)   

factory.register('fieldset', 
                 factory.extractors('compound'), 
                 factory.renderers('compound') + [fieldset_renderer],
                 factory.preprocessors('compound'))

def form_renderer(widget, data):
    props = widget.attrs
    method = props.get('method', 'post')
    enctype_default = method == 'post' and 'multipart/form-data' or None
    form_attrs = {
        'action': props.action,
        'method': method,
        'enctype': props.get('enctype', enctype_default),
        'class_': props.get('class_'),
        'id': 'form-%s' % '-'.join(widget.path),
    }
    return tag('form', data.last_rendered, **form_attrs)

factory.register('form', 
                 factory.extractors('compound'), 
                 factory.renderers('compound') + [form_renderer],
                 factory.preprocessors('compound'))