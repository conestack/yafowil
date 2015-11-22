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
