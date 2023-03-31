# -*- coding: utf-8 -*-
from node.utils import UNSET
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.base import fetch_value
from yafowil.compat import ITER_TYPES
from yafowil.compat import STR_TYPE
# alias generic_datatype_extractor and generic_emptyvalue_extractor imports
# for now to make deprecated import warnings work
from yafowil.datatypes import generic_datatype_extractor as generic_datatype_extractor_
from yafowil.datatypes import generic_emptyvalue_extractor as generic_emptyvalue_extractor_
from yafowil.datatypes import lookup_datatype_converter
from yafowil.tsf import _
from yafowil.utils import as_data_attrs
from yafowil.utils import attr_value
from yafowil.utils import css_managed_props
from yafowil.utils import cssclasses
from yafowil.utils import cssid
from yafowil.utils import managedprops
from zope.deferredimport import deprecated


###############################################################################
# B/C
###############################################################################

# button
deprecated(
    '``submit_renderer`` has been moved to ``yafowil.button``.',
    submit_renderer='yafowil.button:submit_renderer'
)
deprecated(
    '``button_renderer`` has been moved to ``yafowil.button``.',
    button_renderer='yafowil.button:button_renderer'
)

# checkbox
deprecated(
    '``checkbox_extractor`` has been moved to ``yafowil.checkbox``.',
    checkbox_extractor='yafowil.checkbox:checkbox_extractor'
)
deprecated(
    '``checkbox_edit_renderer`` has been moved to ``yafowil.checkbox``.',
    checkbox_edit_renderer='yafowil.checkbox:checkbox_edit_renderer'
)
deprecated(
    '``checkbox_display_renderer`` has been moved to ``yafowil.checkbox``.',
    checkbox_display_renderer='yafowil.checkbox:checkbox_display_renderer'
)

# datatypes
deprecated(
    '``generic_emptyvalue_extractor`` has been moved to ``yafowil.datatypes``.',
    generic_emptyvalue_extractor='yafowil.datatypes:generic_emptyvalue_extractor'
)
deprecated(
    '``generic_datatype_extractor`` has been moved to ``yafowil.datatypes``.',
    generic_datatype_extractor='yafowil.datatypes:generic_datatype_extractor'
)
deprecated(
    '``DATATYPE_LABELS`` has been moved to ``yafowil.datatypes``.',
    DATATYPE_LABELS='yafowil.datatypes:DATATYPE_LABELS'
)

# email
deprecated(
    '``email_extractor`` has been moved to ``yafowil.email``.',
    email_extractor='yafowil.email:email_extractor'
)

# field
deprecated(
    '``field_renderer`` has been moved to ``yafowil.field``.',
    field_renderer='yafowil.field:field_renderer'
)
deprecated(
    '``label_renderer`` has been moved to ``yafowil.field``.',
    label_renderer='yafowil.field:label_renderer'
)
deprecated(
    '``help_renderer`` has been moved to ``yafowil.field``.',
    help_renderer='yafowil.field:help_renderer'
)
deprecated(
    '``error_renderer`` has been moved to ``yafowil.field``.',
    error_renderer='yafowil.field:error_renderer'
)

# file
deprecated(
    '``file_extractor`` has been moved to ``yafowil.file``.',
    file_extractor='yafowil.file:file_extractor'
)
deprecated(
    '``mimetype_extractor`` has been moved to ``yafowil.file``.',
    mimetype_extractor='yafowil.file:mimetype_extractor'
)
deprecated(
    '``input_file_edit_renderer`` has been moved to ``yafowil.file``.',
    input_file_edit_renderer='yafowil.file:input_file_edit_renderer'
)
deprecated(
    '``convert_bytes`` has been moved to ``yafowil.file``.',
    convert_bytes='yafowil.file:convert_bytes'
)
deprecated(
    '``input_file_display_renderer`` has been moved to ``yafowil.file``.',
    input_file_display_renderer='yafowil.file:input_file_display_renderer'
)
deprecated(
    '``file_options_renderer`` has been moved to ``yafowil.file``.',
    file_options_renderer='yafowil.file:file_options_renderer'
)

