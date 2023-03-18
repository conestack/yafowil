# -*- coding: utf-8 -*-
from node.utils import UNSET
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.compat import BYTES_TYPE
from yafowil.compat import IS_PY2
from yafowil.compat import LONG_TYPE
from yafowil.compat import STR_TYPE
from yafowil.compat import UNICODE_TYPE
from yafowil.tsf import _
from yafowil.utils import EMPTY_VALUE
from yafowil.utils import attr_value
from yafowil.utils import managedprops
import codecs
import uuid
import warnings


@managedprops('emptyvalue')
def generic_emptyvalue_extractor(widget, data):
    """Return emptyvalue if widget present in request and raw value is empty.
    """
    try:
        if not data.request[widget.dottedpath]:
            return attr_value('emptyvalue', widget, data, data.extracted)
    except KeyError:
        pass
    return data.extracted


factory.doc['props']['emptyvalue'] = """\
If configured and received value in request is empty, return as extracted
value.
"""


class DatatypeConverter(object):
    """Value conversion for extraction and rendering."""

    def __init__(self, type_=None):
        self.type_ = type_

    def to_value(self, value):
        """Convert given value on extraction to desired type."""
        try:
            if isinstance(value, self.type_):
                return value
        except TypeError:
            # type is class or function
            pass
        return self.type_(value)

    def to_form(self, value):
        """Convert given value to unicode string for rendering."""
        if not isinstance(value, UNICODE_TYPE):
            value = u'{}'.format(value)
        return value.replace('"', '&quot;')


class BytesDatatypeConverter(DatatypeConverter):
    """Datatype converter for bytes."""

    def to_value(self, value):
        if isinstance(value, BYTES_TYPE):
            return value
        # passed unicode value must contain ascii characters only
        return codecs.escape_decode(value.encode('ascii'))[0]

    def to_form(self, value):
        if isinstance(value, UNICODE_TYPE):
            return value
        return codecs.escape_encode(value)[0].decode('ascii')


class UnicodeDatatypeConverter(DatatypeConverter):
    """Datatype converter for unicode."""

    def __init__(self):
        super(UnicodeDatatypeConverter, self).__init__(UNICODE_TYPE)

    def to_value(self, value):
        if isinstance(value, self.type_):
            return value
        return self.type_(value, encoding='utf-8')


class FloatDatatypeConverter(DatatypeConverter):
    """Datatype converter for float."""

    def __init__(self):
        super(FloatDatatypeConverter, self).__init__(float)

    def to_value(self, value):
        if isinstance(value, STR_TYPE):
            value = value.replace(',', '.')
        return self.type_(value)


DATATYPE_CONVERTERS = {
    BYTES_TYPE: BytesDatatypeConverter(),
    UNICODE_TYPE: UnicodeDatatypeConverter(),
    float: FloatDatatypeConverter()
}

# B/C, will be removed as of yafowil 3.2
LEGACY_DATATYPE_CONVERTERS = {
    'str': BytesDatatypeConverter(),
    'unicode': UnicodeDatatypeConverter(),
    'int': int,
    'integer': int,
    'long': LONG_TYPE,  # long only exists in python 2
    'float': FloatDatatypeConverter(),
    'uuid': uuid.UUID
}


def lookup_datatype_converter(datatype):
    """Lookup datatype converter for given datatype.

    Datatype is either a type or an instance of ``DatatypeConverter``.
    If datatype is a type, an instance of ``DatatypeConverter`` gets created.

    For B/C behavior, datatype can be a string out of 'str', 'unicode',
    'int', 'integer', 'long', 'float' or 'uuid'. This behavior is deprecated
    and will be removed as of yafowil 3.2.
    """
    if isinstance(datatype, STR_TYPE):
        warnings.warn(
            'Passing ``datatype`` as string to ``convert_value_to_datatype`` '
            'is deprecated and will be removed as of yafowil 3.2.'
        )
        converter = LEGACY_DATATYPE_CONVERTERS[datatype]
    else:
        converter = DATATYPE_CONVERTERS.get(datatype, datatype)
    if not isinstance(converter, DatatypeConverter):
        converter = DatatypeConverter(converter)
    return converter


def convert_value_to_datatype(value, datatype, empty_value=EMPTY_VALUE):
    """Convert given value to datatype.

    Uses ``lookup_datatype_converter`` to lookup the appropriate datatype
    converter.

    If value is ``UNSET``, return ``UNSET``, regardless of given datatype.

    If value is ``EMPTY_VALUE``, return ``empty_value``, which defaults to
    ``EMPTY_VALUE`` marker.

    If value is ``None`` or ``''``, return ``empty_value``, which defaults to
    ``EMPTY_VALUE`` marker. Be aware that empty value marker is even returned
    if ``str`` datatype, to provide a consistent behavior.

    Converter callables must raise one out of the following exceptions if
    conversion fails:

        * ``ValueError``
        * ``UnicodeDecodeError``
        * ``UnicodeEncodeError``
    """
    if value is UNSET:
        return UNSET
    if value is EMPTY_VALUE:
        return empty_value
    if value in [None, '']:
        return empty_value
    converter = lookup_datatype_converter(datatype)
    return converter.to_value(value)


