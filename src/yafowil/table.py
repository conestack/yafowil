from yafowil.base import factory
from yafowil.utils import tag

def table_renderer(widget, data):
    attrs = {
        'id': widget.attrs.get('id'),
        'class_': widget.attrs.get('class'),
    }
    return tag('table', data.rendered, **attrs)

factory.register('table',
                 factory.extractors('compound'),
                 factory.renderers('compound') + [table_renderer])

def thead_renderer(widget, data):
    return tag('thead', data.rendered)

factory.register('thead',
                 factory.extractors('compound'),
                 factory.renderers('compound') + [thead_renderer])

def tbody_renderer(widget, data):
    return tag('tbody', data.rendered)

factory.register('tbody',
                 factory.extractors('compound'),
                 factory.renderers('compound') + [tbody_renderer])

def tr_renderer(widget, data):
    attrs = {
        'id': widget.attrs.get('id'),
        'class_': widget.attrs.get('class'),
    }
    return tag('tr', data.rendered, **attrs)

factory.register('tr',
                 factory.extractors('compound'),
                 factory.renderers('compound') + [tr_renderer])

def th_renderer(widget, data):
    attrs = {
        'id': widget.attrs.get('id'),
        'class_': widget.attrs.get('class'),
        'colspan': widget.attrs.get('colspan'),
        'rowspan': widget.attrs.get('rowspan'),
    }
    return tag('th', data.rendered, **attrs)

factory.register('th',
                 factory.extractors('compound'),
                 factory.renderers('compound') + [th_renderer])

def td_renderer(widget, data):
    attrs = {
        'id': widget.attrs.get('id'),
        'class_': widget.attrs.get('class'),
        'colspan': widget.attrs.get('colspan'),
        'rowspan': widget.attrs.get('rowspan'),
    }
    return tag('td', data.rendered, **attrs)

factory.register('td',
                 factory.extractors('compound'),
                 [td_renderer])