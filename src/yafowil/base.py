from threading import RLock
from zodict import AttributedNode
from zodict.node import NodeAttributes

class Unset(object): 
    
    def __nonzero__(self):
        return False
    
    def __str__(self):
        return ''
    
    def __repr__(self):
        return '<UNSET>'

UNSET = Unset()

callable = lambda o: hasattr(o, '__call__')

class RuntimeData(AttributedNode):
    """Holds Runtime data of widget."""
    
    def __init__(self, name=None):
        super(RuntimeData, self).__init__(name=name)
        self.request = UNSET
        self.value = UNSET
        self.preprocessed = False
        self.extracted = UNSET
        self.rendered = UNSET
        self.errors= list()
        
    def fetch(self, path):
        if isinstance(path, basestring):
            path = path.split('.')
        data = self.root
        if path[0] != data.__name__:
            raise KeyError, 'Invalid name of root element'
        for key in path[1:]:
            data = data[key]
        return data
                            
    def __repr__(self):
        rep = "<RuntimeData %s, value=%s, extracted=%s" % (
                 '.'.join([str(_) for _ in self.path]), 
                 repr(self.value), 
                 repr(self.extracted)
        )  
        if self.errors:
            rep += ', %d error(s)' % len(self.errors)
        if self.attrs:
            rep += ', attrs=%s' % repr(self.attrs)
        rep += ' at %s>' % hex(id(self))[:-1]
        return rep

    @property
    def noderepr(self):
        return repr(self)     
    
    __str__ = __repr__

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
        Exception.__init__(self, msg)
        self.abort = abort
        
    def __repr__(self):
        return u"ExtractionError('%s',)" % str(self)
        
class WidgetAttributes(NodeAttributes):
    
    def __getitem__(self, name):
        prefixed = '%s.%s' % (self._node.current_prefix or '', name)
        value = super(WidgetAttributes, self).get(prefixed, UNSET)
        if value is not UNSET:
            return value
        value = super(WidgetAttributes, self).get(name, UNSET)
        if value is not UNSET:
            return value
        node = object.__getattribute__(self, '_node')
        value = node.defaults.get(prefixed, UNSET)          
        if value is not UNSET:
            return value
        return node.defaults[name]
    
    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default
        
class Widget(AttributedNode):
    """Base Widget Class
    """
    
    attributes_factory = WidgetAttributes
    
    def __init__(self, extractors, renderers, preprocessors, 
                 uniquename=None, value_or_getter=None, properties=dict(),
                 defaults=dict()
                 ):
        """Initialize the widget. 
            
        ``extractors``
            list of tuples with chain part name and callables extracting the 
            data and returning it. Each extractor in chain is called. Expects 
            to raise ``ExtractionException`` and provide error-message if 
            something went wrong. You can call this validation. 
            Need to accept some ``request`` (dict like object), ``value`` 
            (same as while rendering), ``uniquename`` and ``properties``, a 
            dict-like. Properties gets a key ``extracted`` set, a list of 
            results of previous extractors in chain-   
            
        ``renderers``
            list of tuples with chain part name and callable rendering widget. 
            Callable need to accept ``value``, ``uniquename`` and properties as 
            dict-like. Properties gets a key ``rendered`` set, a list of results 
            of previous extractors in chain. Has same signature a s extract.

        ``preprocessors``
            list of tuples with chain part name and callable executed before 
            extract or rendering. Executed only once for a given runtime data.
            Has same signature a s extract. 
                         
        ``uniquename``
            id as string containing characters from a-z, A-Z, 0-9 only. Must not
            start with numerical character. 
            
        ``value_or_getter``
            either a callable or the value itself. If callable, its called 
            before passing to given ``renderer`` 
                        
        ``properties``
            arbitrary dict-like passed through for use in renderer and 
            extractor, static data must never be modifed!
            
        ``defaults``
            a dict with defaults value for the widgets attributes.
        """
        super(Widget, self).__init__(uniquename)
        self.getter = value_or_getter
        self.extractors = extractors
        self.renderers = renderers
        self.preprocessors = preprocessors or list()
        self.defaults = defaults
        self.__name__ = uniquename
        self._lock = RLock()
        self.current_prefix = None
        for key in properties:
            self.attributes[key] = properties[key]
            
    def lock(self):
        self._lock.acquire()

    def unlock(self):
        self._lock.release()        
                
    def __call__(self, data=None, request=None):
        """renders the widget.
        
        If data is passed in request is ignored! Request can't be passed in 
        together with data.
        
        ``data``
            runtime data, information collected in one run of the widget. 
            Passed in. Extract need to be called separate before. 
            Expects either an initialized RuntimeData instance or None (default) 
            to create an empty widget.
            
        ``request``
            pass in request. if passed in it will be available at data. 
            but extraction does not happen. call extract explicit before if
            needed. 
        """
        if data is not None and request is not None:
            raise ValueError, 'if data is passed in dont pass in request!' 
        if data is None:
            data = RuntimeData(self.__name__)
            if request is not None:
                data.request = request
            data = self._runpreprocessors(data)
        self.lock()
        for ren_name, renderer in self.renderers:
            self.current_prefix = ren_name
            try:
                rendered = renderer(self, data)
            except Exception, e:
                self.current_prefix = None
                self.unlock()
                e.args = [a for a in e.args] + [str(renderer)] + self.path
                raise e
            data.rendered = rendered
        self.current_prefix = None
        self.unlock()                   
        return data.rendered
    
    def extract(self, request):
        """extract the data from the request by calling the given extractors. 
        
        ``request`` 
            expects a dict-like object       

        """
        data = RuntimeData(self.__name__)
        data.request = request
        data = self._runpreprocessors(data)
        self.lock()         
        for ex_name, extractor in self.extractors:     
            self.current_prefix = ex_name
            try:
                extracted = extractor(self, data)
            except ExtractionError, e:
                data.errors.append(e)
                if e.abort:
                    break
            except Exception, e:
                self.current_prefix = None
                self.unlock()                   
                e.args = [a for a in e.args] + [str(extractor)] + self.path
                raise e
            else:
                data.extracted = extracted
        self.current_prefix = None
        self.unlock()                   
        return data
    
    @property
    def dottedpath(self):
        return '.'.join(self.path)

    def _runpreprocessors(self, data):                
        if data.preprocessed:
            return data
        if callable(self.getter):
            data.value = self.getter(self, data)
        else:
            data.value = self.getter        
        for ppname, pp in self.preprocessors:
            data.current_prefix = ppname
            try:
                data = pp(self, data)
            except Exception, e:
                data.current_prefix = None 
                e.args = [a for a in e.args] + [str(pp)] + self.path
                raise e
        data.current_prefix = None
        data.preprocessed = True 
        return data
        
