class Controller(object):
    """Form controller.
    """
    
    def __init__(self, widget, request):
        """Initialize controller
                    
        ``widget``
            yafowil.base.Widget tree.
        """
        self.widget = widget
        self.request = request
        self.error = False
        self.next = None
        self.data = self.widget.extract(request)
        self._error(self.data)
        if self.error:
            return
        for action in self.actions:
            if self.triggered(request, action):
                if action.attributes.get('handler'):
                    action.attributes.handler(self.widget, self.data)
                if action.attrs.get('next'):
                    self.next = action.attrs.next(request)
    
    @property
    def rendered(self):
        return self.form(data=self.data)
    
    @property
    def actions(self):
        return [w for w in self.widget.values() if w.attrs.get('action')]
    
    def triggered(self, request, action):
        return request.get('action.%s' % '.'.join(action.path))
    
    def _error(self, data):
        if data.get('errors'):
            self.error = True
            return
        for sub in data['extracted']:
            if not isinstance(sub, dict):
                continue
            for key in sub.keys():
                self._error(sub[key])