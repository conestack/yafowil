class Controller(object):
    """Form controller.
    """
    
    def __init__(self, widget):
        """Initialize controller
                    
        ``widget``
            yafowil.base.Widget tree.
        """
        self.widget = widget
    
    def __call__(self, request):
        """Perform form processing for widget.
        """
        data = self.widget.extract(request)
        
        # XXX: if data err -> return renderer for re-rendering the form
        
        self.handle(self.widget, request)
        for action in self.actions:
            if self.triggered(request, action):
                if action.attributes.next:
                    return action.attributes.next()
        return None
    
    @property
    def actions(self):
        return [w for w in self.widget.values() if w.attributes.get('action')]
    
    def triggered(self, request, action):
        return request.params.get('action.%s' % '.'.join(action.path))
    
    def handle(self, widget, request):
        for action in self.actions:
            if self.triggered(request, action):
                if action.attributes.handler:
                    action.attributes.handler(request)
        for sub in widget.values():
            self.handle(sub, request)