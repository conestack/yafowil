# -*- coding: utf-8 -*-
from node.utils import UNSET
from pkg_resources import iter_entry_points
from yafowil.compat import BYTES_TYPE
from yafowil.compat import IS_PY2
from yafowil.compat import LONG_TYPE
from yafowil.compat import STR_TYPE
from yafowil.compat import UNICODE_TYPE
import json
import logging
import re
import unicodedata
import uuid


class entry_point(object):
    """Decorator for yafowil entry points.
    """

    def __init__(self, order=0):
        self.order = order

    def __call__(self, ob):
        ob.order = self.order
        return ob


_yafowil_plugins = None


def get_plugins(ns=None):
    global _yafowil_plugins
    if _yafowil_plugins is None:
        _yafowil_plugins = list()
        for ep in iter_entry_points('yafowil.plugin'):
            cb = ep.load()
            _yafowil_plugins.append((ep, cb))
        _yafowil_plugins = sorted(
            _yafowil_plugins,
            key=lambda x: getattr(x[1], 'order', 0)
        )
    for ep, cb in _yafowil_plugins:
        if ns is not None and ep.name != ns:
            continue
        yield (ep, cb)


_plugin_names = dict()


def get_plugin_names(ns=None):
    if ns not in _plugin_names:
        _plugin_names[ns] = list(set(
            [ep.dist.project_name for ep, cb in get_plugins(ns=ns)]
        ))
    return _plugin_names[ns]


def get_example(example_name):
    for ep, cb in get_plugins(ns='example'):
        if ep.dist.project_name != example_name:
            continue
        info = cb()
        return info


def get_example_names():
    result = []
    for ep, cb in get_plugins(ns='example'):
        result.append(ep.dist.project_name)
    return result


def vocabulary(definition):
    """Convert different kinds of input into a list of bi-tuples, both strings.
    """
    if callable(definition):
        definition = definition()
    if isinstance(definition, STR_TYPE):
        return [(definition, definition), ]
    # dict-like
    if hasattr(definition, '__getitem__') and hasattr(definition, 'keys'):
        return [(_, definition[_]) for _ in definition.keys()]
    # iterable
    if hasattr(definition, '__iter__'):
        new_vocab = []
        for entry in definition:
            if isinstance(entry, STR_TYPE):
                # entry is a string
                new_vocab.append((entry, entry))
            elif hasattr(entry, '__iter__'):
                # entry is a sequence
                parts = [_ for _ in entry]
                if len(parts) > 1:
                    # take first two parts and skips others
                    new_vocab.append(entry[0:2])
                else:
                    # rare case, inner has one value only
                    new_vocab.append((entry[0], entry[0]))
        return new_vocab
    return definition


class Tag(object):

    def __init__(self, translate):
        self.translate = translate
        self.encoding = 'utf-8'

    def __call__(self, tag_name, *inners, **attributes):
        """Generates some xml/html tag.

        ``tagname``
            name of a valid tag

        ``inners``
            inner content of the tag. If empty a closed tag is generated

        ``attributes``
            attributes of the tag, leading or trailing ``_`` underscores are
            omitted from keywords.

        Example::

            >>> tag('p', 'Lorem Ipsum.', u'Hello World!',
            ...     class_='fancy', id='2f5b8a234ff')
            <p class="fancy" id="2f5b8a234ff">Lorem Ipsum. Hello World.</p>

        """
        cl = list()
        for key, value in attributes.items():
            if value is None or value is UNSET:
                continue
            value = self.translate(value)
            if not isinstance(value, UNICODE_TYPE):
                if isinstance(value, bytes):
                    value = value.decode(self.encoding)
                else:
                    value = str(value)
            cl.append((key.strip('_'), value))
        attributes = u''
        # NOTE: data attributes are enclosed in single quotes, since this makes
        # passing json lists possible. jQuery only recognizes JSON lists in
        # data attributes as such, if they are enclosed in single quotes,
        # because the JSON standard requires string values to be enclosed in
        # double quotes.
        if cl:
            attributes = list()
            for attr in cl:
                if 'data-' in attr[0]:
                    attributes.append(u"{0}='{1}'".format(*attr))
                else:
                    attributes.append(u'{0}="{1}"'.format(*attr))
            attributes = u' {0}'.format(u' '.join(sorted(attributes)))
        cl = list()
        for inner in inners:
            inner = self.translate(inner)
            if not isinstance(inner, UNICODE_TYPE):
                # XXX: inner = str(inner).decode(self.encoding)
                if isinstance(inner, bytes):
                    inner = inner.decode(self.encoding)
                else:
                    inner = str(inner)
            cl.append(inner)
        if not cl:
            return u'<{name}{attrs} />'.format(**{
                'name': tag_name,
                'attrs': attributes,
            })
        return u'<{name}{attrs}>{value}</{name}>'.format(**{
            'name': tag_name,
            'attrs': attributes,
            'value': u''.join(i for i in cl),
        })


