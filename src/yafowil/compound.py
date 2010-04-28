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
    fieldset_id = cssid(widget, 'fieldset')
    rendered = data.last_rendered
    if widget.attrs.legend:
        rendered = tag('legend', widget.attrs.legend) + rendered
    return tag('fieldset', rendered, id=fieldset_id)   

factory.defaults['fieldset.legend'] = False
factory.register('fieldset', 
                 factory.extractors('compound'), 
                 factory.renderers('compound') + [fieldset_renderer],
                 factory.preprocessors('compound'))

def form_renderer(widget, data):
    form_attrs = {
        'action': widget.attrs.action,
        'method': widget.attrs.method,
        'enctype': widget.attrs.method=='post' and widget.attrs.enctype or None,
        'class_': widget.attrs.get('class'),
        'id': 'form-%s' % '-'.join(widget.path),
    }
    return tag('form', data.last_rendered, **form_attrs)

factory.defaults['form.method'] = 'post'
factory.defaults['form.enctype'] = 'multipart/form-data'
factory.defaults['form.class'] = None
factory.register('form', 
                 factory.extractors('compound'), 
                 factory.renderers('compound') + [form_renderer],
                 factory.preprocessors('compound'))