class Controller(object):
    """Form controller.
    """
    
    def __init__(self, widget):
        """Initialize controller
                    
        ``widget``
            yafowil.base.Widget tree.
        """
        self.widget = widget
        self.error = False
    
    def __call__(self, request):
        """Perform form processing for widget.
        """
        data = self.widget.extract(request)
        self.error = False
        self._error(data)
        if self.error:
            return None
        self.handle(self.widget, data)
        for action in self.actions:
            if self.triggered(request, action):
                if action.attrs.get('next'):
                    return action.attrs.next(request)
        return None
    
    @property
    def actions(self):
        return [w for w in self.widget.values() if w.attrs.get('action')]
    
    def triggered(self, request, action):
        return request.get('action.%s' % '.'.join(action.path))
    
    def handle(self, widget, data):
        for action in self.actions:
            if self.triggered(data['request'], action):
                if action.attributes.get('handler'):
                    action.attributes.handler(widget, data)
        for sub in widget.values():
            #  XXX: delegation in data needed
            self.handle(sub, data)
    
    def _error(self, data):
        if data.get('errors'):
            self.error = True
            return
        for sub in data['extracted']:
            if not isinstance(sub, dict):
                continue
            for key in sub.keys():
                self._error(sub[key])