# Deprecation message
def _deprecated_null_localization(msg):
    logging.warning(
        "Deprecated usage of 'yafowil.utils.tag', please "
        "use the tag factory on RuntimeData instead."
    )
    return msg


tag = Tag(_deprecated_null_localization)


class managedprops(object):

    def __init__(self, *args):
        self.__yafowil_managed_props__ = args

    def __call__(self, func):
        func.__yafowil_managed_props__ = self.__yafowil_managed_props__
        return func


def cssid(widget, prefix, postfix=None):
    if widget.attrs.get('structural', False):
        return None
    path = widget.dottedpath.replace(u'.', u'-')
    cssid = u'{0}-{1}'.format(prefix, path)
    if postfix is not None:
        cssid = u'{0}-{1}'.format(cssid, postfix)
    return unicodedata.normalize('NFKD', cssid)\
        .encode('ASCII', 'ignore')\
        .replace(b' ', b'_').decode()


def callable_value(value, widget, data):
    """Call value if callable with widget and data as arguments and return
    the callables return value. If value not callable, return as is.
    """
    if not callable(value):
        return value
    return value(widget, data)


def attr_value(key, widget, data, default=None):
    """Return widget attribute value by key or default. If value is callable,
    it's return value is used.
    """
    return callable_value(
        widget.attrs.get(key, default),
        widget,
        data
    )


def as_data_attrs(data):
    """Convert either dict or list of (key, value) pairs into dict containing
    HTML5 data attributes.

    Keys gets prefixed with ``data-``, ``CamelCase`` gets converted
    to ``caml-case``.

    Values are ignored if ``None`` or ``UNSET``. If value is string, it's
    taken as is, otherwise it's assumed that value is list or dict and gets
    dumped as JSON string.

    :param data: Either dict or list of (key, value) pairs.
    :return: Dict containing HTML5 data attributes
    """
    data_attrs = {}
    # no data passed, return empty dict
    if not data:
        return data_attrs
    # expect dict if no list
    if not isinstance(data, list):
        data = data.items()
    for key, val in data:
        # check against None and UNSET separately to please coverage tests
        # rnix, 2014-04-30
        if val is None:
            continue
        if val is UNSET:
            continue
        # convert value to JSON dump if no string.
        if not isinstance(val, STR_TYPE):
            # also remove leading and trailing double quotes,
            # they are not needed for data-attributes
            val = json.dumps(val).strip('"')
        # replace camelCase with camel-case
        key = re.sub(r'([a-z])([A-Z])', r'\g<1>-\g<2>', key).lower()
        data_attrs['data-{0}'.format(key)] = val
    return data_attrs


# B/C: deprecate as of yafowil 2.4, remove in yafowil 3.0
generic_html5_attrs = as_data_attrs


