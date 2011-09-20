Runtime Data
------------

Initial RuntimeData is empty::    

    >>> from yafowil.base import RuntimeData
    >>> data = RuntimeData()
    >>> data.request
    <UNSET>
    
    >>> data.value
    <UNSET>

    >>> data.extracted
    <UNSET>
    
    >>> data.rendered
    <UNSET>

    >>> data.errors
    []
    
    >>> data.keys()
    []
    
    >>> repr(data.__name__)
    'None'
    
Initial RuntimeData can get its name passed in::

    >>> data = RuntimeData('root')
    >>> data.__name__
    'root'    

RuntimeData can have children::   
    
    >>> data['surname'] = RuntimeData()
    >>> data['fieldset'] = RuntimeData()
    >>> data.keys()
    ['surname', 'fieldset']
    
    >>> data['surname'].__name__
    'surname'
    
And each child can have children again::
    
    >>> data['fieldset']['age'] = RuntimeData()
    >>> data['fieldset']['age'].value = 36
    
RuntimeData can have arbitrary attributes::

    >>> data['surname'].attrs['somekey'] = 'somevalue'
    >>> data['surname'].attrs['somekey']
    'somevalue'
    
You can fetch other data also by its dotted absolute path::
    
    >>> fetched = data.fetch('root.fieldset.age')
    >>> fetched.value 
    36

Or by the absolute path as an list of strings::    

    >>> fetched = data.fetch(['root', 'fieldset', 'age'])
    >>> fetched.value 
    36
    
It works on children::

    >>> fetched = data['fieldset']['age'].fetch('root.surname')
    >>> fetched.__name__
    'surname'

Same with path as a list::

    >>> fetched = data['fieldset']['age'].fetch(['root', 'surname'])
    >>> fetched.__name__
    'surname'
    
It fails if if root element name is wrong::

    >>> fetched = data['fieldset']['age'].fetch(['foobar', 'surname']) 
    Traceback (most recent call last):
    ...
    KeyError: 'Invalid name of root element'

It fails if sub path element is wrong::

    >>> fetched = data['fieldset']['age'].fetch('root.unknown') 
    Traceback (most recent call last):
    ...
        data = data[key]
       - __traceback_info__: fetch path: ['root', 'unknown']
    ...
    KeyError: 'unknown'

Base Widget
-----------
::
    >>> from yafowil.base import Widget
    >>> from yafowil.base import ExtractionError
    
Create some test dummies::

    >>> def test_extractor(widget, data):
    ...     return 'e1'

    >>> def test_extractor2(widget, data):
    ...     return 'e2'

    >>> def test_extractor3(widget, data):
    ...     number = data.request[widget.__name__]
    ...     try:
    ...         return int(number)
    ...     except:
    ...         raise ExtractionError('e3: Integer expected, got %s' % number)
    ...     return value

    >>> def fail_extractor(widget, data):
    ...     raise ValueError, 'extractor has to fail'
    
    >>> def test_edit_renderer(widget, data):
    ...     return 'r1', widget.__name__, str(data), str(widget.attributes)

    >>> def test_edit_renderer2(widget, data):
    ...     return 'r2', widget.__name__, str(data), str(widget.attributes)

    >>> def fail_edit_renderer(widget, data):
    ...     raise ValueError, 'renderer has to fail'

    >>> def test_display_renderer(widget, data):
    ...     return 'disr1', widget.__name__, str(data), str(widget.attributes)

    >>> def fail_display_renderer(widget, data):
    ...     raise ValueError, 'display renderer has to fail'
    
    >>> def test_preprocessor(widget, data):
    ...     data.attrs['test_preprocessor'] = 'called'
    ...     return data
    
    >>> def test_getter(widget, data):
    ...     return 'Test Value'

    >>> def test_getter2(widget, data):
    ...     return 999

