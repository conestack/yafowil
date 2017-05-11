# -*- coding: utf-8 -*-
from node.utils import UNSET
from odict import odict
from yafowil.base import factory
from yafowil.utils import attr_value
from yafowil.utils import css_managed_props
from yafowil.utils import cssclasses
from yafowil.utils import cssid
from yafowil.utils import generic_html5_attrs
from yafowil.utils import managedprops


###############################################################################
# compound
###############################################################################

@managedprops('structural')
def compound_extractor(widget, data):
    """Delegates extraction to children.
    """
    for child in widget.values():
        # regular child widget, extract
        if not attr_value('structural', child, data):
            child.extract(data.request, parent=data)
            continue
        # structural child widget, go one level deeper
        for subchild in child.values():
            # sub child widget may be structural as well
            structural = attr_value('structural', subchild, data)
            # use compound extractor if sub child widget has children and is
            # structural
            if len(subchild) and structural:
                compound_extractor(subchild, data)
            # call extract on sub child widget directly if not structural
            elif not structural:
                subchild.extract(data.request, parent=data)
    return odict([(k, v.extracted) for k, v in data.items()])


def compound_renderer(widget, data):
    """Delegates rendering to children.
    """
    value = widget.getter
    result = u''
    for childname in widget:
        child = widget[childname]
        if attr_value('structural', child, data):
            subdata = data
            if value is not UNSET and child.getter is UNSET:
                child.getter = value
        else:
            subdata = data.get(childname, None)
            if callable(value):
                value = value(widget, data)
            if value is not UNSET and childname in value:
                # XXX: if compound renderer is called multiple times on the
                #      same widget within one form processing cycle
                #      ``child.getter`` has been set, so the condition is True
                #      and ``ValueError`` is raised. Think about widget
                #      instance annotations to mark value delegation already
                #      processed.
                if child.getter is UNSET:
                    child.getter = value[childname]
                else:
                    raise ValueError(
                        u"Both compound and compound member "
                        u"provide a value for '{0}'".format(childname)
                    )
        if subdata is None:
            result += child(request=data.request)
        else:
            result += child(data=subdata)
    return result


factory.register(
    'compound',
    extractors=[compound_extractor],
    edit_renderers=[compound_renderer],
    display_renderers=[compound_renderer])

factory.doc['blueprint']['compound'] = """\
A blueprint to create a compound of widgets. This blueprint creates a node. A
node can contain sub-widgets.
"""

factory.defaults['structural'] = False
factory.doc['props']['structural'] = """\
If a compound is structural, it will be omitted in the dotted-path levels and
will not have an own runtime-data.
"""


###############################################################################
# hybrid
###############################################################################

@managedprops('leaf')
def hybrid_extractor(widget, data):
    """This extractor can be used if a blueprint can act as compound or leaf.
    """
    if len(widget) and not attr_value('leaf', widget, data):
        return compound_extractor(widget, data)
    return data.extracted


@managedprops('leaf')
def hybrid_renderer(widget, data):
    """This renderer can be used if a blueprint can act as compound or leaf.
    """
    if len(widget) and not attr_value('leaf', widget, data):
        rendered = compound_renderer(widget, data)
    else:
        rendered = data.rendered
        if data.rendered is None:
            rendered = u''
    return rendered


factory.defaults['leaf'] = None
factory.doc['props']['leaf'] = """\
Leaf property can be used in conjunction with ``hybrid_extractor`` and
``hybrid_renderer`` using blueprints in order to mark compound widgets as leaf.

If set True, it causes bypassing auto delegation of extraction and rendering
to ``compound_renderer`` respective ``compound_extractor`` if widget contains
children.

This is useful if mixing blueprints which renders and handles compounds on it's
own with blueprints using hybrid rendering and extraction in order to prevent
side effects due to multiple child rendering and extraction.
"""


###############################################################################
# div
###############################################################################

@managedprops('id', *css_managed_props)
def div_renderer(widget, data):
    attrs = {
        'id': attr_value('id', widget, data),
        'class_': cssclasses(widget, data)
    }
    attrs.update(generic_html5_attrs(attr_value('data', widget, data)))
    return data.tag('div', data.rendered, **attrs)


factory.register(
    'div',
    extractors=[hybrid_extractor],
    edit_renderers=[
        hybrid_renderer,
        div_renderer
    ],
    display_renderers=[
        hybrid_renderer,
        div_renderer
    ])

factory.doc['blueprint']['div'] = """\
Blueprint rendering a '<div>' element.

This is a hybrid blueprint. Check ``leaf`` property for details.
"""

factory.defaults['div.id'] = None
factory.doc['props']['div.id'] = """\
Id attribute for div tag.
"""

factory.defaults['div.class'] = None
factory.doc['props']['div.class'] = """\
CSS classes for div tag.
"""

factory.defaults['div.data'] = None
factory.doc['props']['div.data'] = """\
Dict containing data attributes for div tag.
"""


###############################################################################
# fieldset
###############################################################################

@managedprops('legend', *css_managed_props)
def fieldset_renderer(widget, data):
    fs_attrs = {
        'id': cssid(widget, 'fieldset'),
        'class_': cssclasses(widget, data)
    }
    rendered = data.rendered
    legend = attr_value('legend', widget, data)
    if legend:
        rendered = data.tag('legend', legend) + rendered
    return data.tag('fieldset', rendered, **fs_attrs)


factory.register(
    'fieldset',
    extractors=[compound_extractor],
    edit_renderers=[
        compound_renderer,
        fieldset_renderer
    ],
    display_renderers=[
        compound_renderer,
        fieldset_renderer
    ])

factory.doc['blueprint']['fieldset'] = """\
Renders a fieldset around the prior rendered output.
"""

factory.defaults['fieldset.legend'] = False
factory.doc['props']['fieldset.legend'] = """\
Content of legend tag if legend should be rendered.
"""

factory.defaults['fieldset.class'] = None


###############################################################################
# form
###############################################################################

@managedprops('action', 'method', 'enctype', 'novalidate', *css_managed_props)
def form_edit_renderer(widget, data):
    method = attr_value('method', widget, data)
    enctype = method == 'post' and attr_value('enctype', widget, data) or None
    noval = attr_value('novalidate', widget, data) and 'novalidate' or None
    form_attrs = {
        'action': attr_value('action', widget, data),
        'method': method,
        'enctype': enctype,
        'novalidate': noval,
        'class_': cssclasses(widget, data),
        'id': 'form-{0}'.format('-'.join(widget.path)),
    }
    return data.tag('form', data.rendered, **form_attrs)


def form_display_renderer(widget, data):
    return data.tag('div', data.rendered)


factory.register(
    'form',
    extractors=[compound_extractor],
    edit_renderers=[
        compound_renderer,
        form_edit_renderer
    ],
    display_renderers=[
        compound_renderer,
        form_display_renderer
    ])

factory.doc['blueprint']['form'] = """\
A html-form element as a compound of widgets.
"""

factory.defaults['form.method'] = 'post'
factory.doc['props']['form.method'] = """\
One out of ``get`` or ``post``.
"""

factory.doc['props']['form.action'] = """\
Target web address (URL) to send the form to.
"""

factory.defaults['form.enctype'] = 'multipart/form-data'
factory.doc['props']['form.enctype'] = """\
Encryption type of the form. Only relevant for method ``post``. Expect one out
of ``application/x-www-form-urlencoded`` or ``multipart/form-data``.
"""

factory.defaults['form.novalidate'] = True
factory.doc['props']['form.novalidate'] = """\
Flag whether HTML5 form validation should be suppressed.
"""
