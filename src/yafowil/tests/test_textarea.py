from node.utils import UNSET
from yafowil.base import factory
from yafowil.persistence import write_mapping_writer
from yafowil.tests import YafowilTestCase


class TestTextarea(YafowilTestCase):

    def test_textarea_blueprint(self):
        # Textarea widget
        widget = factory(
            'textarea',
            name='MYTEXTAREA',
            value=None)
        self.assertEqual(widget(), (
            '<textarea class="textarea" cols="80" id="input-MYTEXTAREA" '
            'name="MYTEXTAREA" rows="25"></textarea>'
        ))

        widget = factory(
            'textarea',
            name='MYTEXTAREA',
            value=None,
            props={
                'data': {
                    'foo': 'bar'
                },
            })
        self.assertEqual(widget(), (
            '<textarea class="textarea" cols="80" data-foo=\'bar\' '
            'id="input-MYTEXTAREA" name="MYTEXTAREA" rows="25"></textarea>'
        ))

        widget.mode = 'display'
        self.assertEqual(widget(), (
            '<div class="display-textarea" data-foo=\'bar\' '
            'id="display-MYTEXTAREA"></div>'
        ))

        # Emptyvalue
        widget = factory(
            'textarea',
            name='MYTEXTAREA',
            props={
                'emptyvalue': 'EMPTYVALUE',
            })
        data = widget.extract(request={'MYTEXTAREA': ''})
        self.assertEqual(data.name, 'MYTEXTAREA')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, 'EMPTYVALUE')
        self.assertEqual(data.errors, [])

        data = widget.extract(request={'MYTEXTAREA': 'NOEMPTY'})
        self.assertEqual(data.name, 'MYTEXTAREA')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, 'NOEMPTY')
        self.assertEqual(data.errors, [])

        # Persist
        widget = factory(
            'textarea',
            name='MYTEXTAREA',
            props={
                'persist_writer': write_mapping_writer
            })
        data = widget.extract(request={'MYTEXTAREA': 'Text'})
        model = dict()
        data.write(model)
        self.assertEqual(model, {'MYTEXTAREA': 'Text'})