# lines
deprecated(
    '``lines_extractor`` has been moved to ``yafowil.lines``.',
    lines_extractor='yafowil.lines:lines_extractor'
)
deprecated(
    '``lines_edit_renderer`` has been moved to ``yafowil.lines``.',
    lines_edit_renderer='yafowil.lines:lines_edit_renderer'
)
deprecated(
    '``lines_display_renderer`` has been moved to ``yafowil.lines``.',
    lines_display_renderer='yafowil.lines:lines_display_renderer'
)

# number
deprecated(
    '``number_extractor`` has been moved to ``yafowil.number``.',
    number_extractor='yafowil.number:number_extractor'
)

# password
deprecated(
    '``minlength_extractor`` has been moved to ``yafowil.password``.',
    minlength_extractor='yafowil.password:minlength_extractor'
)
deprecated(
    '``ascii_extractor`` has been moved to ``yafowil.password``.',
    ascii_extractor='yafowil.password:ascii_extractor'
)
deprecated(
    '``password_extractor`` has been moved to ``yafowil.password``.',
    password_extractor='yafowil.password:password_extractor'
)
deprecated(
    '``password_edit_renderer`` has been moved to ``yafowil.password``.',
    password_edit_renderer='yafowil.password:password_edit_renderer'
)
deprecated(
    '``password_display_renderer`` has been moved to ``yafowil.password``.',
    password_display_renderer='yafowil.password:password_display_renderer'
)

# proxy
deprecated(
    '``input_proxy_renderer`` has been moved to ``yafowil.proxy``.',
    input_proxy_renderer='yafowil.proxy:input_proxy_renderer'
)

# select
deprecated(
    '``select_extractor`` has been moved to ``yafowil.select``.',
    select_extractor='yafowil.select:select_extractor'
)
deprecated(
    '``select_exists_marker`` has been moved to ``yafowil.select``.',
    select_exists_marker='yafowil.select:select_exists_marker'
)
deprecated(
    '``select_edit_renderer_props`` has been moved to ``yafowil.select``.',
    select_edit_renderer_props='yafowil.select:select_edit_renderer_props'
)
deprecated(
    '``select_block_edit_renderer`` has been moved to ``yafowil.select``.',
    select_block_edit_renderer='yafowil.select:select_block_edit_renderer'
)
deprecated(
    '``select_cb_edit_renderer`` has been moved to ``yafowil.select``.',
    select_cb_edit_renderer='yafowil.select:select_cb_edit_renderer'
)
deprecated(
    '``select_edit_renderer`` has been moved to ``yafowil.select``.',
    select_edit_renderer='yafowil.select:select_edit_renderer'
)
deprecated(
    '``select_display_renderer`` has been moved to ``yafowil.select``.',
    select_display_renderer='yafowil.select:select_display_renderer'
)

# url
deprecated(
    '``url_extractor`` has been moved to ``yafowil.url``.',
    url_extractor='yafowil.url:url_extractor'
)

###############################################################################
# common defaults
###############################################################################

factory.defaults['default'] = UNSET
factory.doc['props']['default'] = """\
Default value for rendering.
"""

factory.defaults['class'] = None
factory.doc['props']['class'] = """\
Common CSS-class to put on.
"""

factory.defaults['class_add'] = None
factory.doc['props']['class_add'] = """\
Additional CSS-class to put on.
"""

factory.defaults['error_class'] = None
factory.doc['props']['error_class'] = """\
CSS-class to put on in case of error after extraction.
"""

factory.defaults['error_class_default'] = 'error'
factory.doc['props']['error_class_default'] = """\
Fallback CSS-class to put on in case of error if no specific class was
given.
"""

factory.defaults['valid_class'] = None
factory.doc['props']['valid_class'] = """\
CSS-class to put on in case of valid value after extraction.
"""

factory.defaults['valid_class_default'] = 'valid'
factory.doc['props']['valid_class_default'] = """\
Fallback CSS-class to put on in case of valid value if no specific class was
given.
"""

