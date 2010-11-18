Introduction
============

This is **Yet Another Form WIdget Library** (XHTML). There are plenty of 'em out 
in Python space. But I did not find anything puristic, thin, userinterface 
centric, with a set of base input widgets which one can adapt to its needs. 

It's all just about rendering widgets and extracting the data returned from the 
browser per widget. 

Yafowil widgets are just configuration. Yafowil provides a factory where you can 
fetch your widgets instances from. Or you register your own.

Dependencies
------------ 
 
Yafowil aims to have no dependencies to any framework. It utilizes ``Node`` from 
``zodict``. And so it has flimsy dependecies to ``zope.location``. It also does 
not know about data-storage, but offers you a hook to add your handler. 

Tired of inventing widgets again and again after switching the python framework 
Yafowil is intentionally written framework-independent. By just feeding it with 
configuration it can be used and extended in most of existing python web 
frameworks. Zope, Pyramid and Django are hot candidates. 


Hello World
===========

For the impatient, code says more than 1000 words: A simple hello world form 
works like so::

    >>> import yafowil.loader
    >>> from yafowil.base import factory
    >>> from yafowil.controller import Controller
    
Create a form::
    
    >>> form = factory('form', name='myform', 
    ...     props={'action': 'http://www.domain.tld/someform'})
    >>> form['someinput'] = factory('label:text', 
    ...     props={'label': 'Your Text'})
    
    >>> def formaction(widget, data):
    ...     data.printtree()

    >>> def formnext(request):
    ...     return 'http://www.domain.tld/result'
    
    >>> form['submit'] = factory('submit', 
    ...     props={'handler': formaction, 'next': formnext, 'action': True})
    

Render an empty form    

    >>> form()
    u'<form action="http://www.domain.tld/someform" 
    enctype="multipart/form-data" id="form-myform" method="post"><label 
    for="input-myform-someinput">Your Text</label><input 
    id="input-myform-someinput" name="myform.someinput" type="text" 
    /><input id="input-myform-submit" name="action.myform.submit" 
    type="submit" value="submit" /></form>'

    
Get form data out of request (request is expected dict-like)::

    >>> request = {'myform.someinput': 'Hello World', 
    ...            'action.myform.submit': 'submit'}
    >>> controller = Controller(form, request)
    <RuntimeData myform, value=None, extracted=None at ...>
      <RuntimeData myform.someinput, value=None, extracted='Hello World', 
      attrs={'input_field_type': 'text'} at ...>
      <RuntimeData myform.submit, value=None, extracted=<UNSET> at ...>
     
Basic functions
===============

It provides widgets for all HTML standard inputs, Such as: text, textarea, 
checkbox, radio, selects (single, multiplefile), file, hidden, submit. 

Usally you request a widget instance from the factory. I.e. by calling:: 

    widget = factory('field:label:text')
    
A form is build dict-like. Same with fieldsets::

    form =  factory('form', 'UNIQUENAME', props={'action': 'someurl'})
    form['somefield'] = factory('field:label:text')
    form['somefieldset'] = factory('fieldset', props={'legend': 'A Fieldset'})
    form['somefieldset']['innerfield'] = factory('field:label:text')
    ...
        
You can inject custom behaviour by marking a part of the widget with 
the asterisk ``*`` character. Behaviours are one or a combination of a

extractor
    extracts, validates and/or converts form-data from the request

renderer
    build the markup 
    
preprocessor
    Generic hook to prepare runtime-data. Runs once per runtime-data instance
    before extractors or renderers are running. 
    
builder
    Generic hook called once at factory time of the widget. Here i.e. subwidgets
    can be created.    

:: 

    def myvalidator(widget, data):
       # validate the data, raise ExtractionError if somethings wrong
       return data.extracted
         
    widget = factory('field:label:*myvalidation:text', 
                     custom: {'myvalidation': ([myvalidator],[],[],[]})

If you need behaviour you need is more general  so you need it more than once -
you can register it in the factory for easy later access::

    factory.register('mybehaviour', [myvalidator], [])    
                      
    widget = factory('field:label:mybehaviour:text')


Architecture
============

The basic widget get all functionality injected as callables. It is reduced to 
the execution-logic. Other logic is injected on initialization time. The value
can be passed in as a callable as value-getter or just the value, 

Also passed is some static configuration:

- name as string,
- arbitary properties as general keyword arguments (for read-only use).
 
Different widget flavors - combinations of preprocessors, extractors, renderers
and builders - are registered in a registry. This registry is also a factory
spitting out configured widgets by name.

Behaviour
=========

Widget instances
----------------
 
To get an instance of the widget call the factory and pass the registered name, 
a unique name for this widget instance, the value (or an getter) and arbitrary 
properties and eventually a mapping to custom behaviour.

Widget instances are providing two functionalities:

extract
    to get values from request as runtime-data back. Extraction means also
    type-conversion or validation. This is all coupled and doing it all in one 
    pipeline makes life easier. In the chain or pipeline of extractors each 
    extractor get the values of all previous extractions with the runtime-data.
    If an extractor fails it raises an exception. If ``abort`` (default is on) 
    is set on the exception by a failing extractor, processing is stopped. 
    For each failing extractor the exception is added to the error-list on 
    runtime-data. 
        
render on ``__call__``
    to get the markup of the widget created either pass already extracted 
    runtime data or - if not passed - it will be called internally.
    In the chain or pipeline of renderers each renderer get the values of all 
    previous rendered with the runtime-data. It has also access to extractions
    and errors.
    
In both cases the preprocessors are called, but only once for each runtime-data.
There are two type of preprocessors: global and by widget registered. Global
ones are called first. Hint: In the preprocessors it is also possible to wrap the 
request or value, i.e. in order to use a request provided by some framework as 
input.

Controller
----------   

The controller handles forms and its several actions. Its convinient to use and 
dispatches the actions to handlers and deals with rendering and re-rendering of
the form. Here you can hook in a callable saving the data to the storage of 
your choice.

Example
=======

Single Widget Example
---------------------

First we import ``factory``::

    >>> from yafowil.base import factory

Second we import ``yafowil.commom`` to trigger registration.
    
    >>> import yafowil.common

To produce a text input field ask the factory::

    >>> textinput = factory('text', 'street', '')
    >>> textinput()
    u'<input id="input-street" name="street" type="text" value="" />'

Provide a value::    
    
    >>> textinput = factory('text', 'street', 'Seeweg 12')
    >>> textinput()
    u'<input id="input-street" name="street" type="text" value="Seeweg 12" />'
    
The same with label::

    >>> import yafowil.labeled
    >>> textinput = factory('label:text', 'street', 'Seeweg 12', 
    ...                     {'label':'street'})    
    >>> textinput()
    u'<label for="input-street" id="label-street">Street<input id="input-street" 
    name="street" type="text" value="Seeweg 12" /></label>'
    
Request is assumed as just a dict-like (you may need to wrap your actual request 
to use it). Let get values from it::

    >>> request = {'street': 'Angerzellgasse 4'}
    >>> data = textinput.extract(request)
    >>> data.last_extracted
    'Angerzellgasse 4'

To re-render the widget pass the extracted runtime data::

    >>> textinput(data=data)
    u'<label for="input-street" id="label-street">Street<input id="input-street" 
    name="street" type="text" value="Angerzellgasse 4" /></label>'
   

Changes
=======

1.0 
----------------------

- Initial: Make it work (jensens)

Contributors
============

- Jens W. Klein <jens@bluedynamics.com>

- Robert Niederrreiter <rnix@squarewave.at>

- Christian Scholz aka MrTopf