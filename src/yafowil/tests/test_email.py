from node.utils import UNSET
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.persistence import write_mapping_writer
from yafowil.tests import YafowilTestCase


class TestEmail(YafowilTestCase):

    def test_email_blueprint(self):
        # Render email input field
        widget = factory(
            'email',
            name='EMAIL')
        self.assertEqual(widget(), (
            '<input class="email" id="input-EMAIL" name="EMAIL" '
            'type="email" value="" />'
        ))

        # Extract not required and empty
        data = widget.extract({'EMAIL': ''})
        self.assertEqual(data.errors, [])

        # Extract invalid email input
        data = widget.extract({'EMAIL': 'foo@bar'})
        self.assertEqual(
            data.errors,
            [ExtractionError('Input not a valid email address.')]
        )

        data = widget.extract({'EMAIL': '@bar.com'})
        self.assertEqual(
            data.errors,
            [ExtractionError('Input not a valid email address.')]
        )

        # Extract valid email input
        data = widget.extract({'EMAIL': 'foo@bar.com'})
        self.assertEqual(data.errors, [])

        # Extract required email input
        widget = factory(
            'email',
            name='EMAIL',
            props={
                'required': 'E-Mail Address is required'
            })
        data = widget.extract({'EMAIL': ''})
        self.assertEqual(
            data.errors,
            [ExtractionError('E-Mail Address is required')]
        )

        data = widget.extract({'EMAIL': 'foo@bar.com'})
        self.assertEqual(data.errors, [])

        # Emptyvalue
        widget = factory(
            'email',
            name='EMAIL',
            props={
                'emptyvalue': 'foo@bar.baz',
            })
        data = widget.extract(request={'EMAIL': ''})
        self.assertEqual(data.name, 'EMAIL')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, 'foo@bar.baz')
        self.assertEqual(data.errors, [])

        data = widget.extract(request={'EMAIL': 'foo@baz.bam'})
        self.assertEqual(data.name, 'EMAIL')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, 'foo@baz.bam')
        self.assertEqual(data.errors, [])

        # Datatype
        widget = factory(
            'email',
            name='EMAIL',
            props={
                'datatype': str
            })
        data = widget.extract(request={'EMAIL': u'foo@example.com'})
        self.assertEqual(data.extracted, u'foo@example.com')
        self.assertTrue(isinstance(data.extracted, str))
        self.assertFalse(isinstance(data.extracted, bytes))

        widget = factory(
            'email',
            name='EMAIL',
            props={
                'datatype': bytes
            })
        data = widget.extract(request={'EMAIL': u'foo@example.com'})
        self.assertEqual(data.extracted, b'foo@example.com')
        self.assertFalse(isinstance(data.extracted, str))
        self.assertTrue(isinstance(data.extracted, bytes))

        # Persist
        widget = factory(
            'email',
            name='EMAIL')
        data = widget.extract({'EMAIL': 'foo@bar.baz'})
        model = dict()
        data.persist_writer = write_mapping_writer
        data.write(model)
        self.assertEqual(model, {'EMAIL': 'foo@bar.baz'})
