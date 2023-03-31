# -*- coding: utf-8 -*-
from node.utils import UNSET
from yafowil.base import factory
from yafowil.base import fetch_value
from yafowil.common import display_proxy_renderer
from yafowil.common import generic_display_renderer
from yafowil.common import generic_extractor
from yafowil.common import generic_positional_rendering_helper
from yafowil.common import generic_required_extractor
from yafowil.compat import ITER_TYPES
from yafowil.compat import STR_TYPE
from yafowil.datatypes import convert_value_to_datatype
from yafowil.datatypes import convert_values_to_datatype
from yafowil.datatypes import generic_datatype_extractor
from yafowil.datatypes import generic_emptyvalue_extractor
from yafowil.utils import EMPTY_VALUE
from yafowil.utils import as_data_attrs
from yafowil.utils import attr_value
from yafowil.utils import css_managed_props
from yafowil.utils import cssclasses
from yafowil.utils import cssid
from yafowil.utils import managedprops
from yafowil.utils import vocabulary


###############################################################################
# select
###############################################################################

@managedprops('multivalued', 'disabled')
def select_extractor(widget, data):
    extracted = generic_extractor(widget, data)
    multivalued = attr_value('multivalued', widget, data)
    exists_marker = '{0}-exists'.format(widget.dottedpath)
    if extracted is UNSET and exists_marker in data.request:
        if multivalued:
            extracted = []
        else:
            extracted = ''
    if extracted is UNSET:
        return extracted
    if multivalued and isinstance(extracted, STR_TYPE):
        extracted = [extracted]
    disabled = widget.attrs.get('disabled', False)
    if not disabled:
        return extracted
    if not multivalued:
        return data.value
    disabled_items = disabled is True and data.value or disabled
    if isinstance(disabled_items, STR_TYPE):
        disabled_items = [disabled_items]
    for item in disabled_items:
        if item in extracted and item not in data.value:
            extracted.remove(item)
        elif item not in extracted and item in data.value:
            extracted.append(item)
    return extracted


def select_exists_marker(widget, data):
    tag = data.tag
    attrs = {
        'type': 'hidden',
        'value': 'exists',
        'name_': "{0}-exists".format(widget.dottedpath),
        'id': cssid(widget, 'exists'),
    }
    return tag('input', **attrs)


def select_edit_renderer_props(widget, data):
    value = fetch_value(widget, data)
    multivalued = attr_value('multivalued', widget, data)
    if isinstance(value, STR_TYPE) or not hasattr(value, '__iter__'):
        value = [value]
    datatype = widget.attrs.get('datatype', None)
    if datatype:
        value = convert_values_to_datatype(value, datatype)
    emptyvalue = attr_value('emptyvalue', widget, data, EMPTY_VALUE)
    if not multivalued and len(value) > 1:
        raise ValueError(u'Multiple values for single selection.')
    disabled = attr_value('disabled', widget, data, False)
    return value, multivalued, datatype, emptyvalue, disabled


def select_block_edit_renderer(widget, data, custom_attrs={}):
    value, multivalued, datatype, emptyvalue, disabled = \
        select_edit_renderer_props(widget, data)
    optiontags = []
    vocab = attr_value('vocabulary', widget, data, [])
    for key, term in vocabulary(vocab):
        vval = key
        if datatype:
            vval = convert_value_to_datatype(
                key,
                datatype,
                empty_value=emptyvalue
            )
        key = '' if key in [None, UNSET] else key
        attrs = {
            'selected': 'selected' if vval in value else None,
            'value': key,
            'id': cssid(widget, 'input', key),
        }
        if disabled and disabled is not True and vval in disabled:
            attrs['disabled'] = 'disabled'
        optiontags.append(data.tag('option', term, **attrs))
    autofocus = \
        attr_value('autofocus', widget, data) and 'autofocus' or None
    required = attr_value('required', widget, data) and 'required' or None
    block_class = attr_value('block_class', widget, data)
    select_attrs = {
        'name_': widget.dottedpath,
        'id': cssid(widget, 'input'),
        'title': attr_value('title', widget, data) or None,
        'class_': cssclasses(widget, data, additional=[block_class]),
        'multiple': multivalued and 'multiple' or None,
        'size': attr_value('size', widget, data) or None,
        'placeholder': attr_value('placeholder', widget, data) or None,
        'autofocus': autofocus,
        'required': required,
    }
    select_attrs.update(as_data_attrs(attr_value('data', widget, data)))
    select_attrs.update(custom_attrs)
    if disabled is True:
        select_attrs['disabled'] = 'disabled'
    if not optiontags:
        optiontags = [' ']
    rendered = data.tag('select', *optiontags, **select_attrs)
    if multivalued:
        attrs = {
            'type': 'hidden',
            'value': 'exists',
            'name_': '{0}-exists'.format(widget.dottedpath),
            'id': cssid(widget, 'exists'),
        }
        rendered = select_exists_marker(widget, data) + rendered
    return rendered


