import logging
from threading import RLock
from plumber import plumber
from node.parts import (
    Adopt,
    Nodify,
    NodeChildValidate,
    OdictStorage,
    Attributes,
    NodeAttributes,
    Nodespaces,
    Order,
)
from yafowil.utils import (
    Tag,
    UNSET,
)


def _dict__repr__(self):
    return '{%s}' % ', '.join(['%s: %s' % (repr(k), repr(v)) 
                               for k,v in self.items()])


class RuntimeDataAttributes(NodeAttributes):
    __str__ = __repr__ = _dict__repr__


class RuntimeData(object):
    """Holds Runtime data of widget.
    """
    __metaclass__ = plumber
    __plumbing__ = (
        Nodespaces,
        Attributes,
        NodeChildValidate,
        Adopt,
        Nodify,
        OdictStorage,
    )
        
    def __init__(self, name=None, parent=None):
        self.__name__ = name
        self.__parent__ = parent
        self.attributes_factory = RuntimeDataAttributes
        self.request = UNSET
        self.value = UNSET
        self.preprocessed = False
        self.extracted = UNSET
        self.rendered = UNSET
        self.errors= list()
        self.translate_callable = lambda msg: msg        
                
    def fetch(self, path):
        if isinstance(path, basestring):
            path = path.split('.')
        data = self.root
        if path[0] != data.__name__:
            raise KeyError, 'Invalid name of root element'
        __traceback_info__ = 'fetch path: %s' % path
        for key in path[1:]:
            data = data[key]
        return data
    
    @property
    def tag(self):
        return Tag(self.translate_callable)
                            
    def __repr__(self):
        rep = "<RuntimeData %s, value=%s, extracted=%s" % (
                 '.'.join([str(_) for _ in self.path]), 
                 repr(self.value), 
                 repr(self.extracted)
        )  
        if self.errors:
            rep += ', %d error(s)' % len(self.errors)
        if len(self.attrs):
            rep += ', attrs=%s' % repr(self.attrs)
        rep += ' at %s>' % hex(id(self))[:-1]
        return rep

    __str__ = __repr__

    @property
    def noderepr(self):
        return repr(self)


class ExtractionError(Exception):
    """Indicates problems on extraction time, such as conversion, validation
    or similar problems.
    """ 
    
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


class TBSupplementWidget(object):

    def __init__(self, widget, func, task, descr):
        self.manageable_object = func
        try:
            name = widget.dottedpath
        except ValueError:                                  #pragma NO COVERAGE
            name = '(name not set)'                         #pragma NO COVERAGE
        self.name = name
        self.task = task
        self.descr = descr
    
    def getInfo(self, html=1):
        if not html:
            info =  '    yafowil widget processing info:\n' 
            info += '    - widget: %s\n' % self.name
            info += '    - task  : %s\n' % self.task
            info += '    - descr : %s' % self.descr
            return info
        tag = Tag(lambda x: x)
        li = tag('li', 'widget: ', tag('strong', self.name))
        li += tag('li', 'task: ', tag('strong', self.task))
        li += tag('li', 'description: ', tag('strong', self.descr))
        return  tag('p', 'yafowil widget processing info:', tag('ul', li))        

class WidgetAttributes(NodeAttributes):
    
    __str__ = __repr__ = _dict__repr__
        
    def __getitem__(self, name):
        prefixed = '%s.%s' % (self.__parent__.current_prefix or '', name)
        try:
            value = NodeAttributes.__getitem__(self, prefixed)
        except KeyError:
            value = UNSET
        if value is not UNSET:
            return value        
        try:
            value = NodeAttributes.__getitem__(self, name)
        except KeyError:
            value = UNSET
        if value is not UNSET:
            return value
        value = self.__parent__.defaults.get(prefixed, UNSET)          
        if value is not UNSET:
            return value
        if name in self.__parent__.defaults:
            return self.__parent__.defaults[name]
        raise KeyError, \
            'Property with key "%s" is not given on widget "%s" (no default).' \
            % (name, self.__parent__.dottedpath)
    
    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

             
