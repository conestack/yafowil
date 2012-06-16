Test entry_point support tools
------------------------------

::

    >>> from yafowil.utils import get_entry_points
    >>> get_entry_points()
    [...EntryPoint.parse('register = yafowil.loader:register')...]

    >>> get_entry_points('nonexisting')
    []

    >>> from yafowil.utils import get_plugin_names
    >>> get_plugin_names()
    [...'yafowil.loader'...]

    >>> get_plugin_names('nonexisting')
    []


Test UNSET
----------

::

    >>> from yafowil.utils import UNSET
    >>> UNSET
    <UNSET>
    
    >>> str(UNSET)
    ''

    >>> bool(UNSET)
    False

    >>> len(UNSET)
    0

Test the Vocabulary
-------------------

::

    >>> from yafowil.utils import vocabulary
    >>> vocabulary('foo')
    [('foo', 'foo')]

    >>> vocabulary({'key': 'value'})
    [('key', 'value')]

    >>> vocabulary(['value', 'value2'])
    [('value', 'value'), ('value2', 'value2')]

    >>> vocabulary([('key', 'value'), ('key2', 'value2', 'v2.3'), ('key3',)])
    [('key', 'value'), ('key2', 'value2'), ('key3', 'key3')]
    
    >>> def callme():
    ...     return 'bar'
    
    >>> vocabulary(callme)
    [('bar', 'bar')]
    
    >>> vocabulary(None) is None
    True

    Vocabulary returns a sorted list:
    >>> vocabulary(['b', 'a', 'c'])
    [('a', 'a'), ('b', 'b'), ('c', 'c')]

    ... dictionaries are sorted by key:  
    >>> vocabulary({'b':5, 'a':10, 'c':1})
    [('a', 10), ('b', 5), ('c', 1)]
        
Test Tag renderer
-----------------

::

    >>> from yafowil.utils import Tag
    >>> tag = Tag(lambda msg: msg)    
    >>> a = {'class': u'fancy', 'id': '2f5b8a234ff'}
    >>> tag('p', 'Lorem Ipsum. ', u'Hello World!', 
    ...     class_='fancy', id='2f5b8a234ff')
    u'<p class="fancy" id="2f5b8a234ff">Lorem Ipsum. Hello World!</p>' 
    
    >>> tag('dummy', name='foo')
     u'<dummy name="foo" />'
     
    >>> tag('dummy', name=None)
    u'<dummy />'
    
    >>> tag('dummy', name=UNSET)
    u'<dummy />'
     
deprecated test::

    >>> from yafowil.utils import tag as deprecated_tag
    >>> deprecated_tag('div', 'foo')
    u'<div>foo</div>'

Test CSS Classes
----------------

::

    >>> from plumber import plumber
    >>> from node.base import OrderedNode
    >>> from node.parts import Nodespaces
    >>> from node.parts import Attributes
    >>> class CSSTestNode(OrderedNode):
    ...     __metaclass__ = plumber
    ...     __plumbing__ = Nodespaces, Attributes
    >>> widget = CSSTestNode()
    >>> widget.attrs['required'] = False
    >>> widget.attrs['required_class'] = None
    >>> widget.attrs['required_class_default'] = 'required'
    >>> widget.attrs['error_class'] = None
    >>> widget.attrs['error_class_default'] = 'error'
    >>> widget.attrs['class'] = None
    
    >>> class DummyData(object):
    ...     def __init__(self):
    ...         self.errors = []
    >>> data = DummyData()
    
    >>> from yafowil.utils import cssclasses
    >>> print cssclasses(widget, data)
    None

    >>> widget.attrs['class'] = 'foo bar'
    >>> print cssclasses(widget, data)
    bar foo
    
    >>> widget.attrs['class'] = None
    >>> widget.attrs['required'] = True
    >>> print cssclasses(widget, data)
    None
    
    >>> widget.required = False
    >>> data.errors = True
    >>> print cssclasses(widget, data)
    None

    >>> widget.attrs['error_class'] = True
    >>> print cssclasses(widget, data)
    error

    >>> widget.attrs['class'] = 'foo bar'
    >>> print cssclasses(widget, data)
    bar error foo

    >>> widget.attrs['class'] = None
    >>> widget.attrs['error_class'] = 'othererror'
    >>> print cssclasses(widget, data)
    othererror

    >>> data.errors = False
    >>> print cssclasses(widget, data)
    None
    
    >>> widget.attrs['required'] = True
    >>> print cssclasses(widget, data)
    None

    >>> widget.attrs['required_class'] = True
    >>> print cssclasses(widget, data)
    required

    >>> widget.attrs['required_class'] = 'otherrequired'
    >>> print cssclasses(widget, data)
    otherrequired

    >>> widget.attrs['error_class'] = True
    >>> data.errors = True
    >>> widget.attrs['required_class'] = 'required'
    >>> print cssclasses(widget, data)
    error required

    >>> widget.attrs['class'] = 'foo bar'
    >>> print cssclasses(widget, data)
    bar error foo required
    
    >>> print cssclasses(widget, data, additional=['zika', 'akiz'])
    akiz bar error foo required zika
    
Test managedprops annotation
----------------------------

::

    >>> from yafowil.utils import managedprops
    >>> @managedprops('foo', 'bar')
    ... def somefunc(a, b, c):
    ...     return a, b, c
    >>> somefunc(1, 2, 3)
    (1, 2, 3)
    >>> somefunc.__yafowil_managed_props__
    ('foo', 'bar')