def select_cb_edit_renderer(widget, data, custom_attrs={}):
    value, multivalued, datatype, emptyvalue, disabled = \
        select_edit_renderer_props(widget, data)
    tags = []
    label_pos = attr_value('listing_label_position', widget, data)
    if label_pos == 'inner':
        # deprecated, use explicit inner-after or inner-before
        label_pos = 'inner-after'
    listing_tag = attr_value('listing_tag', widget, data)
    item_tag = listing_tag == 'div' and 'div' or 'li'
    if multivalued:
        tagtype = 'checkbox'
        wrapper_class = attr_value('checkbox_wrapper_class', widget, data)
        label_class = attr_value('checkbox_label_class', widget, data)
        input_class_additional = attr_value('checkbox_input_class', widget, data)
        # B/C deprecated as of yafowil 2.2
        if not label_class:
            label_class = attr_value('label_checkbox_class', widget, data)
    else:
        tagtype = 'radio'
        wrapper_class = attr_value('radio_wrapper_class', widget, data)
        label_class = attr_value('radio_label_class', widget, data)
        input_class_additional = attr_value('radio_input_class', widget, data)
        # B/C deprecated as of yafowil 2.2
        if not label_class:
            label_class = attr_value('label_radio_class', widget, data)
    vocab = attr_value('vocabulary', widget, data, [])
    for key, term in vocabulary(vocab):
        vval = key
        if datatype:
            vval = convert_value_to_datatype(
                key,
                datatype,
                empty_value=emptyvalue
            )
        key = '' if key in [None, UNSET] else key
        input_attrs = {
            'type': tagtype,
            'value': key,
            'checked': 'checked' if vval in value else None,
            'name_': widget.dottedpath,
            'id': cssid(widget, 'input', key),
            'class_': cssclasses(
                widget,
                data,
                additional=[input_class_additional]
            ),
        }
        if (disabled and disabled is not True and vval in disabled) \
           or disabled is True:
            input_attrs['disabled'] = 'disabled'
        inputtag = data.tag('input', **input_attrs)
        label_attrs = dict(for_=input_attrs['id'], _class=label_class)
        item = generic_positional_rendering_helper(
            'label', term, label_attrs, inputtag, label_pos, data.tag)
        item_wrapper = data.tag(item_tag, item, **{
            'id': cssid(widget, tagtype, key),
            'class': wrapper_class,
        })
        tags.append(item_wrapper)
    wrapper_attrs = {'id': cssid(widget, tagtype, 'wrapper')}
    wrapper_attrs.update(as_data_attrs(attr_value('data', widget, data)))
    wrapper_attrs.update(custom_attrs)
    taglisting = data.tag(listing_tag, *tags, **wrapper_attrs)
    return select_exists_marker(widget, data) + taglisting


@managedprops(
    'data',
    'title',
    'format',
    'vocabulary',
    'multivalued',
    'disabled',
    'listing_label_position',
    'listing_tag',
    'size',
    'block_class',
    'autofocus',
    'placeholder',
    'datatype',
    'emptyvalue',
    'checkbox_wrapper_class',
    'checkbox_label_class',
    'checkbox_input_class',
    'radio_wrapper_class',
    'radio_label_class',
    'radio_input_class',
    *css_managed_props)
def select_edit_renderer(widget, data, custom_attrs={}):
    if attr_value('format', widget, data) == 'block':
        return select_block_edit_renderer(
            widget,
            data,
            custom_attrs=custom_attrs
        )
    return select_cb_edit_renderer(widget, data, custom_attrs=custom_attrs)


