from node.utils import UNSET
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.tests import YafowilTestCase
from yafowil.tests import fxml
from yafowil.tests import wrapped_fxml


class TestField(YafowilTestCase):

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

    def test_help_blueprint(self):
        # Render some additional help text
        widget = factory(
            'field:help:text',
            name='HELPEXAMPLE',
            props={
                'label': 'Help',
                'help': 'Shout out loud here'
            })
        self.checkOutput("""
        <div class="field" id="field-HELPEXAMPLE">
          <div class="help">Shout out loud here</div>
          <input class="text" id="input-HELPEXAMPLE" name="HELPEXAMPLE"
                 type="text" value=""/>
        </div>
        """, fxml(widget()))

        # Render empty (WHAT'S THIS GOOD FOR?)
        widget = factory(
            'field:help:text',
            name='HELPEXAMPLE',
            props={
                'label': 'Help',
                'help': False,
                'render_empty': False
            })
        self.checkOutput("""
        <div class="field" id="field-HELPEXAMPLE">
          <input class="text" id="input-HELPEXAMPLE" name="HELPEXAMPLE"
                 type="text" value=""/>
        </div>
        """, fxml(widget()))

    def test_error_blueprint(self):
        # Chained password inside error inside field
        widget = factory(
            'field:error:password',
            name='PASSWORD',
            props={
                'label': 'Password',
                'required': 'No password given!'
            })
        data = widget.extract({'PASSWORD': ''})
        self.checkOutput("""
        <div class="field" id="field-PASSWORD">
          <div class="error">
            <div class="errormessage">No password given!</div>
            <input class="password required" id="input-PASSWORD" name="PASSWORD"
                   required="required" type="password" value=""/>
          </div>
        </div>
        """, fxml(widget(data=data)))  # noqa

        data = widget.extract({'PASSWORD': 'secret'})
        self.checkOutput("""
        <div class="field" id="field-PASSWORD">
          <input class="password required" id="input-PASSWORD" name="PASSWORD"
                 required="required" type="password" value="secret"/>
        </div>
        """, fxml(widget(data=data)))

        widget = factory(
            'error:text',
            name='MYDISPLAY',
            value='somevalue',
            mode='display')
        self.assertEqual(widget(), (
            '<div class="display-text" id="display-MYDISPLAY">somevalue</div>'
        ))

        # Error wrapping in div element can be suppressed
        widget = factory(
            'field:error:password',
            name='PASSWORD',
            props={
                'label': 'Password',
                'required': 'No password given!',
                'message_tag': None
            })
        data = widget.extract({'PASSWORD': ''})
        self.checkOutput("""
        <div class="field" id="field-PASSWORD">
          <div class="error">No password given!<input class="password required"
               id="input-PASSWORD" name="PASSWORD" required="required"
               type="password" value=""/></div>
        </div>
        """, fxml(widget(data=data)))
