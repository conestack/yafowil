from yafowil.base import (
    factory,
    register_renderer_prefixed,
)
from yafowil.utils import ( 
    tag,
    cssid, 
    cssclasses,
)

def label_renderer(widget, data):
    label_text = widget.attributes.get('label', widget.__name__)
    _classes = list()
    label_attrs = {
        'class_': cssclasses(widget, data, 'label'),
        'id': widget.attributes.get('id',{}).get('label', 
                                                 cssid(widget.uname, 'label')),
        'for_': 'input-%s' % cssid(widget.__name__, 'label'),
    }
    pos = widget.attributes.get('labelpos', None)
    if pos == 'inner':
        return tag('label', label_text, data.last_rendered, **label_attrs)
    elif pos == 'after':
        return data.last_rendered + tag('label', label_text, **label_attrs)
    return tag('label', label_text, **label_attrs) + data.last_rendered


def field_renderer(widget, data):
    div_attrs = {
        'class_': cssclasses(widget, data, 'field', ['field']),
        'id': widget.attributes.get('id',{}).get('field', 
                                                 cssid(widget.uname, 'field')),
    }
    return tag('div', data.last_rendered, **div_attrs)

def register_labeled(registered_name):
    register_renderer_prefixed('label', registered_name, [label_renderer])

def register_as_field(registered_name):
    register_renderer_prefixed('field', registered_name, 
                               [label_renderer, field_renderer])

#
#factory.register('label.text', 
#                 factory.extractors('text'), 
#                 factory.renderers('text') + [label_renderer],
#                 factory.preprocessors('text'))
#
#factory.register('label.select', 
#                 factory.extractors('select'), 
#                 factory.renderers('select') + [label_renderer],
#                 factory.preprocessors('select'))
#
#factory.register('label.file', 
#                 factory.extractors('file'), 
#                 factory.renderers('file') + [label_renderer],
#                 factory.preprocessors('file'))
#
#factory.register('label.textarea', 
#                 factory.extractors('textarea'), 
#                 factory.renderers('textarea') + [label_renderer],
#                 factory.preprocessors('textarea'))
#
#factory.register('label.select_or_add', 
#                 factory.extractors('select_or_add'), 
#                 factory.renderers('select_or_add') + [label_renderer],
#                 factory.preprocessors('select_or_add'))
#
#factory.register('field.text', 
#                 factory.extractors('label.text'), 
#                 factory.renderers('label.text') + [field_renderer],
#                 factory.preprocessors('label.text'))
#
#factory.register('field.select', 
#                 factory.extractors('label.select'), 
#                 factory.renderers('label.select') + [field_renderer],
#                 factory.preprocessors('label.select'))
#
#factory.register('field.file', 
#                 factory.extractors('label.file'), 
#                 factory.renderers('label.file') + [field_renderer],
#                 factory.preprocessors('label.file'))
#
#factory.register('field.textarea', 
#                 factory.extractors('label.textarea'), 
#                 factory.renderers('label.textarea') + [field_renderer],
#                 factory.preprocessors('label.textarea'))
#
#factory.register('field.select_or_add', 
#                 factory.extractors('label.select_or_add'), 
#                 factory.renderers('label.select_or_add') + [field_renderer],
#                 factory.preprocessors('label.select_or_add'))
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