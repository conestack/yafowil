# -*- coding: utf-8 -*-
from node.utils import UNSET
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.common import generic_required_extractor
from yafowil.common import input_attributes_common
from yafowil.tsf import _
from yafowil.utils import as_data_attrs
from yafowil.utils import attr_value
from yafowil.utils import css_managed_props
from yafowil.utils import cssclasses
from yafowil.utils import cssid
from yafowil.utils import managedprops
from yafowil.utils import vocabulary


###############################################################################
# file
###############################################################################

def file_extractor(widget, data):
    """Return a dict with following keys:

    mimetype
        Mimetype of file.
    headers
        rfc822.Message instance.
    original
        Original file handle from underlying framework.
    file
        File descriptor containing the data.
    filename
        File name.
    action
        widget flags 'new', 'keep', 'replace', 'delete'
    """
    name = widget.dottedpath
    if name not in data.request:
        return UNSET
    if not '{0}-action'.format(name) in data.request:
        value = data.request[name]
        if value:
            value['action'] = 'new'
        return value
    value = data.value
    action = value['action'] = data.request.get(
        '{0}-action'.format(name),
        'keep'
    )
    if action == 'delete':
        value['file'] = UNSET
    elif action == 'replace':
        new_val = data.request[name]
        if not new_val:
            raise ExtractionError(_(
                'file_replace_no_upload',
                default='Cannot replace file. No file uploaded.'
            ))
        value = new_val
        value['action'] = 'replace'
    return value


@managedprops('accept')
def mimetype_extractor(widget, data):
    accept = attr_value('accept', widget, data)
    extracted = data.extracted
    if not extracted or not accept:
        return extracted
    extracted_mimetype = extracted.get('mimetype')
    if not extracted_mimetype:
        return extracted
    extracted_type, extracted_sub = extracted_mimetype.split('/')
    matches = False
    for mimetype in accept.split(','):
        type_, sub = mimetype.split('/')
        if type_ == '*':
            matches = True
            break
        if type_ != extracted_type:
            continue
        if sub == '*':
            matches = True
            break
        if sub == extracted_sub:
            matches = True
            break
    if not matches:
        message = _(
            'file_invalid_mimetype',
            default=u'Mimetype of uploaded file not matches'
        )
        raise ExtractionError(message)
    return extracted


@managedprops(
    'accept',
    'placeholder',
    'autofocus',
    'required',
    *css_managed_props)
def input_file_edit_renderer(widget, data):
    tag = data.tag
    input_attrs = input_attributes_common(widget, data, excludes=['value'])
    input_attrs['type'] = 'file'
    if attr_value('accept', widget, data):
        input_attrs['accept'] = attr_value('accept', widget, data)
    return tag('input', **input_attrs)


def convert_bytes(value):
    value = float(value)
    if value >= 1099511627776:
        terabytes = value / 1099511627776
        size = '{0:.2f}T'.format(terabytes)
    elif value >= 1073741824:
        gigabytes = value / 1073741824
        size = '{0:.2f}G'.format(gigabytes)
    elif value >= 1048576:
        megabytes = value / 1048576
        size = '{0:.2f}M'.format(megabytes)
    elif value >= 1024:
        kilobytes = value / 1024
        size = '{0:.2f}K'.format(kilobytes)
    else:
        size = '{0:.2f}b'.format(value)
    return size


def input_file_display_renderer(widget, data):
    tag = data.tag
    value = data.value
    attrs = {
        'class': cssclasses(widget, data),
    }
    attrs.update(as_data_attrs(attr_value('data', widget, data)))
    if not value:
        no_file_message = _('no_file', default=u'No file')
        return tag('div', no_file_message, **attrs)
    file_val = value['file']
    size = convert_bytes(len(file_val.read()))
    file_val.seek(0)
    unknown_message = _('unknown', default=u'Unknown')
    filename_message = _('filename', default=u'Filename: ')
    mimetype_message = _('mimetype', default=u'Mimetype: ')
    size_message = _('size', default=u'Size: ')
    filename = value.get('filename', unknown_message)
    mimetype = value.get('mimetype', unknown_message)
    return tag(
        'div',
        tag(
            'ul',
            tag('li', tag('strong', filename_message), filename),
            tag('li', tag('strong', mimetype_message), mimetype),
            tag('li', tag('strong', size_message), size)),
        **attrs
    )


@managedprops('vocabulary', *css_managed_props)
def file_options_renderer(widget, data):
    if data.value in [None, UNSET, '']:
        return data.rendered
    tag = data.tag
    if data.request:
        value = [
            data.request.get('{0}-action'.format(widget.dottedpath), 'keep')
        ]
    else:
        value = ['keep']
    tags = []
    vocab = attr_value('vocabulary', widget, data, [])
    for key, term in vocabulary(vocab):
        attrs = {
            'type': 'radio',
            'value': key,
            'checked': (key in value) and 'checked' or None,
            'name_': '{0}-action'.format(widget.dottedpath),
            'id': cssid(widget, 'input', key),
            'class_': cssclasses(widget, data),
        }
        taginput = tag('input', **attrs)
        text = tag('span', term)
        tags.append(tag(
            'div',
            taginput,
            text,
            **{'id': cssid(widget, 'radio', key)}
        ))
    return data.rendered + u''.join(tags)


factory.register(
    'file',
    extractors=[
        file_extractor,
        mimetype_extractor,
        generic_required_extractor
    ],
    edit_renderers=[
        input_file_edit_renderer,
        file_options_renderer
    ],
    display_renderers=[input_file_display_renderer]
)

factory.doc['blueprint']['file'] = """\
A basic file upload blueprint.
"""

factory.defaults['file.accept'] = None
factory.doc['props']['file.accept'] = """\
The accept attribute value is a string that defines the file types the file
input should accept. This string is a comma-separated list of unique file type
specifiers. Because a given file type may be identified in more than one
manner, it's useful to provide a thorough set of type specifiers when you need
files of a given format.
"""

factory.defaults['file.vocabulary'] = [
    ('keep', _('file_keep', default=u'Keep Existing file')),
    ('replace', _('file_replace', default=u'Replace existing file')),
    ('delete', _('file_delete', default=u'Delete existing file')),
]
factory.doc['props']['file.vocabulary'] = """\
Vocabulary with available actions for existing files.
"""
