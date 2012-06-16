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
    text['plain'] = factory('label:error:text', props={
        'label': 'Text Input',
    })
    text['email'] = factory('label:error:email', props={
        'label': 'E-Mail Input',
    })
    text['number'] = factory('label:error:number', props={
        'label': 'Number Input (float)',
    })
    text['intnumber'] = factory('label:error:number', props={
        'label': 'Number Input (int)',
        'datatype': 'integer',
    })
    text['password'] = factory('label:error:password', props={
        'label': 'Password Input',
    })
    select = factory('compound', name='yafowil-text')
    select['radiosingle'] = factory('label:error:select', props={
        'label': 'Select (radio, single)',
        'vocabulary': ['Python 2', 'Python 3'],
        'format': 'radio',
    })
    select['blocksingle'] = factory('label:error:select', props={
        'label': 'Select (block, single)',
        'vocabulary': ['Python', 'Java', 'Perl', 'Erlang', 'C', 'C++', 'C#'],
        'format': 'block',
    })
    select['checkboxmultiple'] = factory('label:error:select', props={
        'label': 'Select (multiple, checkbox)',
        'vocabulary': ['Python 2', 'Python 3'],
        'format': 'checkbox',
        'multivalued': True,
    })
    select['blockmultiple'] = factory('label:error:select', props={
        'label': 'Select (multiple, checkbox)',
        'vocabulary': ['Python', 'Java', 'Perl', 'Erlang', 'C', 'C++', 'C#'],
        'format': 'block',
        'multivalued': True,
    })
    return [{'widget': text, 'doc': DOC_TEXT, 'title': 'Text'},
            {'widget': select, 'doc': DOC_SELECT, 'title': 'Select'}]