factory.defaults['autofocus'] = None
factory.doc['props']['autofocus'] = """\
Whether this field gets the focus automatically or not (if browser supports
it).
"""

factory.defaults['autocomplete'] = None
factory.doc['props']['autocomplete'] = """\
Switch autocomplete explizit to ``on`` or ``off``.
"""

factory.defaults['placeholder'] = None
factory.doc['props']['placeholder'] = """\
Whether this input has a placeholder value or not (if browser supports it).
"""

factory.defaults['required'] = False
factory.doc['props']['required'] = """\
Whether this value is required or not.
"""

factory.defaults['required_message'] = _(
    'required_message', default=u'Mandatory field was empty')
factory.doc['props']['required_message'] = """\
Message to be shown if required condition was not met.
"""

factory.defaults['required_class'] = None
factory.doc['props']['required_class'] = """\
CSS-class to put on in case if required condition was not met.
"""

factory.defaults['type'] = None
factory.doc['props']['type'] = """\
HTML type attribute.
"""

factory.defaults['size'] = None
factory.doc['props']['size'] = """\
Allowed input size.
"""

factory.defaults['maxlength'] = None
factory.doc['props']['maxlength'] = """\
Input maxlength.
"""

factory.defaults['disabled'] = None
factory.doc['props']['disabled'] = """\
Disables input.
"""

factory.defaults['required_class_default'] = 'required'
factory.doc['props']['required_class_default'] = """\
CSS-class to apply if required condition was not met - if no specific class
was given.
"""

factory.defaults['template'] = '%s'
factory.doc['props']['template'] = """\
Format string with pythons built-in string format template. If a callable
is given it will be used instead and is called with ``widget`` and ``data`` as
parameters.
"""

factory.defaults['title'] = None
factory.doc['props']['title'] = """\
Optional help text to be rendered in the title attribute.
"""

factory.defaults['data'] = dict()
factory.doc['props']['data'] = """\
Additional data rendered as HTML5 data attributes on DOM Element.
"""

factory.defaults['display_proxy'] = False
factory.doc['props']['display_proxy'] = """\
If 'True' and widget mode 'display', widget value gets rendered as hidden
input.
"""


###############################################################################
# generic
###############################################################################

def generic_extractor(widget, data):
    """Extract raw value from request by ``widget.dottedpath``.

    Return ``UNSET`` if widget not present in request.
    """
    __managed_props = []  # noqa
    try:
        return data.request[widget.dottedpath]
    except KeyError:
        return UNSET


@managedprops('required', 'required_message')
def generic_required_extractor(widget, data):
    """Validate required.

    If ``required`` is set and some raw value has been extracted,
    evaluate ``data.extracted`` to boolean. Raise ``ExtractionError`` if
    ``False``.
    """
    required = attr_value('required', widget, data)
    if not required or bool(data.extracted) or data.extracted is UNSET:
        return data.extracted
    if isinstance(required, STR_TYPE):
        raise ExtractionError(required)
    raise ExtractionError(attr_value('required_message', widget, data))


def input_attributes_common(widget, data, excludes=list(), value=None):
    if value is None:
        value = fetch_value(widget, data)
    datatype = widget.attrs.get('datatype', None)
    if datatype is not None:
        converter = lookup_datatype_converter(datatype)
        value = converter.to_form(value)
    # XXX: get rid of this, we probaly want to have a default datatype
    #      converter here
    elif isinstance(value, STR_TYPE):
        value = value.replace('"', '&quot;')
    autofocus = attr_value('autofocus', widget, data) and 'autofocus' or None
    disabled = attr_value('disabled', widget, data)
    disabled = bool(disabled) and 'disabled' or None
    required = attr_value('required', widget, data) and 'required' or None
    input_attrs = {
        'autofocus': autofocus,
        'class_': cssclasses(widget, data),
        'disabled': disabled,
        'id': cssid(widget, 'input'),
        'name_': widget.dottedpath,
        'placeholder': attr_value('placeholder', widget, data),
        'required': required,
        'size': attr_value('size', widget, data),
        'maxlength': attr_value('maxlength', widget, data),
        'title': attr_value('title', widget, data),
        'type': attr_value('type', widget, data),
        'value': value,
    }
    input_attrs.update(as_data_attrs(attr_value('data', widget, data)))
    for attr_name in excludes:
        del input_attrs[attr_name]
    return input_attrs


