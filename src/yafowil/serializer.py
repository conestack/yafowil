from node.serializer import serializer
from yafowil.base import RuntimeData
from yafowil.base import Widget


@serializer(Widget)
def widget_serializer(encoder, node, data):
    data['factory'] = ':'.join(node.blueprints)


@serializer(RuntimeData)
def runtime_data_serializer(encoder, node, data):
    pass
