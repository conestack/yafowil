# -*- coding: utf-8 -*-
from node.behaviors import Adopt
from node.behaviors import Attributes
from node.behaviors import DictStorage
from node.behaviors import NodeAttributes
from node.behaviors import NodeChildValidate
from node.behaviors import Nodespaces
from node.behaviors import Nodify
from node.behaviors import OdictStorage
from node.behaviors import Order
from node.utils import UNSET
from node.utils import instance_property
from plumber import plumbing
from threading import RLock
from yafowil.utils import Tag
from yafowil.utils import attr_value
import copy
import types


def _dict__repr__(self):
    return '{{{0}}}'.format(
        ', '.join(['{0}: {1}'.format(
            repr(k),
            repr(v)
        ) for k, v in self.items()])
    )


class RuntimeDataAttributes(NodeAttributes):
    __str__ = __repr__ = _dict__repr__


@plumbing(
    Nodespaces,
    Attributes,
    NodeChildValidate,
    Adopt,
    Nodify,
    OdictStorage)
class RuntimeData(object):
    """Holds Runtime data of widget.
    """
    attributes_factory = RuntimeDataAttributes

    def __init__(self,
                 name=None,
                 parent=None,
                 request=UNSET,
                 persist=None,
                 persist_target=None,
                 persist_writer=None):
        self.__name__ = name
        self.__parent__ = parent
        if parent is not None:
            parent[self.name] = self
        self.request = request
        self.value = UNSET
        self.preprocessed = False
        self.extracted = UNSET
        self.rendered = UNSET
        self.errors = list()
        self.translate_callable = lambda msg: msg
        self._persist = persist
        self._persist_target = persist_target
        self._persist_writer = persist_writer

    @property
    def persist(self):
        return self._persist

    @persist.setter
    def persist(self, value):
        # override only if not defined yet and given value not None
        if self._persist is None and value is not None:
            self._persist = value

    @property
    def persist_target(self):
        return self._persist_target

    @persist_target.setter
    def persist_target(self, value):
        # override only if not defined yet and given value not None
        if self._persist_target is None and value is not None:
            self._persist_target = value

    @property
    def persist_writer(self):
        return self._persist_writer

    @persist_writer.setter
    def persist_writer(self, value):
        # override only if not defined yet and given value not None
        if self._persist_writer is None and value is not None:
            self._persist_writer = value

    @instance_property
    def has_errors(self):
        """Return ``True`` if extraction error occurred on self or children
        of self, otherwise ``False``.
        """
        error = bool(self.errors)
        if not error:
            for child in self.values():
                error = child.has_errors
                if error:
                    break
        return error

    @property
    def tag(self):
        return Tag(self.translate_callable)

    def fetch(self, path):
        if isinstance(path, basestring):
            path = path.split('.')
        data = self.root
        if path[0] != data.name:
            raise KeyError('Invalid name of root element')
        __traceback_info__ = 'fetch path: {0}'.format(path)
        for key in path[1:]:
            data = data[key]
        return data

    def write(self, model, writer=None, recursiv=True):
        if self.has_errors:
            raise RuntimeError(
                'Attempt to persist data which failed to extract'
            )
        current_writer = self.persist_writer or writer
        if not current_writer:
            raise ValueError('No persistence writer found')
        if not writer:
            writer = current_writer
        if self.persist:
            target = self.persist_target
            if not target:
                target = self.name
            current_writer(model, target, self.extracted)
        if not recursiv:
            return
        for child in self.values():
            child.write(model, writer=writer, recursiv=recursiv)

    def __repr__(self):
        rep = "<RuntimeData {0}, value={1}, extracted={2}".format(
            '.'.join([str(_) for _ in self.path]),
            repr(self.value),
            repr(self.extracted)
        )
        if self.errors:
            rep += ', {0} error(s)'.format(len(self.errors))
        if len(self.attrs):
            rep += ', attrs={0}'.format(repr(self.attrs))
        rep += ' at {0}>'.format(hex(id(self))[:-1])
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
        return u"ExtractionError('{0}',)".format(str(self))