def input_attributes_full(widget, data, value=None):
    input_attrs = input_attributes_common(widget, data, value=value)
    input_attrs['autocomplete'] = attr_value(
        'autocomplete', widget, data)
    if attr_value('type', widget, data) in ['range', 'number']:
        input_attrs['min'] = attr_value('min', widget, data)
        input_attrs['max'] = attr_value('max', widget, data)
        input_attrs['step'] = attr_value('step', widget, data)
    return input_attrs


@managedprops(*css_managed_props)
def input_generic_renderer(widget, data, custom_attrs={}):
    """Generic HTML ``input`` tag render.
    """
    input_attrs = input_attributes_full(widget, data)
    input_attrs.update(custom_attrs)
    return data.tag('input', **input_attrs)


# multivalued is not documented, because its only valid for specific blueprints
@managedprops('display_proxy')
def display_proxy_renderer(widget, data):
    rendered = data.rendered
    if attr_value('display_proxy', widget, data):
        orgin_type = attr_value('type', widget, data)
        widget.attrs['type'] = 'hidden'
        value = fetch_value(widget, data)
        multivalued = attr_value('multivalued', widget, data)
        if multivalued and isinstance(value, STR_TYPE):
            value = [value]
        if multivalued or type(value) in ITER_TYPES:
            for val in value:
                input_attrs = input_attributes_full(widget, data, value=val)
                rendered += data.tag('input', **input_attrs)
        else:
            rendered += input_generic_renderer(widget, data)
        if orgin_type:
            widget.attrs['type'] = orgin_type
        else:
            del widget.attrs['type']
    return rendered


@managedprops('template', 'class')
def generic_display_renderer(widget, data, value=None):
    """Generic display renderer to render a value.
    """
    if callable(widget.attrs['template']):
        content = widget.attrs['template'](widget, data)
    elif value is None:
        value = fetch_value(widget, data)
        if value in [UNSET, None]:
            value = u''
        content = widget.attrs['template'] % value
    else:
        content = widget.attrs['template'] % value
    attrs = {
        'id': cssid(widget, 'display'),
        'class_': 'display-{0}'.format(
            attr_value('class', widget, data) or 'generic'
        )
    }
    attrs.update(as_data_attrs(attr_value('data', widget, data)))
    return data.tag('div', content, **attrs)


def empty_display_renderer(widget, data):
    """Display renderer which renders an empty string.
    """
    return data.rendered or u''


def generic_positional_rendering_helper(
        tagname, message, attrs, rendered, pos, tag
    ):
    """returns new tag with rendered content dependent on position

    tagname
        name of new tag, ie. div, p, label and so on

    message
        text included in new tag

    attrs
        attributes on new tag

    rendered
        prior rendered text

    pos
        position how to place the newtag relative to the prior rendered:
        'before'='<newtag>message</newtag>rendered',
        'after' ='<newtag>message</newtag>'
        'inner-before'= <newtag>message rendered</newtag>
        'inner-after'= <newtag>rendered message</newtag>
    """
    if pos not in ['before', 'after', 'inner-before', 'inner-after']:
        raise ValueError('Invalid value for position "{0}"'.format(pos))
    if pos.startswith('inner'):
        if pos.endswith('before'):
            inner = message, rendered
        else:
            inner = rendered, message
        return tag(tagname, *inner, **attrs)
    else:
        newtag = tag(tagname, message, **attrs)
        if pos == 'before':
            return newtag + rendered
        return rendered + newtag


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


###############################################################################
# text
###############################################################################

@managedprops(
    'data',
    'title',
    'size',
    'disabled',
    'autofocus',
    'placeholder',
    'autocomplete',
    *css_managed_props)
def text_edit_renderer(widget, data):
    return input_generic_renderer(widget, data)


