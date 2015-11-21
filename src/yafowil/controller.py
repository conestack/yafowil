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
            if action.attrs.get('skip'):
                if action.attrs.get('next'):
                    self.next = action.attrs['next'](self.request)
                return
            self.performed = True
            if self.error:
                return
            if action.attrs.get('handler'):
                action.attrs['handler'](self.widget, self.data)
            if action.attrs.get('next'):
                self.next = action.attrs['next'](self.request)

    @property
    def rendered(self):
        if not self.performed:
            return self.widget(request=self.request)
        return self.widget(data=self.data)

    @property
    def actions(self):
        result = []

        def collect_actions(level):
            for widget in level.values():
                if widget.attrs.get('action'):
                    result.append(widget)
                collect_actions(widget)

        collect_actions(self.widget)
        return result

    def triggered(self, action):
        return self.request.get('action.{0}'.format(action.dottedpath))

    def _error(self, data):
        if data.errors:
            self.error = True
            return
        for subdata in data.values():
            self._error(subdata)
