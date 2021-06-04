from node.serializer import serialize
from node.tests import NodeTestCase
from yafowil.base import factory
import json
import yafowil.loader  # noqa


class TestSerializer(NodeTestCase):

    def test_serialize_Widget(self):
        form = factory(
            'form',
            name='form',
            props={
                'action': 'http://example.com/form'
            })
        form['title'] = factory(
            'field:label:text',
            value='Hallo',
            props={
                'label': 'Title',
                'help': 'I am the title',
                'required': 'Title is required'
            })
        json_form = json.loads(serialize(form, simple_mode=True))
        self.assertEqual(json_form, {
            u'factory': u'form',
            u'name': u'form',
            u'attrs': {
                u'action': u'http://example.com/form'
            },
            u'children': [{
                u'factory': u'field:label:text',
                u'name': u'title',
                u'attrs': {
                    u'label': u'Title',
                    u'help': u'I am the title',
                    u'required': u'Title is required'
                },
            }],
        })