def data_attrs_helper(widget, data, attrs):
    """Creates a dictionary of JSON encoded data-attributes from a list of
    attribute-keys, ready to inject to a tag-renderer as expanded keyword
    arguments.

    :param widget: The yafowil widget.
    :param data: The data object.
    :param attrs: A list of data-attributes-keys to be used to generate the
                  data attributes dictionary.
    :type attrs: list
    :returns: Dictionary with keys as data-attribute-names, prefixed with
              'data-' and values from the widget.
    :rtype: dictionary

    The items in the list are the keys of the attributes for the target tag.
    Each key is prepended with 'data-'. The values are fetched from properties
    set on the widget. If a value is None, it isn't set. Other values are JSON
    encoded, which includes strings, booleans, lists, dicts.

    .. note::
      For camelCase attribute names are automatically split on word boundaries
      and made lowercase (e.g. camel-case). Since jQuery 1.6, the keys are
      converted to camelCase again after getting them with .data().

    .. note::
      The Tag class encloses data-attribute values in single quotes, since the
      JSON standard requires strings to be enclosed in double-quotes. jQuery
      requires this or .data() can't create lists or arrays out of
      data-attribute values.
    """
    items = [(key, attr_value(key, widget, data)) for key in attrs]
    return as_data_attrs(items)


css_managed_props = [
    'class', 'class_add',
    'valid_class', 'valid_class_default',
    'error_class', 'error_class_default',
    'required_class', 'required_class_default',
]


def cssclasses(widget, data, classattr='class', additional=[]):
    _classes = list()
    attrs = widget.attrs
    if attrs['error_class'] and data.errors:
        if isinstance(attrs['error_class'], STR_TYPE):
            _classes.append(attrs['error_class'])
        else:
            _classes.append(attrs['error_class_default'])
    elif attrs['valid_class'] and data.root.extracted:
        if isinstance(attrs['valid_class'], STR_TYPE):
            _classes.append(attrs['valid_class'])
        else:
            _classes.append(attrs['valid_class_default'])
    if attrs['required_class'] and attrs['required']:
        if isinstance(attrs['required_class'], STR_TYPE):
            _classes.append(attrs['required_class'])
        else:
            _classes.append(attrs['required_class_default'])
    if attrs[classattr]:
        _classes += attr_value(classattr, widget, data).split()
    if attrs['class_add']:
        _classes += attr_value('class_add', widget, data).split()
    additional = [add for add in additional if add]
    _classes += additional
    return _classes and ' '.join(sorted(_classes)) or None


class EmptyValue(object):
    """Used to identify empty values in conjunction with data type conversion.
    """

    def __nonzero__(self):
        return False

    __bool__ = __nonzero__

    def __str__(self):
        return ''

    def __len__(self):
        return 0

    def __repr__(self):
        return '<EMPTY_VALUE>'


EMPTY_VALUE = EmptyValue()


DATATYPE_PRECONVERTERS = {
    float: lambda x: isinstance(x, STR_TYPE) and x.replace(',', '.') or x
}
# B/C
DATATYPE_PRECONVERTERS['float'] = DATATYPE_PRECONVERTERS[float]
DATATYPE_CONVERTERS = {
    'str': BYTES_TYPE,
    'unicode': UNICODE_TYPE,
    'int': int,
    'integer': int,
    'long': LONG_TYPE,
    'float': float,
    'uuid': uuid.UUID
}


def convert_value_to_datatype(value, datatype, empty_value=EMPTY_VALUE):
    """Convert given value to datatype.

    Datatype is either a callable or a string out of ``'str'``, ``'unicode'``,
    ``'int'``, ``'integer'``, ``'long'``, ``'float'`` or ``'uuid'``

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
    if isinstance(datatype, STR_TYPE):
        converter = DATATYPE_CONVERTERS[datatype]
    else:
        converter = datatype
    try:
        if isinstance(value, converter):
            return value
    except TypeError:
        # converter is instance of class or function
        pass
    preconverter = DATATYPE_PRECONVERTERS.get(datatype)
    if preconverter:
        value = preconverter(value)
    # special case bytes or str buildin type in python 3
    # uses ascii codec to emulate same behavior as when converting with python2
    # this is supposed to change in future
    if not IS_PY2 and converter in (bytes, str):
        return converter(value, 'ascii')  # pragma: no cover
    return converter(value)


def convert_values_to_datatype(value, datatype, empty_value=EMPTY_VALUE):
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