class Widget(object):
    """Base Widget Class
    """
    __metaclass__ = plumber
    __plumbing__ = (
        Nodespaces,
        Attributes,
        NodeChildValidate,
        Adopt,
        Order,
        Nodify,
        OdictStorage,
    )
    
    def __init__(self,
                 blueprints,
                 extractors,
                 edit_renderers,
                 display_renderers, 
                 preprocessors,
                 uniquename=None,
                 value_or_getter=UNSET, 
                 properties=dict(),
                 custom=dict(),
                 defaults=dict(),
                 mode='edit'):
        """Initialize the widget. 
        
        ``blueprints``
            The blueprint names used to create this widget as list of strings.
            
        ``extractors``
            list of tuples with chain part name and callables extracting the 
            data and returning it. Each extractor in chain is called. Expects 
            to raise ``ExtractionException`` and provide error-message if 
            something went wrong. You can call this validation. 
            Need to accept some ``request`` (dict like object), ``value`` 
            (same as while rendering), ``uniquename`` and ``properties``, a 
            dict-like. Properties gets a key ``extracted`` set, a list of 
            results of previous extractors in chain-   
            
        ``edit_renderers``
            list of tuples with chain part name and callable rendering widget in 
            edit mode. Callable need to accept ``value``, ``uniquename`` and 
            properties as dict-like. Properties gets a key ``rendered`` set, a 
            list of results  of previous extractors in chain. Has same signature 
            as extract.

        ``display_renderers``
            list of tuples with chain part name and callable rendering widget in 
            display mode. Callable need to accept ``value``, ``uniquename`` and 
            properties as dict-like. Properties gets a key ``rendered`` set, a 
            list of results of previous extractors in chain. Has same signature 
            as extract.

        ``preprocessors``
            list of tuples with chain part name and callable executed before 
            extract or rendering. Executed only once for a given runtime data.
            Has same signature a s extract. 
                         
        ``uniquename``
            id as string containing characters from a-z, A-Z, 0-9 only. Must not
            start with numerical character. 
            
        ``value_or_getter``
            either a callable or the value itself. If callable, its called 
            before passing to given ``renderer`` .
                        
        ``properties``
            arbitrary dict-like passed through for use in renderer and 
            extractor, static data must never be modifed!
        
        ``custom``
            Definitions for custom factory chain parts.
            
        ``defaults``
            a dict with defaults value for the widgets attributes.

        ``mode``
            Rendering mode of widget: One out of ``edit``, ``display``, 
            ``skip``.  Default is ``edit`` Expects string or callable accepting 
            two parameters  ``widget`` and ``data``.
        """
        self.__name__ = uniquename
        self.__parent__ = None
        self.attributes_factory = WidgetAttributes
        self.blueprints = blueprints
        self.getter = value_or_getter
        self.mode = mode
        self.extractors = extractors
        self.edit_renderers = edit_renderers
        self.display_renderers = display_renderers
        self.preprocessors = preprocessors or list()
        self.defaults = defaults
        self._lock = RLock()
        self.current_prefix = None
        # keep properties for use in dottedpath to avoid recursion errors
        self.properties = properties
        for key in properties:
            self.attrs[key] = properties[key]
        self.custom = custom
            
    def lock(self):
        self._lock.acquire()

    def unlock(self):
        self._lock.release()        
                
    def __call__(self, data=None, request=None):
        """Renders the widget.
        
        If data is passed in request is ignored! Request can't be passed in 
        together with data.
        
        ``data``
            runtime data, information collected in one run of the widget. 
            If passed in, extract need to be called separate before. 
            Expects either an initialized RuntimeData instance or None (default) 
            to create an empty widget.
            
        ``request``
            pass in request. if passed in it will be available at data. 
            but extraction does not happen. call extract explicit before if
            needed. 
        """
        if data is not None and request is not None:
            raise ValueError, "if data is passed in, don't pass in request!" 
        if data is None:
            data = RuntimeData(self.__name__)
            if request is not None:
                data.request = request
            data = self._runpreprocessors(data)
        if data.mode == 'skip':
            data.rendered = u''
            return data.rendered
        elif data.mode == 'display':
            renderers = self.display_renderers
        else:
            renderers = self.edit_renderers
        if not renderers:
            raise ValueError, "no renderers given for widget '%s' at mode '%s'"\
                              % (self.dottedpath, data.mode) 
        self.lock()
        try:
            for ren_name, renderer in renderers:
                self.current_prefix = ren_name
                __traceback_supplement__ = (TBSupplementWidget, self, renderer, 
                                            'render', 
                                            'with name "%s"' % ren_name)
                data.rendered = renderer(self, data)
        finally:
            self.current_prefix = None
            self.unlock()
        return data.rendered
    
    def extract(self, request, parent=None):
        """Extract the data from the request by calling the given extractors. 
        
        ``request`` 
            expects a dict-like object
            
        ``parent``
            parent data       
        """
        data = RuntimeData(self.__name__)
        data.request = request
        if parent is not None:
            parent[self.__name__] = data
        data = self._runpreprocessors(data)
        if data.mode != 'edit':
            return data
        self.lock()     
        try:    
            for ex_name, extractor in self.extractors:     
                self.current_prefix = ex_name
                __traceback_supplement__ = (TBSupplementWidget, self, extractor, 
                                            'extract', 
                                            'with name "%s"' % ex_name)
                try:
                    data.extracted = extractor(self, data)
                except ExtractionError, e:
                    data.errors.append(e)
                    if e.abort:
                        break
        finally:
            self.current_prefix = None
            self.unlock()                                   
        return data
    
    @property
    def dottedpath(self):
        if self.path[0] is None:
            raise ValueError, \
                  'Root widget has no name! Pass it to factory.'
        path = list()
        node = self
        while node is not None:
            if not node.properties.get('structural'):
                path.append(node.__name__)
            node = node.__parent__
        path.reverse()
        return '.'.join(path)

    def _runpreprocessors(self, data):                
        __traceback_supplement__ = (TBSupplementWidget, self,
                                    self._runpreprocessors, 
                                    'run preprocessors', 'execute')
        if data.preprocessed:
            return data
        if callable(self.getter):
            data.value = self.getter(self, data)
        else:
            data.value = self.getter        
        if callable(self.mode):
            data.mode = self.mode(self, data)
        else:
            data.mode = self.mode
        if data.mode not in ('edit', 'display', 'skip'):
            raise ValueError, "mode must be one out of 'edit', 'display', "+\
                              "'skip', but '%s' was given " % data.mode            
        for ppname, pp in self.preprocessors:
            data.current_prefix = ppname
            __traceback_supplement__ = (TBSupplementWidget, self, pp, 
                                        'preprocessor', 
                                        'with name "%s"' % ppname)
            data = pp(self, data)
        data.current_prefix = None
        data.preprocessed = True 
        return data


