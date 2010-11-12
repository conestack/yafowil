from yafowil.base import factory
from yafowil.utils import tag

def table_renderer(widget, data):
    attrs = {
        'id': widget.attrs.get('id'),
        'class_': widget.attrs.get('class'),
    }
    return tag('table', data.rendered, **attrs)

factory.register('table', [], [table_renderer])

def thead_renderer(widget, data):
    return tag('thead', data.rendered)

factory.register('thead', [], [thead_renderer])

def tbody_renderer(widget, data):
    return tag('tbody', data.rendered)

factory.register('tbody', [], [tbody_renderer])

def tr_renderer(widget, data):
    attrs = {
        'id': widget.attrs.get('id'),
        'class_': widget.attrs.get('class'),
    }
    return tag('tr', data.rendered, **attrs)

factory.register('tr', [], [tr_renderer])

def th_renderer(widget, data):
    attrs = {
        'id': widget.attrs.get('id'),
        'class_': widget.attrs.get('class'),
        'colspan': widget.attrs.get('colspan'),
        'rowspan': widget.attrs.get('rowspan'),
    }
    return tag('th', data.rendered, **attrs)

factory.register('th', [], [th_renderer])

def td_renderer(widget, data):
    attrs = {
        'id': widget.attrs.get('id'),
        'class_': widget.attrs.get('class'),
        'colspan': widget.attrs.get('colspan'),
        'rowspan': widget.attrs.get('rowspan'),
    }
    return tag('td', data.rendered, **attrs)

factory.register('td', [], [td_renderer])