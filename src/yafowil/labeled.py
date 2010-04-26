from yafowil.base import factory
from yafowil.utils import ( 
    tag,
    cssid, 
    cssclasses,
)

def label_renderer(widget, data):
    label_text = widget.attributes.get('label', widget.__name__)
    label_attrs = {
        'id': cssid(widget, 'label'),
        'for_': cssid(widget, 'input'),
    }
    pos = widget.attributes.get('labelpos', None)
    if pos == 'inner':
        return tag('label', label_text, data.last_rendered, **label_attrs)
    elif pos == 'after':
        return data.last_rendered + tag('label', label_text, **label_attrs)
    return tag('label', label_text, **label_attrs) + data.last_rendered

factory.register('label', [], [label_renderer])

def field_renderer(widget, data):
    div_attrs = {
        'id': cssid(widget, 'field'),
        'class_': cssclasses(widget, data)
    }
    return tag('div', data.last_rendered, **div_attrs)

factory.register('field', [], [label_renderer, field_renderer])
