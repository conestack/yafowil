
def cssid(uname, prefix):
    uname = uname.replace('.', '-')
    return "%s-%s" % (prefix, uname)
    
# XXX ist das sinnvoll???
def cssclasses(widget, data, specific, additional=[]):
    _classes = list()
    attr = widget.attributes
    if attr.get('class', {}).get(specific, False):
        _classes.append(attr['class'][specific])      
    if data['errors']:
        _classes.append('error')
    if attr.get('required', None):
        _classes.append('required')        
    if additional:
        _classes += additional
    return _classes and ' '.join(sorted(_classes)) or None