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
        self.error = self._error(data)
        if self.error:
            return None
        self.handle(self.widget, request)
        for action in self.actions:
            if self.triggered(request, action):
                if action.attributes.get('next'):
                    return action.attributes.next(request)
        return None
    
    @property
    def actions(self):
        return [w for w in self.widget.values() if w.attributes.get('action')]
    
    def triggered(self, request, action):
        return request.get('action.%s' % '.'.join(action.path))
    
    def handle(self, widget, request):
        for action in self.actions:
            if self.triggered(request, action):
                if action.attributes.get('handler'):
                    action.attributes.handler(widget, request)
        for sub in widget.values():
            self.handle(sub, request)
    
    def _error(self, data):
        if isinstance(data, dict):
            if data.get('errors'):
                return True
        else:
            return False
        for sub in data['extracted']:
            for key in sub.keys():
                if self._error(sub[key]['extracted']):
                    return True
        return False