class TBSupplementWidget(object):
    """Supplement for Tracebacks in case a widget chain part fails.

    - in conjunction with ```zExceptions``` or ```zope.exceptions```
    - goal is to ease debugging of runtime problems while processing and
      rendering.
    """

    def __init__(self, widget, func, task, descr):
        self.manageable_object = func
        try:
            name = widget.dottedpath
        except ValueError:
            name = '(name not set)'
        self.func = func
        self.name = name
        self.blueprints = widget.blueprints
        self.task = task
        self.descr = descr

    def getInfo(self, as_html=0):
        """returns additional info. zExceptions expects formatted HTML if
        as_html evaluates to True. zope.excpetions doesnt care and turns the
        result into HTML on its own.
        """
        if not as_html:
            info = '    yafowil widget processing info:\n'
            info += '    - path      : {0}\n'.format(self.name)
            info += '    - blueprints: {0}\n'.format(self.blueprints)
            info += '    - task      : {0}\n'.format(self.task)
            info += '    - descr     : {0}'.format(self.descr)
            return info
        tag = Tag(lambda x: x)
        li = tag('li', 'path: ', tag('strong', self.name))
        li += tag('li', 'blueprints: ', tag('strong', self.blueprints))
        li += tag('li', 'task: ', tag('strong', self.task))
        li += tag('li', 'description: ', tag('strong', self.descr))
        return tag('p', 'yafowil widget processing info:', tag('ul', li))


@plumbing(
    NodeChildValidate,
    Adopt,
    Nodify,
    DictStorage)
class WidgetAttributes(object):
    allow_non_node_childs = True
    __str__ = __repr__ = _dict__repr__

    def __init__(self, name=None, parent=None):
        self.__name__ = name
        self.__parent__ = parent

    def __getitem__(self, name):
        prefixed = '{0}.{1}'.format(self.parent.current_prefix, name)
        storage = self.storage
        if prefixed in storage:
            return storage[prefixed]
        if name in storage:
            return storage[name]
        defaults = self.parent.defaults
        if prefixed in defaults:
            return defaults[prefixed]
        if name in defaults:
            return defaults[name]
        raise KeyError((
            'Property with key "{0}" is not given on widget "{1}" (no default)'
        ).format(name, self.parent.dottedpath))


@plumbing(
    Nodespaces,
    Attributes,
    NodeChildValidate,
    Adopt,
    Order,
    Nodify,
    OdictStorage)
