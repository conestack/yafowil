from odict import odict
from yafowil.base import factory
from yafowil.utils import (
    UNSET,
    cssid,
    cssclasses,
    css_managed_props,
    managedprops,
)


@managedprops('structural')
def compound_extractor(widget, data):
    """Delegates extraction to children.
    """
    for childname in widget:
        child = widget[childname]
        if child.attrs.get('structural'):
            for structuralchildname in child:
                structuralchild = child[structuralchildname]
                if len(structuralchild) \
                  and structuralchild.attrs.get('structural'):
                    # call compound extractor if structural child has children
                    # which are as well structural compounds.
                    compound_extractor(structuralchild, data)
                else:
                    # call extract on widget directly
                    structuralchild.extract(data.request, parent=data)
        else:
            child.extract(data.request, parent=data)
    return odict([(k, v.extracted) for k, v in data.items()])


def compound_renderer(widget, data):
    """Delegates rendering to children.
    """
    value = widget.getter
    result = u''
    for childname in widget:
        child = widget[childname]
        if child.attrs.get('structural'):
            subdata = data
            if value is not UNSET and child.getter is UNSET:
                child.getter = value
        else:
            subdata = data.get(childname, None)
            if callable(value):
                value = value(widget, data)
            if value is not UNSET and childname in value:
                if child.getter is UNSET:
                    child.getter = value[childname]
                else:
                    raise ValueError(u"Both compound and compound member "
                                     u"provide a value for '%s'" % childname)
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


def hybrid_extractor(widget, data):
    """This extractor can be used if a blueprint can act as compound or leaf.
    """
    if len(widget):
        return compound_extractor(widget, data)
    return data.extracted


@managedprops('id', *css_managed_props)
def div_renderer(widget, data):
    attrs = {
        'id': widget.attrs.get('id'),
        'class_': cssclasses(widget, data),
    }
    if len(widget):
        rendered = compound_renderer(widget, data)
    else:
        rendered = data.rendered
    return data.tag('div', rendered, **attrs)


factory.register(
    'div',
    extractors=[hybrid_extractor],
    edit_renderers=[div_renderer],
    display_renderers=[div_renderer])

factory.doc['blueprint']['div'] = """\
Like ``compound`` blueprint but renders within '<div>' element.
"""

factory.defaults['div.id'] = None
factory.doc['props']['div.id'] = \
"""HTML id attribute.
"""


@managedprops('legend', *css_managed_props)
def fieldset_renderer(widget, data):
    fs_attrs = {
        'id': cssid(widget, 'fieldset'),
        'class_': cssclasses(widget, data)
    }
    rendered = data.rendered
    if widget.attrs['legend']:
        rendered = data.tag('legend', widget.attrs['legend']) + rendered
    return data.tag('fieldset', rendered, **fs_attrs)


factory.register(
    'fieldset',
    extractors=factory.extractors('compound'),
    edit_renderers=factory.edit_renderers('compound') + [fieldset_renderer],
    display_renderers=factory.display_renderers('compound') + \
        [fieldset_renderer])

factory.doc['blueprint']['fieldset'] = """\
Renders a fieldset around the prior rendered output.
"""

factory.defaults['fieldset.legend'] = False
factory.doc['props']['fieldset.legend'] = \
"""Content of legend tag if legend should be rendered.
"""

factory.defaults['fieldset.class'] = None


@managedprops('action', 'method', 'enctype', 'novalidate', *css_managed_props)
def form_edit_renderer(widget, data):
    form_attrs = {
        'action': widget.attrs['action'],
        'method': widget.attrs['method'],
        'enctype': widget.attrs['method'] == 'post' and \
                   widget.attrs['enctype'] or None,
        'novalidate': widget.attrs['novalidate'] and 'novalidate' or None,
        'class_': cssclasses(widget, data),
        'id': 'form-%s' % '-'.join(widget.path),
    }
    if callable(form_attrs['action']):
        form_attrs['action'] = form_attrs['action'](widget, data)
    return data.tag('form', data.rendered, **form_attrs)


def form_display_renderer(widget, data):
    return data.tag('div', data.rendered)


factory.register(
    'form',
    extractors=factory.extractors('compound'),
    edit_renderers=factory.edit_renderers('compound') + [form_edit_renderer],
    display_renderers=factory.display_renderers('compound') + \
        [form_display_renderer])

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
factory.doc['props']['form.novalidate'] = \
"""Flag whether HTML5 form validation should be suppressed.
"""
