from node.utils import UNSET
from yafowil.base import factory


factory.defaults['persist'] = False
factory.doc['props']['persist'] = """\
Marker that widget data should be considered in when using persistence
mechanism.
"""

factory.defaults['persist_target'] = UNSET
factory.doc['props']['persist_target'] = """\
Target when using persistence mechanism. If not set, target is widget name.
"""

factory.defaults['persist_writer'] = UNSET
factory.doc['props']['persist_writer'] = """\
Callback used to persist data. Accepts model, target and value as parameters.
"""


def attribute_writer(model, target, value):
    """Write ``value`` to ``target`` attribute on ``model``.
    """
    setattr(model, target, value)


def write_mapping_writer(model, target, value):
    """Write ``value`` to ``target`` write mapping key on ``model``.
    """
    model[target] = value


def node_attribute_writer(model, target, value):
    """Write ``value`` to ``target`` node.attrs key on ``model``.
    """
    model.attrs[target] = value
