from node.utils import UNSET
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.persistence import write_mapping_writer
from yafowil.tests import YafowilTestCase


class TestNumber(YafowilTestCase):

    def test_number_blueprint(self):
        # Display renderer
        widget = factory(
            'number',
            name='NUMBER',
            value=3,
            mode='display')
        self.assertEqual(widget(), (
            '<div class="display-number" id="display-NUMBER">3</div>'
        ))

        # Render number input
        widget = factory(
            'number',
            name='NUMBER',
            value=lambda w, d: 3)
        self.assertEqual(widget(), (
            '<input class="number" id="input-NUMBER" name="NUMBER" '
            'type="number" value="3" />'
        ))

        # Extract unset
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        self.assertEqual(data.name, 'NUMBER')
        self.assertEqual(data.value, 3)
        self.assertEqual(data.extracted, UNSET)
        self.assertEqual(data.errors, [])

        # Extract not required and empty
        data = widget.extract({'NUMBER': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        # Extract invalid floating point input
        data = widget.extract({'NUMBER': 'abc'})
        self.assertEqual(
            data.errors,
            [ExtractionError('Input is not a valid floating point number.')]
        )

        # Extract valid floating point input
        data = widget.extract({'NUMBER': '10'})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, 10.)

        data = widget.extract({'NUMBER': '10.0'})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, 10.)

        data = widget.extract({'NUMBER': '10,0'})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, 10.)

        # Instanciate with invalid datatype
        widget = factory(
            'number',
            name='NUMBER',
            props={
                'datatype': 'invalid'
            })
        with self.assertRaises(ValueError) as arc:
            widget.extract({'NUMBER': '10.0'})
        self.assertEqual(str(arc.exception), 'Datatype not allowed: "invalid"')

        # Extract invalid integer input
        widget = factory(
            'number',
            name='NUMBER',
            props={
                'datatype': int
            })
        data = widget.extract({'NUMBER': '10.0'})
        self.assertEqual(
            data.errors,
            [ExtractionError('Input is not a valid integer.')]
        )

        # Extract with min value set
        widget = factory(
            'number',
            name='NUMBER',
            props={
                'min': 10
            })
        data = widget.extract({'NUMBER': '9'})
        self.assertEqual(
            data.errors,
            [ExtractionError('Value has to be at minimum 10.')]
        )

        data = widget.extract({'NUMBER': '10'})
        self.assertEqual(data.errors, [])

        data = widget.extract({'NUMBER': '11'})
        self.assertEqual(data.errors, [])

        # Extract min value 0
        widget = factory(
            'number',
            name='NUMBER',
            props={
                'min': 0
            })
        data = widget.extract({'NUMBER': '-1'})
        self.assertEqual(
            data.errors,
            [ExtractionError('Value has to be at minimum 0.')]
        )

        data = widget.extract({'NUMBER': '0'})
        self.assertEqual(data.errors, [])

        # Extract with max value set
        widget = factory(
            'number',
            name='NUMBER',
            props={
                'max': lambda w, d: 10
            })
        data = widget.extract({'NUMBER': '9'})
        self.assertEqual(data.errors, [])

        data = widget.extract({'NUMBER': '10'})
        self.assertEqual(data.errors, [])

        data = widget.extract({'NUMBER': '11'})
        self.assertEqual(
            data.errors,
            [ExtractionError('Value has to be at maximum 10.')]
        )

        # Extract max value 0
        widget = factory(
            'number',
            name='NUMBER',
            props={'max': 0}
        )
        data = widget.extract({'NUMBER': '1'})
        self.assertEqual(
            data.errors,
            [ExtractionError('Value has to be at maximum 0.')]
        )

        data = widget.extract({'NUMBER': '0'})
        self.assertEqual(data.errors, [])

        # Extract with step set
        widget = factory(
            'number',
            name='NUMBER',
            props={
                'step': 2
            })
        data = widget.extract({'NUMBER': '9'})
        self.assertEqual(
            data.errors,
            [ExtractionError('Value 9.0 has to be in stepping of 2')]
        )

        data = widget.extract({'NUMBER': '6'})
        self.assertEqual(data.errors, [])

        # Extract with step and min value set
        widget = factory(
            'number',
            name='NUMBER',
            props={
                'step': 2,
                'min': 3
            })
        data = widget.extract({'NUMBER': '7'})
        self.assertEqual(data.errors, [])

        data = widget.extract({'NUMBER': '6'})
        self.assertEqual(
            data.errors,
            [ExtractionError(
                'Value 6.0 has to be in stepping of 2 based on a floor '
                'value of 3'
            )]
        )

        # Extract 0 value
        widget = factory(
            'number',
            name='NUMBER')
        data = widget.extract({'NUMBER': '0'})
        self.assertEqual(data.extracted, 0.0)

        widget = factory(
            'number',
            name='NUMBER',
            props={
                'datatype': int
            })
        data = widget.extract({'NUMBER': '0'})
        self.assertEqual(data.extracted, 0)

        # Persist
        widget = factory(
            'number',
            name='NUMBER',
            props={
                'datatype': int
            })
        data = widget.extract({'NUMBER': '0'})
        model = dict()
        data.persist_writer = write_mapping_writer
        data.write(model)
        self.assertEqual(model, {'NUMBER': 0})