def convert_values_to_datatype(value, datatype, empty_value=EMPTY_VALUE):
    """Convert given value(s) to datatype.

    If value is list, each item in list gets converted to datatype.

    ``convert_value_to_datatype`` function is used for each value.

    Returns converted value or list of converted values.
    """
    if isinstance(value, list):
        res = list()
        for item in value:
            res.append(convert_value_to_datatype(
                item,
                datatype,
                empty_value=empty_value
            ))
        return res
    return convert_value_to_datatype(value, datatype, empty_value=empty_value)


DATATYPE_LABELS = {
    BYTES_TYPE: _('datatype_str', default='string'),
    UNICODE_TYPE: _('datatype_unicode', default='unicode'),
    int: _('datatype_integer', default='integer'),
    float: _('datatype_float', default='floating point number'),
    uuid.UUID: _('datatype_uuid', default='UUID')
}
if IS_PY2:  # pragma: no cover
    DATATYPE_LABELS[LONG_TYPE] = _('datatype_long', default='long integer')
else:  # pragma: no cover
    DATATYPE_LABELS[LONG_TYPE] = DATATYPE_LABELS[int]
# B/C, will be removed as of yafowil 3.2
DATATYPE_LABELS['str'] = DATATYPE_LABELS[BYTES_TYPE]
DATATYPE_LABELS['unicode'] = DATATYPE_LABELS[UNICODE_TYPE]
DATATYPE_LABELS['int'] = DATATYPE_LABELS[int]
DATATYPE_LABELS['integer'] = DATATYPE_LABELS[int]
DATATYPE_LABELS['long'] = DATATYPE_LABELS[LONG_TYPE]
DATATYPE_LABELS['float'] = DATATYPE_LABELS[float]
DATATYPE_LABELS['uuid'] = DATATYPE_LABELS[uuid.UUID]


@managedprops(
    'datatype',
    'allowed_datatypes',
    'datatype_message',
    'emptyvalue')
def generic_datatype_extractor(widget, data):
    """Convert extracted value to ``datatype``.

    If extracted value is ``UNSET`` return ``UNSET``.

    If no ``datatype`` given, return extracted value.

    Otherwise try to convert value to given ``datatype`` and return the
    converted value or raise an ``ExtractionError`` if conversion fails.

    Extraction error message can be customized with ``datatype_message``
    property. Value can also be a list, then all items inside the list are
    converted.
    """
    extracted = data.extracted
    if extracted is UNSET:
        return extracted
    # datatype is one of the rare cases where an attribute callable not follows
    # the typical signature taking widget and data as arguments, but is just
    # called with the value.
    datatype = widget.attrs.get('datatype', None)
    if not datatype:
        return extracted
    allowed_datatypes = attr_value('allowed_datatypes', widget, data)
    if allowed_datatypes and datatype not in allowed_datatypes:
        raise ValueError('Datatype not allowed: "{0}"'.format(datatype))
    try:
        emptyvalue = attr_value('emptyvalue', widget, data, EMPTY_VALUE)
        return convert_values_to_datatype(
            extracted,
            datatype,
            empty_value=emptyvalue
        )
    except KeyError:
        raise ValueError('Datatype unknown: "{0}"'.format(datatype))
    except (ValueError, UnicodeEncodeError, UnicodeDecodeError):
        datatype_message = attr_value('datatype_message', widget, data)
        if not datatype_message:
            datatype_label = DATATYPE_LABELS.get(datatype)
            if not datatype_label:
                datatype_message = _(
                    'generic_datatype_message',
                    default=u'Input conversion failed.'
                )
            else:
                if data.tag.translate:
                    datatype_label = data.tag.translate(datatype_label)
                datatype_message = _(
                    'standard_datatype_message',
                    default=u'Input is not a valid ${datatype}.',
                    mapping={
                        'datatype': datatype_label
                    }
                )
        raise ExtractionError(datatype_message)


factory.defaults['datatype'] = None
factory.doc['props']['datatype'] = """\
Datatype is either a type or an instance of ``DatatypeConverter``.
If datatype is a type, an instance of ``DatatypeConverter`` gets created.

For B/C behavior, datatype can be a string out of 'str', 'unicode',
'int', 'integer', 'long', 'float' or 'uuid'. This behavior is deprecated
and will be removed as of yafowil 3.2.

**NOTE**: As of Python 3, string identifiers should not be used at all, but if
you do so, the following rules apply:
    * 'str' maps to ``bytes`` type.
    * 'unicode' maps to ``str`` type.
    * 'long' maps to ``int`` type.

Custom datatype converters must raise one out of the following exceptions if
conversion fails:
    * ``ValueError``
    * ``UnicodeDecodeError``
    * ``UnicodeEncodeError``
"""

factory.defaults['allowed_datatypes'] = UNSET
factory.doc['props']['allowed_datatypes'] = """\
List of allowed datatypes. If ``UNSET``, datatype converters are not
restricted.
"""

factory.defaults['datatype_message'] = None
factory.doc['props']['datatype_message'] = """\
Custom extraction error message if ``datatype`` conversion fails.
"""
