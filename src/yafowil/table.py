from yafowil.base import factory
from yafowil.utils import (
    cssclasses,
    css_managed_props,
    managedprops,
)

@managedprops('id', *css_managed_props)
def table_renderer(widget, data):
    attrs = {
        'id': widget.attrs.get('id'),
        'class_': cssclasses(widget, data),
    }
    return data.tag('table', data.rendered, **attrs)

factory.doc['widget']['table'] = """\
``<table>`` compound widget for table creation.
"""
factory.register('table',
                 factory.extractors('compound'),
                 factory.renderers('compound') + [table_renderer])

def thead_renderer(widget, data):
    return data.tag('thead', data.rendered)

factory.doc['widget']['thead'] = """\
``<thead>`` compound widget for table creation.
"""
factory.register('thead',
                 factory.extractors('compound'),
                 factory.renderers('compound') + [thead_renderer])

def tbody_renderer(widget, data):
    return data.tag('tbody', data.rendered)

factory.doc['widget']['tbody'] = """\
``<tbody>`` compound widget for table creation.
"""
factory.register('tbody',
                 factory.extractors('compound'),
                 factory.renderers('compound') + [tbody_renderer])

@managedprops('id', *css_managed_props)
def tr_renderer(widget, data):
    attrs = {
        'id': widget.attrs.get('id'),
        'class_': cssclasses(widget, data),
    }
    return data.tag('tr', data.rendered, **attrs)

factory.doc['widget']['tr'] = """\
``<tr>`` compound widget for table creation.
"""
factory.register('tr',
                 factory.extractors('compound'),
                 factory.renderers('compound') + [tr_renderer])

@managedprops('id', 'rowspan', 'colspan', 'label', *css_managed_props)
def th_renderer(widget, data):
    attrs = {
        'id': widget.attrs.get('id'),
        'class_': cssclasses(widget, data),
        'colspan': widget.attrs.get('colspan'),
        'rowspan': widget.attrs.get('rowspan'),
    }
    contents = widget.attrs.get('label')
    if not contents:
        contents = data.rendered
    return data.tag('th', contents, **attrs)

factory.doc['widget']['th'] = """\
``<th>`` compound widget for table creation.
"""
factory.register('th',
                 [],
                 [th_renderer])

@managedprops('id', 'rowspan', 'colspan', *css_managed_props)
def td_renderer(widget, data):
    attrs = {
        'id': widget.attrs.get('id'),
        'class_': cssclasses(widget, data),
        'colspan': widget.attrs.get('colspan'),
        'rowspan': widget.attrs.get('rowspan'),
    }
    return data.tag('td', data.rendered, **attrs)

factory.doc['widget']['td'] = """\
``<td>`` compound widget for table creation.
"""
factory.register('td',
                 [],
                 [td_renderer])