The widget class::    
    
    >>> test_request = {'MYUID': 'New Test Value'}
    >>> testwidget = Widget([('1', test_extractor)], 
    ...                     [('1', test_edit_renderer)], 
    ...                     [('1', test_display_renderer)], 
    ...                     [('1', test_preprocessor)],
    ...                     'MYUID', test_getter,
    ...                     dict(test1='Test1', test2='Test2'))
        
    >>> testwidget() 
    ('r1', 'MYUID', "<RuntimeData MYUID, value='Test Value', extracted=<UNSET>, 
    attrs={'test_preprocessor': 'called'} at ...>", "{'test1': 'Test1', 
    'test2': 'Test2'}")
    
A passed in request does not trigger extraction::    
    
    >>> testwidget(request=test_request) 
    ('r1', 'MYUID', "<RuntimeData MYUID, value='Test Value', extracted=<UNSET>, 
    attrs={'test_preprocessor': 'called'} at ...>", "{'test1': 'Test1', 
    'test2': 'Test2'}")
    
Extraction is an explicit task::    
    
    >>> data = testwidget.extract(test_request)
    >>> data
    <RuntimeData MYUID, value='Test Value', extracted='e1', 
    attrs={'test_preprocessor': 'called'} at ...>
    
    >>> data.attrs['test_preprocessor']
    'called'
    
Preprocessor is only called once!::    
    
    >>> data.attrs['test_preprocessor'] = 'reset'
    >>> data = testwidget._runpreprocessors(data)
    >>> data.attrs['test_preprocessor']
    'reset'    
    
Different cases,

a.1) defaults: edit::     
    
    >>> testwidget = Widget([('1', test_extractor)], 
    ...                     [('1', test_edit_renderer)], 
    ...                     [('1', test_display_renderer)], 
    ...                     [],
    ...                     'MYUID', test_getter,
    ...                     dict(test1='Test1', test2='Test2'),
    ...                     )    
    >>> testwidget()
    ('r1', 'MYUID', "<RuntimeData MYUID, value='Test Value', extracted=<UNSET> 
    at ...>", "{'test1': 'Test1', 'test2': 'Test2'}")

a.2) mode display::   
    
    >>> testwidget = Widget([('1', test_extractor)], 
    ...                     [('1', test_edit_renderer)], 
    ...                     [('1', test_display_renderer)], 
    ...                     [],
    ...                     'MYUID', test_getter,
    ...                     dict(test1='Test1', test2='Test2'),
    ...                     mode='display')    
    >>> testwidget()
    ('disr1', 'MYUID', "<RuntimeData MYUID, value='Test Value', extracted=<UNSET> 
    at ...>", "{'test1': 'Test1', 'test2': 'Test2'}")

a.3) mode skip::   
    
    >>> testwidget = Widget([('1', test_extractor)], 
    ...                     [('1', test_edit_renderer)], 
    ...                     [('1', test_display_renderer)], 
    ...                     [],
    ...                     'MYUID', test_getter,
    ...                     dict(test1='Test1', test2='Test2'),
    ...                     mode='skip')    
    >>> testwidget()
    u''
    
a.4) mode w/o renderer:: 

    >>> testwidget = Widget([('1', test_extractor)], 
    ...                     [], [], [],
    ...                     'MYUID', test_getter,
    ...                     dict(test1='Test1', test2='Test2'),
    ...                     mode='display')    
    >>> testwidget()
    Traceback (most recent call last):
    ...
    ValueError: no renderers given for widget 'MYUID' at mode 'display'
    
b.1) two extractors w/o request:: 
        
    >>> testwidget = Widget([('1', test_extractor), ('2', test_extractor2)], 
    ...                     [('1', test_edit_renderer), 
    ...                      ('2', test_edit_renderer2)], 
    ...                     [('1', test_display_renderer)], 
    ...                     [],
    ...                     'MYUID2', test_getter,
    ...                     dict(test1='Test1', test2='Test2'))
    >>> testwidget()
    ('r2', 'MYUID2', "<RuntimeData MYUID2, value='Test Value', 
    extracted=<UNSET> at ...>", "{'test1': 'Test1', 'test2': 'Test2'}")
    
b.2) extractor with request, non int has to fail::
    
    >>> testwidget = Widget([('1', test_extractor3)], 
    ...                     [('1', test_edit_renderer)], 
    ...                     [('1', test_display_renderer)], 
    ...                     [],
    ...                     'MYUID2', test_getter2,
    ...                     dict(test1='Test1', test2='Test2'))
    >>> testwidget.extract({'MYUID2': 'ABC'})
    <RuntimeData MYUID2, value=999, extracted=<UNSET>, 1 error(s) at ...>    

b.3) extractor with request, but mode display::
    
    >>> testwidget = Widget([('1', test_extractor3)], 
    ...                     [('1', test_edit_renderer)], 
    ...                     [('1', test_display_renderer)], 
    ...                     [],
    ...                     'MYUID2', test_getter2,
    ...                     dict(test1='Test1', test2='Test2'),
    ...                     mode='display')    
    >>> testwidget.extract({'MYUID2': '123'})
    <RuntimeData MYUID2, value=999, extracted=<UNSET> ...>    

