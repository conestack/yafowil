from yafowil.base import (
    factory, 
    fetch_value
)
from yafowil.utils import (
    cssid, 
    cssclasses,
    css_managed_props,
    managedprops,
    UNSET
)

def edit_renderer(widget, data):
    return data.rendered

def none_renderer(widget, data):
    return u''

@managedprops(*css_managed_props)
def hidden_renderer(widget, data):
    hidden_attrs = {
        'type': 'hidden',
        'value':  fetch_value(widget, data),
        'name_': widget.dottedpath,
        'id': cssid(widget, 'input'),    
        'class_': cssclasses(widget, data),    
    }
    return data.tag('input', **hidden_attrs)

@managedprops('mode', 'edit', 'none', 'hidden', 'display', 'showbool')
def mode_renderer(widget, data):
    tag = data.tag
    mode = widget.attrs['mode']
    if not isinstance(mode, basestring):
        mode = mode(widget, data)
    ren = widget.attrs.get(mode)
    if ren:
        return ren(widget, data)
    value = data.value
    if isinstance(value, bool):
        value = widget.attrs['showbool'][value and 1 or 0]
    if isinstance(value, basestring):
        return tag('div', value)
    items = [tag('li', item) for item in value]
    return tag('ul', *items)
factory.doc['widget']['mode'] = UNSET
factory.defaults['mode.mode'] = 'edit'
factory.defaults['mode.edit'] = edit_renderer
factory.defaults['mode.none'] = none_renderer
factory.defaults['mode.hidden'] = hidden_renderer
factory.defaults['mode.display'] = None
factory.defaults['mode.showbool'] = ('False', 'True')
factory.register('mode', [], [mode_renderer])