from yafowil.base import factory
from yafowil.persistence import write_mapping_writer
from yafowil.tests import YafowilTestCase
from yafowil.utils import EMPTY_VALUE


class TestProxy(YafowilTestCase):

    def test_proxy_blueprint(self):
        # Used to pass hidden arguments out of form namespace
        widget = factory(
            'proxy',
            name='PROXY',
            value='1')
        self.assertEqual(widget(), (
            '<input id="input-PROXY" name="PROXY" type="hidden" value="1" />'
        ))
        self.assertEqual(widget(request={'PROXY': '2'}), (
            '<input id="input-PROXY" name="PROXY" type="hidden" value="2" />'
        ))

        # Emptyvalue
        widget = factory(
            'proxy',
            name='PROXY',
            value='',
            props={
                'emptyvalue': '1.0'
            })
        data = widget.extract(request={'PROXY': ''})
        self.assertEqual(data.name, 'PROXY')
        self.assertEqual(data.value, '')
        self.assertEqual(data.extracted, '1.0')
        self.assertEqual(data.errors, [])

        # Datatype
        widget = factory(
            'proxy',
            name='PROXY',
            value='',
            props={
                'emptyvalue': '1.0',
                'datatype': float
            })
        data = widget.extract(request={'PROXY': '2.0'})
        self.assertEqual(data.name, 'PROXY')
        self.assertEqual(data.value, '')
        self.assertEqual(data.extracted, 2.0)
        self.assertEqual(data.errors, [])

        data = widget.extract(request={'PROXY': ''})
        self.assertEqual(data.name, 'PROXY')
        self.assertEqual(data.value, '')
        self.assertEqual(data.extracted, 1.0)
        self.assertEqual(data.errors, [])

        # Default emptyvalue extraction
        del widget.attrs['emptyvalue']
        data = widget.extract(request={'PROXY': ''})
        self.assertEqual(data.name, 'PROXY')
        self.assertEqual(data.value, '')
        self.assertEqual(data.extracted, EMPTY_VALUE)
        self.assertEqual(data.errors, [])

        # Persist defaults to false
        widget = factory(
            'proxy',
            name='PROXY',
            props={
                'persist_writer': write_mapping_writer
            })
        data = widget.extract(request={'PROXY': '10'})
        model = dict()
        data.write(model)
        self.assertEqual(model, {})

        # If proxy widgets really need to be persisted, ``persist`` property
        # needs to be set explicitely
        widget.attrs['persist'] = True
        data = widget.extract(request={'PROXY': '10'})
        data.write(model)
        self.assertEqual(model, {'PROXY': '10'})
