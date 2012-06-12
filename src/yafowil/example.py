from .base import factory

DOC_TEXT = """\
Text Widgets
------------

::

  Literal Write me
"""

def get_example():
    textparts = factory('compound', name='yafowil')
    textparts['text'] = factory('fieldset', props={
        'legend': 'Input Widgets',
    })
    textparts['text']['plain'] = factory('field:label:error:text', props={
        'label': 'Text Input',
    })
    textparts['text']['email'] = factory('field:label:error:email', props={
        'label': 'E-Mail Input',
    })
    textparts['text']['number'] = factory('field:label:error:number', props={
        'label': 'Number Input (float)',
    })
    textparts['text']['intnumber'] = factory('field:label:error:number', props={
        'label': 'Number Input (int)',
        'datatype': 'int',
    })
    textparts['text']['password'] = factory('field:label:error:password', props={
        'label': 'Password Input',
    })
    return [{'widget': textparts, 'doc': DOC_TEXT}]
