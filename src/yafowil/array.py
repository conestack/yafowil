import sys
import copy
import re
from yafowil.base import (
    factory,
    cssid,
    tag,
    ExtractionError,
)

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