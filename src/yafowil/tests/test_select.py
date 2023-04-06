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


class TestSelect(YafowilTestCase):

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
        self.checkOutput("""
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

        self.checkOutput("""
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
        self.checkOutput("""
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
        self.checkOutput("""
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
        self.checkOutput("""
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

        self.checkOutput("""
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
        self.checkOutput("""
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
        self.checkOutput("""
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
                'datatype': int
            })
        self.checkOutput("""
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

        self.checkOutput("""
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
        self.checkOutput("""
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
        self.checkOutput("""
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
        self.checkOutput("""
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

        self.checkOutput("""
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
        self.checkOutput("""
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
        self.checkOutput("""
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
        self.checkOutput("""
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
        self.checkOutput("""
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
        self.checkOutput("""
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
        self.checkOutput("""
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

        self.checkOutput("""
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
                'datatype': uuid.UUID,
                'format': 'single',
            })
        self.checkOutput("""
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

        self.checkOutput("""
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
        self.checkOutput("""
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
        self.checkOutput("""
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
        self.checkOutput("""
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
        self.checkOutput("""
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

        self.checkOutput("""
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
        self.checkOutput("""
        <ul class="display-select" id="display-MYSELECT">
          <li>One</li>
          <li>Two</li>
        </ul>
        """, fxml(widget()))

        # Multi selection display mode with display proxy
        widget.attrs['display_proxy'] = True
        self.checkOutput("""
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

        self.checkOutput("""
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
        self.checkOutput("""
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
        self.checkOutput("""
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
        with self.assertRaises(ValueError) as arc:
            widget()
        self.assertEqual(
            str(arc.exception),
            'Multiple values for single selection.'
        )

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
                'datatype': float,
                'multivalued': True,
                'vocabulary': vocab,
                'emptyvalue': []
            })
        self.checkOutput("""
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

        self.checkOutput("""
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
        self.checkOutput("""
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
        self.checkOutput("""
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
        self.checkOutput("""
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
        self.checkOutput("""
        <ul class="display-select" id="display-MYSELECT">
          <li>One</li>
        </ul>
        """, fxml(widget()))

        # Checkbox multi selection display mode with display proxy
        widget.attrs['display_proxy'] = True
        self.checkOutput("""
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

        self.checkOutput("""
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
        self.checkOutput("""
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
        self.checkOutput("""
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
        self.checkOutput("""
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
        self.checkOutput("""
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
        self.checkOutput("""
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
        self.checkOutput("""
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
        self.checkOutput("""
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
        self.checkOutput("""
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
