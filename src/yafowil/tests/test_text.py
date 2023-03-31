from node.utils import UNSET
from yafowil.base import factory
from yafowil.persistence import write_mapping_writer
from yafowil.tests import YafowilTestCase


class TestText(YafowilTestCase):

    def test_text_blueprint(self):
        # Regular text input
        widget = factory(
            'text',
            name='MYTEXT',
            value='Test Text "Some Text"')
        self.assertEqual(widget(), (
            '<input class="text" id="input-MYTEXT" name="MYTEXT" type="text" '
            'value="Test Text &quot;Some Text&quot;" />'
        ))

        widget.mode = 'display'
        self.assertEqual(widget(), (
            '<div class="display-text" id="display-MYTEXT">'
            'Test Text "Some Text"</div>'
        ))

        # Render with title attribute
        widget = factory(
            'text',
            name='MYTEXT',
            value='ja ha!',
            props={
                'title': 'My awesome title'
            })
        self.assertEqual(widget(), (
            '<input class="text" id="input-MYTEXT" name="MYTEXT" '
            'title="My awesome title" type="text" value="ja ha!" />'
        ))

        # Generic HTML5 Data
        widget = factory(
            'text',
            name='MYTEXT',
            value='ja ha!',
            props={
                'title': 'My awesome title',
                'data': {'foo': 'bar'}
            })
        self.assertEqual(widget(), (
            '<input class="text" data-foo=\'bar\' id="input-MYTEXT" '
            'name="MYTEXT" title="My awesome title" type="text" '
            'value="ja ha!" />'
        ))

        # Extract and persist
        widget = factory(
            'text',
            name='MYTEXT',
            props={
                'persist_writer': write_mapping_writer
            })
        data = widget.extract(request={'MYTEXT': '10'})
        self.assertEqual(data.name, 'MYTEXT')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, '10')

        model = dict()
        data.write(model)
        self.assertEqual(model, {'MYTEXT': '10'})
