from node.utils import UNSET
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.persistence import write_mapping_writer
from yafowil.tests import YafowilTestCase


class TestUrl(YafowilTestCase):

    def test_url_blueprint(self):
        # Render URL input field
        widget = factory(
            'url',
            name='URL')
        self.assertEqual(widget(), (
            '<input class="url" id="input-URL" name="URL" '
            'type="url" value="" />'
        ))

        # Extract not required and empty
        data = widget.extract({'URL': ''})
        self.assertEqual(data.errors, [])

        # Extract invalid URL input
        data = widget.extract({'URL': 'htt:/bla'})
        self.assertEqual(
            data.errors,
            [ExtractionError('Input not a valid web address.')]
        )

        data = widget.extract({'URL': 'invalid'})
        self.assertEqual(
            data.errors,
            [ExtractionError('Input not a valid web address.')]
        )

        # Extract value URL input
        data = widget.extract({
            'URL': 'http://www.foo.bar.com:8080/bla#fasel?blubber=bla&bla=fasel'  # noqa
        })
        self.assertEqual(data.errors, [])

        # Emptyvalue
        widget = factory(
            'url',
            name='URL',
            props={
                'emptyvalue': 'http://www.example.com',
            })
        data = widget.extract(request={'URL': ''})
        self.assertEqual(data.name, 'URL')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, 'http://www.example.com')
        self.assertEqual(data.errors, [])

        data = widget.extract(request={'URL': 'http://www.example.org'})
        self.assertEqual(data.name, 'URL')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, 'http://www.example.org')
        self.assertEqual(data.errors, [])

        # Persist
        widget = factory(
            'url',
            name='URL')
        data = widget.extract({'URL': 'http://www.example.org'})
        model = dict()
        data.persist_writer = write_mapping_writer
        data.write(model)
        self.assertEqual(model, {'URL': 'http://www.example.org'})