@managedprops('data', 'template', 'class', 'multivalued')
def select_display_renderer(widget, data):
    value = fetch_value(widget, data)
    if type(value) in ITER_TYPES and not value:
        value = u''
    multivalued = attr_value('multivalued', widget, data)
    vocab = dict(attr_value('vocabulary', widget, data, []))
    if not multivalued or not value:
        value = vocab.get(value, value)
        if data.tag.translate:
            value = data.tag.translate(value)
        return generic_display_renderer(widget, data, value=value)
    attrs = {
        'id': cssid(widget, 'display'),
        'class_': 'display-{0}'.format(attr_value('class', widget, data))
    }
    attrs.update(as_data_attrs(attr_value('data', widget, data)))
    content = u''
    if multivalued and isinstance(value, STR_TYPE):
        value = [value]
    for key in value:
        content += data.tag('li', vocab.get(key, key))
    return data.tag('ul', content, **attrs)


factory.register(
    'select',
    extractors=[
        select_extractor,
        generic_required_extractor,
        generic_emptyvalue_extractor,
        generic_datatype_extractor,
    ],
    edit_renderers=[select_edit_renderer],
    display_renderers=[
        select_display_renderer,
        display_proxy_renderer
    ]
)

factory.doc['blueprint']['select'] = """\
Selection Blueprint. Single selection as dropdown or radio-buttons. Multiple
selection as selection-list or as checkboxes.
"""

factory.defaults['select.multivalued'] = None
factory.doc['props']['select.multivalued'] = """\
Flag whether multiple items can be selected.
"""

factory.defaults['select.size'] = None
factory.doc['props']['select.size'] = """\
Size of input if multivalued and format 'block'.
"""

# maybe callable returning '' for single select and [] for multi select
factory.defaults['select.default'] = UNSET

factory.defaults['select.format'] = 'block'
factory.doc['props']['select.format'] = """\
Every value except 'block' results in either a list of radio buttons or
checkboxes depending on the 'multivalued' property.
"""

factory.defaults['select.class'] = 'select'

factory.defaults['select.block_class'] = None
factory.doc['props']['select.block_class'] = """\
CSS class to render on selection if block format.
"""

factory.defaults['select.checkbox_wrapper_class'] = None
factory.doc['props']['select.checkbox_wrapper_class'] = """\
CSS class to render on checkbox wrapper.
"""

factory.defaults['select.checkbox_label_class'] = None
factory.doc['props']['select.checkbox_label_class'] = """\
CSS class to render on checkbox labels.
"""

factory.defaults['select.label_checkbox_class'] = None
factory.doc['props']['select.label_checkbox_class'] = """\
CSS class to render on checkbox labels.

This property is deprecated and will be remove as of yafowil 2.2. Use
``checkbox_label_class`` instead.
"""

factory.defaults['select.checkbox_input_class'] = None
factory.doc['props']['select.checkbox_input_class'] = """\
CSS class to render on checkbox input tag.
"""

factory.defaults['select.radio_wrapper_class'] = None
factory.doc['props']['select.radio_wrapper_class'] = """\
CSS class to render on radio button wrapper.
"""

factory.defaults['select.radio_label_class'] = None
factory.doc['props']['select.radio_label_class'] = """\
CSS class to render on radio button labels.
"""

factory.defaults['select.label_radio_class'] = None
factory.doc['props']['select.label_radio_class'] = """\
CSS class to render on radio button labels.

This property is deprecated and will be remove as of yafowil 2.2. Use
``radio_label_class`` instead.
"""

factory.defaults['select.radio_input_class'] = None
factory.doc['props']['select.radio_input_class'] = """\
CSS class to render on radio button input tag.
"""

factory.defaults['select.listing_tag'] = 'div'
factory.doc['props']['select.listing_tag'] = """\
Desired rendering tag for selection if selection format is 'single'. Valid
values are 'div' and 'ul'.
"""

factory.defaults['select.listing_label_position'] = 'inner-after'
factory.doc['props']['select.listing_label_position'] = """\
Label position if format is 'single'. Behaves the same way as label widget
position property.
"""

factory.doc['props']['select.vocabulary'] = """\
Vocabulary to be used for the selection list. Expects a dict-like or an
iterable or a callable which returns one of both first. An iterable can consist
out of strings or out of tuples with ``(key, value)``. The items in the result
list are in the same order like the vocabulary.
"""

factory.doc['props']['select.disabled'] = """\
Disables the whole widget or single selections. To disable the whole widget
set the value to 'True'. To disable single selection pass a iterable of keys to
disable, i.e. ``['foo', 'baz']``. Defaults to False.
"""

factory.defaults['select.persist'] = True
