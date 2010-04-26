from yafowil.base import (
    register_renderer_prefixed,
)
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


def field_renderer(widget, data):
    div_attrs = {
        'id': cssid(widget, 'field'),
        'class_': cssclasses(widget, data)
    }
    return tag('div', data.last_rendered, **div_attrs)

def register_as_labeled_and_field(registered_name):
    register_renderer_prefixed('label', registered_name, [label_renderer])
    register_renderer_prefixed('field', registered_name, 
                               [label_renderer, field_renderer])

register_as_labeled_and_field('text')
register_as_labeled_and_field('select')
register_as_labeled_and_field('file')
register_as_labeled_and_field('textarea')
#
#factory.register('field.submit', 
#                 factory.extractors('submit'), 
#                 factory.renderers('submit') + [field_renderer],
#                 factory.preprocessors('submit'))
#
#factory.register('field.array', 
#                 factory.extractors('array'), 
#                 factory.renderers('array') + [label_renderer, field_renderer],
#                 factory.preprocessors('array'))