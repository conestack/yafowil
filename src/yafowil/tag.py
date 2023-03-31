# -*- coding: utf-8 -*-
from yafowil.base import factory
from yafowil.utils import as_data_attrs
from yafowil.utils import attr_value
from yafowil.utils import css_managed_props
from yafowil.utils import cssclasses
from yafowil.utils import cssid
from yafowil.utils import managedprops


###############################################################################
# tag
###############################################################################

@managedprops('tag', 'text', 'data', *css_managed_props)
def tag_renderer(widget, data):
    """Renderer for HTML tags.
    """
    attrs = {
        'id': cssid(widget, 'tag'),
        'class_': cssclasses(widget, data),
    }
    attrs.update(as_data_attrs(attr_value('data', widget, data)))
    tag = attr_value('tag', widget, data)
    text = attr_value('text', widget, data)
    return data.tag(tag, text, **attrs)


factory.register(
    'tag',
    edit_renderers=[tag_renderer],
    display_renderers=[tag_renderer]
)

factory.doc['blueprint']['tag'] = """\
Render HTML tags with text. Useful for rendering headings etc.
"""

factory.doc['props']['tag.tag'] = """\
HTML tag name.
"""

factory.doc['props']['tag.text'] = """\
Tag contents.
"""
