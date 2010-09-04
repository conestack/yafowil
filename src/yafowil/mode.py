from yafowil.base import factory
from yafowil.utils import tag, cssid, cssclasses
from yafowil.common import _value

def edit_renderer(widget, data):
    return data.rendered

def none_renderer(widget, data):
    return u''

def hidden_renderer(widget, data):
    hidden_attrs = {
        'type': 'hidden',
        'value':  _value(widget, data),
        'name_': widget.dottedpath,
        'id': cssid(widget, 'input'),    
        'class_': cssclasses(widget, data),    
    }
    return tag('input', **hidden_attrs)

def mode_renderer(widget, data):
    mode = widget.attrs['mode']
    if not isinstance(mode, basestring):
        mode = mode(widget, data)
    ren = widget.attrs.get(mode)
    if ren:
        return ren(widget, data)
    value = data.value
    if isinstance(value, basestring):
        return tag('div', value)
    if isinstance(value, bool):
        if value:
            return tag('div', 'True')
        return tag('div', 'False')
    items = [tag('li', item) for item in value]
    return tag('ul', *items)

factory.defaults['mode.mode'] = 'edit'
factory.defaults['mode.edit'] = edit_renderer
factory.defaults['mode.none'] = none_renderer
factory.defaults['mode.hidden'] = hidden_renderer
factory.defaults['mode.display'] = None
factory.register('mode', [], [mode_renderer])