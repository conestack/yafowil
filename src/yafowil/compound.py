from yafowil.base import factory
from yafowil.utils import (
    UNSET,
    cssid,
    cssclasses,
    css_managed_props,
    managedprops,
)

@managedprops('structural')
def compound_extractor(widget, data):
    """Delegates extraction to children.
    """
    for childname in widget:
        child = widget[childname]
        if child.attrs.get('structural'):
            for structuralchildname in child:
                compound_extractor(child[structuralchildname], data)
        else:
            childdata = child.extract(data.request, parent=data)
    return

def compound_renderer(widget, data):
    """Delegates rendering to children."""
    result = u''
    for childname in widget:
        subdata = data.get(childname, None)
        if subdata is None:
            result += widget[childname](request=data.request)
        else:
            result += widget[childname](data=subdata)
    return result

factory.register('compound', 
                 [compound_extractor], 
                 [compound_renderer],
                 [])

@managedprops('legend', *css_managed_props)
def fieldset_renderer(widget, data):
    fs_attrs = {
        'id': cssid(widget, 'fieldset'),
        'class_': cssclasses(widget, data)
    }
    rendered = data.rendered
    if widget.attrs['legend']:
        rendered = data.tag('legend', widget.attrs['legend']) + rendered
    return data.tag('fieldset', rendered, **fs_attrs)   

factory.defaults['fieldset.legend'] = False
factory.defaults['fieldset.class'] = None
factory.register('fieldset', 
                 factory.extractors('compound'), 
                 factory.renderers('compound') + [fieldset_renderer])

@managedprops('action', 'method', 'enctype', *css_managed_props)
def form_renderer(widget, data):
    form_attrs = {
        'action': widget.attrs['action'],
        'method': widget.attrs['method'],
        'enctype': widget.attrs['method']=='post' and \
                   widget.attrs['enctype'] or None,
        'class_': cssclasses(widget, data),
        'id': 'form-%s' % '-'.join(widget.path),
    }
    if callable(form_attrs['action']):
        form_attrs['action'] =  form_attrs['action'](widget, data)
    return data.tag('form', data.rendered, **form_attrs)

factory.defaults['form.method'] = 'post'
factory.defaults['form.enctype'] = 'multipart/form-data'
factory.defaults['form.class'] = None
factory.register('form', 
                 factory.extractors('compound'), 
                 factory.renderers('compound') + [form_renderer])