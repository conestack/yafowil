from odict import odict
from node.utils import UNSET
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.controller import Controller
from yafowil.tests import YafowilTestCase
from yafowil.tests import fxml
from yafowil.utils import Tag
import yafowil.common
import yafowil.compound # noqa


###############################################################################
# Helpers
###############################################################################

tag = Tag(lambda msg: msg)


###############################################################################
# Tests
###############################################################################

class TestCompound(YafowilTestCase):

    def test_compound_blueprint_value_via_compound(self):
        # Render Compound with values set via compound widget
        value = {
            'inner': 'Value 1 from parent',
            'inner2': 'Value 2 from parent',
        }
        compound = factory(
            'compound',
            name='COMPOUND',
            value=value)
        compound['inner'] = factory('text')
        compound['inner2'] = factory(
            'text',
            props={
                'required': True
            })
        self.check_output("""
        <div>
          <input class="text" id="input-COMPOUND-inner" name="COMPOUND.inner"
                 type="text" value="Value 1 from parent"/>
          <input class="required text" id="input-COMPOUND-inner2"
                 name="COMPOUND.inner2" required="required" type="text"
                 value="Value 2 from parent"/>
        </div>
        """, fxml(tag('div', compound())))

    def test_compound_blueprint_value_via_members(self):
        # Render Compound with values set via compound members
        compound = factory(
            'compound',
            name='COMPOUND')
        compound['inner'] = factory(
            'text',
            value='value1')
        compound['inner2'] = factory(
            'error:text',
            value='value2',
            props={
                'required': True
            })
        self.check_output("""
        <div>
          <input class="text" id="input-COMPOUND-inner" name="COMPOUND.inner"
                 type="text" value="value1"/>
          <input class="required text" id="input-COMPOUND-inner2"
                 name="COMPOUND.inner2" required="required" type="text"
                 value="value2"/>
        </div>
        """, fxml(tag('div', compound())))

    def test_compound_blueprint_value_conflict(self):
        # ValueError if value for a compound member is defined both
        value = {'inner': 'Value 1 from parent'}
        compound = factory(
            'compound',
            name='COMPOUND',
            value=value)
        compound['inner'] = factory(
            'text',
            value='value1')
        err = self.expect_error(
            ValueError,
            compound
        )
        msg = "Both compound and compound member provide a value for 'inner'"
        self.assertEqual(str(err), msg)

    def test_compound_blueprint_extraction(self):
        compound = factory('compound', name='COMPOUND')
        compound['inner'] = factory('text', value='value1')
        compound['inner2'] = factory(
            'error:text',
            value='value2',
            props={
                'required': True
            })

        # Extract Compound with empty request
        data = compound.extract({})
        self.assertEqual(data.name, 'COMPOUND')
        self.assertEqual(data.value, UNSET)
        expected = odict()
        expected['inner'] = UNSET
        expected['inner2'] = UNSET
        self.assertEqual(data.extracted, expected)
        self.assertEqual(data.errors, [])

        inner_data = data['inner']
        self.assertEqual(inner_data.name, 'inner')
        self.assertEqual(inner_data.value, 'value1')
        self.assertEqual(inner_data.extracted, UNSET)
        self.assertEqual(inner_data.errors, [])

        # Extract with a value in request
        request = {
            'COMPOUND.inner': 'newvalue',
            'COMPOUND.inner2': '',
        }
        data = compound.extract(request)
        data_inner = data['inner']
        self.assertEqual(data_inner.name, 'inner')
        self.assertEqual(data_inner.value, 'value1')
        self.assertEqual(data_inner.extracted, 'newvalue')
        self.assertEqual(data_inner.errors, [])

        data_inner2 = data['inner2']
        self.assertEqual(data_inner2.name, 'inner2')
        self.assertEqual(data_inner2.value, 'value2')
        self.assertEqual(data_inner2.extracted, '')
        self.assertEqual(
            data_inner2.errors,
            [ExtractionError('Mandatory field was empty')]
        )

        expected = odict()
        expected['inner'] = 'newvalue'
        expected['inner2'] = ''
        self.assertEqual(data.extracted, expected)

        self.check_output("""
        <div>
          <input class="text" id="input-COMPOUND-inner" name="COMPOUND.inner"
                 type="text" value="newvalue"/>
          <div class="error">
            <div class="errormessage">Mandatory field was empty</div>
            <input class="required text" id="input-COMPOUND-inner2"
                   name="COMPOUND.inner2" required="required"
                   type="text" value=""/>
          </div>
        </div>
        """, fxml('<div>' + compound(data=data) + '</div>'))

    def test_compound_blueprint_display_rendering(self):
        # Compound display renderers, same as edit renderers
        compound = factory(
            'compound',
            name='COMPOUND',
            mode='display')
        self.assertEqual(tag('div', compound()), '<div></div>')

    def test_compound_blueprint_structural_children(self):
        # Compound with structural compound as child
        value = {
            'inner': 'Value 1 from parent',
            'inner2': 'Value 2 from parent',
        }
        compound = factory(
            'compound',
            name='COMPOUND',
            value=value)
        structural = compound['STRUCTURAL'] = factory(
            'compound',
            props={
                'structural': True
            })
        structural['inner'] = factory('text')
        structural['inner2'] = factory(
            'text',
            props={
                'required': True
            })
        self.check_output("""
        <div>
          <input class="text" id="input-COMPOUND-inner" name="COMPOUND.inner"
                 type="text" value="Value 1 from parent"/>
          <input class="required text" id="input-COMPOUND-inner2"
                 name="COMPOUND.inner2" required="required" type="text"
                 value="Value 2 from parent"/>
        </div>
        """, fxml(tag('div', compound())))

        self.assertEqual(compound.treerepr().split('\n'), [
            "<class 'yafowil.base.Widget'>: COMPOUND",
            "  <class 'yafowil.base.Widget'>: STRUCTURAL",
            "    <class 'yafowil.base.Widget'>: inner",
            "    <class 'yafowil.base.Widget'>: inner2",
            ""
        ])

        data = compound.extract({
            'COMPOUND.inner': 'newvalue',
            'COMPOUND.inner2': '',
        })
        self.assertEqual(data.name, 'COMPOUND')
        self.assertEqual(data.value, {
            'inner2': 'Value 2 from parent',
            'inner': 'Value 1 from parent'
        })
        expected = odict()
        expected['inner'] = 'newvalue'
        expected['inner2'] = ''
        self.assertEqual(data.extracted, expected)

        data_inner = data['inner']
        self.assertEqual(data_inner.name, 'inner')
        self.assertEqual(data_inner.value, 'Value 1 from parent')
        self.assertEqual(data_inner.extracted, 'newvalue')
        self.assertEqual(data_inner.errors, [])

        data_inner2 = data['inner2']
        self.assertEqual(data_inner2.name, 'inner2')
        self.assertEqual(data_inner2.value, 'Value 2 from parent')
        self.assertEqual(data_inner2.extracted, '')
        self.assertEqual(
            data_inner2.errors,
            [ExtractionError('Mandatory field was empty')]
        )

    def test_compound_blueprint_compound_children(self):
        # Compound with compound as child
        value = {
            'CHILD_COMPOUND': {
                'inner': 'Value 1 from parent',
                'inner2': 'Value 2 from parent',
            }
        }
        compound = factory(
            'compound',
            name='COMPOUND',
            value=value)
        child_compound = compound['CHILD_COMPOUND'] = factory('compound')
        child_compound['inner'] = factory('text')
        child_compound['inner2'] = factory(
            'text',
            props={
                'required': True
            })
        self.check_output("""
        <div>
          <input class="text" id="input-COMPOUND-CHILD_COMPOUND-inner"
                 name="COMPOUND.CHILD_COMPOUND.inner" type="text"
                 value="Value 1 from parent"/>
          <input class="required text" id="input-COMPOUND-CHILD_COMPOUND-inner2"
                 name="COMPOUND.CHILD_COMPOUND.inner2" required="required"
                 type="text" value="Value 2 from parent"/>
        </div>
        """, fxml(tag('div', compound())))  # noqa

        self.assertEqual(compound.treerepr().split('\n'), [
            "<class 'yafowil.base.Widget'>: COMPOUND",
            "  <class 'yafowil.base.Widget'>: CHILD_COMPOUND",
            "    <class 'yafowil.base.Widget'>: inner",
            "    <class 'yafowil.base.Widget'>: inner2",
            ""
        ])

        data = compound.extract({
            'COMPOUND.CHILD_COMPOUND.inner': 'newvalue',
            'COMPOUND.CHILD_COMPOUND.inner2': 'newvalue2',
        })
        self.assertEqual(data.name, 'COMPOUND')
        self.assertEqual(data.value, {
            'CHILD_COMPOUND': {
                'inner2': 'Value 2 from parent',
                'inner': 'Value 1 from parent'
            }
        })
        expected = odict()
        expected['CHILD_COMPOUND'] = odict()
        expected['CHILD_COMPOUND']['inner'] = 'newvalue'
        expected['CHILD_COMPOUND']['inner2'] = 'newvalue2'
        self.assertEqual(data.extracted, expected)
        self.assertEqual(data.errors, [])

        data_compound = data['CHILD_COMPOUND']
        self.assertEqual(data_compound.name, 'CHILD_COMPOUND')
        self.assertEqual(data_compound.value, {
            'inner2': 'Value 2 from parent',
            'inner': 'Value 1 from parent'
        })
        expected = odict()
        expected['inner'] = 'newvalue'
        expected['inner2'] = 'newvalue2'
        self.assertEqual(data_compound.extracted, expected)
        self.assertEqual(data_compound.errors, [])

        data_inner = data['CHILD_COMPOUND']['inner']
        self.assertEqual(data_inner.name, 'inner')
        self.assertEqual(data_inner.value, 'Value 1 from parent')
        self.assertEqual(data_inner.extracted, 'newvalue')
        self.assertEqual(data_inner.errors, [])

        data_inner2 = data['CHILD_COMPOUND']['inner2']
        self.assertEqual(data_inner2.name, 'inner2')
        self.assertEqual(data_inner2.value, 'Value 2 from parent')
        self.assertEqual(data_inner2.extracted, 'newvalue2')
        self.assertEqual(data_inner2.errors, [])

    def test_compound_blueprint_structural_and_compound_children(self):
        # Compound with structural compound with compound as children
        value = {
            'CHILD_COMPOUND': {
                'inner': 'Value 1 from parent',
                'inner2': 'Value 2 from parent',
            }
        }
        compound = factory(
            'compound',
            name='COMPOUND',
            value=value)
        structural = compound['STRUCTURAL'] = factory(
            'compound',
            props={
                'structural': True
            })
        child_compound = structural['CHILD_COMPOUND'] = factory('compound')
        child_compound['inner'] = factory('text')
        child_compound['inner2'] = factory(
            'text',
            props={
                'required': True
            })
        self.check_output("""
        <div>
          <input class="text" id="input-COMPOUND-CHILD_COMPOUND-inner"
                 name="COMPOUND.CHILD_COMPOUND.inner" type="text"
                 value="Value 1 from parent"/>
          <input class="required text" id="input-COMPOUND-CHILD_COMPOUND-inner2"
                 name="COMPOUND.CHILD_COMPOUND.inner2" required="required"
                 type="text" value="Value 2 from parent"/>
        </div>
        """, fxml(tag('div', compound())))  # noqa

        self.assertEqual(compound.treerepr().split('\n'), [
            "<class 'yafowil.base.Widget'>: COMPOUND",
            "  <class 'yafowil.base.Widget'>: STRUCTURAL",
            "    <class 'yafowil.base.Widget'>: CHILD_COMPOUND",
            "      <class 'yafowil.base.Widget'>: inner",
            "      <class 'yafowil.base.Widget'>: inner2",
            ""
        ])
        self.assertEqual(
            compound['STRUCTURAL'].attrs.storage,
            {'structural': True}
        )
        self.assertEqual(
            compound['STRUCTURAL']['CHILD_COMPOUND'].attrs.storage,
            {}
        )

        data = compound.extract({
            'COMPOUND.CHILD_COMPOUND.inner': 'newvalue',
            'COMPOUND.CHILD_COMPOUND.inner2': 'newvalue2',
        })
        self.assertEqual(data.name, 'COMPOUND')
        self.assertEqual(data.value, {
            'CHILD_COMPOUND': {
                'inner2': 'Value 2 from parent',
                'inner': 'Value 1 from parent'
            }
        })
        expected = odict()
        expected['CHILD_COMPOUND'] = odict()
        expected['CHILD_COMPOUND']['inner'] = 'newvalue'
        expected['CHILD_COMPOUND']['inner2'] = 'newvalue2'
        self.assertEqual(data.extracted, expected)
        self.assertEqual(data.errors, [])

        data_compound = data['CHILD_COMPOUND']
        self.assertEqual(data_compound.name, 'CHILD_COMPOUND')
        self.assertEqual(data_compound.value, {
            'inner2': 'Value 2 from parent',
            'inner': 'Value 1 from parent'
        })
        expected = odict()
        expected['inner'] = 'newvalue'
        expected['inner2'] = 'newvalue2'
        self.assertEqual(data_compound.extracted, expected)
        self.assertEqual(data_compound.errors, [])

        data_inner = data['CHILD_COMPOUND']['inner']
        self.assertEqual(data_inner.name, 'inner')
        self.assertEqual(data_inner.value, 'Value 1 from parent')
        self.assertEqual(data_inner.extracted, 'newvalue')
        self.assertEqual(data_inner.errors, [])

        data_inner2 = data['CHILD_COMPOUND']['inner2']
        self.assertEqual(data_inner2.name, 'inner2')
        self.assertEqual(data_inner2.value, 'Value 2 from parent')
        self.assertEqual(data_inner2.extracted, 'newvalue2')
        self.assertEqual(data_inner2.errors, [])

    def test_compound_blueprint_address_compound_value_parent(self):
        # Address different compounds with value on parent
        value = {
            'c1': {
                'f1': 'Foo',
            },
            'c2': {
                'f2': 'Bar',
                'f3': 'Baz',
            },
        }
        compound = factory(
            'compound',
            'comp',
            value=value)
        compound['c1'] = factory('compound')
        compound['c1']['f1'] = factory('text')
        compound['c2'] = factory('compound')
        compound['c2']['f2'] = factory('text')
        compound['c2']['f3'] = factory('text')
        compound['c3'] = factory('compound')
        compound['c3']['f4'] = factory('text')

        self.check_output("""
        <div>
          <input class="text" id="input-comp-c1-f1" name="comp.c1.f1"
                 type="text" value="Foo"/>
          <input class="text" id="input-comp-c2-f2" name="comp.c2.f2"
                 type="text" value="Bar"/>
          <input class="text" id="input-comp-c2-f3" name="comp.c2.f3"
                 type="text" value="Baz"/>
          <input class="text" id="input-comp-c3-f4" name="comp.c3.f4"
                 type="text" value=""/>
        </div>
        """, fxml(tag('div', compound())))

        self.assertEqual(compound.treerepr().split('\n'), [
            "<class 'yafowil.base.Widget'>: comp",
            "  <class 'yafowil.base.Widget'>: c1",
            "    <class 'yafowil.base.Widget'>: f1",
            "  <class 'yafowil.base.Widget'>: c2",
            "    <class 'yafowil.base.Widget'>: f2",
            "    <class 'yafowil.base.Widget'>: f3",
            "  <class 'yafowil.base.Widget'>: c3",
            "    <class 'yafowil.base.Widget'>: f4",
            ""
        ])

        data = compound.extract({
            'comp.c1.f1': 'Foo 1',
            'comp.c2.f2': 'Bar 2',
            'comp.c2.f3': 'Baz 1',
        })
        self.assertEqual(data.name, 'comp')
        self.assertEqual(data.value, {
            'c2': {
                'f2': 'Bar',
                'f3': 'Baz'
            },
            'c1': {
                'f1': 'Foo'
            }
        })
        expected = odict()
        expected['c1'] = odict()
        expected['c1']['f1'] = 'Foo 1'
        expected['c2'] = odict()
        expected['c2']['f2'] = 'Bar 2'
        expected['c2']['f3'] = 'Baz 1'
        expected['c3'] = odict()
        expected['c3']['f4'] = UNSET
        self.assertEqual(data.extracted, expected)
        self.assertEqual(data.errors, [])

        # c1
        data_c1 = data['c1']
        self.assertEqual(data_c1.name, 'c1')
        self.assertEqual(data_c1.value, {'f1': 'Foo'})
        expected = odict()
        expected['f1'] = 'Foo 1'
        self.assertEqual(data_c1.extracted, expected)
        self.assertEqual(data_c1.errors, [])

        data_f1 = data['c1']['f1']
        self.assertEqual(data_f1.name, 'f1')
        self.assertEqual(data_f1.value, 'Foo')
        self.assertEqual(data_f1.extracted, 'Foo 1')
        self.assertEqual(data_f1.errors, [])

        # c2
        data_c2 = data['c2']
        self.assertEqual(data_c2.name, 'c2')
        self.assertEqual(data_c2.value, {
            'f2': 'Bar',
            'f3': 'Baz'
        })
        expected = odict()
        expected['f2'] = 'Bar 2'
        expected['f3'] = 'Baz 1'
        self.assertEqual(data_c2.extracted, expected)
        self.assertEqual(data_c2.errors, [])

        data_f2 = data['c2']['f2']
        self.assertEqual(data_f2.name, 'f2')
        self.assertEqual(data_f2.value, 'Bar')
        self.assertEqual(data_f2.extracted, 'Bar 2')
        self.assertEqual(data_f2.errors, [])

        data_f3 = data['c2']['f3']
        self.assertEqual(data_f3.name, 'f3')
        self.assertEqual(data_f3.value, 'Baz')
        self.assertEqual(data_f3.extracted, 'Baz 1')
        self.assertEqual(data_f3.errors, [])

        # c3
        data_c3 = data['c3']
        self.assertEqual(data_c3.name, 'c3')
        self.assertEqual(data_c3.value, UNSET)
        expected = odict()
        expected['f4'] = UNSET
        self.assertEqual(data_c3.extracted, expected)
        self.assertEqual(data_c3.errors, [])

        data_f4 = data['c3']['f4']
        self.assertEqual(data_f4.name, 'f4')
        self.assertEqual(data_f4.value, UNSET)
        self.assertEqual(data_f4.extracted, UNSET)
        self.assertEqual(data_f4.errors, [])

    def test_compound_blueprint_value_callbacks(self):
        # Check compound with value callbacks
        def val(widget, data):
            return 'val F1'
        value = {
            'f1': val,
        }
        compound = factory(
            'compound',
            'comp',
            value=value)
        compound['f1'] = factory('text')
        self.assertEqual(compound(), (
            '<input class="text" id="input-comp-f1" name="comp.f1" '
            'type="text" value="val F1" />'
        ))

        data = compound.extract({'comp.f1': 'New val 1'})
        self.assertEqual(data.name, 'comp')
        self.assertEqual(data.value, {'f1': val})
        expected = odict()
        expected['f1'] = 'New val 1'
        self.assertEqual(data.extracted, expected)
        self.assertEqual(data.errors, [])

        def value(widget, data):
            return {
                'f1': 'F1 Val'
            }
        compound = factory(
            'compound',
            'comp',
            value=value)
        compound['f1'] = factory('text')
        self.assertEqual(compound(), (
            '<input class="text" id="input-comp-f1" name="comp.f1" '
            'type="text" value="F1 Val" />'
        ))

        data = compound.extract({'comp.f1': 'New val 1'})
        self.assertEqual(data.name, 'comp')
        self.assertEqual(data.value, {'f1': 'F1 Val'})
        expected = odict()
        expected['f1'] = 'New val 1'
        self.assertEqual(data.extracted, expected)
        self.assertEqual(data.errors, [])

    def test_div_blueprint_compound(self):
        # Div blueprint as compound
        div = factory(
            'div',
            name='DIV_COMPOUND')
        div['inner'] = factory(
            'text',
            value='value1')
        div['inner2'] = factory(
            'text',
            value='value2',
            props={
                'required': True
            })
        self.check_output("""
        <div>
          <input class="text" id="input-DIV_COMPOUND-inner"
                 name="DIV_COMPOUND.inner" type="text" value="value1"/>
          <input class="required text" id="input-DIV_COMPOUND-inner2"
                 name="DIV_COMPOUND.inner2" required="required" type="text"
                 value="value2"/>
        </div>
        """, fxml(div()))

        data = div.extract({
            'DIV_COMPOUND.inner': '1',
            'DIV_COMPOUND.inner2': '2',
        })
        self.assertEqual(data.name, 'DIV_COMPOUND')
        self.assertEqual(data.value, UNSET)
        expected = odict()
        expected['inner'] = '1'
        expected['inner2'] = '2'
        self.assertEqual(data.extracted, expected)
        self.assertEqual(data.errors, [])

        data_inner = data['inner']
        self.assertEqual(data_inner.name, 'inner')
        self.assertEqual(data_inner.value, 'value1')
        self.assertEqual(data_inner.extracted, '1')
        self.assertEqual(data_inner.errors, [])

        data_inner2 = data['inner2']
        self.assertEqual(data_inner2.name, 'inner2')
        self.assertEqual(data_inner2.value, 'value2')
        self.assertEqual(data_inner2.extracted, '2')
        self.assertEqual(data_inner2.errors, [])

    def test_div_blueprint_compound_leaf(self):
        # Div blueprint as compound, but with ``leaf`` property set. Causes
        # ``hybrid_renderer`` and ``hybrid_extractor`` to skip auto delegating
        # to ``compound_renderer`` and ``compound_extractor``
        div = factory(
            'div',
            name='DIV_COMPOUND_LEAF',
            props={
                'leaf': True
            })
        div['inner'] = factory(
            'text',
            value='value1')
        div['inner2'] = factory(
            'text',
            value='value2',
            props={
                'required': True
            })
        self.assertEqual(div(), '<div></div>')

        data = div.extract({
            'DIV_COMPOUND_LEAF.inner': '1',
            'DIV_COMPOUND_LEAF.inner2': '2',
        })
        self.assertEqual(data.name, 'DIV_COMPOUND_LEAF')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, UNSET)
        self.assertEqual(data.errors, [])
        self.assertEqual(data.keys(), [])

    def test_div_blueprint_as_leaf(self):
        # Div blueprint as leaf
        input = factory(
            'div:text',
            name='DIV',
            value='1')
        self.check_output("""
        <div>
          <input class="text" id="input-DIV" name="DIV"
                 type="text" value="1"/>
        </div>
        """, fxml(input()))

        data = input.extract({
            'DIV': '2',
        })
        self.assertEqual(data.name, 'DIV')
        self.assertEqual(data.value, '1')
        self.assertEqual(data.extracted, '2')
        self.assertEqual(data.errors, [])

        # Empty div
        input = factory(
            'div',
            name='DIV')
        self.assertEqual(input(), '<div></div>')

        # Div with data attributes
        input = factory(
            'div',
            name='DIV',
            props={
                'data': {
                    'foo': 'bar'
                }
            })
        self.assertEqual(input(), "<div data-foo='bar'></div>")

        # Display mode
        div = factory(
            'div',
            name='DIV',
            props={
                'class': 'foo'
            },
            mode='display')
        self.assertEqual(div(), '<div class="foo"></div>')

        input = factory(
            'div:text',
            name='DIV',
            value='1',
            mode='display')
        self.check_output("""
        <div>
          <div class="display-text" id="display-DIV">1</div>
        </div>
        """, fxml(input()))

    def test_fieldset_blueprint(self):
        compound = factory(
            'fieldset',
            'COMPOUND',
            props={
                'legend': 'Some Test'
            })
        compound['inner'] = factory('text', 'inner', 'value')
        compound['inner2'] = factory('text', 'inner2', 'value2')
        self.check_output("""
        <fieldset id="fieldset-COMPOUND">
          <legend>Some Test</legend>
          <input class="text" id="input-COMPOUND-inner" name="COMPOUND.inner"
                 type="text" value="value"/>
          <input class="text" id="input-COMPOUND-inner2" name="COMPOUND.inner2"
                 type="text" value="value2"/>
        </fieldset>
        """, fxml(compound()))

        # Structural fieldset renders without id attribute
        compound = factory(
            'fieldset',
            'COMPOUND',
            props={
                'structural': True
            })
        self.assertEqual(compound(), '<fieldset></fieldset>')

        # Fieldset display renderers are the same as fieldset edit renderers
        compound = factory(
            'fieldset',
            'COMPOUND',
            props={
                'legend': 'Some Test'
            },
            mode='display')
        self.check_output("""
        <fieldset id="fieldset-COMPOUND">
          <legend>Some Test</legend>
        </fieldset>
        """, fxml(compound()))

    def test_form_blueprint(self):
        # Test Form
        form = factory(
            'form',
            name='FORM',
            props={
                'action': 'http://fubar.com'
            })
        self.assertEqual(form(), (
            '<form action="http://fubar.com" enctype="multipart/form-data" '
            'id="form-FORM" method="post" novalidate="novalidate"></form>'
        ))

        # Form action as callable
        def action(widget, data):
            return 'http://fubar.com'

        form = factory(
            'form',
            name='FORM',
            props={
                'action': action
            })
        self.assertEqual(form(), (
            '<form action="http://fubar.com" enctype="multipart/form-data" '
            'id="form-FORM" method="post" novalidate="novalidate"></form>'
        ))

        # Form display renderer
        form = factory(
            'form',
            name='FORM',
            props={
                'action': 'http://fubar.com'
            },
            mode='display')
        self.assertEqual(form(), '<div></div>')

        # Create a form with some children
        form = factory(
            'form',
            name='myform',
            props={
                'action': 'http://www.domain.tld/someform'
            })
        form['someinput'] = factory(
            'label:text',
            props={
                'label': 'Your Text'
            })

        self.form_data = None

        def formaction(widget, data):
            self.form_data = data

        def formnext(request):
            return 'http://www.domain.tld/result'

        form['submit'] = factory(
            'submit',
            props={
                'handler': formaction,
                'next': formnext,
                'action': True
            })

        # Render an empty form
        self.check_output("""
        <form action="http://www.domain.tld/someform"
              enctype="multipart/form-data" id="form-myform" method="post"
              novalidate="novalidate">
          <label for="input-myform-someinput">Your Text</label>
          <input class="text" id="input-myform-someinput"
                 name="myform.someinput" type="text" value=""/>
          <input id="input-myform-submit" name="action.myform.submit"
                 type="submit" value="submit"/>
        </form>
        """, fxml(form()))

        # Get form data out of request (request is expected dict-like)
        request = {
            'myform.someinput': 'Hello World',
            'action.myform.submit': 'submit'
        }
        Controller(form, request)

        form_data = self.form_data
        self.assertEqual(form_data.name, 'myform')
        self.assertEqual(form_data.value, UNSET)
        expected = odict()
        expected['someinput'] = 'Hello World'
        expected['submit'] = UNSET
        self.assertEqual(form_data.extracted, expected)
        self.assertEqual(form_data.errors, [])

        input_data = form_data['someinput']
        self.assertEqual(input_data.name, 'someinput')
        self.assertEqual(input_data.value, UNSET)
        self.assertEqual(input_data.extracted, 'Hello World')
        self.assertEqual(input_data.errors, [])

        # submit blueprint gets a runtime data as well, but it's never needed
        # or used so far
        submit_data = form_data['submit']
        self.assertEqual(submit_data.name, 'submit')
        self.assertEqual(submit_data.value, UNSET)
        self.assertEqual(submit_data.extracted, UNSET)
        self.assertEqual(submit_data.errors, [])

        del self.form_data

        # Form action property can be callable
        def action(widget, data):
            return 'actionfromcall'

        form = factory(
            'form',
            name='form',
            props={
                'action': action,
            })
        self.assertEqual(form(), (
            '<form action="actionfromcall" enctype="multipart/form-data" '
            'id="form-form" method="post" novalidate="novalidate"></form>'
        ))

        # Create label for field in other compound
        form = factory(
            'form',
            name='form',
            props={
                'action': 'action'
            })
        form['label'] = factory(
            'label',
            props={
                'label': 'Foo',
                'for': 'field'
            })
        form['field'] = factory('text')
        self.check_output("""
        <form action="action" enctype="multipart/form-data" id="form-form"
              method="post" novalidate="novalidate">
          <label for="input-form-field">Foo</label>
          <input class="text" id="input-form-field" name="form.field"
                 type="text" value=""/>
        </form>
        """, fxml(form()))
