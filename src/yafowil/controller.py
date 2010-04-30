class Controller(object):
    """Form controller.
    """
    
    def __init__(self, widget, request):
        """Initialize controller
                    
        ``widget``
            yafowil.base.Widget tree.
            
        ``request``
            native request
        """
        self.widget = widget
        self.performed = False
        self.error = False
        self.next = None
        self.data = self.widget.extract(request)
        self.request = self.data.request        
        self._error(self.data)
        for action in self.actions:
            if not self.triggered(action):
                continue
            self.performed = True
            if self.error:
                return
            if action.attrs.get('handler'):
                action.attrs.handler(self.widget, self.data)
            if action.attrs.get('next'):
                self.next = action.attrs.next(self.request)
    
    @property
    def rendered(self):
        if not self.performed:
            return self.widget(request=self.request)
        return self.widget(data=self.data)
    
    @property
    def actions(self):
        # XXX TODO: collect actions recursive.
        return [w for w in self.widget.values() if w.attrs.get('action')]
    
    def triggered(self, action):
        return self.request.get('action.%s' % action.dottedpath)
    
    def _error(self, data):
        if data.errors:
            self.error = True
            return
        for subdata in data.values():
            self._error(subdata)