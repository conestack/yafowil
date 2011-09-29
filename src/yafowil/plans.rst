Check if plans were registered
==============================

::

    >>> from yafowil import loader
    >>> from yafowil.base import factory
    >>> widget = factory('#stringfield')
    >>> widget.blueprints
    ['field', 'label', 'error', 'text']