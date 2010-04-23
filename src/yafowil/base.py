from zodict import LifecycleNode

class Unset(object): 
    
    def __nonzero__(self):
        return False
    
    def __str__(self):
        return ''
    
    def __repr__(self):
        return '<UNSET>'

UNSET = Unset()

callable = lambda o: hasattr(o, '__call__')

class RuntimeData(dict):
    """Holds Runtime data of widget."""
    
    def __init__(self, *args, **kw):
        super(RuntimeData, self).__init__(*args, **kw)
        self['extracted'] = list()
        self['rendered'] = list()
        self['errors'] = list()
        
    def _last(self, key, default):
        if not len(self[key]):
            return default
        return self.get(key)[-1]    
        
    @property
    def last_extracted(self):
        return self._last('extracted', UNSET)

    @property
    def last_rendered(self):
        return self._last('rendered', u'')
    
    @property
    def has_extracted(self):
        """looks if some value was extracted.
        
        It always looks at last_extracted and goes then recursively into the 
        tree of runtimedata. It considers a tree when a) last_extracted is a 
        dict instance and all contained values are RuntimeData instances or b)
        if last_extracted is a list and all contained values are RuntimeData 
        instances. Mixing RuntimeData instances at this level with non 
        RuntimeData is not allowed and will this method make fail.
        """
        last = self.last_extracted
        if not isinstance(last, dict):
            if isinstance(last, list) and \
               [_ for _ in last if isinstance(_, self.__class__)]:
                return bool([_ for _ in last if _.has_extracted])
            return bool(last)
        values = last.values()
        lvalues = len(values)
        ldata = len([_ for _ in values if isinstance(_, self.__class__)])
        if not ldata:
            return bool(values)
        if ldata!=lvalues:
            raise ValueError
        for value in values:
            if value.has_extracted:             
                return True
        return False        
                    
    def __repr__(self):
        va = ', '.join(["'%s': %s" % (_, repr(self[_])) \
                        for _ in sorted(self.keys()) ])
        return '{%s}' % va

class ExtractionError(Exception):
    """Indicates problems on extraction time, such as conversion, validation
    or similar problems.""" 
    
    def __init__(self, msg, abort=True):       
        """Initialize Exception
        
        ``msg`` 
            error message - usally best unicode in one-liner style.
                    
        ``abort``
            if True the extraction chain continues. Default to False, which 
            stops extraction.
        
        """
        super(ExtractionError, self).__init__(msg)
        self.abort = abort

class Widget(LifecycleNode):
    """Base Widget Class
    """
    def __init__(self, extractors, renderers, preprocessors, 
                 uniquename=None, value_or_getter=None, properties=dict()):
        """Initialize the widget. 
            
        ``extractors``
            list of callables extracting the data and returning it. Each 
            extractor in chain is called. Expects to raise 
            ``ExtractionException`` and provide error-message if something went 
            wrong. You can call this validation. 
            Need to accept some ``request`` (dict like object), ``value`` 
            (same as while rendering), ``uniquename`` and ``properties``, a 
            dict-like. Properties gets a key ``extracted`` set, a list of 
            results of previous extractors in chain-   
            
        ``renderers``
            list of callables rendering widget. Need to accept ``value``, 
            ``uniquename`` and properties as dict-like. Properties gets a key 
            ``rendered`` set, a list of results of previous extractors in chain.

        ``preprocessors``
            list of callables executed before extract or rendering. Executed 
            only once for a given runtime data. has same signature a s extract.
             
        ``uniquename``
            id as string containing characters from a-z, A-Z, 0-9 only. Must not
            start with numerical character. 
            
        ``value_or_getter``
            either a callable or the value itself. If callable, its called 
            before passing to given ``renderer`` 
                        
        ``properties``
            arbitrary dict-like passed through for use in renderer and 
            extractor, static data must never be modifed!
        """
        super(Widget, self).__init__(uniquename)
        self.getter = value_or_getter
        self.extractors = extractors
        self.renderers = renderers
        self.preprocessors = preprocessors or list()
        self.__name__ = uniquename
        for key in properties:
            self.attributes[key] = properties[key]
    
    def _value(self, request):
        if callable(self.getter):
            return self.getter(request)
        return self.getter
        
    def __call__(self, request={}, data=None):
        """renders the widget.
        
        ``request`` 
            expects a dict-like object, if non-empty given extraction takes 
            place before rendering.      
        
        ``data``
            runtime data, information collected in one run of the widget. May be
            passed in i.e if extract was called seperate before it should not 
            run twice. Expects either a dict-like object or None to create an 
            empty dict.
        """
        if data is None:
            data = RuntimeData()
        data = self._runpreprocessors(request, data)
        if request and not data['extracted']:
            self.extract(request)
        for renderer in self.renderers:
            try:
                value = renderer(self, data)
            except Exception, e:
                e.args = [_ for _ in e.args]+[str(renderer)]
                raise e
            
            data['rendered'].append(value)
        return data.last_rendered
    
    def __setitem__(self, name, widget):
        if not widget.__name__:
            widget.__name__ = name
        LifecycleNode.__setitem__(self, name, widget)
    
    def extract(self, request):
        """extract the data from the request by calling the given extractors. 
        
        ``request`` 
            expects a dict-like object       

        """
        data = self._runpreprocessors(request, RuntimeData())
        for extractor in self.extractors:            
            try:
                value = extractor(self, data)
            except ExtractionError, e:
                data['errors'].append(e)
                if e.abort:
                    break
            except Exception, e:
                e.args = [_ for _ in e.args]+[str(extractor)]
                raise e
            else:
                data['extracted'].append(value)
        return data
    
    @property
    def uname(self):
        return '.'.join(self.path)

    def _runpreprocessors(self, request, data):                
        if 'value' in data and 'request' in data:
            return data
        data['value'] = self._value(request)
        data['request'] = request
        for pp in self.preprocessors:
            try:
                data = pp(self, data)
            except Exception, e:
                e.args = [_ for _ in e.args]+[str(pp)]
                raise e
        return data
        
class Factory(object):
    
    def __init__(self):
        self._factories = dict()
        self._global_preprocessors = list()
        
    def register(self, name, extractors, renderers, preprocessors=None):
        self._factories[name] = (extractors, renderers, preprocessors or list())
        
    def register_global_preprocessors(self, preprocessors):
        self._global_preprocessors += preprocessors
        
    def __call__(self, registeredname, 
                 name=None, value_or_getter=None, properties=dict()):
        extractors, renderers, preproc = self._factories[registeredname]
        return Widget(extractors, renderers, 
                      self._global_preprocessors + preproc, 
                      uniquename=name, 
                      value_or_getter=value_or_getter, 
                      properties=properties)
    
    def extractors(self, name):
        return self._factories[name][0]
    
    def renderers(self, name):
        return self._factories[name][1]

    def preprocessors(self, name):
        return self._global_preprocessors + self._factories[name][2]
    
factory = Factory()

def register_renderer_prefixed(prefix, registered_name, renderers):
    factory.register('%s.%s' % (prefix, registered_name), 
                     factory.extractors(registered_name), 
                     factory.renderers(registered_name) + renderers,
                     factory.preprocessors(registered_name))