class Factory(object):
    
    def __init__(self):
        self._blueprints = dict()
        self._global_preprocessors = list()
        self._plans = dict()
        self.defaults = dict()
        self.doc = {
            'props': dict(),
            'blueprint': dict(),
        }
    
    def _name_check(self, name):
        for chara in '*:#':
            if chara in name:
                raise ValueError, '"%s" as char not allowed as name.' % chara
        
    def register(self, name, extractors=[], edit_renderers=[], 
                 preprocessors=[], builders=[], display_renderers=[]):
        """Registers a blueprint in the factory.
        """
        self._name_check(name)
        self._blueprints[name] = (extractors, edit_renderers, 
                                 preprocessors, builders, display_renderers)
        
    def register_global_preprocessors(self, preprocessors):
        self._global_preprocessors += preprocessors
        
    def register_plan(self, name, blueprints):
        self._name_check(name)
        self._plans[name] = blueprints
                
    def _expand_blueprints(self, blueprints):
        result = list()
        if isinstance(blueprints, basestring):
            blueprints = blueprints.split(':')
        for blueprint in blueprints:            
            if blueprint.startswith('#'):
                plan_name = blueprint[1:]
                if plan_name not in self._plans:
                    msg = "Plan with name '%s' is not registered in factory" % \
                          plan_name
                    raise ValueError(msg)
                result += self._expand_blueprints(self._plans[plan_name])
            else:
                result.append(blueprint)
        return result
        
    def __call__(self, blueprints, 
                 name=None, 
                 value=UNSET, 
                 props=dict(),
                 custom=dict(),
                 mode="edit"):
        """Creates a widget from blueprints.
        
        ``blueprints``
            chain of blueprint names. Either a colon separated string or a list 
            of strings defining which widget to build.             
            I.e. creating a simple text widget use ``"text"``. Wrapping a text 
            blueprint with a label use ``"label:text"`` or 
            ``["label", "text"]``.  
            Custom blueprints not registered in the registry are added using the 
            asterisk syntax. I.e. inject a validating extractor with 
            ``label:*myextractor:text`` and use the ``custom`` keyword argument 
            (see below).
            
        ``name``
            a name for the widget. optional. if not set it has to be set later
            at the  ``__name__`` attribute of the widget.
            if not set the widget wont work. 
            
        ``value``
            a value or a callable used as getter. If callable is given it has 
            to accept widget and runtime-data as argument.
            
        ``props``
            dict-like object containing properties to be copied to widgets 
            attributes.
            
        ``custom`` 
            dict, where keys are matching to asterisk prefixed custom chains.
            each chains part is tuple with 4 lists of callables: extractors, 
            renderers, preprocessors, builders, display_renderers.   
        
        ``mode``
            either a callable (widget and runtime-data as argument) or string 
            returning one of 'edit', 'display', 'skip' or direct value. 
            Defaults to 'edit'.
        """
        extractors = list()
        edit_renderers = list()
        disp_renderers = list()
        preprocessors = list()
        builders = list()
        blueprints = self._expand_blueprints(blueprints)
        for blueprint in blueprints:
            if blueprint.startswith('*'):
                part_name = blueprint[1:]
                if len(custom[part_name]) < 5:
                    # BBB:
                    ex, eren, pre, bui = custom[part_name]
                    dren = []
                else:
                    ex, eren, pre, bui, dren = custom[part_name]
            else:                   
                part_name = blueprint
                ex, eren, pre, bui, dren  = self._blueprints[part_name]
            extractors = [(part_name, _) for _ in ex]  + extractors
            edit_renderers = [(part_name, _) for _ in eren] + edit_renderers
            disp_renderers = [(part_name, _) for _ in dren] + disp_renderers
            preprocessors = preprocessors + [(part_name, _) for _ in pre]
            builders      = builders + [(part_name, _) for _ in bui]            
        global_pre  = [('__GLOBAL__', _) for _ in self._global_preprocessors]
        widget = Widget(blueprints,
                        extractors, 
                        edit_renderers, 
                        disp_renderers, 
                        global_pre + preprocessors,
                        uniquename=name, 
                        value_or_getter=value, 
                        properties=props,
                        custom=custom,
                        defaults=self.defaults,
                        mode=mode)
        for part_name, builder_func in builders:
            widget.current_prefix = part_name
            builder_func(widget, self)
            widget.current_prefix = None
        return widget
    
    def extractors(self, name):
        return self._blueprints[name][0]
    
    def renderers(self, name):
        raise RuntimeError, 'Deprecated since 1.2, use either edit_renderers '+\
                            'or display_renderers'

    def edit_renderers(self, name):
        return self._blueprints[name][1]

    def display_renderers(self, name):
        return self._blueprints[name][1]

    def preprocessors(self, name):
        return self._global_preprocessors + self._blueprints[name][2]

    def builders(self, name):
        return self._blueprints[name][3]

factory = Factory()        
        
def fetch_value(widget, data):
    """Fetch extracted, either form-data, value or default .
    """
    if data.extracted is not UNSET:
        return data.extracted
    if data.value is not UNSET:
        return data.value 
    return widget.attrs['default']