factory.register(
    'text',
    extractors=[
        generic_extractor,
        generic_required_extractor,
        generic_emptyvalue_extractor_,
        generic_datatype_extractor_,
    ],
    edit_renderers=[text_edit_renderer],
    display_renderers=[
        generic_display_renderer,
        display_proxy_renderer
    ]
)

factory.doc['blueprint']['text'] = """\
One line text input blueprint.
"""

factory.defaults['text.type'] = 'text'
factory.doc['props']['text.type'] = """\
Type of input tag.
"""

factory.defaults['text.required_class'] = 'required'

factory.defaults['text.default'] = ''

factory.defaults['text.class'] = 'text'

factory.defaults['text.disabled'] = False
factory.doc['props']['text.disabled'] = """\
Flag  input field is disabled.
"""

factory.defaults['text.persist'] = True


###############################################################################
# hidden
###############################################################################

factory.register(
    'hidden',
    extractors=[
        generic_extractor,
        generic_emptyvalue_extractor_,
        generic_datatype_extractor_
    ],
    edit_renderers=[input_generic_renderer],
    display_renderers=[empty_display_renderer]
)

factory.doc['blueprint']['hidden'] = """\
Hidden input blueprint.
"""

factory.defaults['hidden.type'] = 'hidden'
factory.doc['props']['hidden.type'] = """\
Type of input tag.
"""

factory.defaults['hidden.default'] = ''

factory.defaults['hidden.class'] = 'hidden'

factory.defaults['hidden.persist'] = True


###############################################################################
# textarea
###############################################################################

def textarea_attributes(widget, data):
    autofocus = attr_value('autofocus', widget, data) and 'autofocus' or None
    disabled = attr_value('disabled', widget, data) and 'disabled' or None
    readonly = attr_value('readonly', widget, data) and 'readonly' or None
    required = attr_value('required', widget, data) and 'required' or None
    ta_attrs = {
        'autofocus': autofocus,
        'class_': cssclasses(widget, data),
        'cols': attr_value('cols', widget, data),
        'disabled': disabled,
        'id': cssid(widget, 'input'),
        'title': attr_value('title', widget, data),
        'name_': widget.dottedpath,
        'placeholder': attr_value('placeholder', widget, data),
        'readonly': readonly,
        'required': required,
        'rows': attr_value('rows', widget, data),
        'wrap': attr_value('wrap', widget, data),
    }
    ta_attrs.update(as_data_attrs(attr_value('data', widget, data)))
    return ta_attrs


textarea_managed_props = [
    'data', 'title', 'autofocus', 'cols', 'disabled',
    'placeholder', 'readonly', 'required', 'rows', 'wrap',
] + css_managed_props


@managedprops(*textarea_managed_props)
def textarea_renderer(widget, data, custom_attrs={}):
    """Renders text area.
    """
    tag = data.tag
    area_attrs = textarea_attributes(widget, data)
    area_attrs.update(custom_attrs)
    value = fetch_value(widget, data)
    if value is None:
        value = ''
    return tag('textarea', value, **area_attrs)


factory.register(
    'textarea',
    extractors=[
        generic_extractor,
        generic_required_extractor,
        generic_emptyvalue_extractor_
    ],
    edit_renderers=[textarea_renderer],
    display_renderers=[
        generic_display_renderer,
        display_proxy_renderer
    ]
)

factory.doc['blueprint']['textarea'] = """\
HTML textarea blueprint.
"""

factory.defaults['textarea.default'] = ''

factory.defaults['textarea.wrap'] = None
factory.doc['props']['textarea.wrap'] = """\
Either ``soft``, ``hard``, ``virtual``, ``physical`` or  ``off``.
"""

factory.defaults['textarea.class'] = 'textarea'

factory.defaults['textarea.cols'] = 80
factory.doc['props']['textarea.cols'] = """\
Number of characters.
"""

factory.defaults['textarea.rows'] = 25
factory.doc['props']['textarea.rows'] = """\
Number of lines.
"""

factory.defaults['textarea.readonly'] = None
factory.doc['props']['textarea.readonly'] = """\
Flag textarea is readonly.
"""

factory.defaults['textarea.persist'] = True
