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
                compound_extractor(child[structuralchildname], data)
        else:
            child.extract(data.request, parent=data)


def compound_renderer(widget, data):
    """Delegates rendering to children.
    """
    result = u''
    for childname in widget:
        child = widget[childname]
        if child.attrs.get('structural'):
            subdata = data
        else:
            subdata = data.get(childname, None)
        if subdata is None:
            result += widget[childname](request=data.request)
        else:
            result += widget[childname](data=subdata)
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

factory.defaults['fieldset.class'] = None


@managedprops('action', 'method', 'enctype', *css_managed_props)
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
        form_attrs['action'] =  form_attrs['action'](widget, data)
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