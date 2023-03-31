from node.utils import UNSET
from yafowil.base import factory
from yafowil.persistence import write_mapping_writer
from yafowil.tests import YafowilTestCase
from yafowil.tests import fxml
from yafowil.tests import wrapped_fxml


class TestLines(YafowilTestCase):

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
