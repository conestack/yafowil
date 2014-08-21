# -*- coding: utf-8 -*-
import inspect
import json
import logging
import re
from pkg_resources import iter_entry_points
from node.utils import UNSET


def get_entry_points(ns=None):
    entry_points = []
    for ep in iter_entry_points('yafowil.plugin'):
        if ns is not None and ep.name != ns:
            continue
        entry_points.append(ep)
    return entry_points


def get_plugin_names(ns=None):
    return list(set([_.dist.project_name for _ in get_entry_points(ns=ns)]))


def get_example(example_name):
    for ep in get_entry_points(ns='example'):
        if ep.dist.project_name != example_name:
            continue
        info = ep.load()()
        return info


def get_example_names():
    result = []
    for ep in get_entry_points(ns='example'):
        result.append(ep.dist.project_name)
    return result


def vocabulary(definition):
    """Convert different kinds of input into a list of bi-tuples, both strings.
    """
    if callable(definition):
        definition = definition()
    if isinstance(definition, basestring):
        return [(definition, definition), ]
    # dict-like
    if hasattr(definition, '__getitem__') and hasattr(definition, 'keys'):
        return [(_, definition[_]) for _ in definition.keys()]
    # iterable
    if hasattr(definition, '__iter__'):
        new_vocab = []
        for entry in definition:
            if isinstance(entry, basestring):
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
            if not isinstance(value, unicode):
                value = str(value).decode(self.encoding)
            cl.append((key.strip('_'), value))
        attributes = u''
        # NOTE: data attributes are enclosed in single quotes, since this makes
        # passing json lists possible. jQuery only recognizes JSON lists in
        # data attributes as such, if they are enclosed in single quotes,
        # because the JSON standard requires string values to be enclosed in
        # double quotes.
        if cl:
            attributes = ['data-' in _[0] and u"%s='%s'" % _ or u'%s="%s"' % _
                          for _ in cl]
            attributes = u' %s' % u' '.join(sorted(attributes))
        cl = list()
        for inner in inners:
            inner = self.translate(inner)
            if not isinstance(inner, unicode):
                inner = str(inner).decode(self.encoding)
            cl.append(inner)
        if not cl:
            return u'<%(name)s%(attrs)s />' % {
                'name': tag_name,
                'attrs': attributes,
            }
        return u'<%(name)s%(attrs)s>%(value)s</%(name)s>' % {
            'name': tag_name,
            'attrs': attributes,
            'value': u''.join(i for i in cl),
        }


# Deprecation message
def _deprecated_null_localization(msg):
    logging.warn("Deprecated usage of 'yafowil.utils.tag', please use the " +
                 "tag factory on RuntimeData instead.")
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
    path = widget.dottedpath.replace('.', '-')
    cssid = "%s-%s" % (prefix, path)
    if postfix is not None:
        cssid = '%s-%s' % (cssid, postfix)
    return cssid


def attr_value(key, widget, data, default=None):
    attr = widget.attrs.get(key, default)
    if callable(attr):
        try:
            return attr(widget, data)
        except Exception, e:  # B/C
            spec = inspect.getargspec(attr)
            if len(spec.args) <= 1 and not spec.keywords:
                logging.warn("Deprecated usage of callback attributes. Please "
                             "accept 'widget' and 'data' as arguments.")
                return attr()
            raise e
    return attr


def generic_html5_attrs(data_dict):
    data_attrs = {}
    if not data_dict:
        return data_attrs  # don't fail on empty data_dict
    for key, val in data_dict.items():
        # check against None and UNSET separately to please coverage tests
        # rnix, 2014-04-30
        if val is None:
            continue
        if val is UNSET:
            continue
        ret = json.dumps(val)  # js-ify
        if isinstance(val, basestring):
            # for strings, remove leading and trailing double quote, since
            # they are not needed for data-attributes
            ret = ret.strip('"')
        # replace camelCase with camel-case
        key = re.sub("([a-z])([A-Z])", "\g<1>-\g<2>", key).lower()
        data_attrs['data-%s' % key] = ret
    return data_attrs


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
      JSON standard requires strings to be enclosed in double-quotes.  jQuery
      requires this or .data() can't create lists or arrays out of
      data-attribute values.

    """
    data_attrs = {}
    for key in attrs:
        val = attr_value(key, widget, data)
        if val is None:
            continue
        ret = json.dumps(val)  # js-ify
        if isinstance(val, basestring):
            # for strings, remove leading and trailing double quote, since
            # they are not needed for data-attributes
            ret = ret.strip('"')
        # replace camelCase with camel-case
        key = re.sub("([a-z])([A-Z])", "\g<1>-\g<2>", key).lower()
        data_attrs['data-%s' % key] = ret
    return data_attrs


css_managed_props = [
    'class', 'class_add',
    'error_class', 'error_class_default',
    'required_class', 'required_class_default',
]


def cssclasses(widget, data, classattr='class', additional=[]):
    _classes = list()
    attrs = widget.attrs
    if attrs['error_class'] and data.errors:
        if isinstance(attrs['error_class'], basestring):
            _classes.append(attrs['error_class'])
        else:
            _classes.append(attrs['error_class_default'])
    if attrs['required_class'] and attrs['required']:
        if isinstance(attrs['required_class'], basestring):
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
