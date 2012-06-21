from .base import factory

DOC_TEXT = """\
Text Widgets
------------

::

  Literal Write me
"""

DOC_SELECT = """\
Selection Widgets
-----------------

Write me.
"""

def get_example():
    text = factory('compound', name='yafowil-text')
    text['plain'] = factory('#field:text', props={
        'label': 'Text Input',
    })
    text['email'] = factory('#field:email', props={
        'label': 'E-Mail Input',
    })
    text['number'] = factory('#field:number', props={
        'label': 'Number Input (float)',
    })
    text['intnumber'] = factory('#field:number', props={
        'label': 'Number Input (int)',
        'datatype': 'integer',
    })
    text['password'] = factory('#field:password', props={
        'label': 'Password Input',
    })
    select = factory('compound', name='yafowil-text')
    select['radiosingle'] = factory('#field:select', props={
        'label': 'Select (radio, single)',
        'vocabulary': ['Python 2', 'Python 3'],
        'format': 'radio',
    })
    select['blocksingle'] = factory('#field:select', props={
        'label': 'Select (block, single)',
        'vocabulary': ['Python', 'Java', 'Perl', 'Erlang', 'C', 'C++', 'C#'],
        'format': 'block',
    })
    select['checkboxmultiple'] = factory('#field:select', props={
        'label': 'Select (multiple, checkbox)',
        'vocabulary': ['Python 2', 'Python 3'],
        'format': 'checkbox',
        'multivalued': True,
    })
    select['blockmultiple'] = factory('#field:select', props={
        'label': 'Select (multiple, checkbox)',
        'vocabulary': ['Python', 'Java', 'Perl', 'Erlang', 'C', 'C++', 'C#'],
        'format': 'block',
        'multivalued': True,
    })
    return [{'widget': text, 'doc': DOC_TEXT, 'title': 'Text'},
            {'widget': select, 'doc': DOC_SELECT, 'title': 'Select'}]