b.3) two extractors with request::

    >>> testwidget = Widget([('1', test_extractor3)], 
    ...                     [('1', test_edit_renderer)], 
    ...                     [('1', test_display_renderer)], 
    ...                     [],
    ...                     'MYUID2', test_getter2,
    ...                     dict(test1='Test1', test2='Test2'))

    >>> testwidget.extract({'MYUID2': '123'})
    <RuntimeData MYUID2, value=999, extracted=123 at ...>
    
A failing widget::

    >>> import sys, traceback
    >>> testwidget = Widget([('1', fail_extractor)], 
    ...                     [('1', fail_edit_renderer)], 
    ...                     [('1', test_display_renderer)], 
    ...                     [],
    ...                     'MYFAIL', '',
    ...                     dict())

    >>> try:
    ...    testwidget.extract({})
    ... except Exception, e:
    ...    traceback.print_exc(file=sys.stdout)
    Traceback (most recent call last):
      ...
        data.extracted = extractor(self, data)
    <p>yafowil widget processing info:<ul><li>widget: 
    <strong>MYFAIL</strong></li><li>task: 
    <strong>extract</strong></li><li>description: 
    <strong>with name "1"</strong></li></ul></p>
      ...
    ValueError: extractor has to fail

XXX: produce non html output test, currently html is default::

    Traceback (most recent call last):
    ...
        data.extracted = extractor(self, data)
        yafowil widget processing info:
        - widget: MYFAIL
        - task  : extract
        - descr : with name "1"
    ...
    ValueError: extractor has to fail   

    >>> try:
    ...    testwidget()
    ... except Exception, e:
    ...    traceback.print_exc(file=sys.stdout)
    Traceback (most recent call last):
    ...
    ValueError: renderer has to fail        
    
Plausability::

    >>> testwidget(data=data, request={})
    Traceback (most recent call last):
    ...
    ValueError: if data is passed in, don't pass in request!
        
The dottedpath.

Fails with no name in root::
 
    >>> testwidget = Widget([], [], [], [])    
    >>> testwidget.dottedpath
    Traceback (most recent call last):
    ...
    ValueError: Root widget has no name! Pass it to factory.
    
At this test level the factory is not used, so we pass it directly to Widget::    

    >>> testwidget = Widget([], [], [], [], uniquename='root')    
    >>> testwidget.dottedpath
    'root'
    
   >>> testwidget['child'] = Widget([], [], [], [])
   >>> testwidget['child'].dottedpath
   'root.child'

   >>> testwidget['child']['level3'] = Widget([], [], [], [])
   >>> testwidget['child']['level3'].dottedpath
   'root.child.level3'

The mode::

    >>> testwidget = Widget([], [], [], [], uniquename='root')
    >>> data = testwidget.extract({})
    >>> data.mode
    'edit'    

    >>> testwidget = Widget([], [], [], [], uniquename='root', mode='display')
    >>> data = testwidget.extract({})
    >>> data.mode
    'display'    

    >>> testwidget = Widget([], [], [], [], uniquename='root', mode='skip')
    >>> data = testwidget.extract({})
    >>> data.mode
    'skip'    

    >>> testwidget = Widget([], [], [], [], uniquename='root', mode='other')
    >>> data = testwidget.extract({})
    Traceback (most recent call last):
    ...      
    ValueError: mode must be one out of 'edit', 'display', 'skip', but 'other' was given
    
    >>> def mode(widget, data):
    ...     return 'edit'
    >>> testwidget = Widget([], [], [], [], uniquename='root', mode=mode)
    >>> data = testwidget.extract({})
    >>> data.mode
    'edit'    

    >>> def mode(widget, data):
    ...     return 'display'
    >>> testwidget = Widget([], [], [], [], uniquename='root', mode=mode)
    >>> data = testwidget.extract({})
    >>> data.mode
    'display'    
     
     
factory
-------

