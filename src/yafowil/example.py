from .base import factory


def get_example():
    root = factory('fieldset', name='yafowil')
    root['text'] = factory('field:label:error:text')
    return root