class Widget(object):
    """Base Widget Class.
    """
    attributes_factory = WidgetAttributes

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
            list of tuples with chain part name and callable rendering widget
            in edit mode. Callable need to accept ``value``, ``uniquename`` and
            properties as dict-like. Properties gets a key ``rendered`` set, a
            list of results  of previous extractors in chain. Has same
            signature as extract.

        ``display_renderers``
            list of tuples with chain part name and callable rendering widget
            in display mode. Callable need to accept ``value``, ``uniquename``
            and properties as dict-like. Properties gets a key ``rendered``
            set, a list of results of previous extractors in chain. Has same
            signature as extract.

        ``preprocessors``
            list of tuples with chain part name and callable executed before
            extract or rendering. Executed only once for a given runtime data.
            Has same signature a s extract.

        ``uniquename``
            id as string containing characters from a-z, A-Z, 0-9 only. Must
            not start with numerical character.

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
        self.blueprints = blueprints
        self.getter = value_or_getter
        self.mode = mode
        self.extractors = extractors
        self.edit_renderers = edit_renderers
        self.display_renderers = display_renderers
        self.preprocessors = preprocessors or list()
        self.defaults = defaults
        self.current_prefix = ''
        # keep properties for use in dottedpath to avoid recursion errors
        self.properties = properties
        self.attrs.update(properties)
        self.custom = custom
        self._lock = RLock()

    def __call__(self, data=None, request=None):
        """Renders the widget.

        If data is passed in request is ignored! Request can't be passed in
        together with data.

        ``data``
            runtime data, information collected in one run of the widget.
            If passed in, extract need to be called separate before.
            Expects either an initialized RuntimeData instance or None
            (default) to create an empty widget.

        ``request``
            pass in request. if passed in it will be available at data.
            but extraction does not happen. call extract explicit before if
            needed.
        """
        if data is not None and request is not None:
            raise ValueError("if data is passed in, don't pass in request!")
        if data is None:
            if request is None:
                request = UNSET
            data = self._runpreprocessors(RuntimeData(
                name=self.name,
                request=request
            ))
        if data.mode == 'skip':
            data.rendered = u''
            return data.rendered
        elif data.mode == 'display':
            renderers = self.display_renderers
        else:
            renderers = self.edit_renderers
        if not renderers:
            raise ValueError(
                "no renderers given for widget '{0}' at mode '{1}'".format(
                    self.dottedpath,
                    data.mode
                )
            )
        with self._lock:
            try:
                for ren_name, renderer in renderers:
                    self.current_prefix = ren_name
                    __traceback_supplement__ = (
                        TBSupplementWidget,
                        self,
                        renderer,
                        'render',
                        "failed at '{0}' in mode '{1}'".format(
                            ren_name,
                            data.mode
                        )
                    )
                    data.rendered = renderer(self, data)
            finally:
                self.current_prefix = ''
        return data.rendered

    def extract(self, request, parent=None):
        """Extract the data from the request by calling the given extractors.

        ``request``
            expects a dict-like object

        ``parent``
            parent data
        """
        data = self._runpreprocessors(RuntimeData(
            name=self.name,
            parent=parent,
            request=request,
            persist=self.attrs.get('persist'),
            persist_target=self.attrs.get('persist_target'),
            persist_writer=self.attrs.get('persist_writer')
        ))
        # don't extract if skip mode
        if data.mode == 'skip':
            return data
        # dont't extract if display mode and no display proxy
        if data.mode == 'display':
            # display_proxy cannot be called here, currently not possible to
            # use ``attr_value``, widget not available. this causes an
            # inconsistency with the use of display_proxy inside blueprint
            # callbacks.
            # XXX: Use ``attr_value`` after signature change.
            if not self.attrs.get('display_proxy'):
                return data
        with self._lock:
            try:
                for ex_name, extractor in self.extractors:
                    self.current_prefix = ex_name
                    # update persistence settings for data node. necessary for
                    # blueprint specific factory defaults to work.
                    data.persist = self.attrs.get('persist')
                    data.persist_target = self.attrs.get('persist_target')
                    data.persist_writer = self.attrs.get('persist_writer')
                    __traceback_supplement__ = (
                        TBSupplementWidget,
                        self,
                        extractor,
                        'extract',
                        "failed at '{0}'".format(ex_name)
                    )
                    try:
                        data.extracted = extractor(self, data)
                    except ExtractionError, e:
                        data.errors.append(e)
                        if e.abort:
                            break
            finally:
                self.current_prefix = ''
        return data

    @property
    def dottedpath(self):
        if self.path[0] is None:
            raise ValueError('Root widget has no name! Pass it to factory.')
        path = list()
        node = self
        while node is not None:
            if not node.properties.get('structural'):
                path.append(node.name)
            node = node.parent
        path.reverse()
        return '.'.join(path)

    def _runpreprocessors(self, data):
        __traceback_supplement__ = (
            TBSupplementWidget,
            self,
            self._runpreprocessors,
            'run preprocessors',
            'execute'
        )
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
            raise ValueError(
                "mode must be one out of 'edit', 'display', 'skip', but "
                "'{0}' was given ".format(data.mode)
            )
        for pp_name, pp in self.preprocessors:
            data.current_prefix = pp_name
            __traceback_supplement__ = (
                TBSupplementWidget,
                self,
                pp,
                'preprocessor',
                "failed at '{0}'".format(pp_name)
            )
            data = pp(self, data)
        data.current_prefix = ''
        data.preprocessed = True
        return data