Fill factory with test blueprints::

    >>> from yafowil.base import Factory
    >>> factory = Factory()
    >>> factory.register('widget_test', [test_extractor], [test_edit_renderer])
    >>> factory.extractors('widget_test')
    [<function test_extractor at ...>]
    
    >>> factory.edit_renderers('widget_test')
    [<function test_edit_renderer at ...>]
    
    >>> testwidget = factory('widget_test', name='MYFAC', value=test_getter, 
    ...                      props=dict(foo='bar'))
    >>> testwidget()
    ('r1', 'MYFAC', "<RuntimeData MYFAC, value='Test Value', extracted=<UNSET> 
    at ...>", "{'foo': 'bar'}")

    >>> factory.register('widget_test', [test_extractor], [test_edit_renderer], 
    ...                  preprocessors=[test_preprocessor])
    
    >>> factory.preprocessors('widget_test')
    [<function test_preprocessor at 0x...>]
    
    >>> def test_global_preprocessor(widget, data):
    ...     return data
    
    >>> factory.register_global_preprocessors([test_global_preprocessor])
    >>> factory.preprocessors('widget_test')
    [<function test_global_preprocessor at 0x...>, 
    <function test_preprocessor at 0x...>]

    >>> testwidget = factory('widget_test', name='MYFAC', value=test_getter, 
    ...                      props=dict(foo='bar'), mode='display')
    >>> data = testwidget.extract({})
    >>> data.mode
    'display'    
        
We can create sets of static builders, i.e. to have a validating password
field with two input fields in. Here a simpler example:: 

    >>> def create_static_compound(widget, factory):
    ...     widget['one'] = factory('widget_test', widget.attrs)
    ...     widget['two'] = factory('widget_test', widget.attrs)
        
    >>> factory.register('static_compound', [], [], 
    ...                  builders=[create_static_compound])
    
    >>> widget = factory('static_compound', props={})
    >>> widget.keys()
    ['one', 'two']
    
    >>> factory.builders('static_compound')
    [<function create_static_compound at 0x...>]
    
Some basic name checks are done::
    
    >>> factory.register('*notallowed', [], [])
    Traceback (most recent call last):
    ...
    ValueError: Asterisk * as first char not allowed as name.

    >>> factory.register('not:allowed', [], [])
    Traceback (most recent call last):
    ...
    ValueError: Colon : as char not allowed in name.


Widget tree manipulation
------------------------

Widget trees provide functionality described in ``node.interfaces.IOrder``,
which makes it possible to insert widgets at a specific place in an existing
widget tree::

    >>> widget = factory('widget_test', name='root')
    >>> widget['1'] = factory('widget_test')
    >>> widget['2'] = factory('widget_test')
    >>> widget.printtree()
    <class 'yafowil.base.Widget'>: root
      <class 'yafowil.base.Widget'>: 1
      <class 'yafowil.base.Widget'>: 2
    
    >>> new = factory('widget_test', name='3')
    >>> ref = widget['1']
    >>> widget.insertbefore(new, ref)
    >>> new = factory('widget_test', name='4')
    >>> widget.insertafter(new, ref)
    >>> widget.printtree()
    <class 'yafowil.base.Widget'>: root
      <class 'yafowil.base.Widget'>: 3
      <class 'yafowil.base.Widget'>: 1
      <class 'yafowil.base.Widget'>: 4
      <class 'yafowil.base.Widget'>: 2


Request chains via factory
--------------------------

Sometimes we want to wrap inputs by UI candy, primary for usability reasons.
This might be a label, some error output or div around. We dont want to register
an amount of X possible widgets with an amount of Y possible wrappers. Therefore
we can factor a widget in a chain defined colon-separated, i.e 'outer:inner' or
'field:error:text'. Chaining works for all parts: edit_renderers, extractors,
preprocessors and builders. Most inner and first executed is right (we prefix
with wrappers)!. The chain can be defined as list instead of a colon seperated
string as well::

    >>> def inner_renderer(widget, data):
    ...     return u'<INNER />'

    >>> def inner_extractor(widget, data):
    ...     return ['extracted inner']

    >>> def outer_renderer(widget, data):
    ...     return u'<OUTER>%s</OUTER>' % data.rendered
    
    >>> def outer_extractor(widget, data):
    ...     return data.extracted + ['extracted outer']
        
    >>> factory.register('inner', [inner_extractor], [inner_renderer])
    >>> factory.register('outer', [outer_extractor], [outer_renderer])    
    >>> factory.display_renderers('inner')
    [<function inner_renderer at ...>]

    >>> factory.edit_renderers('inner')
    [<function inner_renderer at ...>]

    >>> factory.renderers('inner')
    Traceback (most recent call last):
    ...
    RuntimeError: Deprecated since 1.2, use either edit_renderers or display_renderers
    
Colon seperated blueprint chain definition::
    
    >>> widget = factory('outer:inner')
    >>> data = widget.extract({})
    >>> data.extracted
    ['extracted inner', 'extracted outer']
    
    >>> widget(data)
    u'<OUTER><INNER /></OUTER>'

Blueprint chain definition as list::
    
    >>> widget = factory(['outer', 'inner'])
    >>> data = widget.extract({})
    >>> data.extracted
    ['extracted inner', 'extracted outer']
    
    >>> widget(data)
    u'<OUTER><INNER /></OUTER>'
    

Inject custom specials blueprints into  chain
---------------------------------------------

You may need an behavior just one time and just for one special widget. Here
you can inject your custom special render or extractor into the chain::
    
    >>> def special_renderer(widget, data):
    ...     return u'<SPECIAL>%s</SPECIAL>' % data.rendered

    >>> def special_extractor(widget, data):
    ...     return data.extracted + ['extracted special']

    >>> widget = factory('outer:*special:inner', 
    ...                  custom={'special': ([special_extractor], 
    ...                                      [special_renderer], 
    ...                                      [], [], [])})
    >>> data = widget.extract({})
    >>> data.extracted
    ['extracted inner', 'extracted special', 'extracted outer']

    >>> widget(data)
    u'<OUTER><SPECIAL><INNER /></SPECIAL></OUTER>'

BBB, w/o display_renderer::        
    >>> widget = factory('outer:*special:inner', 
    ...                  custom={'special': ([special_extractor], 
    ...                                      [special_renderer], 
    ...                                      [], [])})
    >>> data = widget.extract({})
    >>> data.extracted
    ['extracted inner', 'extracted special', 'extracted outer']


Prefixes with widgets and factories
-----------------------------------

Factory called widget attributes should know about its factory name with a
prefix:: 

    >>> def prefix_renderer(widget, data):
    ...     return u'<ID>%s</ID>' % widget.attrs['id']
    
    >>> factory.register('prefix', [], [prefix_renderer])
    >>> widget = factory('prefix', props={'prefix.id': 'Test'})
    >>> widget()
    u'<ID>Test</ID>'

    >>> widget = factory('prefix', name='test', props={'id': 'Test2'})
    >>> widget()
    u'<ID>Test2</ID>'
    
    
modify defaults for widgets attributes via factory
--------------------------------------------------

1st look for prefixed in attributes::

    >>> factory.defaults['id'] = 'Test3'
    >>> widget = factory('prefix', name='test')
    >>> widget()
    u'<ID>Test3</ID>'

2nd look for unprefixed in attributes::

    >>> factory.defaults['prefix.id'] = 'Test4'
    >>> widget = factory('prefix', name='test')
    >>> widget()
    u'<ID>Test4</ID>'

3rd look for prefixed in defaults::

    >>> widget = factory('prefix', name='test', props={'prefix.id': 'Test'})
    >>> widget()
    u'<ID>Test</ID>'

4th look for unprefixed in defaults::

    >>> widget = factory('prefix', name='test', props={'id': 'Test2'})
    >>> widget()
    u'<ID>Test2</ID>'

5th raise keyerror::

    >>> del factory.defaults['id']
    >>> del factory.defaults['prefix.id']
    >>> widget = factory('prefix', name='test')
    >>> try:
    ...     widget()
    ... except KeyError, e:
    ...     print e
    'Property with key "id" is not given on widget "test" (no default).'


fetch value
-----------
::
    >>> from yafowil.base import fetch_value
    >>> dmarker = list()
    >>> defaults = dict(default=dmarker)
    >>> widget_no_return = Widget([],[],[], 'empty', defaults=defaults)
    >>> widget_with_value = Widget([],[],[], 'value', 
    ...                            value_or_getter='withvalue', 
    ...                            defaults=defaults)
    >>> widget_with_default = Widget([],[],[], 'default',
    ...                              properties=dict(default='defaultvalue'),
    ...                              defaults=defaults)
    >>> widget_with_both = Widget([],[],[], 'both', 
    ...                           value_or_getter='valueboth',  
    ...                           properties=dict(default='defaultboth'),
    ...                           defaults=defaults)
    >>> data_empty = RuntimeData()
    >>> data_filled = RuntimeData()
    >>> data_filled.extracted = 'extractedvalue'    
    
    >>> data_empty.value = widget_no_return.getter
    >>> fetch_value(widget_no_return, data_empty) is dmarker
    True

    >>> data_filled.value = widget_no_return.getter
    >>> fetch_value(widget_no_return, data_filled)
    'extractedvalue'

    >>> data_empty.value = widget_with_value.getter
    >>> fetch_value(widget_with_value, data_empty)
    'withvalue'

    >>> data_filled.value = widget_with_value.getter
    >>> fetch_value(widget_with_value, data_filled)
    'extractedvalue'    

    >>> data_empty.value = widget_with_default.getter
    >>> fetch_value(widget_with_default, data_empty)
    'defaultvalue'

    >>> data_filled.value = widget_with_default.getter
    >>> fetch_value(widget_with_default, data_filled)
    'extractedvalue'        

    >>> data_empty.value = widget_with_both.getter
    >>> fetch_value(widget_with_both, data_empty)
    'valueboth'

    >>> data_filled.value = widget_with_both.getter
    >>> fetch_value(widget_with_default, data_filled)
    'extractedvalue'        