class Factory(object):
    
    def __init__(self):
        self._factories = dict()
        self._global_preprocessors = list()
        self.defaults = dict()
        
    def register(self, name, extractors, renderers, 
                 preprocessors=[], subwidgets=[]):
        if name.startswith('*'):
            raise ValueError, 'Asterisk * as first sign not allowed as name.'
        self._factories[name] = (extractors, renderers, 
                                 preprocessors, subwidgets)
        
    def register_global_preprocessors(self, preprocessors):
        self._global_preprocessors += preprocessors
        
    def __call__(self, reg_names, 
                 name=None, 
                 value=None, 
                 props=dict(),
                 custom=dict()):
        """creates a widget.
        
        ``reg_names``
            a string defining which widget to build. it contains a colon 
            separated list of names in the registry. To create a simple 
            text widget from common its ``text``. To wrap a text widget with
            a label it is ``label:text``. Latter concatenates the chains of 
            both. registrations. Custom chains not registered in the registry 
            can be added by using the asterisk syntax. I.e. injecting an 
            validating extractor works with ``label:*myextractor:text``. Latter
            implies to use the ``custom`` keyword argument (see below)   
            
        ``name``
            a name for the widget. optional. if not set it has to be set later
            at the  ``__name__`` attribute of the widget.
            if not set the widget wont work. 
            
        ``value``
            a value or a callable used as getter. if a callable is given it has 
            to accept the widget and runtime data as argument.
            
        ``props``
            dict-like object containing properties to be copied to widgets 
            attributes.
            
        ``custom`` 
            dict, where keys are matching to asterisk prefixed custom chains.
            each chains part is tuple with 4 lists of callables: extractors, 
            renderers, preprocessors, subwidgets.    
        """
        extractors = list()
        renderers = list()
        preprocessors = list()
        subwidgets = list()
        for reg_name in reg_names.split(':'):
            if reg_name.startswith('*'):
                part_name = reg_name[1:]
                ex, ren, pre, sub = custom[part_name]
            else:                   
                part_name = reg_name
                ex, ren, pre, sub = self._factories[part_name]
            extractors    = [(part_name, _) for _ in ex]  + extractors
            renderers     = [(part_name, _) for _ in ren] + renderers
            preprocessors = preprocessors + [(part_name, _) for _ in pre]
            subwidgets    = subwidgets    + [(part_name, _) for _ in sub]
        global_pre  = [('__GLOBAL__', _) for _ in self._global_preprocessors]
        widget = Widget(extractors, 
                        renderers, 
                        global_pre + preprocessors,
                        uniquename=name, 
                        value_or_getter=value, 
                        properties=props,
                        defaults=self.defaults)
        for part_name, subwidget_func in subwidgets:
            widget.current_prefix = part_name
            subwidget_func(widget, self)
            widget.current_prefix = None
        return widget
    
    def extractors(self, name):
        return self._factories[name][0]
    
    def renderers(self, name):
        return self._factories[name][1]

    def preprocessors(self, name):
        return self._global_preprocessors + self._factories[name][2]

    def subwidgets(self, name):
        return self._factories[name][3]
    
factory = Factory()