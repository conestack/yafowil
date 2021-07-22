from node.serializer import I_ATTRS_NS
from node.serializer import I_NODE_NS
from node.serializer import serialize
from node.serializer import serializer
from node.serializer import SerializerSettings
from yafowil.base import Widget


@serializer(Widget)
def widget_serializer(encoder, node, data):
    data['factory'] = ':'.join(node.blueprints)


def serialize_widget(widget):
    settings = SerializerSettings()
    settings.set(I_NODE_NS, 'children_key', 'widgets')
    settings.set(I_ATTRS_NS, 'attrs_key', 'props')
    return serialize(widget, simple_mode=True, settings=settings)
