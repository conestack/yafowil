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
============

Yafowil aims to have no dependencies to any framework. It utilizes the ``node``  
package. It also does not know about data-storage, but offers you a hook to add 
your handler. 

Tired of inventing widgets again and again after switching the python framework 
Yafowil is intentionally written framework-independent. By just feeding it with 
configuration it can be used and extended in most of existing python web 
frameworks. Zope, Pyramid and Django are hot candidates. 

Integration packages such as ``yafowil.zope2`` or ``yafowil.webob`` are providing 
neccessary hooks to specific frameworks.


Example
=======

For the impatient, code says more than 1000 words: A very simple example form 
works like so.
::

    >>> import yafowil.loader
    >>> from yafowil.base import factory
    >>> from yafowil.controller import Controller

Create a form.
::

    >>> form = factory(
    ...     'form',
    ...     name='myform', 
    ...     props={
    ...         'action': 'http://www.domain.tld/someform',
    ...     }
    ... )
    >>> form['someinput'] = factory(
    ...     'label:text', 
    ...     props={
    ...         'label': 'Your Text',
    ...     }
    ... )
    
    >>> def formaction(widget, data):
    ...     data.printtree()

    >>> def formnext(request):
    ...     return 'http://www.domain.tld/result'

    >>> form['submit'] = factory(
    ...     'submit', 
    ...     props={
    ...         'handler': formaction, 
    ...         'next': formnext,
    ...         'action': True,
    ...     }
    ... )    

Render empty form.   
::

    >>> form()
    u'<form action="http://www.domain.tld/someform" 
    enctype="multipart/form-data" id="form-myform" method="post"><label 
    for="input-myform-someinput">Your Text</label><input 
    id="input-myform-someinput" name="myform.someinput" type="text" 
    /><input id="input-myform-submit" name="action.myform.submit" 
    type="submit" value="submit" /></form>'

Get form data out of request (request is expected dict-like).
::

    >>> request = {
    ...     'myform.someinput': 'Hello World', 
    ...     'action.myform.submit': 'submit',
    ... }
    >>> controller = Controller(form, request)
    <RuntimeData myform, value=None, extracted=None at ...>
      <RuntimeData myform.someinput, value=None, extracted='Hello World', 
      attrs={'input_field_type': 'text'} at ...>
      <RuntimeData myform.submit, value=None, extracted=<UNSET> at ...>

Basic functions
===============

Yafowil provides widgets for all HTML standard inputs, Such as:

- text
- textarea
- checkbox
- radio
- selects (single, multiple)
- file
- hidden
- submit
- and some more

Usally you request a widget instance from the factory. I.e. by calling
:: 

    widget = factory('text')

where ``text`` is the widget registration name.

A form or part of a form is organized as a tree of widgets. Thus, a widget is 
either a compound (form, fieldset, etc) containing child widgets or leafs. 

Widgets can be chained. Let's say we want a HTML field containing a label
and an input, this looks like
::

    widget = factory('field:label:text')

This causes the widget to use the registered renderers, extractors, etc of the
widgets ``field``, ``label`` and ``text`` in order.

Compounds are build dict-like (form, fieldsets, etc).
::

    >>> form = factory(
    ...     'form',
    ...     'UNIQUENAME',
    ...     props={
    ...         'action': 'someurl',
    ...     },
    ... )
    >>> form['somefield'] = factory(
    ...     'field:label:text',
    ...     props={
    ...         'label': 'Some Field',
    ...     },
    ... )
    >>> form['somefieldset'] = factory(
    ...     'fieldset',
    ...     props={
    ...         'legend': 'A Fieldset',
    ...     },
    ... )
    >>> form['somefieldset']['innerfield'] = factory(
    ...     'field:label:text',
    ...     props={
    ...         'label': 'Inner Field',
    ...     },
    ... )
    
You can inject custom behaviour by marking a part of the widget name chain with 
the asterisk ``*`` character. Behaviours are one or a combination of a

``extractor``
    extracts, validates and/or converts form-data from the request

``renderer``
    build the markup 

``preprocessor``
    Generic hook to prepare runtime-data. Runs once per runtime-data instance
    before extractors or renderers are running. 

``builder``
    Generic hook called once at factory time of the widget. Here i.e. subwidgets
    can be created.    

:: 

    >>> def myvalidator(widget, data):
    ...    # validate the data, raise ExtractionError if somethings wrong
    ...    return data.extracted
         
    >>> widget = factory(
    ...     'field:label:*myvalidation:text',
    ...     props={
    ...         'label': 'Inner Field',
    ...     },
    ...     custom: {
    ...         'myvalidation': ([myvalidator],[],[],[]),
    ...     }
    ... )

If behaviour is more general and you need it more than once you can register it
in the factory
::

    >>> factory.register('mybehaviour', [myvalidator], [])    

for easy later access
::

    >>> widget = factory(
    ...     'field:label:mybehaviour:text',
    ...     props={
    ...         'label': 'Inner Field',
    ...     },
    ... )

Detailed Documentation
======================

Theres a `detailed documentation <http://packages.python.org/yafowil>`_ available (TODO).

Source Code
===========

The sources are in a GIT DVCS with its main branches at `github <http://github.com/bluedynamics/yafowil>`_.

We'd be happy to see many forks and pull-requests to make YAFOWIL even better.

Changes
=======

1.0 
---

- Make it work (jensens, rnix)


Contributors
============

- Jens W. Klein <jens@bluedynamics.com>

- Robert Niederrreiter <rnix@squarewave.at>

- Attila Olah

- Christian Scholz aka MrTopf (initial discussion)