class Factory(object):

    def __init__(self):
        self._blueprints = dict()
        self._global_preprocessors = list()
        self._macros = dict()
        self._themes = dict()
        self.theme = 'default'
        self.defaults = dict()
        self.doc = {
            'props': dict(),
            'blueprint': dict(),
        }

    def _name_check(self, name):
        for chara in '*:#':
            if chara in name:
                raise ValueError(
                    '"{0}" as char not allowed as name.'.format(chara)
                )

    def register(self, name, extractors=[], edit_renderers=[],
                 preprocessors=[], builders=[], display_renderers=[]):
        """Registers a blueprint in the factory.
        """
        self._name_check(name)
        self._blueprints[name] = (
            extractors,
            edit_renderers,
            preprocessors,
            builders,
            display_renderers
        )

    def register_global_preprocessors(self, preprocessors):
        self._global_preprocessors += preprocessors

    def register_macro(self, name, blueprints, props):
        self._name_check(name)
        if isinstance(blueprints, basestring):
            blueprints = blueprints.split(':')
        self._macros[name] = blueprints, props

    def register_theme(self, themename, widgetname,
                       resourcedir=None, js=[], css=[]):
        """Register theme for addon widget.
        """
        theme = self._themes.setdefault(themename, {})
        widget_theme = theme.setdefault(widgetname, {})
        widget_theme['resourcedir'] = resourcedir
        widget_theme['js'] = js
        widget_theme['css'] = css

    def resources_for(self, widgetname, copy_resources=True):
        theme = self._themes.get(self.theme, {})
        default = self._themes.get('default', {})
        resources = theme.get(widgetname)
        if not resources:
            resources = default.get(widgetname)
        # return copy, some integrations might modify, resources are static
        if copy_resources:
            return copy.deepcopy(resources)
        return resources

    def _expand_blueprints(self, blueprints, props):
        result = list()
        if isinstance(blueprints, basestring):
            blueprints = blueprints.split(':')
        for blueprint in blueprints:
            if blueprint.startswith('#'):
                macro_name = blueprint[1:]
                if macro_name not in self._macros:
                    raise ValueError(
                        "Macro named '{}' is not registered in factory".format(
                            macro_name
                        )
                    )
                macro_chain, macro_props = self._macros[macro_name]
                for key in macro_props:
                    if key not in props:
                        props[key] = macro_props[key]
                expanded, props = self._expand_blueprints(macro_chain, props)
                result += expanded
            else:
                result.append(blueprint)
        return result, props

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
            Custom blueprints not registered in the registry are added using
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
            edit_renderers, preprocessors, builders, display_renderers.

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
        blueprints, props = self._expand_blueprints(blueprints, props)
        for blueprint in blueprints:
            if blueprint.startswith('*'):
                part_name = blueprint[1:]
                if type(custom[part_name]) in (types.ListType,
                                               types.TupleType):
                    if len(custom[part_name]) < 5:
                        # BBB:
                        ex, eren, pre, bui = custom[part_name]
                        dren = []
                    else:
                        ex, eren, pre, bui, dren = custom[part_name]
                else:  # expect dict
                    ex = custom[part_name].get('extractors', list())
                    eren = custom[part_name].get('edit_renderers', list())
                    pre = custom[part_name].get('preprocessors', list())
                    bui = custom[part_name].get('builders', list())
                    dren = custom[part_name].get('display_renderers', list())
            else:
                part_name = blueprint
                ex, eren, pre, bui, dren = self._blueprints[part_name]
            extractors = [(part_name, _) for _ in ex] + extractors
            edit_renderers = [(part_name, _) for _ in eren] + edit_renderers
            disp_renderers = [(part_name, _) for _ in dren] + disp_renderers
            preprocessors = preprocessors + [(part_name, _) for _ in pre]
            builders = builders + [(part_name, _) for _ in bui]
        global_pre = [('__GLOBAL__', _) for _ in self._global_preprocessors]
        widget = Widget(
            blueprints,
            extractors,
            edit_renderers,
            disp_renderers,
            global_pre + preprocessors,
            uniquename=name,
            value_or_getter=value,
            properties=props,
            custom=custom,
            defaults=self.defaults,
            mode=mode
        )
        for part_name, builder_func in builders:
            widget.current_prefix = part_name
            builder_func(widget, self)
            widget.current_prefix = ''
        return widget

    def extractors(self, name):
        return self._blueprints[name][0]

    def renderers(self, name):
        raise RuntimeError(
            'Deprecated since 1.2, use edit_renderers or display_renderers'
        )

    def edit_renderers(self, name):
        return self._blueprints[name][1]

    def display_renderers(self, name):
        return self._blueprints[name][4]

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
    return attr_value('default', widget, data)
