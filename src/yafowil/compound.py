import sys
import copy
import re
from yafowil.base import (
    factory,
    cssid,
    tag,
    ExtractionError,
)

def compound_preprocessor(uname, data, properties):
    if properties.get('widgets', 0) and data.get('widgets', 0):
        raise ValueError('key "widgets" found in both, properties and '
                         'runtime data.')
    widgets = properties.get('widgets', False) or data.get('widgets', None)
    delegate = properties.get('delegate', data.get('delegate', False))
    data['widgets'] = list()
    for widget in widgets:
        pwidget = copy.copy(widget)
        pwidget.uname = "%s.%s" % (uname, widget.uname)
        pwidget.uname_original = widget.uname
        if delegate:
            if data['value'] is None:
                raise ValueError, "compound_preprocessor data['value'] is None at %s" % uname
            pwidget.getter = data['value'].get(widget.uname, None)
        data['widgets'].append(pwidget)
    return data

def compound_extractor(uname, data, properties):
    result = dict()    
    for widget in data.get('widgets', properties.get('widgets')):
        result[widget.uname_original] = widget.extract(data['request'])
    return result

def compound_renderer(uname, data, properties):
    result = u''
    for widget in data.get('widgets', properties.get('widgets')):
        kw = dict() 
        if data['extracted']: 
            subuname = hasattr(widget, 'uname_original') and \
                    widget.uname_original or widget.uname
            kw['data'] = data['extracted'][0][subuname]
        result += widget(**kw)
    return result
        
factory.register('compound', 
                 [compound_extractor], 
                 [compound_renderer],
                 [compound_preprocessor])

def fieldset_renderer(uname, data, properties):
    fieldset_id = properties.get('id',{}).get('fieldset', cssid(uname, 'fieldset'))
    class_ = properties.get('class',{}).get('fieldset', None)
    rendered = data.last_rendered
    if properties.get('legend', False):
        rendered = tag('legend', properties.get('legend')) + rendered
    return tag('fieldset', rendered, id=fieldset_id, class_=class_)   

factory.register('fieldset', 
                 factory.extractors('compound'), 
                 factory.renderers('compound')+[fieldset_renderer],
                 factory.preprocessors('compound'))

def form_renderer(uname, data, properties):
    method = properties.get('method', None)
    enctype_default = method == 'post' and 'multipart/form-data' or None
    form_attrs = {
        'action': properties['action'],
        'method': method,
        'enctype': properties.get('enctype', enctype_default),
        'class_': properties.get('class', {}).get('form', None),
        'id': properties.get('id', {}).get('form', 'form-%s' % uname),
    }
    return tag('form', data.last_rendered, **form_attrs)

factory.register('form', 
                 factory.extractors('compound'), 
                 factory.renderers('compound')+[form_renderer],
                 factory.preprocessors('compound'))

class ArrayWidgetFactory(object):    
    
    def __init__(self, uname, data, properties):
        self.uname = uname
        self.data = data
        self.properties = properties
        
    def _make_names(self, uname, length):
        return ['%s-%07d' % (uname, _) for _ in range(0, length)]
        
    @property 
    def names(self):
        if hasattr(self, '_names'):
            return self._names
        self._names = None
        swidget = self.data.get('widget', self.properties.get('widget'))
        minimal = self.properties.get('min', 1)
        additional = self.properties.get('additional', 0)
        length = None
        if self.data.last_extracted:
            # extraction worked already             
            length = len(self.data.last_extracted)    
        elif self.data['request']:
            # before extractors run we need to check the request
            self._names = list()           
            matching = list()
            full_uname = '%s\.(%s' % (self.uname.replace('.', '\.'), 
                                      swidget.uname)
            matcher = re.compile('%s-[0-9]*).*' % full_uname)
            for key in sorted(self.data['request']):
                match = matcher.match(key)
                if match:
                    self._names.append(match.groups()[0]) 
                self._names.sort()
            length = len(self._names)
        if length is None and self.data['value']:
            # from value
            length = len(self.data['value'])            
        if length is None:
            # minimal
            length = max(minimal, additional)
        else:
            length += additional
        if length < minimal:
            length = minimal
        if self._names is None:
            self._names = self._make_names(swidget.uname, length)
        else:
            if length < len(self._names):
                self._names = self._names[:length]
            elif length > len(self._names):
                newnames = self._make_names(swidget.uname, length)
                self._names += newnames[len(self._names):]
        return self._names
                
    def __iter__(self):
        def widgetgenerator():
            count = 0
            swidget = self.data.get('widget', self.properties.get('widget'))
            names = self.names                
            while True:                        
                if count >= len(names) \
                   or count >= self.properties.get('max', sys.maxint):
                     return                
                widget = copy.copy(swidget)
                widget.uname = names[count]
                yield widget                 
                count += 1
        return widgetgenerator()

def array_preprocessor(uname, data, properties):
    data['widgets'] = ArrayWidgetFactory(uname, data, properties)
    names = data['widgets'].names
    nvalue = dict()
    count = 0
    for pos in range(0, len(names)):
        if pos < len(data['value']):
            nvalue[names[pos]] = data['value'][pos]
        else:
            nvalue[names[pos]] = {}
        count += 1 
    data['value'] = nvalue
    return data

def array_extractor(uname, data, properties):
    if not data.last_extracted:
        return data.last_extracted
    result = list()
    last = data.last_extracted
    for key in last:
        if last[key]:
            result.append(last[key])
    return result
        
factory.register('array', 
                 factory.extractors('compound')+[array_extractor], 
                 factory.renderers('compound'),
                 [array_preprocessor]+factory.preprocessors('compound'))