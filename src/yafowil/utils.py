import logging
from pkg_resources import iter_entry_points


def get_entry_points(ns=None):
    entry_points = []
    for ep in iter_entry_points('yafowil.plugin'):
        if ns is not None and ep.name != ns:
            continue
        entry_points.append(ep)
    return entry_points


def get_plugin_names(ns=None):
    return list(set([_.module_name for _ in get_entry_points(ns=ns)]))


def get_resource_directory(module_name):
    result = []
    for ep in get_entry_points(ns='resourcedir'):
        if ep.module_name != module_name:
            continue
        return ep.load()()


def _get_filepaths(module_name, ns, thirdparty):    
    for ep in get_entry_points(ns=ns):
        if ep.module_name == module_name:
            return ep.load()(thirdparty=thirdparty)
    return []


def get_javascripts(module_name, thirdparty=True):
    return _get_filepaths(module_name, 'javascripts', thirdparty)


def get_stylesheets(module_name, thirdparty=True):
    return _get_filepaths(module_name, 'stylesheets', thirdparty)


class Unset(object): 
    
    def __nonzero__(self):
        return False
    
    def __str__(self):
        return ''
    
    def __len__(self):
        return 0
    
    def __repr__(self):
        return '<UNSET>'

UNSET = Unset()


def vocabulary(definition):
    """Convert different kinds of input into a list of bi-tuples, both strings.
    """
    if callable(definition):
        definition = definition() 
    if isinstance(definition, basestring):
        return [(definition, definition),]
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
        if cl:
            attributes = u' %s' % u' '.join(sorted([u'%s="%s"' % _ for _ in cl]))     
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


## Deprecation message
def _deprecated_null_localization(msg):
    logging.warn("Deprecated usage of 'yafowil.utils.tag', please use the "+\
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
    path = widget.dottedpath.replace('.', '-')
    id = "%s-%s" % (prefix, path)
    if postfix is not None:
        id = '%s-%s' % (id, postfix) 
    return id


css_managed_props = ['class', 'error_class', 'error_class_default',
                     'required_class', 'required_class_default']

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
        _classes += attrs[classattr].split()
    _classes += additional
    return _classes and ' '.join(sorted(_classes)) or None