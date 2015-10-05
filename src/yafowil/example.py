# -*- coding: utf-8 -*-
from yafowil.base import factory


DOC_PLAIN_TEXT = """\
Plain Text
----------

Simple plaintext widget.

.. code-block:: python

    plaintext = factory('#field:text', props={
        'label': 'Plain Text Input',
        'required': 'Input is required',
        'help': 'Simple Plain Text Field',
    })
"""


def plaintext():
    comp = factory('compound', name='yafowil-plaintext')
    comp['plain'] = factory('#field:text', props={
        'label': 'Plain Text Input',
        'required': 'Input is required',
        'help': 'Simple Plain Text Field',
    })
    return {
        'widget': comp,
        'doc': DOC_PLAIN_TEXT,
        'title': 'Plain Text',
    }


DOC_EMAIL = """
Email
-----

Text input for email addresses.

.. code-block:: python

    email = factory('#field:email', props={
        'label': 'E-Mail Input',
        'help': 'E-Mail Address Field',
    })
"""


def email():
    comp = factory('compound', name='yafowil-email')
    comp['email'] = factory('#field:email', props={
        'label': 'E-Mail Input',
        'help': 'E-Mail Address Field',
    })
    return {
        'widget': comp,
        'doc': DOC_EMAIL,
        'title': 'Email',
    }


DOC_NUMBER = """
Number
------

Input field accepting floating point numbers.

.. code-block:: python

    number = factory('#field:number', props={
        'label': 'Number Input (float)',
        'help': 'Field for floating point number input',
    })
"""


def number():
    comp = factory('compound', name='yafowil-number')
    comp['number'] = factory('#field:number', props={
        'label': 'Number Input (float)',
        'help': 'Field for floating point number input',
    })
    return {
        'widget': comp,
        'doc': DOC_NUMBER,
        'title': 'Number',
    }


DOC_INT = """
Integer
-------

Input field accepting integer values.

.. code-block:: python

    integer = factory('#field:number', props={
        'label': 'Number Input (int)',
        'datatype': 'integer',
        'help': 'Field for integer input',
    })
"""


def integer():
    comp = factory('compound', name='yafowil-integer')
    comp['intnumber'] = factory('#field:number', props={
        'label': 'Number Input (int)',
        'datatype': 'integer',
        'help': 'Field for integer input',
    })
    return {
        'widget': comp,
        'doc': DOC_INT,
        'title': 'Integer',
    }


DOC_PASSWORD = """
Password
--------

Password field.

.. code-block:: python

    password = factory('#field:password', props={
        'label': 'Password Input',
        'help': 'Field for password',
    })
"""


def password():
    comp = factory('compound', name='yafowil-password')
    comp['password'] = factory('#field:password', props={
        'label': 'Password Input',
        'help': 'Field for password',
    })
    return {
        'widget': comp,
        'doc': DOC_PASSWORD,
        'title': 'Password',
    }


DOC_URL = """
URL
---

URL field.

.. code-block:: python

    password = factory('#field:url', props={
        'label': 'URL Input',
        'help': 'Field for URL',
    })
"""


def url():
    comp = factory('compound', name='yafowil-url')
    comp['password'] = factory('#field:url', props={
        'label': 'URL Input',
        'help': 'Field for URL',
    })
    return {
        'widget': comp,
        'doc': DOC_URL,
        'title': 'URL',
    }


DOC_TEXTAREA = """
Textarea
--------

Textarea field.

.. code-block:: python

    textarea = factory('#field:textarea', props={
        'label': 'Textarea',
        'help': 'Textarea field',
        'rows': 5,
    })
"""


def textarea():
    comp = factory('compound', name='yafowil-textarea')
    comp['textarea'] = factory('#field:textarea', props={
        'label': 'Textarea',
        'help': 'Textarea field',
        'rows': 5,
    })
    return {
        'widget': comp,
        'doc': DOC_TEXTAREA,
        'title': 'Textarea',
    }


DOC_RADIO = """\
Radio buttons
-------------

Selection with radio buttons.

.. code-block:: python

    radiobuttons = factory('#field:select', props={
        'label': 'Select',
        'help': 'Single selection as radio buttons',
        'vocabulary': ['Python 2', 'Python 3'],
        'format': 'radio',
    })
"""


def radio():
    comp = factory('compound', name='yafowil-radio')
    comp['radio'] = factory('#field:select', props={
        'label': 'Select',
        'help': 'Single selection as radio buttons',
        'vocabulary': ['Python 2', 'Python 3'],
        'format': 'radio',
    })
    return {
        'widget': comp,
        'doc': DOC_RADIO,
        'title': 'Radio buttons',
    }


DOC_DROPDOWN = """
Selection Dropdown
------------------

Single selection dropdown.

.. code-block:: python

    dropdown = factory('#field:select', props={
        'label': 'Select',
        'help': 'Single selection as dropdown',
        'vocabulary': ['Python', 'Java', 'Perl', 'Erlang', 'C', 'C++', 'C#'],
        'format': 'block',
    })
"""


def dropdown():
    comp = factory('compound', name='yafowil-dropdown')
    comp['dropdown'] = factory('#field:select', props={
        'label': 'Select',
        'help': 'Single selection as dropdown',
        'vocabulary': ['Python', 'Java', 'Perl', 'Erlang', 'C', 'C++', 'C#'],
        'format': 'block',
    })
    return {
        'widget': comp,
        'doc': DOC_DROPDOWN,
        'title': 'Selection Dropdown',
    }


DOC_CHECKBOX = """
Checkbox selection
------------------

Multi selection with checkboxes.

.. code-block:: python

    checkboxes = factory('#field:select', props={
        'label': 'Select',
        'help': 'Multiple selection with checkboxes',
        'vocabulary': ['Python 2', 'Python 3'],
        'format': 'checkbox',
        'multivalued': True,
    })
"""


def checkbox():
    comp = factory('compound', name='yafowil-checkbox')
    comp['checkbox'] = factory('#field:select', props={
        'label': 'Select',
        'help': 'Multiple selection with checkboxes',
        'vocabulary': ['Python 2', 'Python 3'],
        'format': 'checkbox',
        'multivalued': True,
    })
    return {
        'widget': comp,
        'doc': DOC_CHECKBOX,
        'title': 'Checkbox selection',
    }


DOC_BLOCK = """
Selection block
---------------

Multi selection as block.

.. code-block:: python

    selection = factory('#field:select', props={
        'label': 'Select',
        'help': 'multiple as block',
        'vocabulary': ['Python', 'Java', 'Perl', 'Erlang', 'C', 'C++', 'C#'],
        'format': 'block',
        'multivalued': True,
    })
"""


def block():
    comp = factory('compound', name='yafowil-block')
    comp['block'] = factory('#field:select', props={
        'label': 'Select',
        'help': 'multiple as block',
        'vocabulary': ['Python', 'Java', 'Perl', 'Erlang', 'C', 'C++', 'C#'],
        'format': 'block',
        'multivalued': True,
    })
    return {
        'widget': comp,
        'doc': DOC_BLOCK,
        'title': 'Selection block',
    }


def get_example():
    return [plaintext(), email(), number(), integer(), password(), url(),
            textarea(), radio(), dropdown(), checkbox(), block()]
