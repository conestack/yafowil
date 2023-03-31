from node.utils import UNSET
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.tests import YafowilTestCase
from yafowil.tests import fxml
from yafowil.tests import wrapped_fxml


class TestCommon(YafowilTestCase):

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

    def test_BC_imports(self):
        # button
        from yafowil.common import submit_renderer
        from yafowil.common import button_renderer

        # checkbox
        from yafowil.common import checkbox_extractor
        from yafowil.common import checkbox_edit_renderer
        from yafowil.common import checkbox_display_renderer

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

        # lines
        from yafowil.common import lines_extractor
        from yafowil.common import lines_edit_renderer
        from yafowil.common import lines_display_renderer

        # number
        from yafowil.common import number_extractor

        # password
        from yafowil.common import minlength_extractor
        from yafowil.common import ascii_extractor
        from yafowil.common import password_extractor
        from yafowil.common import password_edit_renderer
        from yafowil.common import password_display_renderer

        # proxy
        from yafowil.common import input_proxy_renderer

        # select
        from yafowil.common import select_extractor
        from yafowil.common import select_exists_marker
        from yafowil.common import select_edit_renderer_props
        from yafowil.common import select_block_edit_renderer
        from yafowil.common import select_cb_edit_renderer
        from yafowil.common import select_edit_renderer
        from yafowil.common import select_display_renderer

        # tag
        from yafowil.common import tag_renderer

        # text
        from yafowil.common import text_edit_renderer

        # textarea
        from yafowil.common import textarea_managed_props
        from yafowil.common import textarea_attributes
        from yafowil.common import textarea_renderer

        # url
        from yafowil.common import url_extractor

        # utils
        from yafowil.utils import convert_value_to_datatype
        from yafowil.utils import convert_values_to_datatype
