Introduction
============

This is **Yet Another Form WIdget Library** (XHTML). There are plenty of 'em out 
in python space. But I did not find anything puristic, thin, userinterface 
centric, with a set of base input widgets which one can adapt to its needs. 

It's all just about rendering widgets and extracting the data returned from the 
browser per widget.

Widgets are just configuration. Yafowil does not provide classes for widgets, 
but a factory where you can fetch your widgets from - and register your own. 
 
Yafowil aims to have no dependencies to any framework. It utilizes ``Node`` from 
``zodict``. And so it has flimsy dependecies to ``zope.location``. It also does 
not know about data-storage, but offers you a hook to add your handler. 

Tired of inventing widgets again and again after switching the python framework 
Yafowil is intentionally written framework-independent. By just feeding it with 
configuration it can be used and extended in most of existing python web 
frameworks. Zope, Bfg and Django are hot candidates.   

It provides widgets for all HTML standard inputs, Such as: text, textarea, 
dropdown, checkbox, radiobutton, file, hidden, submit. 

There are different possibilities to group or wrap widgets and their behaviour.

First you can register chains of renderers and/or extractors under an own name.

Sesond you can request such chains from the factory. I.e. by calling 
``widget = factory('field:label:text')``. 

Additional it provides the possibility to build compounds (aka subforms). 
The main form is also just a compound. Fieldset is a kind of compound. Compounds
are built using the dict-like and location aware ``Node`` mentioned above.

If one needs an compound several times, it can be build at factory time by 
registering one or more subwidget functions. A good example for such a static 
compound is a validating password widgets (those annoying ones where you need to 
enter your password twice. Its an compound of two simple password widgets plus an 
validation (extractor) on the surrounding compund.

With an ``array`` repeating any widget several times is possible. An array is an 
special dynamic compound.

Other widgets are provided in separate packages. The idea is to use the same 
namespace: ``yafowil.*``. 

Architecture
============

The basic widget get all functionality injected as callables. It is reduced to 
the execution-logic. Other logic is injected on initialization time:

value 
    callable as value-getter or just the value, 

preprocessors 
    list of callables preparing runtime data
    
renderers 
    list of callables creating markup.
    
extractors
    list of callables getting form data out of request, providing it dict-like.

subwidgets
    list of callables constructing contained widgets at factory time.

Also passed is some static configuration:

- name as string,
- arbitary properties as general keyword arguments (for read-only use).
 
Different widget flavors - combinations of preprocessors, extractors, renderers
and subwidgets - are registered in a registry. This registry is also a factory
spitting out configured widgets by name.  

Behaviour
=========
 
To get an instance of the widget call the factory and pass the registered name, 
a unique name for this widget instance, the value (or an getter) and arbitrary 
properties.

Widget instances are providing two functionalities:

extract
    to get values from request as runtime-data back. Extraction means also
    type-conversion or validation. This is all coupled and doing all in one 
    pipeline makes life easier. In the chain or pipeline of extractors each 
    extractor get the values of all previous extractions with the runtime-data.
    If an extractor fails it raises an exception. If ``abort`` (default is on) 
    is set on the exception by a failing extractor, processing is stopped. 
    For each failing extractor the exception is added to the error-list on 
    runtime-data. 
        
render on ``__call__``
    to get the markup of the widget created. you can either pass already 
    extracted runtime data or if not passed it will be called internally.
    In the chain or pipeline of renderers each renderer get the values of all 
    previous rendered with the runtime-data. It has also access to extractions
    and errors.
    
In both cases the preprocessors are called, but only once for each runtime-data.
There are two type of preprocessors: global and by registered widget. Global
ones are called first. In the preprocessors it is also possible to wrap the 
request or value, i.e. in order to use a request provided by some framework as 
input.   

Example
=======

Single Widget Example
---------------------

First we import ``factory``::

    >>> from yafowil.base import factory

To produce a text input field ask the factory::

    >>> textinput = factory('text', 'street', '')
    >>> textinput()
    u'<input id="input-street" name="street" type="text" value="" />'

Provide a css class and a value::    
    
    >>> textinput = factory('text', 'street', 'Seeweg 12', 
    ...                     {'css': {'input': 'aclass'}})
    >>> textinput()
    u'<input class="aclass" id="input-street" name="street" type="text" value="Seeweg 12" />'
    
The same with label::

    >>> textinput = factory('labeled.text', 'street', 'Seeweg 12', 
    ...                     {'css': {'input': 'aclass'},
    ...                      'label':'street'})    
    >>> textinput()
    u'<label for="input-street" id="label-street">Street<input 
    class="aclass" id="input-street" name="street" type="text" 
    value="Seeweg 12" /></label>'
    
Request is assumed as just a dict-like (you may need to wrap your actual request 
to use it). Let get values from it::

    >>> request = {'street': 'Angerzellgasse 4'}
    >>> data = textinput.extract(request)
    >>> data.last_extracted
    'Angerzellgasse 4'

To re-render the widget pass the extracted runtime data::

    >>> textinput(data=data)
    >>> u'<label for="input-street" id="label-street">Street<input 
    class="aclass" id="input-street" name="street" type="text" 
    value="Angerzellgasse 4" /></label>'
   

Changes
=======

1.0 (work in progress)
----------------------

- Initial: Make it work (jensens)

Credits
=======

- Written and concepted by Jens W. Klein <jens@bluedynamics.com>

- Credits to Christian Scholz aka MrTopf for the good discussion about formlibs
  simplified. 
