# -*- coding: utf-8 -*-
from node.utils import UNSET
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.compat import UNICODE_TYPE
from yafowil.persistence import write_mapping_writer
from yafowil.tests import YafowilTestCase
from yafowil.tests import fxml
from yafowil.tests import wrapped_fxml
from yafowil.utils import EMPTY_VALUE
import uuid


###############################################################################
# Tests
###############################################################################

class TestCommon(YafowilTestCase):

    def test_BC_imports(self):
        # button
        from yafowil.common import submit_renderer
        from yafowil.common import button_renderer

        # datatypes
        from yafowil.common import generic_emptyvalue_extractor
        from yafowil.common import generic_datatype_extractor
        from yafowil.common import DATATYPE_LABELS

        # email
        from yafowil.common import email_extractor

        # field
        from yafowil.common import field_renderer
        from yafowil.common import label_renderer
        from yafowil.common import help_renderer
        from yafowil.common import error_renderer

        # file
        from yafowil.common import file_extractor
        from yafowil.common import mimetype_extractor
        from yafowil.common import input_file_edit_renderer
        from yafowil.common import convert_bytes
        from yafowil.common import input_file_display_renderer
        from yafowil.common import file_options_renderer

        # number
        from yafowil.common import number_extractor

        # select
        from yafowil.common import select_extractor
        from yafowil.common import select_exists_marker
        from yafowil.common import select_edit_renderer_props
        from yafowil.common import select_block_edit_renderer
        from yafowil.common import select_cb_edit_renderer
        from yafowil.common import select_edit_renderer
        from yafowil.common import select_display_renderer

        # url
        from yafowil.common import url_extractor

        # utils
        from yafowil.utils import convert_value_to_datatype
        from yafowil.utils import convert_values_to_datatype

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

    def test_tag_blueprint(self):
        # Custom tag widget
        widget = factory(
            'tag',
            name='MYTAG',
            props={
                'tag': 'h3',
                'text': 'A Headline',
                'class': 'form_heading'
            })
        self.assertEqual(
            widget(),
            '<h3 class="form_heading" id="tag-MYTAG">A Headline</h3>'
        )

        # Skip tag
        widget = factory(
            'tag',
            name='MYTAG',
            props={
                'tag': 'h3',
                'text': 'A Headline',
                'class': 'form_heading'
            },
            mode='skip')
        self.assertEqual(widget(), '')

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

    def test_emptyvalue_extraction(self):
        # Empty values
        widget = factory(
            'text',
            name='MYTEXT',
            props={
                'title': 'Default tests',
                'data': {'foo': 'bar'},
                'default': 'defaultvalue'
            })
        self.assertEqual(widget(), (
            '<input class="text" data-foo=\'bar\' id="input-MYTEXT" '
            'name="MYTEXT" title="Default tests" type="text" '
            'value="defaultvalue" />'
        ))

        data = widget.extract(request={})
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract(request={'MYTEXT': ''})
        self.assertEqual(data.extracted, '')

        widget.attrs['emptyvalue'] = 'emptyvalue'
        data = widget.extract(request={'MYTEXT': ''})
        self.assertEqual(data.extracted, 'emptyvalue')

        widget.attrs['emptyvalue'] = False
        data = widget.extract(request={})
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract(request={'MYTEXT': ''})
        self.assertFalse(data.extracted, False)

        widget.attrs['emptyvalue'] = UNSET
        data = widget.extract(request={})
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract(request={'MYTEXT': ''})
        self.assertEqual(data.extracted, UNSET)

    def test_autofocus_property(self):
        # Widget with autofocus property
        widget = factory(
            'text',
            name='AUTOFOCUS',
            value='',
            props={
                'autofocus': True
            })
        self.assertEqual(widget(), (
            '<input autofocus="autofocus" class="text" id="input-AUTOFOCUS" '
            'name="AUTOFOCUS" type="text" value="" />'
        ))

    def test_placeholder_property(self):
        # Widget with placeholder property
        widget = factory(
            'text',
            name='PLACEHOLDER',
            value='',
            props={
                'placeholder': 'This is a placeholder.'
            })
        self.assertEqual(widget(), (
            '<input class="text" id="input-PLACEHOLDER" name="PLACEHOLDER" '
            'placeholder="This is a placeholder." type="text" value="" />'
        ))

    def test_required_extractor(self):
        # Widget with requires input
        widget = factory(
            'text',
            name='REQUIRED',
            value='',
            props={
                'required': True,
                'error_class': True
            })
        self.assertEqual(widget(), (
            '<input class="required text" id="input-REQUIRED" name="REQUIRED" '
            'required="required" type="text" value="" />'
        ))

        # Extract with empty request, key not in request therefore no error
        data = widget.extract({})
        self.assertEqual(data.name, 'REQUIRED')
        self.assertEqual(data.value, '')
        self.assertEqual(data.extracted, UNSET)
        self.assertEqual(data.errors, [])

        # Extract with empty input sent, required error expected
        data = widget.extract({'REQUIRED': ''})
        self.assertEqual(data.name, 'REQUIRED')
        self.assertEqual(data.value, '')
        self.assertEqual(data.extracted, '')
        self.assertEqual(
            data.errors,
            [ExtractionError('Mandatory field was empty')]
        )

        # With getter value set, empty request, no error expected
        widget = factory(
            'text',
            name='REQUIRED',
            value='Test Text',
            props={
                'required': True,
                'error_class': True
            })
        data = widget.extract({})
        self.assertEqual(data.name, 'REQUIRED')
        self.assertEqual(data.value, 'Test Text')
        self.assertEqual(data.extracted, UNSET)
        self.assertEqual(data.errors, [])
        self.assertEqual(widget(data=data), (
            '<input class="required text" id="input-REQUIRED" name="REQUIRED" '
            'required="required" type="text" value="Test Text" />'
        ))

        # With getter value set, request given, error expected
        data = widget.extract({'REQUIRED': ''})
        self.assertEqual(data.name, 'REQUIRED')
        self.assertEqual(data.value, 'Test Text')
        self.assertEqual(data.extracted, '')
        self.assertEqual(
            data.errors,
            [ExtractionError('Mandatory field was empty')]
        )
        self.assertEqual(widget(data=data), (
            '<input class="error required text" id="input-REQUIRED" '
            'name="REQUIRED" required="required" type="text" value="" />'
        ))

        # Create a custom error message
        widget = factory(
            'text',
            name='REQUIRED',
            value='',
            props={
                'required': 'You fool, fill in a value!'
            })
        data = widget.extract({'REQUIRED': ''})
        self.assertEqual(data.name, 'REQUIRED')
        self.assertEqual(data.value, '')
        self.assertEqual(data.extracted, '')
        self.assertEqual(
            data.errors,
            [ExtractionError('You fool, fill in a value!')]
        )

        # ``required`` property could be a callable as well
        def required_callback(widget, data):
            return u"Foooo"

        widget = factory(
            'text',
            name='REQUIRED',
            value='',
            props={
                'required': required_callback
            })
        data = widget.extract({'REQUIRED': ''})
        self.assertEqual(data.errors, [ExtractionError('Foooo')])

    def test_generic_display_renderer(self):
        # Display mode of text widget uses ``generic_display_renderer``
        widget = factory(
            'text',
            name='DISPLAY',
            value='lorem ipsum',
            mode='display')
        self.assertEqual(
            widget(),
            '<div class="display-text" id="display-DISPLAY">lorem ipsum</div>'
        )

        widget = factory(
            'text',
            name='DISPLAY',
            value=123.4567890,
            mode='display',
            props={
                'template': '%0.3f'
            })
        self.assertEqual(
            widget(),
            '<div class="display-text" id="display-DISPLAY">123.457</div>'
        )

        def mytemplate(widget, data):
            return '<TEMPLATE>%s</TEMPLATE>' % data.value

        widget = factory(
            'text',
            name='DISPLAY',
            value='lorem ipsum',
            mode='display',
            props={
                'template': mytemplate
            })
        self.checkOutput("""
        <div class="display-text" id="display-DISPLAY">
          <TEMPLATE>lorem ipsum</TEMPLATE>
        </div>
        """, fxml(widget()))

        # ``display_proxy`` can be used if mode is 'display' to proxy the value
        # in a hidden field
        widget = factory(
            'text',
            name='DISPLAY',
            value='lorem ipsum',
            mode='display',
            props={
                'display_proxy': True
            })
        self.checkOutput("""
        <div>
          <div class="display-text" id="display-DISPLAY">lorem ipsum</div>
          <input class="text" id="input-DISPLAY" name="DISPLAY" type="hidden"
                 value="lorem ipsum"/>
        </div>
        """, wrapped_fxml(widget()))

        # On widgets with display mode display_proxy property set, the data
        # gets extracted
        data = widget.extract(request={'DISPLAY': 'lorem ipsum'})
        self.assertEqual(data.name, 'DISPLAY')
        self.assertEqual(data.value, 'lorem ipsum')
        self.assertEqual(data.extracted, 'lorem ipsum')

        # Skip mode renders empty string
        widget = factory(
            'text',
            name='SKIP',
            value='lorem ipsum',
            mode='skip')
        self.assertEqual(widget(), '')

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

    def test_lines_blueprint(self):
        # Render empty
        widget = factory(
            'lines',
            name='MYLINES',
            value=None)
        self.assertEqual(widget(), (
            '<textarea class="lines" cols="40" id="input-MYLINES" '
            'name="MYLINES" rows="8"></textarea>'
        ))

        # Render with preset value, expected as list
        widget = factory(
            'lines',
            name='MYLINES',
            value=['a', 'b', 'c'])
        self.checkOutput("""
        <textarea class="lines" cols="40" id="input-MYLINES"
                  name="MYLINES" rows="8">a
        b
        c</textarea>
        """, fxml(widget()))

        # Extract empty
        data = widget.extract({'MYLINES': ''})
        self.assertEqual(data.extracted, [])

        # Extract with data
        data = widget.extract({'MYLINES': 'a\nb'})
        self.assertEqual(data.extracted, ['a', 'b'])

        # Render with extracted data
        self.checkOutput("""
        <textarea class="lines" cols="40" id="input-MYLINES"
                  name="MYLINES" rows="8">a
        b</textarea>
        """, fxml(widget(data=data)))

        # Display mode with preset value
        widget = factory(
            'lines',
            name='MYLINES',
            value=['a', 'b', 'c'],
            mode='display')
        self.checkOutput("""
        <ul class="display-lines" id="display-MYLINES">
          <li>a</li>
          <li>b</li>
          <li>c</li>
        </ul>
        """, fxml(widget()))

        # Display mode with empty preset value
        widget = factory(
            'lines',
            name='MYLINES',
            value=[],
            mode='display')
        self.checkOutput("""
        <ul class="display-lines" id="display-MYLINES"/>
        """, fxml(widget()))

        # Display mode with ``display_proxy``
        widget = factory(
            'lines',
            name='MYLINES',
            value=['a', 'b', 'c'],
            props={
                'display_proxy': True,
            },
            mode='display')
        self.checkOutput("""
        <div>
          <ul class="display-lines" id="display-MYLINES">
            <li>a</li>
            <li>b</li>
            <li>c</li>
          </ul>
          <input class="lines" id="input-MYLINES" name="MYLINES" type="hidden"
                 value="a"/>
          <input class="lines" id="input-MYLINES" name="MYLINES" type="hidden"
                 value="b"/>
          <input class="lines" id="input-MYLINES" name="MYLINES" type="hidden"
                 value="c"/>
        </div>
        """, wrapped_fxml(widget()))

        data = widget.extract({'MYLINES': 'a\nb'})
        self.assertEqual(data.name, 'MYLINES')
        self.assertEqual(data.value, ['a', 'b', 'c'])
        self.assertEqual(data.extracted, ['a', 'b'])
        self.assertEqual(data.errors, [])

        self.checkOutput("""
        <div>
          <ul class="display-lines" id="display-MYLINES">
            <li>a</li>
            <li>b</li>
          </ul>
          <input class="lines" id="input-MYLINES" name="MYLINES" type="hidden"
                 value="a"/>
          <input class="lines" id="input-MYLINES" name="MYLINES" type="hidden"
                 value="b"/>
        </div>
        """, wrapped_fxml(widget(data=data)))

        # Generic HTML5 Data
        widget = factory(
            'lines',
            name='MYLINES',
            value=['a', 'b', 'c'],
            props={
                'data': {'foo': 'bar'}
            })
        self.checkOutput("""
        <textarea class="lines" cols="40" data-foo="bar" id="input-MYLINES"
                  name="MYLINES" rows="8">a
        b
        c</textarea>
        """, fxml(widget()))

        widget = factory(
            'lines',
            name='MYLINES',
            value=['a', 'b', 'c'],
            props={
                'data': {'foo': 'bar'}
            },
            mode='display')
        self.checkOutput("""
        <ul class="display-lines" data-foo="bar" id="display-MYLINES">
          <li>a</li>
          <li>b</li>
          <li>c</li>
        </ul>
        """, fxml(widget()))

        # Emptyvalue
        widget = factory(
            'lines',
            name='MYLINES',
            value=['a', 'b', 'c'],
            props={
                'emptyvalue': ['1']
            })
        data = widget.extract(request={'MYLINES': ''})
        self.assertEqual(data.name, 'MYLINES')
        self.assertEqual(data.value, ['a', 'b', 'c'])
        self.assertEqual(data.extracted, ['1'])
        self.assertEqual(data.errors, [])

        data = widget.extract(request={'MYLINES': '1\n2'})
        self.assertEqual(data.name, 'MYLINES')
        self.assertEqual(data.value, ['a', 'b', 'c'])
        self.assertEqual(data.extracted, ['1', '2'])
        self.assertEqual(data.errors, [])

        # Datatype
        widget = factory(
            'lines',
            name='MYLINES',
            props={
                'emptyvalue': [1],
                'datatype': int
            })
        data = widget.extract(request={'MYLINES': ''})
        self.assertEqual(data.name, 'MYLINES')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, [1])
        self.assertEqual(data.errors, [])

        data = widget.extract(request={'MYLINES': '1\n2'})
        self.assertEqual(data.name, 'MYLINES')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, [1, 2])
        self.assertEqual(data.errors, [])

        widget.attrs['emptyvalue'] = ['1']
        data = widget.extract(request={'MYLINES': ''})
        self.assertEqual(data.name, 'MYLINES')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, [1])
        self.assertEqual(data.errors, [])

        # Persist
        widget = factory(
            'lines',
            name='MYLINES',
            props={
                'persist_writer': write_mapping_writer
            })
        data = widget.extract(request={'MYLINES': '1\n2'})
        model = dict()
        data.write(model)
        self.assertEqual(model, {'MYLINES': ['1', '2']})

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

    def test_password_blueprint(self):
        # Password widget has some additional properties, ``strength``,
        # ``minlength`` and ``ascii``.

        # Use in add forms, no password set yet
        widget = factory(
            'password',
            name='PWD')
        self.assertEqual(widget(), (
            '<input class="password" id="input-PWD" name="PWD" '
            'type="password" value="" />'
        ))

        data = widget.extract({})
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'PWD': 'xx'})
        self.assertEqual(data.extracted, 'xx')

        widget.mode = 'display'
        self.assertEqual(widget(), '')

        # Use in edit forms. note that password is never shown up in markup,
        # but a placeholder is used when a password is already set. Thus, if a
        # extracted password value is UNSET, this means that password was not
        # changed
        widget = factory(
            'password',
            name='PASSWORD',
            value='secret')
        self.assertEqual(widget(), (
            '<input class="password" id="input-PASSWORD" name="PASSWORD" '
            'type="password" value="_NOCHANGE_" />'
        ))

        data = widget.extract({'PASSWORD': '_NOCHANGE_'})
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'PASSWORD': 'foo'})
        self.assertEqual(data.extracted, 'foo')

        self.assertEqual(widget(data=data), (
            '<input class="password" id="input-PASSWORD" name="PASSWORD" '
            'type="password" value="foo" />'
        ))

        widget.mode = 'display'
        self.assertEqual(widget(), '********')

        # Password validation
        widget = factory(
            'password',
            name='PWD',
            props={
                'strength': 5,  # max 4, does not matter, max is used
            })
        data = widget.extract({'PWD': ''})
        self.assertEqual(data.errors, [ExtractionError('Password too weak')])

        data = widget.extract({'PWD': 'A0*'})
        self.assertEqual(data.errors, [ExtractionError('Password too weak')])

        data = widget.extract({'PWD': 'a0*'})
        self.assertEqual(data.errors, [ExtractionError('Password too weak')])

        data = widget.extract({'PWD': 'aA*'})
        self.assertEqual(data.errors, [ExtractionError('Password too weak')])

        data = widget.extract({'PWD': 'aA0'})
        self.assertEqual(data.errors, [ExtractionError('Password too weak')])

        data = widget.extract({'PWD': 'aA0*'})
        self.assertEqual(data.errors, [])

        # Minlength validation
        widget = factory(
            'password',
            name='PWD',
            props={
                'minlength': 3,
            })
        data = widget.extract({'PWD': 'xx'})
        self.assertEqual(
            data.errors,
            [ExtractionError('Input must have at least 3 characters.')]
        )

        data = widget.extract({'PWD': 'xxx'})
        self.assertEqual(data.errors, [])

        # Ascii validation
        widget = factory(
            'password',
            name='PWD',
            props={
                'ascii': True,
            })
        data = widget.extract({'PWD': u'äää'})
        self.assertEqual(
            data.errors,
            [ExtractionError('Input contains illegal characters.')]
        )

        data = widget.extract({'PWD': u'xx'})
        self.assertEqual(data.errors, [])

        # Combine all validations
        widget = factory(
            'password',
            name='PWD',
            props={
                'required': 'No Password given',
                'minlength': 6,
                'ascii': True,
                'strength': 4,
            })
        data = widget.extract({'PWD': u''})
        self.assertEqual(data.errors, [ExtractionError('No Password given')])

        data = widget.extract({'PWD': u'xxxxx'})
        self.assertEqual(
            data.errors,
            [ExtractionError('Input must have at least 6 characters.')]
        )

        data = widget.extract({'PWD': u'xxxxxä'})
        self.assertEqual(
            data.errors,
            [ExtractionError('Input contains illegal characters.')]
        )

        data = widget.extract({'PWD': u'xxxxxx'})
        self.assertEqual(data.errors, [ExtractionError('Password too weak')])

        data = widget.extract({'PWD': u'xX1*00'})
        self.assertEqual(data.errors, [])

        # Emptyvalue
        widget = factory(
            'password',
            name='PWD',
            props={
                'emptyvalue': 'DEFAULTPWD',  # <- not a good idea, but works
            })
        data = widget.extract(request={'PWD': ''})
        self.assertEqual(data.name, 'PWD')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, 'DEFAULTPWD')
        self.assertEqual(data.errors, [])

        data = widget.extract(request={'PWD': 'NOEMPTY'})
        self.assertEqual(data.name, 'PWD')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, 'NOEMPTY')
        self.assertEqual(data.errors, [])

        # Persist
        widget = factory(
            'password',
            name='PWD',
            props={
                'persist_writer': write_mapping_writer
            })
        data = widget.extract(request={'PWD': '1234'})
        model = dict()
        data.write(model)
        self.assertEqual(model, {'PWD': '1234'})

    def test_bytes_datatype_rendering_and_extraction(self):
        widget = factory(
            'text',
            value=b'\r\n\x01\x9a\x03\xff',
            name='BYTES',
            props={
                'datatype': bytes
            })
        self.assertEqual(widget(), (
            u'<input class="text" id="input-BYTES" name="BYTES" '
            u'type="text" value="\\r\\n\\x01\\x9a\\x03\\xff" />'
        ))

        widget = factory(
            'text',
            name='BYTES',
            props={
                'datatype': bytes
            })
        data = widget.extract({'BYTES': u'\\r\\n\\x01\\x9a\\x03\\xff'})
        self.assertEqual(data.extracted, b'\r\n\x01\x9a\x03\xff')
