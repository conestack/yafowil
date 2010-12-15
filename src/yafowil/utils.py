import logging

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
            if value is None:
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
    
    def __init__(self, *names):
        self._managed_props = names    

    def __call__(self, func):
        return func
    
def cssid(widget, prefix, postfix=None):
    path = widget.dottedpath.replace('.', '-')
    id = "%s-%s" % (prefix, path)
    if postfix is not None:
        id = '%s-%s' % (id, postfix) 
    return id
    
css_managed_props = ['error_class', 'error_class_default',
                     'required_class', 'required_class_default']
def cssclasses(widget, data, classattr='class'):
    _classes = list()
    if widget.attrs['error_class'] and data.errors:
        if isinstance(widget.attrs['error_class'], basestring):
            _classes.append(widget.attrs['error_class'])
        else:
            _classes.append(widget.attrs['error_class_default'])
    if widget.attrs['required_class'] and widget.attrs['required']:
        if isinstance(widget.attrs['required_class'], basestring):
            _classes.append(widget.attrs['required_class'])
        else:
            _classes.append(widget.attrs['required_class_default'])
    if widget.attrs[classattr]:
        _classes+= widget.attrs[classattr].split()
    return _classes and ' '.join(sorted(_classes)) or None