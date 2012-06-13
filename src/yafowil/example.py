from .base import factory

DOC_TEXT = """\
Text Widgets
------------

::

  Literal Write me
"""

def get_example():
    textparts = factory('compound', name='yafowil')
    textparts['plain'] = factory('label:error:text', props={
        'label': 'Text Input',
    })
    textparts['email'] = factory('label:error:email', props={
        'label': 'E-Mail Input',
    })
    textparts['number'] = factory('label:error:number', props={
        'label': 'Number Input (float)',
    })
    textparts['intnumber'] = factory('label:error:number', props={
        'label': 'Number Input (int)',
        'datatype': 'int',
    })
    textparts['password'] = factory('label:error:password', props={
        'label': 'Password Input',
    })
    return [{'widget': textparts, 'doc': DOC_TEXT}]
