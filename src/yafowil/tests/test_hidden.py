from node.utils import UNSET
from yafowil.base import factory
from yafowil.persistence import write_mapping_writer
from yafowil.tests import YafowilTestCase
from yafowil.utils import EMPTY_VALUE


class TestHidden(YafowilTestCase):

    def test_hidden_blueprint(self):
        # Hidden input blueprint
        widget = factory(
            'hidden',
            name='MYHIDDEN',
            value='Test Hidden')
        self.assertEqual(widget(), (
            '<input class="hidden" id="input-MYHIDDEN" name="MYHIDDEN" '
            'type="hidden" value="Test Hidden" />'
        ))

        # Display mode of hidden widget renders empty string
        widget = factory(
            'hidden',
            name='MYHIDDEN',
            value='Test Hidden',
            mode='display')
        self.assertEqual(widget(), '')

        # As well does skip mode
        widget = factory(
            'hidden',
            name='MYHIDDEN',
            value='Test Hidden',
            mode='skip')
        self.assertEqual(widget(), '')

        # Generic HTML5 Data
        widget = factory(
            'hidden',
            name='MYHIDDEN',
            value='Test Hidden',
            props={
                'data': {
                    'foo': 'bar'
                }
            })
        self.assertEqual(widget(), (
            '<input class="hidden" data-foo=\'bar\' id="input-MYHIDDEN" '
            'name="MYHIDDEN" type="hidden" value="Test Hidden" />'
        ))

        # Emptyvalue
        widget = factory(
            'hidden',
            name='MYHIDDEN',
            props={
                'emptyvalue': 'EMPTYVALUE'
            })
        data = widget.extract(request={'MYHIDDEN': ''})
        self.assertEqual(data.name, 'MYHIDDEN')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, 'EMPTYVALUE')

        # Datatype
        widget = factory(
            'hidden',
            name='MYHIDDEN',
            props={
                'emptyvalue': 0,
                'datatype': int
            })
        data = widget.extract(request={'MYHIDDEN': ''})
        self.assertEqual(data.name, 'MYHIDDEN')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, 0)

        # Default emptyvalue extraction
        del widget.attrs['emptyvalue']
        data = widget.extract(request={'MYHIDDEN': ''})
        self.assertEqual(data.name, 'MYHIDDEN')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, EMPTY_VALUE)

        # Persist property
        widget = factory(
            'hidden',
            name='MYHIDDEN',
            props={
                'emptyvalue': 0,
                'datatype': int,
                'persist_writer': write_mapping_writer,
            })
        data = widget.extract(request={'MYHIDDEN': '10'})
        model = dict()
        data.write(model)
        self.assertEqual(model, {'MYHIDDEN': 10})

        data.persist_target = 'myhidden'
        model = dict()
        data.write(model)
        self.assertEqual(model, {'myhidden': 10})
