# -*- coding: utf-8 -*-
from node.utils import UNSET
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.common import convert_bytes
from yafowil.compat import BYTES_TYPE
from yafowil.compat import IS_PY2
from yafowil.compat import LONG_TYPE
from yafowil.compat import UNICODE_TYPE
from yafowil.persistence import write_mapping_writer
from yafowil.tests import fxml
from yafowil.tests import YafowilTestCase
from yafowil.utils import EMPTY_VALUE
from yafowil.utils import Tag

import uuid

if IS_PY2:
    from StringIO import StringIO
else:
    from io import StringIO


###############################################################################
# Helpers
###############################################################################

tag = Tag(lambda msg: msg)


def wrapped_fxml(value):
    return fxml(u'<div>' + value + u'</div>')


###############################################################################
# Tests
###############################################################################

class TestCommon(YafowilTestCase):
    # Common Blueprints

    # This test creates widgets from ist blueprints with different properties.

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
        self.check_output("""
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
        self.check_output("""
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

    def test_datatype_extractor(self):
        # No datatype given, no datatype conversion happens at all
        widget = factory(
            'text',
            name='MYFIELD',
            value='')
        data = widget.extract({'MYFIELD': u''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, '')

        # Test emptyvalue if ``str`` datatype set
        widget = factory(
            'text',
            name='MYDATATYPEFIELD',
            value='',
            props={
                'datatype': 'str',
            })

        # Default emptyvalue
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, EMPTY_VALUE)

        # None emptyvalue
        widget.attrs['emptyvalue'] = None
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, None)

        # UNSET emptyvalue
        widget.attrs['emptyvalue'] = UNSET
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        # String emptyvalue
        widget.attrs['emptyvalue'] = 'abc'
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, b'abc')

        # Unicode emptyvalue
        widget.attrs['emptyvalue'] = u''
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        # Test emptyvalue if ``int`` datatype set
        widget = factory(
            'text',
            name='MYDATATYPEFIELD',
            value='',
            props={
                'datatype': 'int',
            })

        # Default emptyvalue
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, EMPTY_VALUE)

        # None emptyvalue
        widget.attrs['emptyvalue'] = None
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, None)

        # UNSET emptyvalue
        widget.attrs['emptyvalue'] = UNSET
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        # Int emptyvalue
        widget.attrs['emptyvalue'] = -1
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, -1)

        # String emptyvalue. If convertable still fine
        widget.attrs['emptyvalue'] = '0'
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, 0)

        # Test emptyvalue if ``long`` datatype set
        widget = factory(
            'text',
            name='MYDATATYPEFIELD',
            value='',
            props={
                'datatype': 'long',
            })

        # Default emptyvalue
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, EMPTY_VALUE)

        # None emptyvalue
        widget.attrs['emptyvalue'] = None
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, None)

        # UNSET emptyvalue
        widget.attrs['emptyvalue'] = UNSET
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        # Int emptyvalue
        widget.attrs['emptyvalue'] = -1
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, LONG_TYPE(-1))

        # String emptyvalue. If convertable still fine
        widget.attrs['emptyvalue'] = '0'
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, LONG_TYPE(0))

        # Test emptyvalue if ``float`` datatype set
        widget = factory(
            'text',
            name='MYDATATYPEFIELD',
            value='',
            props={
                'datatype': 'float',
            })

        # Default emptyvalue
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, EMPTY_VALUE)

        # None emptyvalue
        widget.attrs['emptyvalue'] = None
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, None)

        # UNSET emptyvalue
        widget.attrs['emptyvalue'] = UNSET
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        # Float emptyvalue
        widget.attrs['emptyvalue'] = 0.1
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, 0.1)

        # String emptyvalue. If convertable still fine
        widget.attrs['emptyvalue'] = '0,2'
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, 0.2)

        # Test emptyvalue if ``uuid`` datatype set
        widget = factory(
            'text',
            name='MYDATATYPEFIELD',
            value='',
            props={
                'datatype': 'uuid',
            })

        # Default emptyvalue
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, EMPTY_VALUE)

        # None emptyvalue
        widget.attrs['emptyvalue'] = None
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, None)

        # UNSET emptyvalue
        widget.attrs['emptyvalue'] = UNSET
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        # UUID emptyvalue
        uid = uuid.uuid4()
        widget.attrs['emptyvalue'] = uid
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, uid)

        # String emptyvalue. If convertable still fine
        widget.attrs['emptyvalue'] = str(uid)
        data = widget.extract({})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYDATATYPEFIELD': ''})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, uid)

        # Integer datatype
        widget = factory(
            'text',
            name='MYDATATYPEFIELD',
            value='',
            props={
                'datatype': 'int',
            })
        data = widget.extract({'MYDATATYPEFIELD': '1'})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, 1)

        data = widget.extract({'MYDATATYPEFIELD': 'a'})
        self.assertEqual(
            data.errors,
            [ExtractionError('Input is not a valid integer.')]
        )

        # Float extraction
        widget = factory(
            'text',
            name='MYDATATYPEFIELD',
            value='',
            props={
                'datatype': 'float',
            })
        data = widget.extract({'MYDATATYPEFIELD': '1.2'})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, 1.2)

        data = widget.extract({'MYDATATYPEFIELD': 'a'})
        self.assertEqual(
            data.errors,
            [ExtractionError('Input is not a valid floating point number.')]
        )

        # UUID extraction
        widget = factory(
            'text',
            name='MYDATATYPEFIELD',
            value='',
            props={
                'datatype': 'uuid',
            })
        data = widget.extract({
            'MYDATATYPEFIELD': '3b8449f3-0456-4baa-a670-3066b0fcbda0'
        })
        self.assertEqual(data.errors, [])
        self.assertEqual(
            data.extracted,
            uuid.UUID('3b8449f3-0456-4baa-a670-3066b0fcbda0')
        )

        data = widget.extract({'MYDATATYPEFIELD': 'a'})
        self.assertEqual(
            data.errors,
            [ExtractionError('Input is not a valid UUID.')]
        )

        # Test ``datatype`` not allowed
        widget = factory(
            'text',
            name='MYDATATYPEFIELD',
            value='',
            props={
                'datatype': 'uuid',
                'allowed_datatypes': [int],
            })

        request = {
            'MYDATATYPEFIELD': '3b8449f3-0456-4baa-a670-3066b0fcbda0'
        }
        err = self.expect_error(
            ValueError,
            widget.extract,
            request
        )
        self.assertEqual(str(err), 'Datatype not allowed: "uuid"')

        # Test ``datatype_message``
        widget = factory(
            'text',
            name='MYDATATYPEFIELD',
            value='',
            props={
                'datatype': int,
                'datatype_message': 'This did not work'
            })
        request = {
            'MYDATATYPEFIELD': 'a'
        }
        data = widget.extract(request)
        self.assertEqual(data.errors, [ExtractionError('This did not work')])
        self.assertEqual(data.extracted, 'a')

        # Test default error message if custom converter given but no
        # ``datatype_message`` defined
        def custom_converter(val):
            raise ValueError

        widget = factory(
            'text',
            name='MYDATATYPEFIELD',
            value='',
            props={
                'datatype': custom_converter,
            })
        request = {
            'MYDATATYPEFIELD': 'a'
        }
        data = widget.extract(request)
        self.assertEqual(
            data.errors,
            [ExtractionError('Input conversion failed.')]
        )
        self.assertEqual(data.extracted, 'a')

        # Test unknown string ``datatype`` identifier
        widget = factory(
            'text',
            name='MYDATATYPEFIELD',
            value='',
            props={
                'datatype': 'inexistent',
            })
        err = self.expect_error(
            ValueError,
            widget.extract,
            {'MYDATATYPEFIELD': 'a'}
        )
        self.assertEqual(str(err), 'Datatype unknown: "inexistent"')

    def test_checkbox_blueprint(self):
        # A boolean checkbox widget (default)
        widget = factory(
            'checkbox',
            name='MYCHECKBOX')
        self.check_output("""
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
        self.check_output("""
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

        # A checkbox with label
        widget = factory(
            'checkbox',
            name='MYCHECKBOX',
            props={
                'with_label': True
            })
        self.check_output("""
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
        self.check_output("""
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
        self.check_output("""
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
        self.check_output("""
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
        self.check_output("""
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
        self.check_output("""
        <RuntimeData MYCHECKBOX, value='Test Checkbox', extracted='1' at ...>
        """, data.treerepr())

        request = {
            'MYCHECKBOX': '',
            'MYCHECKBOX-exists': 'checkboxexists'
        }
        data = widget.extract(request)
        self.check_output("""
        <RuntimeData MYCHECKBOX, value='Test Checkbox', extracted='' at ...>
        """, data.treerepr())

        request = {
            'MYCHECKBOX': 1,
        }
        data = widget.extract(request)
        self.check_output("""
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
        self.check_output("""
        <RuntimeData MYCHECKBOX, value='Test Checkbox', extracted=True at ...>
        """, data.treerepr())

        request = {
            'MYCHECKBOX-exists': 'checkboxexists'
        }
        data = widget.extract(request)
        self.check_output("""
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
        err = self.expect_error(
            ValueError,
            widget.extract,
            request
        )
        msg = "Checkbox widget has invalid format 'invalid' set"
        self.assertEqual(str(err), msg)

        # Render in display mode
        widget = factory(
            'checkbox',
            name='MYCHECKBOX',
            value=False,
            mode='display',
            props={
                'format': 'bool'
            })
        self.check_output("""
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
        self.check_output("""
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
        self.check_output("""
        <div class="display-checkbox" id="display-MYCHECKBOX">Yes<input
        class="checkbox" id="input-MYCHECKBOX" name="MYCHECKBOX" type="hidden"
        value="" /><input id="checkboxexists-MYCHECKBOX"
        name="MYCHECKBOX-exists" type="hidden" value="checkboxexists" /></div>
        """, widget())

        data = widget.extract(request={'MYCHECKBOX-exists': 'checkboxexists'})
        self.assertEqual(data.name, 'MYCHECKBOX')
        self.assertEqual(data.value, True)
        self.assertEqual(data.extracted, False)

        self.check_output("""
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

        self.check_output("""
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
        self.check_output("""
        <div class="display-checkbox" id="display-MYCHECKBOX">yes<input
        class="checkbox" id="input-MYCHECKBOX" name="MYCHECKBOX"
        type="hidden" value="yes" /><input id="checkboxexists-MYCHECKBOX"
        name="MYCHECKBOX-exists" type="hidden" value="checkboxexists" /></div>
        """, widget())

        data = widget.extract(request={'MYCHECKBOX-exists': 'checkboxexists'})
        self.assertEqual(data.name, 'MYCHECKBOX')
        self.assertEqual(data.value, 'yes')
        self.assertEqual(data.extracted, '')

        self.check_output("""
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

        self.check_output("""
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

        self.check_output("""
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
        self.check_output("""
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
        self.check_output("""
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
        self.check_output("""
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
        self.check_output("""
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
        self.check_output("""
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
        self.check_output("""
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

        self.check_output("""
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
        self.check_output("""
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
        self.check_output("""
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

    def test_select_blueprint_single_value(self):
        # Default single value selection
        vocab = [
            ('one', 'One'),
            ('two', 'Two'),
            ('three', 'Three'),
            ('four', 'Four')
        ]
        widget = factory(
            'select',
            name='MYSELECT',
            value='one',
            props={
                'vocabulary': vocab
            })
        self.check_output("""
        <select class="select" id="input-MYSELECT" name="MYSELECT">
          <option id="input-MYSELECT-one" selected="selected"
                  value="one">One</option>
          <option id="input-MYSELECT-two" value="two">Two</option>
          <option id="input-MYSELECT-three" value="three">Three</option>
          <option id="input-MYSELECT-four" value="four">Four</option>
        </select>
        """, fxml(widget()))

        data = widget.extract({'MYSELECT': 'two'})
        self.assertEqual(data.errors, [])
        self.assertEqual(data.extracted, 'two')

        self.check_output("""
        <select class="select" id="input-MYSELECT" name="MYSELECT">
          <option id="input-MYSELECT-one" value="one">One</option>
          <option id="input-MYSELECT-two" selected="selected"
                  value="two">Two</option>
          <option id="input-MYSELECT-three" value="three">Three</option>
          <option id="input-MYSELECT-four" value="four">Four</option>
        </select>
        """, fxml(widget(data=data)))

        # Single value selection completly disabled
        widget.attrs['disabled'] = True
        self.check_output("""
        <select class="select" disabled="disabled" id="input-MYSELECT"
                name="MYSELECT">
          <option id="input-MYSELECT-one" selected="selected"
                  value="one">One</option>
          <option id="input-MYSELECT-two" value="two">Two</option>
          <option id="input-MYSELECT-three" value="three">Three</option>
          <option id="input-MYSELECT-four" value="four">Four</option>
        </select>
        """, fxml(widget()))

        # Single value selection with specific options disabled
        widget.attrs['disabled'] = ['two', 'four']
        self.check_output("""
        <select class="select" id="input-MYSELECT" name="MYSELECT">
          <option id="input-MYSELECT-one" selected="selected"
                  value="one">One</option>
          <option disabled="disabled" id="input-MYSELECT-two"
                  value="two">Two</option>
          <option id="input-MYSELECT-three" value="three">Three</option>
          <option disabled="disabled" id="input-MYSELECT-four"
                  value="four">Four</option>
        </select>
        """, fxml(widget()))

        del widget.attrs['disabled']

        # Single value selection display mode
        widget.mode = 'display'
        self.assertEqual(
            widget(),
            '<div class="display-select" id="display-MYSELECT">One</div>'
        )

        widget.attrs['display_proxy'] = True
        self.check_output("""
        <div>
          <div class="display-select" id="display-MYSELECT">One</div>
          <input class="select" id="input-MYSELECT" name="MYSELECT"
                 type="hidden" value="one"/>
        </div>
        """, wrapped_fxml(widget()))

        data = widget.extract(request={'MYSELECT': 'two'})
        self.assertEqual(data.name, 'MYSELECT')
        self.assertEqual(data.value, 'one')
        self.assertEqual(data.extracted, 'two')
        self.assertEqual(data.errors, [])

        self.check_output("""
        <div>
          <div class="display-select" id="display-MYSELECT">Two</div>
          <input class="select" id="input-MYSELECT" name="MYSELECT"
                 type="hidden" value="two"/>
        </div>
        """, wrapped_fxml(widget(data=data)))

        # Single value selection with datatype set
        widget = factory(
            'select',
            name='MYSELECT',
            props={
                'datatype': uuid.UUID
            })

        # Preselected values
        widget.getter = UNSET
        widget.attrs['vocabulary'] = [
            (UNSET, 'Empty value'),
            (uuid.UUID('1b679ef8-9068-45f5-8bb8-4007264aa7f7'), 'One')
        ]
        res = widget()
        self.check_output("""
        <select class="select" id="input-MYSELECT" name="MYSELECT">
          <option id="input-MYSELECT-" selected="selected"
                  value="">Empty value</option>
          <option id="input-MYSELECT-1b679ef8-..."
                  value="1b679ef8-...">One</option>
        </select>
        """, fxml(res))

        widget.getter = EMPTY_VALUE
        widget.attrs['vocabulary'][0] = (EMPTY_VALUE, 'Empty value')
        self.assertEqual(res, widget())

        widget.getter = None
        widget.attrs['vocabulary'][0] = (None, 'Empty value')
        self.assertEqual(res, widget())

        widget.getter = ''
        widget.attrs['vocabulary'][0] = ('', 'Empty value')
        self.assertEqual(res, widget())

        widget.getter = uuid.UUID('1b679ef8-9068-45f5-8bb8-4007264aa7f7')
        res = widget()
        self.check_output("""
        <select class="select" id="input-MYSELECT" name="MYSELECT">
          <option id="input-MYSELECT-"
                  value="">Empty value</option>
          <option id="input-MYSELECT-1b679ef8-..."
                  selected="selected" value="1b679ef8-...">One</option>
        </select>
        """, fxml(res))

        # Note, vocabulary keys are converted to ``datatype`` while widget
        # value needs to be of type defined in ``datatype`` or one from the
        # valid empty values
        widget.attrs['vocabulary'] = [
            (UNSET, 'Empty value'),
            ('1b679ef8-9068-45f5-8bb8-4007264aa7f7', 'One')
        ]
        res = widget()
        self.assertEqual(res, widget())

        # Test ``datatype`` extraction with selection
        vocab = [
            (EMPTY_VALUE, 'Empty value'),
            (1, 'One'),
            (2, 'Two'),
        ]
        widget = factory(
            'select',
            name='MYSELECT',
            value=2,
            props={
                'vocabulary': vocab,
                'datatype': 'int'
            })
        self.check_output("""
        <select class="select" id="input-MYSELECT" name="MYSELECT">
          <option id="input-MYSELECT-" value="">Empty value</option>
          <option id="input-MYSELECT-1" value="1">One</option>
          <option id="input-MYSELECT-2" selected="selected"
                  value="2">Two</option>
        </select>
        """, fxml(widget()))

        data = widget.extract({'MYSELECT': ''})
        self.assertEqual(data.extracted, EMPTY_VALUE)

        data = widget.extract({'MYSELECT': '1'})
        self.assertEqual(data.extracted, 1)

        self.check_output("""
        <select class="select" id="input-MYSELECT" name="MYSELECT">
          <option id="input-MYSELECT-" value="">Empty value</option>
          <option id="input-MYSELECT-1" selected="selected"
                  value="1">One</option>
          <option id="input-MYSELECT-2" value="2">Two</option>
        </select>
        """, fxml(widget(data=data)))

        # Test extraction with ``emptyvalue`` set
        widget.attrs['emptyvalue'] = UNSET
        data = widget.extract({})
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYSELECT': ''})
        self.assertEqual(data.extracted, UNSET)

        widget.attrs['emptyvalue'] = None
        data = widget.extract({})
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYSELECT': ''})
        self.assertEqual(data.extracted, None)

        widget.attrs['emptyvalue'] = 0
        data = widget.extract({})
        self.assertEqual(data.extracted, UNSET)

        data = widget.extract({'MYSELECT': ''})
        self.assertEqual(data.extracted, 0)

        # Single value selection with ``datatype`` set completly disabled
        widget.attrs['disabled'] = True
        self.check_output("""
        <select class="select" disabled="disabled" id="input-MYSELECT"
                name="MYSELECT">
          <option id="input-MYSELECT-" value="">Empty value</option>
          <option id="input-MYSELECT-1" value="1">One</option>
          <option id="input-MYSELECT-2" selected="selected"
                  value="2">Two</option>
        </select>
        """, fxml(widget()))

        # Single value selection with ``datatype`` with specific options
        # disabled
        widget.attrs['emptyvalue'] = None
        widget.attrs['disabled'] = [None, 2]
        rendered = widget()
        self.check_output("""
        <select class="select" id="input-MYSELECT" name="MYSELECT">
          <option disabled="disabled" id="input-MYSELECT-"
                  value="">Empty value</option>
          <option id="input-MYSELECT-1" value="1">One</option>
          <option disabled="disabled" id="input-MYSELECT-2"
                  selected="selected" value="2">Two</option>
        </select>
        """, fxml(rendered))

        widget.attrs['emptyvalue'] = UNSET
        widget.attrs['disabled'] = [UNSET, 2]
        self.assertEqual(widget(), rendered)

        widget.attrs['emptyvalue'] = EMPTY_VALUE
        widget.attrs['disabled'] = [EMPTY_VALUE, 2]
        self.assertEqual(widget(), rendered)

        widget.attrs['emptyvalue'] = 0
        widget.attrs['disabled'] = [0, 2]
        self.assertEqual(widget(), rendered)

        del widget.attrs['disabled']

        # Single value selection with datatype display mode
        widget.mode = 'display'
        self.assertEqual(
            widget(),
            '<div class="display-select" id="display-MYSELECT">Two</div>'
        )

        widget.attrs['display_proxy'] = True
        self.check_output("""
        <div>
          <div class="display-select" id="display-MYSELECT">Two</div>
          <input class="select" id="input-MYSELECT" name="MYSELECT"
                 type="hidden" value="2"/>
        </div>
        """, wrapped_fxml(widget()))

        data = widget.extract(request={'MYSELECT': '1'})
        self.assertEqual(data.name, 'MYSELECT')
        self.assertEqual(data.value, 2)
        self.assertEqual(data.extracted, 1)
        self.assertEqual(data.errors, [])

        self.check_output("""
        <div>
          <div class="display-select" id="display-MYSELECT">One</div>
          <input class="select" id="input-MYSELECT" name="MYSELECT"
                 type="hidden" value="1"/>
        </div>
        """, wrapped_fxml(widget(data=data)))

        # Generic HTML5 Data
        widget = factory(
            'select',
            name='MYSELECT',
            value='one',
            props={
                'data': {'foo': 'bar'},
                'vocabulary': [('one', 'One')]
            })
        self.check_output("""
        <select class="select" data-foo="bar" id="input-MYSELECT"
                name="MYSELECT">
          <option id="input-MYSELECT-one" selected="selected"
                  value="one">One</option>
        </select>
        """, fxml(widget()))

        widget = factory(
            'select',
            name='MYSELECT',
            value='one',
            props={
                'data': {'foo': 'bar'},
                'vocabulary': [('one', 'One')]
            },
            mode='display')
        self.check_output("""
        <div class="display-select" data-foo="bar"
             id="display-MYSELECT">One</div>
        """, fxml(widget()))

        # Persist
        widget = factory(
            'select',
            name='MYSELECT',
            props={
                'vocabulary': [('one', 'One')]
            })
        data = widget.extract({'MYSELECT': 'one'})
        model = dict()
        data.persist_writer = write_mapping_writer
        data.write(model)
        self.assertEqual(model, {'MYSELECT': 'one'})

    def test_select_blueprint_single_radio(self):
        # Render single selection as radio inputs
        vocab = [
            ('one', 'One'),
            ('two', 'Two'),
            ('three', 'Three'),
            ('four', 'Four')
        ]
        widget = factory(
            'select',
            name='MYSELECT',
            value='one',
            props={
                'vocabulary': vocab,
                'format': 'single',
                'listing_label_position': 'before'
            })
        self.check_output("""
        <div>
          <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden"
                 value="exists"/>
          <div id="radio-MYSELECT-wrapper">
            <div id="radio-MYSELECT-one">
              <label for="input-MYSELECT-one">One</label>
              <input checked="checked" class="select" id="input-MYSELECT-one"
                     name="MYSELECT" type="radio" value="one"/>
            </div>
            <div id="radio-MYSELECT-two">
              <label for="input-MYSELECT-two">Two</label>
              <input class="select" id="input-MYSELECT-two" name="MYSELECT"
                     type="radio" value="two"/>
            </div>
            <div id="radio-MYSELECT-three">
              <label for="input-MYSELECT-three">Three</label>
              <input class="select" id="input-MYSELECT-three" name="MYSELECT"
                     type="radio" value="three"/>
            </div>
            <div id="radio-MYSELECT-four">
              <label for="input-MYSELECT-four">Four</label>
              <input class="select" id="input-MYSELECT-four" name="MYSELECT"
                     type="radio" value="four"/>
            </div>
          </div>
        </div>
        """, wrapped_fxml(widget()))

        # Render single selection as radio inputs, disables all
        widget.attrs['disabled'] = True
        self.check_output("""
        <div>
          <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden"
                 value="exists"/>
          <div id="radio-MYSELECT-wrapper">
            <div id="radio-MYSELECT-one">
              <label for="input-MYSELECT-one">One</label>
              <input checked="checked" class="select" disabled="disabled"
                     id="input-MYSELECT-one" name="MYSELECT" type="radio"
                     value="one"/>
            </div>
            <div id="radio-MYSELECT-two">
              <label for="input-MYSELECT-two">Two</label>
              <input class="select" disabled="disabled" id="input-MYSELECT-two"
                     name="MYSELECT" type="radio" value="two"/>
            </div>
            <div id="radio-MYSELECT-three">
              <label for="input-MYSELECT-three">Three</label>
              <input class="select" disabled="disabled"
                     id="input-MYSELECT-three" name="MYSELECT" type="radio"
                     value="three"/>
            </div>
            <div id="radio-MYSELECT-four">
              <label for="input-MYSELECT-four">Four</label>
              <input class="select" disabled="disabled"
                     id="input-MYSELECT-four" name="MYSELECT" type="radio"
                     value="four"/>
            </div>
          </div>
        </div>
        """, wrapped_fxml(widget()))

        # Render single selection as radio inputs, disables some
        widget.attrs['disabled'] = ['one', 'three']
        self.check_output("""
        <div>
          <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden"
                 value="exists"/>
          <div id="radio-MYSELECT-wrapper">
            <div id="radio-MYSELECT-one">
              <label for="input-MYSELECT-one">One</label>
              <input checked="checked" class="select" disabled="disabled"
                     id="input-MYSELECT-one" name="MYSELECT" type="radio"
                     value="one"/>
            </div>
            <div id="radio-MYSELECT-two">
              <label for="input-MYSELECT-two">Two</label>
              <input class="select" id="input-MYSELECT-two" name="MYSELECT"
                     type="radio" value="two"/>
            </div>
            <div id="radio-MYSELECT-three">
              <label for="input-MYSELECT-three">Three</label>
              <input class="select" disabled="disabled"
                     id="input-MYSELECT-three"
                     name="MYSELECT" type="radio" value="three"/>
            </div>
            <div id="radio-MYSELECT-four">
              <label for="input-MYSELECT-four">Four</label>
              <input class="select" id="input-MYSELECT-four" name="MYSELECT"
                     type="radio" value="four"/>
            </div>
          </div>
        </div>
        """, wrapped_fxml(widget()))

        del widget.attrs['disabled']

        # Radio single valued display mode
        widget.mode = 'display'
        self.assertEqual(
            widget(),
            '<div class="display-select" id="display-MYSELECT">One</div>'
        )

        widget.attrs['display_proxy'] = True
        self.check_output("""
        <div>
          <div class="display-select" id="display-MYSELECT">One</div>
          <input class="select" id="input-MYSELECT" name="MYSELECT"
                 type="hidden" value="one"/>
        </div>
        """, wrapped_fxml(widget()))

        data = widget.extract(request={'MYSELECT': 'two'})
        self.assertEqual(data.name, 'MYSELECT')
        self.assertEqual(data.value, 'one')
        self.assertEqual(data.extracted, 'two')
        self.assertEqual(data.errors, [])

        self.check_output("""
        <div>
          <div class="display-select" id="display-MYSELECT">Two</div>
          <input class="select" id="input-MYSELECT" name="MYSELECT"
                 type="hidden" value="two"/>
        </div>
        """, wrapped_fxml(widget(data=data)))

        # Radio single value selection with uuid datatype set
        vocab = [
            ('3762033b-7118-4bad-89ed-7cb71f5ab6d1', 'One'),
            ('74ef603d-29d0-4016-a003-334719dde835', 'Two'),
            ('b1116392-4a80-496d-86f1-3a2c87e09c59', 'Three'),
            ('e09471dc-625d-463b-be03-438d7089ec13', 'Four')
        ]
        widget = factory(
            'select',
            name='MYSELECT',
            value='b1116392-4a80-496d-86f1-3a2c87e09c59',
            props={
                'vocabulary': vocab,
                'datatype': 'uuid',
                'format': 'single',
            })
        self.check_output("""
        <div>
          <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden"
                 value="exists"/>
          <div id="radio-MYSELECT-wrapper">
            <div id="radio-MYSELECT-3762033b-7118-4bad-89ed-7cb71f5ab6d1">
              <label
                for="input-MYSELECT-3762033b-7118-4bad-89ed-7cb71f5ab6d1"><input
                class="select"
                id="input-MYSELECT-3762033b-7118-4bad-89ed-7cb71f5ab6d1"
                name="MYSELECT" type="radio"
                value="3762033b-7118-4bad-89ed-7cb71f5ab6d1"/>One</label>
            </div>
            <div id="radio-MYSELECT-74ef603d-29d0-4016-a003-334719dde835">
              <label
                for="input-MYSELECT-74ef603d-29d0-4016-a003-334719dde835"><input
                class="select"
                id="input-MYSELECT-74ef603d-29d0-4016-a003-334719dde835"
                name="MYSELECT" type="radio"
                value="74ef603d-29d0-4016-a003-334719dde835"/>Two</label>
            </div>
            <div id="radio-MYSELECT-b1116392-4a80-496d-86f1-3a2c87e09c59">
              <label
                for="input-MYSELECT-b1116392-4a80-496d-86f1-3a2c87e09c59"><input
                checked="checked"
                class="select"
                id="input-MYSELECT-b1116392-4a80-496d-86f1-3a2c87e09c59"
                name="MYSELECT" type="radio"
                value="b1116392-4a80-496d-86f1-3a2c87e09c59"/>Three</label>
            </div>
            <div id="radio-MYSELECT-e09471dc-625d-463b-be03-438d7089ec13">
              <label
                for="input-MYSELECT-e09471dc-625d-463b-be03-438d7089ec13"><input
                class="select"
                id="input-MYSELECT-e09471dc-625d-463b-be03-438d7089ec13"
                name="MYSELECT" type="radio"
                value="e09471dc-625d-463b-be03-438d7089ec13"/>Four</label>
            </div>
          </div>
        </div>
        """, wrapped_fxml(widget()))

        data = widget.extract({
            'MYSELECT': 'e09471dc-625d-463b-be03-438d7089ec13'
        })
        self.assertEqual(
            data.extracted,
            uuid.UUID('e09471dc-625d-463b-be03-438d7089ec13')
        )

        self.check_output("""
        <div>
          <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden"
                 value="exists"/>
          <div id="radio-MYSELECT-wrapper">
            <div id="radio-MYSELECT-3762033b-7118-4bad-89ed-7cb71f5ab6d1">
              <label
                for="input-MYSELECT-3762033b-7118-4bad-89ed-7cb71f5ab6d1"><input
                class="select"
                id="input-MYSELECT-3762033b-7118-4bad-89ed-7cb71f5ab6d1"
                name="MYSELECT" type="radio"
                value="3762033b-7118-4bad-89ed-7cb71f5ab6d1"/>One</label>
            </div>
            <div id="radio-MYSELECT-74ef603d-29d0-4016-a003-334719dde835">
              <label
                for="input-MYSELECT-74ef603d-29d0-4016-a003-334719dde835"><input
                class="select"
                id="input-MYSELECT-74ef603d-29d0-4016-a003-334719dde835"
                name="MYSELECT" type="radio"
                value="74ef603d-29d0-4016-a003-334719dde835"/>Two</label>
            </div>
            <div id="radio-MYSELECT-b1116392-4a80-496d-86f1-3a2c87e09c59">
              <label
                for="input-MYSELECT-b1116392-4a80-496d-86f1-3a2c87e09c59"><input
                class="select"
                id="input-MYSELECT-b1116392-4a80-496d-86f1-3a2c87e09c59"
                name="MYSELECT" type="radio"
                value="b1116392-4a80-496d-86f1-3a2c87e09c59"/>Three</label>
            </div>
            <div id="radio-MYSELECT-e09471dc-625d-463b-be03-438d7089ec13">
              <label
                for="input-MYSELECT-e09471dc-625d-463b-be03-438d7089ec13"><input
                checked="checked" class="select"
                id="input-MYSELECT-e09471dc-625d-463b-be03-438d7089ec13"
                name="MYSELECT" type="radio"
                value="e09471dc-625d-463b-be03-438d7089ec13"/>Four</label>
            </div>
          </div>
        </div>
        """, wrapped_fxml(widget(data=data)))

        # Generic HTML5 Data
        widget = factory(
            'select',
            name='MYSELECT',
            value='one',
            props={
                'vocabulary': [('one', 'One')],
                'format': 'single',
                'listing_label_position': 'before',
                'data': {'foo': 'bar'}
            })
        self.check_output("""
        <div>
          <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden"
                 value="exists"/>
          <div data-foo="bar" id="radio-MYSELECT-wrapper">
            <div id="radio-MYSELECT-one">
              <label for="input-MYSELECT-one">One</label>
              <input checked="checked" class="select" id="input-MYSELECT-one"
                     name="MYSELECT" type="radio" value="one"/>
            </div>
          </div>
        </div>
        """, wrapped_fxml(widget()))

        widget = factory(
            'select',
            name='MYSELECT',
            value='one',
            props={
                'vocabulary': [('one', 'One')],
                'format': 'single',
                'listing_label_position': 'before',
                'data': {'foo': 'bar'}
            },
            mode='display')
        self.check_output("""
        <div>
          <div class="display-select" data-foo="bar"
               id="display-MYSELECT">One</div>
        </div>
        """, wrapped_fxml(widget()))

    def test_select_blueprint_multi(self):
        # Empty multi valued
        widget = factory(
            'select',
            name='EMPTYSELECT',
            value=UNSET,
            props={
                'multivalued': True,
                'vocabulary': []
            })
        self.check_output("""
        <div>
          <input id="exists-EMPTYSELECT" name="EMPTYSELECT-exists"
                 type="hidden" value="exists"/>
          <select class="select" id="input-EMPTYSELECT" multiple="multiple"
                  name="EMPTYSELECT"> </select>
        </div>
        """, wrapped_fxml(widget()))

        # Default multi valued
        vocab = [
            ('one', 'One'),
            ('two', 'Two'),
            ('three', 'Three'),
            ('four', 'Four')
        ]
        widget = factory(
            'select',
            name='MYSELECT',
            value=['one', 'two'],
            props={
                'multivalued': True,
                'vocabulary': vocab
            })
        self.check_output("""
        <div>
          <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden"
                 value="exists"/>
          <select class="select" id="input-MYSELECT" multiple="multiple"
                  name="MYSELECT">
            <option id="input-MYSELECT-one" selected="selected"
                    value="one">One</option>
            <option id="input-MYSELECT-two" selected="selected"
                    value="two">Two</option>
            <option id="input-MYSELECT-three" value="three">Three</option>
            <option id="input-MYSELECT-four" value="four">Four</option>
          </select>
        </div>
        """, wrapped_fxml(widget()))

        # Extract multi valued selection and render widget with extracted data
        data = widget.extract(request={'MYSELECT': ['one', 'four']})
        self.assertEqual(data.name, 'MYSELECT')
        self.assertEqual(data.value, ['one', 'two'])
        self.assertEqual(data.extracted, ['one', 'four'])
        self.assertEqual(data.errors, [])

        self.check_output("""
        <div>
          <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden"
                 value="exists"/>
          <select class="select" id="input-MYSELECT" multiple="multiple"
                  name="MYSELECT">
            <option id="input-MYSELECT-one" selected="selected"
                    value="one">One</option>
            <option id="input-MYSELECT-two" value="two">Two</option>
            <option id="input-MYSELECT-three" value="three">Three</option>
            <option id="input-MYSELECT-four" selected="selected"
                    value="four">Four</option>
          </select>
        </div>
        """, wrapped_fxml(widget(data=data)))

        # Multi selection display mode
        widget.mode = 'display'
        self.check_output("""
        <ul class="display-select" id="display-MYSELECT">
          <li>One</li>
          <li>Two</li>
        </ul>
        """, fxml(widget()))

        # Multi selection display mode with display proxy
        widget.attrs['display_proxy'] = True
        self.check_output("""
        <div>
          <ul class="display-select" id="display-MYSELECT">
            <li>One</li>
            <li>Two</li>
          </ul>
          <input class="select" id="input-MYSELECT" name="MYSELECT"
                 type="hidden" value="one"/>
          <input class="select" id="input-MYSELECT" name="MYSELECT"
                 type="hidden" value="two"/>
        </div>
        """, wrapped_fxml(widget()))

        # Multi selection display mode with display proxy and extracted data
        data = widget.extract(request={'MYSELECT': ['one']})
        self.assertEqual(data.name, 'MYSELECT')
        self.assertEqual(data.value, ['one', 'two'])
        self.assertEqual(data.extracted, ['one'])
        self.assertEqual(data.errors, [])

        self.check_output("""
        <div>
          <ul class="display-select" id="display-MYSELECT">
            <li>One</li>
          </ul>
          <input class="select" id="input-MYSELECT" name="MYSELECT"
                 type="hidden" value="one"/>
        </div>
        """, wrapped_fxml(widget(data=data)))

        # Multi selection display with empty values list
        widget = factory(
            'select',
            name='MYSELECT',
            value=[],
            props={
                'vocabulary': [],
                'multivalued': True
            },
            mode='display')
        self.check_output("""
        <div>
          <div class="display-select" id="display-MYSELECT"/>
        </div>
        """, wrapped_fxml(widget()))

        # Multi selection display with missing term in vocab
        widget = factory(
            'select',
            name='MYSELECT',
            value=['one', 'two'],
            props={
                'multivalued': True,
                'vocabulary': [('two', 'Two')]
            },
            mode='display')
        self.check_output("""
        <ul class="display-select" id="display-MYSELECT">
          <li>one</li>
          <li>Two</li>
        </ul>
        """, fxml(widget()))

        # Multiple values on single valued selection fails
        vocab = [
            ('one', 'One'),
            ('two', 'Two'),
            ('three', 'Three'),
            ('four', 'Four')
        ]
        widget = factory(
            'select',
            name='MYSELECT',
            value=['one', 'two'],
            props={
                'vocabulary': vocab
            })
        err = self.expect_error(
            ValueError,
            widget
        )
        self.assertEqual(str(err), 'Multiple values for single selection.')

        # Multi value selection with float datatype set
        vocab = [
            (1.0, 'One'),
            (2.0, 'Two'),
            (3.0, 'Three'),
            (4.0, 'Four')
        ]
        widget = factory(
            'select',
            name='MYSELECT',
            value=[1.0, 2.0],
            props={
                'datatype': 'float',
                'multivalued': True,
                'vocabulary': vocab,
                'emptyvalue': []
            })
        self.check_output("""
        <div>
          <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden"
                 value="exists"/>
          <select class="select" id="input-MYSELECT" multiple="multiple"
                  name="MYSELECT">
            <option id="input-MYSELECT-1.0" selected="selected"
                    value="1.0">One</option>
            <option id="input-MYSELECT-2.0" selected="selected"
                    value="2.0">Two</option>
            <option id="input-MYSELECT-3.0" value="3.0">Three</option>
            <option id="input-MYSELECT-4.0" value="4.0">Four</option>
          </select>
        </div>
        """, wrapped_fxml(widget()))

        request = {
            'MYSELECT': ['2.0', '3.0']
        }
        data = widget.extract(request=request)
        self.assertEqual(data.extracted, [2.0, 3.0])

        self.check_output("""
        <div>
          <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden"
                 value="exists"/>
          <select class="select" id="input-MYSELECT" multiple="multiple"
                  name="MYSELECT">
            <option id="input-MYSELECT-1.0" value="1.0">One</option>
            <option id="input-MYSELECT-2.0" selected="selected"
                    value="2.0">Two</option>
            <option id="input-MYSELECT-3.0" selected="selected"
                    value="3.0">Three</option>
            <option id="input-MYSELECT-4.0" value="4.0">Four</option>
          </select>
        </div>
        """, wrapped_fxml(widget(data=data)))

        request = {
            'MYSELECT': '4.0'
        }
        data = widget.extract(request=request)
        self.assertEqual(data.extracted, [4.0])

        request = {
            'MYSELECT': ''
        }
        data = widget.extract(request=request)
        self.assertEqual(data.extracted, [])

        # Generic HTML5 Data
        vocab = [
            ('one', 'One'),
            ('two', 'Two')
        ]
        widget = factory(
            'select',
            name='MYSELECT',
            value=['one', 'two'],
            props={
                'multivalued': True,
                'data': {'foo': 'bar'},
                'vocabulary': vocab
            })
        self.check_output("""
        <div>
          <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden"
            value="exists"/>
          <select class="select" data-foo="bar" id="input-MYSELECT"
                  multiple="multiple" name="MYSELECT">
            <option id="input-MYSELECT-one" selected="selected"
                    value="one">One</option>
            <option id="input-MYSELECT-two" selected="selected"
                    value="two">Two</option>
          </select>
        </div>
        """, wrapped_fxml(widget()))

        widget.mode = 'display'
        self.check_output("""
        <ul class="display-select" data-foo="bar" id="display-MYSELECT">
          <li>One</li>
          <li>Two</li>
        </ul>
        """, fxml(widget()))

        # Persist
        widget = factory(
            'select',
            name='MYSELECT',
            value=['one', 'two'],
            props={
                'multivalued': True,
                'vocabulary': vocab
            })
        data = widget.extract({'MYSELECT': ['one', 'two', 'three']})
        model = dict()
        data.persist_writer = write_mapping_writer
        data.write(model)
        self.assertEqual(model, {'MYSELECT': ['one', 'two', 'three']})

    def test_select_blueprint_multi_checkboxes(self):
        # Render multi selection as checkboxes
        vocab = [
            ('one', 'One'),
            ('two', 'Two'),
            ('three', 'Three'),
            ('four', 'Four')
        ]
        widget = factory(
            'select',
            name='MYSELECT',
            value='one',
            props={
                'multivalued': True,
                'vocabulary': vocab,
                'format': 'single'
            })
        self.check_output("""
        <div>
          <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden"
                 value="exists"/>
          <div id="checkbox-MYSELECT-wrapper">
            <div id="checkbox-MYSELECT-one">
              <label for="input-MYSELECT-one"><input checked="checked"
                     class="select" id="input-MYSELECT-one" name="MYSELECT"
                     type="checkbox" value="one"/>One</label>
            </div>
            <div id="checkbox-MYSELECT-two">
              <label for="input-MYSELECT-two"><input class="select"
                     id="input-MYSELECT-two" name="MYSELECT" type="checkbox"
                     value="two"/>Two</label>
            </div>
            <div id="checkbox-MYSELECT-three">
              <label for="input-MYSELECT-three"><input class="select"
                     id="input-MYSELECT-three" name="MYSELECT" type="checkbox"
                     value="three"/>Three</label>
            </div>
            <div id="checkbox-MYSELECT-four">
              <label for="input-MYSELECT-four"><input class="select"
                     id="input-MYSELECT-four" name="MYSELECT" type="checkbox"
                     value="four"/>Four</label>
            </div>
          </div>
        </div>
        """, wrapped_fxml(widget()))

        # Checkbox multi selection display mode. Note, other as above, preset
        # value for multivalued widget is set as string, which is treaten as
        # one item selected and covered with the below tests
        widget.mode = 'display'
        self.check_output("""
        <ul class="display-select" id="display-MYSELECT">
          <li>One</li>
        </ul>
        """, fxml(widget()))

        # Checkbox multi selection display mode with display proxy
        widget.attrs['display_proxy'] = True
        self.check_output("""
        <div>
          <ul class="display-select" id="display-MYSELECT">
            <li>One</li>
          </ul>
          <input class="select" id="input-MYSELECT" name="MYSELECT"
                 type="hidden" value="one"/>
        </div>
        """, wrapped_fxml(widget()))

        # Checkbox multi selection display mode with display proxy and
        # extracted data
        data = widget.extract(request={'MYSELECT': ['two']})
        self.assertEqual(data.name, 'MYSELECT')
        self.assertEqual(data.value, 'one')
        self.assertEqual(data.extracted, ['two'])
        self.assertEqual(data.errors, [])

        self.check_output("""
        <div>
          <ul class="display-select" id="display-MYSELECT">
            <li>Two</li>
          </ul>
          <input class="select" id="input-MYSELECT" name="MYSELECT"
                 type="hidden" value="two"/>
        </div>
        """, wrapped_fxml(widget(data=data)))

        # Generic HTML5 Data
        widget = factory(
            'select',
            name='MYSELECT',
            value='one',
            props={
                'multivalued': True,
                'data': {'foo': 'bar'},
                'vocabulary': [('one', 'One')],
                'format': 'single'
            })
        self.check_output("""
        <div>
          <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden"
                 value="exists"/>
          <div data-foo="bar" id="checkbox-MYSELECT-wrapper">
            <div id="checkbox-MYSELECT-one">
              <label for="input-MYSELECT-one"><input checked="checked"
                     class="select" id="input-MYSELECT-one" name="MYSELECT"
                     type="checkbox" value="one"/>One</label>
            </div>
          </div>
        </div>
        """, wrapped_fxml(widget()))

        widget.mode = 'display'
        self.check_output("""
        <ul class="display-select" data-foo="bar" id="display-MYSELECT">
          <li>One</li>
        </ul>
        """, fxml(widget()))

    def test_select_blueprint_misc(self):
        # Using 'ul' instead of 'div' for rendering radio or checkbox
        # selections
        vocab = [
            ('one', 'One'),
            ('two', 'Two'),
            ('three', 'Three'),
            ('four', 'Four')
        ]
        widget = factory(
            'select',
            name='MYSELECT',
            value='one',
            props={
                'multivalued': True,
                'vocabulary': vocab,
                'format': 'single',
                'listing_tag': 'ul'
            })
        self.check_output("""
        <div>
          <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden"
                 value="exists"/>
          <ul id="checkbox-MYSELECT-wrapper">
            <li id="checkbox-MYSELECT-one">
              <label for="input-MYSELECT-one"><input checked="checked"
                     class="select" id="input-MYSELECT-one" name="MYSELECT"
                     type="checkbox" value="one"/>One</label>
            </li>
            <li id="checkbox-MYSELECT-two">
              <label for="input-MYSELECT-two"><input class="select"
                     id="input-MYSELECT-two" name="MYSELECT" type="checkbox"
                     value="two"/>Two</label>
            </li>
            <li id="checkbox-MYSELECT-three">
              <label for="input-MYSELECT-three"><input class="select"
                     id="input-MYSELECT-three" name="MYSELECT" type="checkbox"
                     value="three"/>Three</label>
            </li>
            <li id="checkbox-MYSELECT-four">
              <label for="input-MYSELECT-four"><input class="select"
                     id="input-MYSELECT-four" name="MYSELECT" type="checkbox"
                     value="four"/>Four</label>
            </li>
          </ul>
        </div>
        """, wrapped_fxml(widget()))

        # Render single format selection with label after input
        widget = factory(
            'select',
            name='MYSELECT',
            value='one',
            props={
                'multivalued': True,
                'vocabulary': [
                    ('one', 'One'),
                    ('two', 'Two'),
                ],
                'format': 'single',
                'listing_tag': 'ul',
                'listing_label_position': 'after'
            })
        self.check_output("""
        <div>
          <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden"
                 value="exists"/>
          <ul id="checkbox-MYSELECT-wrapper">
            <li id="checkbox-MYSELECT-one">
              <input checked="checked" class="select" id="input-MYSELECT-one"
                     name="MYSELECT" type="checkbox" value="one"/>
              <label for="input-MYSELECT-one">One</label>
            </li>
            <li id="checkbox-MYSELECT-two">
              <input class="select" id="input-MYSELECT-two" name="MYSELECT"
                     type="checkbox" value="two"/>
              <label for="input-MYSELECT-two">Two</label>
            </li>
          </ul>
        </div>
        """, wrapped_fxml(widget()))

        # Render single format selection with input inside label before
        # checkbox
        widget = factory(
            'select',
            name='MYSELECT',
            value='one',
            props={
                'multivalued': True,
                'vocabulary': [
                    ('one', 'One'),
                    ('two', 'Two'),
                ],
                'format': 'single',
                'listing_tag': 'ul',
                'listing_label_position': 'inner-before'
            })
        self.check_output("""
        <div>
          <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden"
                 value="exists"/>
          <ul id="checkbox-MYSELECT-wrapper">
            <li id="checkbox-MYSELECT-one">
              <label for="input-MYSELECT-one">One<input checked="checked"
                     class="select" id="input-MYSELECT-one" name="MYSELECT"
                     type="checkbox" value="one"/></label>
            </li>
            <li id="checkbox-MYSELECT-two">
              <label for="input-MYSELECT-two">Two<input class="select"
                     id="input-MYSELECT-two" name="MYSELECT" type="checkbox"
                     value="two"/></label>
            </li>
          </ul>
        </div>
        """, wrapped_fxml(widget()))

        # Check BBB 'inner' for 'listing_label_position' which behaves like
        # 'inner-after'
        widget = factory(
            'select',
            name='MYSELECT',
            value='one',
            props={
                'vocabulary': [('one', 'One')],
                'format': 'single',
                'listing_label_position': 'inner'
            })
        self.check_output("""
        <div>
          <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden"
                 value="exists"/>
          <div id="radio-MYSELECT-wrapper">
            <div id="radio-MYSELECT-one">
              <label for="input-MYSELECT-one"><input checked="checked"
                     class="select" id="input-MYSELECT-one" name="MYSELECT"
                     type="radio" value="one"/>One</label>
            </div>
          </div>
        </div>
        """, wrapped_fxml(widget()))

        # Check selection required
        vocab = [
            ('one', 'One'),
            ('two', 'Two'),
            ('three', 'Three'),
            ('four', 'Four')
        ]
        widget = factory(
            'select',
            name='MYSELECT',
            props={
                'required': 'Selection required',
                'vocabulary': vocab
            })
        self.check_output("""
        <select class="select" id="input-MYSELECT" name="MYSELECT"
                required="required">
          <option id="input-MYSELECT-one" value="one">One</option>
          <option id="input-MYSELECT-two" value="two">Two</option>
          <option id="input-MYSELECT-three" value="three">Three</option>
          <option id="input-MYSELECT-four" value="four">Four</option>
        </select>
        """, fxml(widget()))

        data = widget.extract(request={'MYSELECT': ''})
        self.assertEqual(data.name, 'MYSELECT')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, '')
        self.assertEqual(data.errors, [ExtractionError('Selection required')])

        vocab = [
            ('one', 'One'),
            ('two', 'Two'),
            ('three', 'Three'),
            ('four', 'Four')
        ]
        widget = factory(
            'select',
            name='MYSELECT',
            props={
                'required': 'Selection required',
                'multivalued': True,
                'vocabulary': vocab
            })
        self.check_output("""
        <div>
          <input id="exists-MYSELECT" name="MYSELECT-exists" type="hidden"
                 value="exists"/>
          <select class="select" id="input-MYSELECT" multiple="multiple"
                  name="MYSELECT" required="required">
            <option id="input-MYSELECT-one" value="one">One</option>
            <option id="input-MYSELECT-two" value="two">Two</option>
            <option id="input-MYSELECT-three" value="three">Three</option>
            <option id="input-MYSELECT-four" value="four">Four</option>
          </select>
        </div>
        """, wrapped_fxml(widget()))

        data = widget.extract(request={'MYSELECT-exists': 'exists'})
        self.assertEqual(data.name, 'MYSELECT')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, [])
        self.assertEqual(data.errors, [ExtractionError('Selection required')])

        # Check selection required with datatype set
        vocab = [
            (1, 'One'),
            (2, 'Two'),
            (3, 'Three'),
            (4, 'Four')
        ]
        widget = factory(
            'select',
            name='MYSELECT',
            props={
                'required': 'Selection required',
                'multivalued': True,
                'vocabulary': vocab,
                'datatype': int,
            })
        data = widget.extract(request={'MYSELECT-exists': 'exists'})
        self.assertEqual(data.name, 'MYSELECT')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, [])
        self.assertEqual(data.errors, [ExtractionError('Selection required')])

        data = widget.extract(request={'MYSELECT': ['1', '2']})
        self.assertEqual(data.name, 'MYSELECT')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, [1, 2])
        self.assertEqual(data.errors, [])

        # Single selection extraction without value
        widget = factory(
            'select',
            name='MYSELECT',
            props={
                'vocabulary': [
                    ('one', 'One'),
                    ('two', 'Two')
                ]
            })
        request = {
            'MYSELECT': 'one',
            'MYSELECT-exists': True,
        }
        data = widget.extract(request)
        self.assertEqual(data.name, 'MYSELECT')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, 'one')
        self.assertEqual(data.errors, [])

        # Single selection extraction with value
        widget = factory(
            'select',
            name='MYSELECT',
            value='two',
            props={
                'vocabulary': [
                    ('one', 'One'),
                    ('two', 'Two')
                ]
            })
        request = {
            'MYSELECT': 'one',
        }
        data = widget.extract(request)
        self.assertEqual(data.name, 'MYSELECT')
        self.assertEqual(data.value, 'two')
        self.assertEqual(data.extracted, 'one')
        self.assertEqual(data.errors, [])

        # Single selection extraction disabled (means browser does not post the
        # value) with value
        widget.attrs['disabled'] = True
        data = widget.extract({'MYSELECT-exists': True})
        self.assertEqual(data.name, 'MYSELECT')
        self.assertEqual(data.value, 'two')
        self.assertEqual(data.extracted, 'two')
        self.assertEqual(data.errors, [])

        # Disabled can be also the value itself
        widget.attrs['disabled'] = 'two'
        data = widget.extract({'MYSELECT-exists': True})
        self.assertEqual(data.name, 'MYSELECT')
        self.assertEqual(data.value, 'two')
        self.assertEqual(data.extracted, 'two')
        self.assertEqual(data.errors, [])

        # Single selection extraction required
        widget = factory(
            'select',
            name='MYSELECT',
            value='two',
            props={
                'required': True,
                'vocabulary': [
                    ('one', 'One'),
                    ('two', 'Two')
                ]
            })
        request = {
            'MYSELECT': '',
        }
        data = widget.extract(request)
        self.assertEqual(data.name, 'MYSELECT')
        self.assertEqual(data.value, 'two')
        self.assertEqual(data.extracted, '')
        self.assertEqual(
            data.errors,
            [ExtractionError('Mandatory field was empty')]
        )

        # A disabled and required returns value itself
        widget.attrs['disabled'] = True
        data = widget.extract({'MYSELECT-exists': True})
        self.assertEqual(data.name, 'MYSELECT')
        self.assertEqual(data.value, 'two')
        self.assertEqual(data.extracted, 'two')
        self.assertEqual(data.errors, [])

        # Multiple selection extraction without value
        widget = factory(
            'select',
            name='MYSELECT',
            props={
                'multivalued': True,
                'vocabulary': [
                    ('one', 'One'),
                    ('two', 'Two')
                ]
            })
        request = {
            'MYSELECT': ['one', 'two'],
        }
        data = widget.extract(request)
        self.assertEqual(data.name, 'MYSELECT')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, ['one', 'two'])
        self.assertEqual(data.errors, [])

        # Multiple selection extraction with value
        vocab = [
            ('one', 'One'),
            ('two', 'Two'),
            ('three', 'Three')
        ]
        widget = factory(
            'select',
            name='MYSELECT',
            value='three',
            props={
                'multivalued': True,
                'vocabulary': vocab
            })
        request = {
            'MYSELECT': 'one',
            'MYSELECT-exists': True,
        }
        data = widget.extract(request)
        self.assertEqual(data.name, 'MYSELECT')
        self.assertEqual(data.value, 'three')
        self.assertEqual(data.extracted, ['one'])
        self.assertEqual(data.errors, [])

        # Multiselection, completly disabled
        widget.attrs['disabled'] = True
        data = widget.extract({'MYSELECT-exists': True})
        self.assertEqual(data.name, 'MYSELECT')
        self.assertEqual(data.value, 'three')
        self.assertEqual(data.extracted, ['three'])
        self.assertEqual(data.errors, [])

        # Multiselection, partly disabled, empty request
        vocab = [
            ('one', 'One'),
            ('two', 'Two'),
            ('three', 'Three'),
            ('four', 'Four')
        ]
        widget = factory(
            'select',
            name='MYSELECT',
            value=['one', 'three'],
            props={
                'multivalued': True,
                'disabled': ['two', 'three'],
                'vocabulary': vocab
            })
        data = widget.extract({})
        self.assertEqual(data.name, 'MYSELECT')
        self.assertEqual(data.value, ['one', 'three'])
        self.assertEqual(data.extracted, UNSET)
        self.assertEqual(data.errors, [])

        # Multiselection, partly disabled, non-empty request
        vocab = [
            ('one', 'One'),
            ('two', 'Two'),
            ('three', 'Three'),
            ('four', 'Four'),
            ('five', 'Five')
        ]
        widget = factory(
            'select',
            name='MYSELECT',
            value=['one', 'two', 'four'],
            props={
                'multivalued': True,
                'disabled': ['two', 'three', 'four', 'five'],
                'vocabulary': vocab,
                'datatype': UNICODE_TYPE,
            })
        request = {
            'MYSELECT': ['one', 'two', 'five'],
            'MYSELECT-exists': True,
        }

        # Explanation:
        #
        # * one is a simple value as usal,
        # * two is disabled and in value, so it should be kept in.
        # * three is disabled and not in value, so it should kept out,
        # * four is disabled and in value, but someone removed it in the
        #   request, it should get recovered,
        # * five is disabled and not in value, but someone put it in the
        #   request. it should get removed.

        # Check extraction

        data = widget.extract(request)
        self.assertEqual(data.name, 'MYSELECT')
        self.assertEqual(data.value, ['one', 'two', 'four'])
        self.assertEqual(data.extracted, [u'one', u'two', u'four'])
        self.assertEqual(data.errors, [])

        # Single selection radio extraction
        vocab = [
            ('one', 'One'),
            ('two', 'Two'),
            ('three', 'Three')
        ]
        widget = factory(
            'select',
            'MYSELECT',
            props={
                'format': 'single',
                'vocabulary': vocab
            })

        # No exists marker in request. Extracts to UNSET
        request = {}
        data = widget.extract(request)
        self.assertEqual(data.name, 'MYSELECT')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, UNSET)
        self.assertEqual(data.errors, [])

        # Exists marker in request. Extracts to empty string
        request = {
            'MYSELECT-exists': '1',
        }
        data = widget.extract(request)
        self.assertEqual(data.name, 'MYSELECT')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, '')
        self.assertEqual(data.errors, [])

        # Select value
        request = {
            'MYSELECT-exists': '1',
            'MYSELECT': 'one',
        }
        data = widget.extract(request)
        self.assertEqual(data.name, 'MYSELECT')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, 'one')
        self.assertEqual(data.errors, [])

        # Multi selection radio extraction
        vocab = [
            ('one', 'One'),
            ('two', 'Two'),
            ('three', 'Three')
        ]
        widget = factory(
            'select',
            name='MYSELECT',
            props={
                'multivalued': True,
                'format': 'single',
                'vocabulary': vocab
            })

        # No exists marker in request. Extracts to UNSET
        request = {}
        data = widget.extract(request)
        self.assertEqual(data.name, 'MYSELECT')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, UNSET)
        self.assertEqual(data.errors, [])

        # Exists marker in request. Extracts to empty list
        request = {
            'MYSELECT-exists': '1',
        }
        data = widget.extract(request)
        self.assertEqual(data.name, 'MYSELECT')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, [])
        self.assertEqual(data.errors, [])

        # Select values
        request = {
            'MYSELECT-exists': '1',
            'MYSELECT': ['one', 'two'],
        }
        data = widget.extract(request)
        self.assertEqual(data.name, 'MYSELECT')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, ['one', 'two'])
        self.assertEqual(data.errors, [])

    def test_file_blueprint(self):
        # Render file input
        widget = factory(
            'file',
            name='MYFILE')
        self.assertEqual(
            widget(),
            '<input id="input-MYFILE" name="MYFILE" type="file" />'
        )

        # Extract empty
        request = {}
        data = widget.extract(request)
        self.assertEqual(data.extracted, UNSET)

        # Extract ``new``
        request = {
            'MYFILE': {'file': StringIO('123')},
        }
        data = widget.extract(request)

        self.assertEqual(data.name, 'MYFILE')

        self.assertEqual(data.value, UNSET)

        self.assertEqual(sorted(data.extracted.keys()), ['action', 'file'])
        self.assertEqual(data.extracted['action'], 'new')
        self.assertTrue(isinstance(data.extracted['file'], StringIO))
        self.assertEqual(data.extracted['file'].read(), '123')

        self.assertEqual(data.errors, [])

        # File with value preset
        widget = factory(
            'file',
            name='MYFILE',
            value={
                'file': StringIO('321'),
            })
        self.check_output("""
        <div>
          <input id="input-MYFILE" name="MYFILE" type="file"/>
          <div id="radio-MYFILE-keep">
            <input checked="checked" id="input-MYFILE-keep"
                   name="MYFILE-action" type="radio" value="keep"/>
            <span>Keep Existing file</span>
          </div>
          <div id="radio-MYFILE-replace">
            <input id="input-MYFILE-replace" name="MYFILE-action"
                   type="radio" value="replace"/>
            <span>Replace existing file</span>
          </div>
          <div id="radio-MYFILE-delete">
            <input id="input-MYFILE-delete" name="MYFILE-action"
                   type="radio" value="delete"/>
            <span>Delete existing file</span>
          </div>
        </div>
        """, wrapped_fxml(widget()))

        # Extract ``keep`` returns original value
        request = {
            'MYFILE': {'file': StringIO('123')},
            'MYFILE-action': 'keep'
        }
        data = widget.extract(request)

        self.assertEqual(data.name, 'MYFILE')

        self.assertEqual(sorted(data.value.keys()), ['action', 'file'])
        self.assertEqual(data.value['action'], 'keep')
        self.assertTrue(isinstance(data.value['file'], StringIO))

        self.assertEqual(sorted(data.extracted.keys()), ['action', 'file'])
        self.assertEqual(data.extracted['action'], 'keep')
        self.assertTrue(isinstance(data.extracted['file'], StringIO))
        self.assertEqual(data.extracted['file'].read(), '321')

        self.assertEqual(data.errors, [])

        # Extract ``replace`` returns new value
        request['MYFILE-action'] = 'replace'
        data = widget.extract(request)

        self.assertEqual(sorted(data.extracted.keys()), ['action', 'file'])
        self.assertEqual(data.extracted['action'], 'replace')
        self.assertEqual(data.extracted['file'].read(), '123')

        # Extract empty ``replace`` results in ``kepp action``
        request = {
            'MYFILE': '',
            'MYFILE-action': 'replace'
        }
        data = widget.extract(request)

        self.assertEqual(sorted(data.extracted.keys()), ['action', 'file'])
        self.assertEqual(data.extracted['action'], 'keep')
        self.assertEqual(data.extracted['file'].read(), '')

        # Extract ``delete`` returns UNSET
        request['MYFILE-action'] = 'delete'
        data = widget.extract(request)
        self.assertEqual(
            data.extracted,
            {'action': 'delete', 'file': UNSET}
        )

        self.assertEqual(data.extracted['action'], 'delete')

        self.check_output("""
        <div>
          <input id="input-MYFILE" name="MYFILE" type="file"/>
          <div id="radio-MYFILE-keep">
            <input id="input-MYFILE-keep" name="MYFILE-action" type="radio"
                   value="keep"/>
            <span>Keep Existing file</span>
          </div>
          <div id="radio-MYFILE-replace">
            <input id="input-MYFILE-replace" name="MYFILE-action" type="radio"
                   value="replace"/>
            <span>Replace existing file</span>
          </div>
          <div id="radio-MYFILE-delete">
            <input checked="checked" id="input-MYFILE-delete"
                   name="MYFILE-action" type="radio" value="delete"/>
            <span>Delete existing file</span>
          </div>
        </div>
        """, wrapped_fxml(widget(request=request)))

        widget = factory(
            'file',
            name='MYFILE',
            props={
                'accept': 'foo/bar'
            })
        self.assertEqual(widget(), (
            '<input accept="foo/bar" id="input-MYFILE" '
            'name="MYFILE" type="file" />'
        ))

        # File display renderer
        self.assertEqual(convert_bytes(1 * 1024 * 1024 * 1024 * 1024), '1.00T')
        self.assertEqual(convert_bytes(1 * 1024 * 1024 * 1024), '1.00G')
        self.assertEqual(convert_bytes(1 * 1024 * 1024), '1.00M')
        self.assertEqual(convert_bytes(1 * 1024), '1.00K')
        self.assertEqual(convert_bytes(1), '1.00b')

        widget = factory(
            'file',
            name='MYFILE',
            mode='display')
        self.check_output("""
        <div>No file</div>
        """, fxml(widget()))

        value = {
            'file': StringIO('12345'),
            'mimetype': 'text/plain',
            'filename': 'foo.txt',
        }
        widget = factory(
            'file',
            name='MYFILE',
            value=value,
            mode='display')
        self.check_output("""
        <div>
          <ul>
            <li><strong>Filename: </strong>foo.txt</li>
            <li><strong>Mimetype: </strong>text/plain</li>
            <li><strong>Size: </strong>5.00b</li>
          </ul>
        </div>
        """, fxml(widget()))

        # Generic HTML5 Data
        widget = factory(
            'file',
            name='MYFILE',
            props={
                'accept': 'foo/bar',
                'data': {
                    'foo': 'bar'
                }
            })
        self.assertEqual(widget(), (
            '<input accept="foo/bar" data-foo=\'bar\' id="input-MYFILE" '
            'name="MYFILE" type="file" />'
        ))

        widget.mode = 'display'
        self.assertEqual(widget(), "<div data-foo='bar'>No file</div>")

    def test_submit_blueprint(self):
        # Render submit button
        widget = factory(
            'submit',
            name='SAVE',
            props={
                'action': True,
                'label': 'Action name',
            })
        self.assertEqual(widget(), (
            '<input id="input-SAVE" name="action.SAVE" type="submit" '
            'value="Action name" />'
        ))

        # If expression is or evaluates to False, skip rendering
        widget = factory(
            'submit',
            name='SAVE',
            props={
                'action': True,
                'label': 'Action name',
                'expression': False,
            })
        self.assertEqual(widget(), '')

        widget = factory(
            'submit',
            name='SAVE',
            props={
                'action': True,
                'label': 'Action name',
                'expression': lambda: False,
            })
        self.assertEqual(widget(), '')

        # Generic HTML5 Data
        widget = factory(
            'submit',
            name='SAVE',
            props={
                'action': True,
                'label': 'Action name',
                'data': {'foo': 'bar'},
            })
        self.assertEqual(widget(), (
            '<input data-foo=\'bar\' id="input-SAVE" name="action.SAVE" '
            'type="submit" value="Action name" />'
        ))

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

    def test_label_blueprint(self):
        # Default
        widget = factory(
            'label:file',
            name='MYFILE',
            props={
                'label': 'MY FILE'
            })
        self.check_output("""
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
        self.check_output("""
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
        self.check_output("""
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
        err = self.expect_error(
            ValueError,
            widget
        )
        self.assertEqual(str(err), 'Invalid value for position "inexistent"')

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
                'label': lambda: 'Fooo',
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

    def test_field_blueprint(self):
        # Chained file inside field with label
        widget = factory(
            'field:label:file',
            name='MYFILE',
            props={
                'label': 'MY FILE'
            })
        self.check_output("""
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

        self.check_output("""
        <div class="field fielderrorclass" id="field-MYFIELD">
          <input class="required text" id="input-MYFIELD" name="MYFIELD"
                 required="required" type="text" value=""/>
        </div>
        """, fxml(widget(data)))

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
        self.check_output("""
        <div class="field" id="field-PASSWORD">
          <div class="error">
            <div class="errormessage">No password given!</div>
            <input class="password required" id="input-PASSWORD" name="PASSWORD"
                   required="required" type="password" value=""/>
          </div>
        </div>
        """, fxml(widget(data=data)))  # noqa

        data = widget.extract({'PASSWORD': 'secret'})
        self.check_output("""
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
        self.check_output("""
        <div class="field" id="field-PASSWORD">
          <div class="error">No password given!<input class="password required"
               id="input-PASSWORD" name="PASSWORD" required="required"
               type="password" value=""/></div>
        </div>
        """, fxml(widget(data=data)))

    def test_help_blueprint(self):
        # Render some additional help text
        widget = factory(
            'field:help:text',
            name='HELPEXAMPLE',
            props={
                'label': 'Help',
                'help': 'Shout out loud here'
            })
        self.check_output("""
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
        self.check_output("""
        <div class="field" id="field-HELPEXAMPLE">
          <input class="text" id="input-HELPEXAMPLE" name="HELPEXAMPLE"
                 type="text" value=""/>
        </div>
        """, fxml(widget()))

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
                'datatype': UNICODE_TYPE
            })
        data = widget.extract(request={'EMAIL': 'foo@example.com'})
        self.assertEqual(data.extracted, u'foo@example.com')
        self.assertTrue(isinstance(data.extracted, UNICODE_TYPE))
        self.assertFalse(isinstance(data.extracted, BYTES_TYPE))

        widget = factory(
            'email',
            name='EMAIL',
            props={
                'datatype': BYTES_TYPE
            })
        data = widget.extract(request={'EMAIL': u'foo@example.com'})
        self.assertEqual(data.extracted, b'foo@example.com')
        self.assertFalse(isinstance(data.extracted, UNICODE_TYPE))
        self.assertTrue(isinstance(data.extracted, BYTES_TYPE))

        # Persist
        widget = factory(
            'email',
            name='EMAIL')
        data = widget.extract({'EMAIL': 'foo@bar.baz'})
        model = dict()
        data.persist_writer = write_mapping_writer
        data.write(model)
        self.assertEqual(model, {'EMAIL': 'foo@bar.baz'})

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

    def test_search_blueprint(self):
        # Render search input field
        widget = factory(
            'search',
            name='SEARCH')
        self.assertEqual(widget(), (
            '<input class="search" id="input-SEARCH" name="SEARCH" '
            'type="search" value="" />'
        ))

        # Extract not required and empty
        data = widget.extract({'SEARCH': ''})
        self.assertEqual(data.errors, [])

        # Extract required empty
        widget.attrs['required'] = True
        data = widget.extract({'SEARCH': ''})
        self.assertEqual(data.name, 'SEARCH')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, '')
        self.assertEqual(
            data.errors,
            [ExtractionError('Mandatory field was empty')]
        )

        del widget.attrs['required']

        # Emptyvalue
        widget.attrs['emptyvalue'] = 'defaultsearch'
        data = widget.extract(request={'SEARCH': ''})
        self.assertEqual(data.name, 'SEARCH')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, 'defaultsearch')
        self.assertEqual(data.errors, [])

        data = widget.extract(request={'SEARCH': 'searchstr'})
        self.assertEqual(data.name, 'SEARCH')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, 'searchstr')
        self.assertEqual(data.errors, [])

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
        err = self.expect_error(
            ValueError,
            widget.extract,
            {'NUMBER': '10.0'}
        )
        self.assertEqual(str(err), 'Datatype not allowed: "invalid"')

        # Extract invalid integer input
        widget = factory(
            'number',
            name='NUMBER',
            props={
                'datatype': 'integer'
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
                'datatype': 'int'
            })
        data = widget.extract({'NUMBER': '0'})
        self.assertEqual(data.extracted, 0)

        # Persist
        widget = factory(
            'number',
            name='NUMBER',
            props={
                'datatype': 'int'
            })
        data = widget.extract({'NUMBER': '0'})
        model = dict()
        data.persist_writer = write_mapping_writer
        data.write(model)
        self.assertEqual(model, {'NUMBER': 0})
