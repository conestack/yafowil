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

# XXX: decouple label and field?
factory.register('field', [], [label_renderer, field_renderer])

def error_extractor(widget, data):
    #XXX:  not called ???
    extracted = data.last_extracted
    if extracted is UNSET or not bool(extracted):
        raise ExtractionError('No password given')
    return extracted

def error_renderer(widget, data):
    errors = ['1', '2', '3']
    content = list()
    for error in errors:
        content.append(tag('p', str(error), class_='errormessage'))
    content += [data.last_rendered]
    return tag('div', *content, class_='error')

factory.register('error', [error_extractor], [error_renderer])