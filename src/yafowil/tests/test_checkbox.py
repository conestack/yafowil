from node.utils import UNSET
from yafowil.base import factory
from yafowil.persistence import write_mapping_writer
from yafowil.tests import YafowilTestCase
from yafowil.tests import wrapped_fxml


class TestCheckbox(YafowilTestCase):

    def test_checkbox_blueprint(self):
        # A boolean checkbox widget (default)
        widget = factory(
            'checkbox',
            name='MYCHECKBOX')
        self.checkOutput("""
        <div>
          <input class="checkbox" id="input-MYCHECKBOX" name="MYCHECKBOX"
                 type="checkbox" value=""/>
          <input id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists"
                 type="hidden" value="checkboxexists"/>
        </div>
        """, wrapped_fxml(widget()))

        widget.mode = 'display'
        self.assertEqual(
            widget(),
            '<div class="display-checkbox" id="display-MYCHECKBOX">No</div>'
        )

        widget = factory(
            'checkbox',
            name='MYCHECKBOX',
            value='True')
        self.checkOutput("""
        <div>
          <input checked="checked" class="checkbox" id="input-MYCHECKBOX"
                 name="MYCHECKBOX" type="checkbox" value=""/>
          <input id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists"
                 type="hidden" value="checkboxexists"/>
        </div>
        """, wrapped_fxml(widget()))

        widget.mode = 'display'
        self.assertEqual(
            widget(),
            '<div class="display-checkbox" id="display-MYCHECKBOX">Yes</div>'
        )

        # A checkbox with custom CSS related empty label
        widget = factory(
            'checkbox',
            name='MYCHECKBOX',
            props={
                'with_label': True
            })
        self.checkOutput("""
        <input class="checkbox" id="input-MYCHECKBOX" name="MYCHECKBOX"
        type="checkbox" value="" /><label class="checkbox_label"
        for="input-MYCHECKBOX">&nbsp;</label><input
        id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists" type="hidden"
        value="checkboxexists" />
        """, widget())

        # A checkbox widget with a value or an empty string
        widget = factory(
            'checkbox',
            name='MYCHECKBOX',
            value='',
            props={
                'format': 'string'
            })
        self.checkOutput("""
        <div>
          <input class="checkbox" id="input-MYCHECKBOX" name="MYCHECKBOX"
                 type="checkbox" value=""/>
          <input id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists"
                 type="hidden" value="checkboxexists"/>
        </div>
        """, wrapped_fxml(widget()))

        widget.mode = 'display'
        self.assertEqual(
            widget(),
            '<div class="display-checkbox" id="display-MYCHECKBOX">No</div>'
        )

        widget = factory(
            'checkbox',
            name='MYCHECKBOX',
            value='Test Checkbox',
            props={
                'format': 'string'
            })
        self.checkOutput("""
        <div>
          <input checked="checked" class="checkbox" id="input-MYCHECKBOX"
                 name="MYCHECKBOX" type="checkbox" value="Test Checkbox"/>
          <input id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists"
                 type="hidden" value="checkboxexists"/>
        </div>
        """, wrapped_fxml(widget()))

        widget.mode = 'display'
        self.assertEqual(widget(), (
            '<div class="display-checkbox" id="display-MYCHECKBOX">'
            'Test Checkbox</div>'
        ))

        # Checkbox with manually set 'checked' attribute
        widget = factory(
            'checkbox',
            name='MYCHECKBOX',
            value='',
            props={
                'format': 'string',
                'checked': True,
            })
        self.checkOutput("""
        <div>
          <input checked="checked" class="checkbox" id="input-MYCHECKBOX"
                 name="MYCHECKBOX" type="checkbox" value=""/>
          <input id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists"
                 type="hidden" value="checkboxexists"/>
        </div>
        """, wrapped_fxml(widget()))

        widget = factory(
            'checkbox',
            name='MYCHECKBOX',
            value='Test Checkbox',
            props={
                'format': 'string',
                'checked': False,
            })
        self.checkOutput("""
        <div>
          <input class="checkbox" id="input-MYCHECKBOX" name="MYCHECKBOX"
                 type="checkbox" value="Test Checkbox"/>
          <input id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists"
                 type="hidden" value="checkboxexists"/>
        </div>
        """, wrapped_fxml(widget()))

        # Checkbox extraction
        request = {
            'MYCHECKBOX': '1',
            'MYCHECKBOX-exists': 'checkboxexists'
        }
        data = widget.extract(request)
        self.checkOutput("""
        <RuntimeData MYCHECKBOX, value='Test Checkbox', extracted='1' at ...>
        """, data.treerepr())

        request = {
            'MYCHECKBOX': '',
            'MYCHECKBOX-exists': 'checkboxexists'
        }
        data = widget.extract(request)
        self.checkOutput("""
        <RuntimeData MYCHECKBOX, value='Test Checkbox', extracted='' at ...>
        """, data.treerepr())

        request = {
            'MYCHECKBOX': 1,
        }
        data = widget.extract(request)
        self.checkOutput("""
        <RuntimeData MYCHECKBOX, value='Test Checkbox', extracted=<UNSET> at ...>
        """, data.treerepr())  # noqa

        model = dict()
        data.persist_writer = write_mapping_writer
        data.write(model)
        self.assertEqual(model, {'MYCHECKBOX': UNSET})

        # bool extraction
        widget = factory(
            'checkbox',
            name='MYCHECKBOX',
            value='Test Checkbox',
            props={
                'format': 'bool'
            })
        request = {
            'MYCHECKBOX': '',
            'MYCHECKBOX-exists': 'checkboxexists'
        }
        data = widget.extract(request)
        self.checkOutput("""
        <RuntimeData MYCHECKBOX, value='Test Checkbox', extracted=True at ...>
        """, data.treerepr())

        request = {
            'MYCHECKBOX-exists': 'checkboxexists'
        }
        data = widget.extract(request)
        self.checkOutput("""
        <RuntimeData MYCHECKBOX, value='Test Checkbox', extracted=False at ...>
        """, data.treerepr())

        model = dict()
        data.persist_writer = write_mapping_writer
        data.write(model)
        self.assertEqual(model, {'MYCHECKBOX': False})

        # invalid format
        widget = factory(
            'checkbox',
            name='MYCHECKBOX',
            props={
                'format': 'invalid'
            })
        request = {
            'MYCHECKBOX': '',
            'MYCHECKBOX-exists': 'checkboxexists'
        }
        with self.assertRaises(ValueError) as arc:
            widget.extract(request)
        msg = "Checkbox widget has invalid format 'invalid' set"
        self.assertEqual(str(arc.exception), msg)

        # Render in display mode
        widget = factory(
            'checkbox',
            name='MYCHECKBOX',
            value=False,
            mode='display',
            props={
                'format': 'bool'
            })
        self.checkOutput("""
        <div>
          <div class="display-checkbox" id="display-MYCHECKBOX">No</div>
        </div>
        """, wrapped_fxml(widget()))

        widget = factory(
            'checkbox',
            name='MYCHECKBOX',
            value=True,
            mode='display',
            props={
                'format': 'bool'
            })
        self.checkOutput("""
        <div>
          <div class="display-checkbox" id="display-MYCHECKBOX">Yes</div>
        </div>
        """, wrapped_fxml(widget()))

        # Display mode and display proxy bool format
        widget = factory(
            'checkbox',
            name='MYCHECKBOX',
            value=True,
            props={
                'format': 'bool',
                'display_proxy': True
            },
            mode='display')
        self.checkOutput("""
        <div class="display-checkbox" id="display-MYCHECKBOX">Yes<input
        class="checkbox" id="input-MYCHECKBOX" name="MYCHECKBOX" type="hidden"
        value="" /><input id="checkboxexists-MYCHECKBOX"
        name="MYCHECKBOX-exists" type="hidden" value="checkboxexists" /></div>
        """, widget())

        data = widget.extract(request={'MYCHECKBOX-exists': 'checkboxexists'})
        self.assertEqual(data.name, 'MYCHECKBOX')
        self.assertEqual(data.value, True)
        self.assertEqual(data.extracted, False)

        self.checkOutput("""
        <div class="display-checkbox" id="display-MYCHECKBOX">No<input
        id="checkboxexists-MYCHECKBOX" name="MYCHECKBOX-exists" type="hidden"
        value="checkboxexists" /></div>
        """, widget(data=data))

        data = widget.extract(request={
            'MYCHECKBOX-exists': 'checkboxexists',
            'MYCHECKBOX': ''
        })
        self.assertEqual(data.name, 'MYCHECKBOX')
        self.assertEqual(data.value, True)
        self.assertEqual(data.extracted, True)

        self.checkOutput("""
        <div class="display-checkbox" id="display-MYCHECKBOX">Yes<input
        class="checkbox" id="input-MYCHECKBOX" name="MYCHECKBOX"
        type="hidden" value="" /><input id="checkboxexists-MYCHECKBOX"
        name="MYCHECKBOX-exists" type="hidden" value="checkboxexists" /></div>
        """, widget(data=data))

        # Display mode and display proxy string format
        widget = factory(
            'checkbox',
            name='MYCHECKBOX',
            value='yes',
            props={
                'format': 'string',
                'display_proxy': True
            },
            mode='display')
        self.checkOutput("""
        <div class="display-checkbox" id="display-MYCHECKBOX">yes<input
        class="checkbox" id="input-MYCHECKBOX" name="MYCHECKBOX"
        type="hidden" value="yes" /><input id="checkboxexists-MYCHECKBOX"
        name="MYCHECKBOX-exists" type="hidden" value="checkboxexists" /></div>
        """, widget())

        data = widget.extract(request={'MYCHECKBOX-exists': 'checkboxexists'})
        self.assertEqual(data.name, 'MYCHECKBOX')
        self.assertEqual(data.value, 'yes')
        self.assertEqual(data.extracted, '')

        self.checkOutput("""
        <div class="display-checkbox" id="display-MYCHECKBOX">No<input
        class="checkbox" id="input-MYCHECKBOX" name="MYCHECKBOX" type="hidden"
        value="" /><input id="checkboxexists-MYCHECKBOX"
        name="MYCHECKBOX-exists" type="hidden" value="checkboxexists" /></div>
        """, widget(data=data))

        data = widget.extract(request={
            'MYCHECKBOX-exists': 'checkboxexists',
            'MYCHECKBOX': ''
        })
        self.assertEqual(data.name, 'MYCHECKBOX')
        self.assertEqual(data.value, 'yes')
        self.assertEqual(data.extracted, '')

        self.checkOutput("""
        <div class="display-checkbox" id="display-MYCHECKBOX">No<input
        class="checkbox" id="input-MYCHECKBOX" name="MYCHECKBOX" type="hidden"
        value="" /><input id="checkboxexists-MYCHECKBOX"
        name="MYCHECKBOX-exists" type="hidden" value="checkboxexists" /></div>
        """, widget(data=data))

        data = widget.extract(request={'MYCHECKBOX-exists': 'checkboxexists',
                                       'MYCHECKBOX': 'foo'})
        self.assertEqual(data.name, 'MYCHECKBOX')
        self.assertEqual(data.value, 'yes')
        self.assertEqual(data.extracted, 'foo')

        self.checkOutput("""
        <div class="display-checkbox" id="display-MYCHECKBOX">foo<input
        class="checkbox" id="input-MYCHECKBOX" name="MYCHECKBOX"
        type="hidden" value="foo" /><input id="checkboxexists-MYCHECKBOX"
        name="MYCHECKBOX-exists" type="hidden" value="checkboxexists" /></div>
        """, widget(data=data))

        # Generic HTML5 Data
        widget = factory(
            'checkbox',
            name='MYCHECKBOX',
            value='Test Checkbox',
            props={
                'data': {'foo': 'bar'}
            })
        self.checkOutput("""
        <input checked="checked" class="checkbox" data-foo=\'bar\'
        id="input-MYCHECKBOX" name="MYCHECKBOX" type="checkbox"
        value="" /><input id="checkboxexists-MYCHECKBOX"
        name="MYCHECKBOX-exists" type="hidden" value="checkboxexists" />
        """, widget())
