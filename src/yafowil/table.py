from yafowil.base import factory
from yafowil.compound import compound_extractor
from yafowil.compound import compound_renderer
from yafowil.compound import hybrid_extractor
from yafowil.utils import attr_value
from yafowil.utils import css_managed_props
from yafowil.utils import cssclasses
from yafowil.utils import managedprops


###############################################################################
# table
###############################################################################

@managedprops('id', *css_managed_props)
def table_renderer(widget, data):
    attrs = {
        'id': attr_value('id', widget, data),
        'class_': cssclasses(widget, data),
    }
    return data.tag('table', data.rendered, **attrs)


factory.register(
    'table',
    extractors=[compound_extractor],
    edit_renderers=[
        compound_renderer,
        table_renderer
    ],
    display_renderers=[
        compound_renderer,
        table_renderer
    ])

factory.doc['blueprint']['table'] = """\
``<table>`` compound widget for table creation.
"""

factory.doc['props']['table.id'] = """\
Value of table id attribute.
"""


###############################################################################
# thead
###############################################################################

def thead_renderer(widget, data):
    return data.tag('thead', data.rendered)


factory.register(
    'thead',
    extractors=[compound_extractor],
    edit_renderers=[
        compound_renderer,
        thead_renderer
    ],
    display_renderers=[
        compound_renderer,
        thead_renderer
    ])

factory.doc['blueprint']['thead'] = """\
``<thead>`` compound widget for table creation.
"""


###############################################################################
# tbody
###############################################################################

def tbody_renderer(widget, data):
    return data.tag('tbody', data.rendered)


factory.register(
    'tbody',
    extractors=[compound_extractor],
    edit_renderers=[
        compound_renderer,
        tbody_renderer
    ],
    display_renderers=[
        compound_renderer,
        tbody_renderer
    ])

factory.doc['blueprint']['tbody'] = """\
``<tbody>`` compound widget for table creation.
"""


###############################################################################
# tr
###############################################################################

@managedprops('id', *css_managed_props)
def tr_renderer(widget, data):
    attrs = {
        'id': attr_value('id', widget, data),
        'class_': cssclasses(widget, data),
    }
    return data.tag('tr', data.rendered, **attrs)


factory.register(
    'tr',
    extractors=[compound_extractor],
    edit_renderers=[
        compound_renderer,
        tr_renderer
    ],
    display_renderers=[
        compound_renderer,
        tr_renderer
    ])

factory.doc['blueprint']['tr'] = """\
``<tr>`` compound widget for table creation.
"""

factory.doc['props']['tr.id'] = """\
Value of id attribute.
"""


###############################################################################
# th
###############################################################################

@managedprops('id', 'rowspan', 'colspan', 'label', *css_managed_props)
def th_renderer(widget, data):
    attrs = {
        'id': attr_value('id', widget, data),
        'class_': cssclasses(widget, data),
        'colspan': attr_value('colspan', widget, data),
        'rowspan': attr_value('rowspan', widget, data),
    }
    contents = attr_value('label', widget, data)
    if not contents:
        contents = data.rendered
    return data.tag('th', contents, **attrs)


factory.register(
    'th',
    edit_renderers=[th_renderer],
    display_renderers=[th_renderer])

factory.doc['blueprint']['th'] = """\
``<th>`` compound widget for table creation.
"""

factory.doc['props']['th.id'] = """\
Value of id attribute.
"""

factory.doc['props']['th.rowspan'] = """\
Value of rowspan attribute.
"""

factory.doc['props']['th.colspan'] = """\
Value of colspan attribute.
"""

factory.doc['props']['th.label'] = """\
Explicit th content. If absent, rendered markup from downstream blueprint(s)
is used.
"""


###############################################################################
# td
###############################################################################

@managedprops('id', 'rowspan', 'colspan', *css_managed_props)
def td_renderer(widget, data):
    attrs = {
        'id': attr_value('id', widget, data),
        'class_': cssclasses(widget, data),
        'colspan': attr_value('colspan', widget, data),
        'rowspan': attr_value('rowspan', widget, data),
    }
    if len(widget):
        rendered = compound_renderer(widget, data)
    else:
        rendered = data.rendered
    return data.tag('td', rendered, **attrs)


factory.register(
    'td',
    extractors=[hybrid_extractor],
    edit_renderers=[td_renderer],
    display_renderers=[td_renderer])

factory.doc['blueprint']['td'] = """\
``<td>`` compound widget for table creation.
"""

factory.doc['props']['td.id'] = """\
Value of id attribute.
"""

factory.doc['props']['td.rowspan'] = """\
Value of rowspan attribute.
"""

factory.doc['props']['td.colspan'] = """\
Value of colspan attribute.
"""
