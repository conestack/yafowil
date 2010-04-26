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

def tag(name, *inners, **attributes):
    """Generates some xml/html tag.
        
    ``name``
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
        if not isinstance(value, unicode):
            value = str(value).decode('utf-8')
        cl.append((key.strip('_'), value))
    attributes = u''
    if cl:
        attributes = u' %s' % u' '.join(sorted([u'%s="%s"' % _ for _ in cl]))     
    cl = list()
    for inner in inners:
        if not isinstance(inner, unicode):
            inner = str(inner).decode('utf-8')
        cl.append(inner)
    if not cl:
        return u'<%(name)s%(attrs)s />' % {
            'name': name,
            'attrs': attributes,
        }
    return u'<%(name)s%(attrs)s>%(value)s</%(name)s>' % {
        'name': name,
        'attrs': attributes,
        'value': u''.join(i for i in cl),
    }

def cssid(widget, prefix, postfix=None):
    id = "%s-%s" % (prefix, '-'.join(widget.path))
    if postfix is not None:
        id = '%s-%s' % (id, postfix) 
    return id
    
def cssclasses(widget, data, additional=[]):
    _classes = list()
    if data['errors']:
        _classes.append('error')
    if widget.attrs.get('required', False):
        _classes.append('required')        
    if additional:
        _classes += additional
    return _classes and ' '.join(sorted(_classes)) or None