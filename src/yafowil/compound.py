from yafowil.base import (
    factory,
)
from yafowil.utils import (
    cssid,
    cssclasses, 
    tag,
)

def compound_extractor(widget, data):
    """Delegates extraction to children.
    """
    for childname in widget:
        data[childname] = widget[childname].extract(data.request)
    return None

def compound_renderer(widget, data):
    """Delegates rendering to children."""
    result = u''
    for childname in widget:
        result += widget[childname](data=data.get(childname, None))
    return result

factory.register('compound', 
                 [compound_extractor], 
                 [compound_renderer],
                 [])

# special case, cover later
#def compound_value_delegation_subwidgets(widget, data):
#    for childname in widget:
#        widget[childname].getter = data['value'].get(childname, None)
#    return data
#        

def fieldset_renderer(widget, data):
    fs_attrs = {
        'id': cssid(widget, 'fieldset'),
        'class_': cssclasses(widget, data)
    }
    rendered = data.rendered
    if widget.attrs.legend:
        rendered = tag('legend', widget.attrs.legend) + rendered
    return tag('fieldset', rendered, **fs_attrs)   

factory.defaults['fieldset.legend'] = False
factory.register('fieldset', 
                 factory.extractors('compound'), 
                 factory.renderers('compound') + [fieldset_renderer])

def form_renderer(widget, data):
    form_attrs = {
        'action': widget.attrs.action,
        'method': widget.attrs.method,
        'enctype': widget.attrs.method=='post' and widget.attrs.enctype or None,
        'class_': widget.attrs.get('class'),
        'id': 'form-%s' % '-'.join(widget.path),
    }
    return tag('form', data.rendered, **form_attrs)

factory.defaults['form.method'] = 'post'
factory.defaults['form.enctype'] = 'multipart/form-data'
factory.defaults['form.class'] = None
factory.register('form', 
                 factory.extractors('compound'), 
                 factory.renderers('compound') + [form_renderer])