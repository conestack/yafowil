# -*- coding: utf-8 -*-
from node.utils import UNSET
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.tests import YafowilTestCase
from yafowil.tests import fxml
from yafowil.tests import wrapped_fxml


class TestStructure(YafowilTestCase):
    # Structure Blueprints

    def test_field_blueprint(self):
        # Chained file inside field with label
        widget = factory(
            'field:label:file',
            name='MYFILE',
            props={
                'label': 'MY FILE'
            })
        self.checkOutput("""
        <div class="field" id="field-MYFILE">
          <label for="input-MYFILE">MY FILE</label>
          <input id="input-MYFILE" name="MYFILE" type="file"/>
        </div>
        """, fxml(widget()))

        # Render error class directly on field
        widget = factory(
            'field:text',
            name='MYFIELD',
            props={
                'required': True,
                'witherror': 'fielderrorclass'
            })
        data = widget.extract({'MYFIELD': ''})
        self.assertEqual(data.name, 'MYFIELD')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, '')
        self.assertEqual(
            data.errors,
            [ExtractionError('Mandatory field was empty')]
        )

        self.checkOutput("""
        <div class="field fielderrorclass" id="field-MYFIELD">
          <input class="required text" id="input-MYFIELD" name="MYFIELD"
                 required="required" type="text" value=""/>
        </div>
        """, fxml(widget(data)))

    def test_label_blueprint(self):
        # Default
        widget = factory(
            'label:file',
            name='MYFILE',
            props={
                'label': 'MY FILE'
            })
        self.checkOutput("""
        <div>
          <label for="input-MYFILE">MY FILE</label>
          <input id="input-MYFILE" name="MYFILE" type="file"/>
        </div>
        """, wrapped_fxml(widget()))

        # Label after widget
        widget = factory(
            'label:file',
            name='MYFILE',
            props={
                'label': 'MY FILE',
                'label.position': 'after'
            })
        self.checkOutput("""
        <div>
          <input id="input-MYFILE" name="MYFILE" type="file"/>
          <label for="input-MYFILE">MY FILE</label>
        </div>
        """, wrapped_fxml(widget()))

        # Same with inner label
        widget = factory(
            'label:file',
            name='MYFILE',
            props={
                'label': 'MY FILE',
                'label.position': 'inner'
            })
        self.checkOutput("""
        <div>
          <label for="input-MYFILE">MY FILE<input id="input-MYFILE"
                 name="MYFILE" type="file"/></label>
        </div>
        """, wrapped_fxml(widget()))

        # Invalid position
        widget = factory(
            'label:file',
            name='MYFILE',
            props={
                'label': 'MY FILE',
                'label.position': 'inexistent'
            })
        with self.assertRaises(ValueError) as arc:
            widget()
        self.assertEqual(
            str(arc.exception),
            'Invalid value for position "inexistent"'
        )

        # Render with title attribute
        widget = factory(
            'label',
            name='MYFILE',
            props={
                'title': 'My awesome title',
            })
        self.assertEqual(widget(), (
            '<label for="input-MYFILE" title="My awesome title">MYFILE</label>'
        ))

        # Label Text can be a callable
        widget = factory(
            'label',
            name='MYFILE',
            props={
                'label': lambda x, y: 'Fooo',
            })
        self.assertEqual(widget(), (
            '<label for="input-MYFILE">Fooo</label>'
        ))

        # Position can be callable
        widget = factory(
            'label',
            name='MYFILE',
            props={
                'label': 'Fooo',
                'position': lambda x, y: 'inner',
            })
        self.assertEqual(widget(), '<label for="input-MYFILE">Fooo</label>')
