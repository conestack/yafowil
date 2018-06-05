from node.utils import UNSET
from odict import odict
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.tests import YafowilTestCase
from yafowil.tests import fxml
import yafowil.common
import yafowil.compound
import yafowil.table  # noqa


class TestTable(YafowilTestCase):
    # Table elements are available as blueprints, often one wanta to
    # organize form elements inside a table, providing pretty looking forms

    def test_table_blueprint(self):
        table = factory(
            'table',
            name='foo')
        self.assertEqual(table(), '<table></table>')

        table = factory(
            'table',
            name='foo_table',
            props={
                'id': 'id',
                'class': 'css'
            })
        self.assertEqual(table(), '<table class="css" id="id"></table>')

        table = factory(
            'table',
            name='foo',
            mode='display')
        self.assertEqual(table(), '<table></table>')

    def test_thead_blueprint(self):
        thead = factory(
            'thead',
            name='foo')
        self.assertEqual(thead(), '<thead></thead>')

        thead = factory(
            'thead',
            name='foo',
            mode='display')
        self.assertEqual(thead(), '<thead></thead>')

    def test_tbody_blueprint(self):
        tbody = factory(
            'tbody',
            name='foo')
        self.assertEqual(tbody(), '<tbody></tbody>')

        tbody = factory(
            'tbody',
            name='foo',
            mode='display')
        self.assertEqual(tbody(), '<tbody></tbody>')

    def test_tr_blueprint(self):
        tr = factory(
            'tr',
            name='foo')
        self.assertEqual(tr(), '<tr></tr>')

        tr = factory(
            'tr',
            name='foo',
            mode='display')
        self.assertEqual(tr(), '<tr></tr>')

        tr = factory(
            'tr',
            name='foo',
            props={
                'id': 'id',
                'class': 'css'
            })
        self.assertEqual(tr(), '<tr class="css" id="id"></tr>')

    def test_th_blueprint(self):
        th = factory(
            'th',
            name='foo')
        self.assertEqual(th(), '<th></th>')

        th = factory(
            'th',
            name='foo',
            mode='display')
        self.assertEqual(th(), '<th></th>')

        th = factory(
            'th',
            name='foo',
            props={
                'id': 'id',
                'class': 'css',
                'colspan': 2,
                'rowspan': 2,
            })
        self.assertEqual(
            th(),
            '<th class="css" colspan="2" id="id" rowspan="2"></th>'
        )

    def test_td_blueprint(self):
        td = factory(
            'td',
            name='foo')
        self.assertEqual(td(), '<td></td>')

        td = factory(
            'td',
            name='foo',
            mode='display')
        self.assertEqual(td(), '<td></td>')

        td = factory(
            'td',
            name='foo',
            props={
                'id': 'id',
                'class': 'css',
                'colspan': 2,
                'rowspan': 2,
            })
        self.assertEqual(
            td(),
            '<td class="css" colspan="2" id="id" rowspan="2"></td>'
        )

    def test_render_table(self):
        form = factory(
            'form',
            name='myform',
            props={
                'action': 'myaction',
            })
        form['table'] = factory('table')
        form['table']['row1'] = factory('tr')
        form['table']['row1']['field1'] = factory(
            'td:text',
            name='field1')
        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform"
              method="post" novalidate="novalidate">
          <table>
            <tr>
              <td>
                <input class="text" id="input-myform-table-row1-field1"
                       name="myform.table.row1.field1" type="text" value=""/>
              </td>
            </tr>
          </table>
        </form>
        """, fxml(form()))

    def test_table_with_structural(self):
        # Build same table again but set some nodes structural. This is
        # considered in ``Widget.dottedpath``
        form = factory(
            'form',
            name='mytableform',
            props={
                'action': 'mytableaction',
            })
        form['table'] = factory(
            'table',
            props={
                'structural': True
            })
        form['table']['row1'] = factory(
            'tr',
            props={
                'structural': True
            })
        # note: td is used in a blueprint chain here
        form['table']['row1']['field1'] = factory(
            'td:error:text',
            props={
                'required': 'Field 1 is required',
            }
        )
        self.check_output("""
        <form action="mytableaction" enctype="multipart/form-data"
              id="form-mytableform" method="post" novalidate="novalidate">
          <table>
            <tr>
              <td>
                <input class="required text" id="input-mytableform-field1"
                       name="mytableform.field1" required="required"
                       type="text" value=""/>
              </td>
            </tr>
          </table>
        </form>
        """, fxml(form()))

        data = form.extract({})
        self.assertEqual(data.name, 'mytableform')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, odict([('field1', UNSET)]))
        self.assertEqual(data.errors, [])

        field_data = data['field1']
        self.assertEqual(field_data.name, 'field1')
        self.assertEqual(field_data.value, UNSET)
        self.assertEqual(field_data.extracted, UNSET)
        self.assertEqual(field_data.errors, [])

        data = form.extract({'mytableform.field1': ''})
        self.assertEqual(data.name, 'mytableform')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, odict([('field1', '')]))
        self.assertEqual(data.errors, [])
        self.assertTrue(data.has_errors)

        field_data = data['field1']
        self.assertEqual(field_data.name, 'field1')
        self.assertEqual(field_data.value, UNSET)
        self.assertEqual(field_data.extracted, '')
        self.assertEqual(field_data.errors, [
            ExtractionError('Field 1 is required')
        ])

        self.check_output("""
        <form action="mytableaction" enctype="multipart/form-data"
              id="form-mytableform" method="post" novalidate="novalidate">
          <table>
            <tr>
              <td>
                <div class="error">
                  <div class="errormessage">Field 1 is required</div>
                  <input class="required text" id="input-mytableform-field1"
                         name="mytableform.field1" required="required"
                         type="text" value=""/>
                </div>
              </td>
            </tr>
          </table>
        </form>
        """, fxml(form(data)))

    def test_table_with_compound_td(self):
        # Create table with 'td' as compound
        form = factory(
            'form',
            name='mytableform',
            props={
                'action': 'mytableaction',
            })
        form['table'] = factory(
            'table',
            props={
                'structural': True
            })
        form['table']['row1'] = factory(
            'tr',
            props={
                'structural': True
            })
        form['table']['row1']['td1'] = factory(
            'td',
            props={
                'structural': True
            })
        form['table']['row1']['td1']['field1'] = factory(
            'error:text',
            props={
                'required': 'Field 1 is required',
            }
        )
        self.check_output("""
        <form action="mytableaction" enctype="multipart/form-data"
              id="form-mytableform" method="post" novalidate="novalidate">
          <table>
            <tr>
              <td>
                <input class="required text" id="input-mytableform-field1"
                       name="mytableform.field1" required="required"
                       type="text" value=""/>
              </td>
            </tr>
          </table>
        </form>
        """, fxml(form()))

        data = form.extract({})
        self.assertEqual(data.name, 'mytableform')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, odict([('field1', UNSET)]))
        self.assertEqual(data.errors, [])

        field_data = data['field1']
        self.assertEqual(field_data.name, 'field1')
        self.assertEqual(field_data.value, UNSET)
        self.assertEqual(field_data.extracted, UNSET)
        self.assertEqual(field_data.errors, [])

        data = form.extract({'mytableform.field1': ''})
        self.assertEqual(data.name, 'mytableform')
        self.assertEqual(data.value, UNSET)
        self.assertEqual(data.extracted, odict([('field1', '')]))
        self.assertEqual(data.errors, [])
        self.assertTrue(data.has_errors)

        field_data = data['field1']
        self.assertEqual(field_data.name, 'field1')
        self.assertEqual(field_data.value, UNSET)
        self.assertEqual(field_data.extracted, '')
        self.assertEqual(field_data.errors, [
            ExtractionError('Field 1 is required')
        ])

        self.check_output("""
        <form action="mytableaction" enctype="multipart/form-data"
              id="form-mytableform" method="post" novalidate="novalidate">
          <table>
            <tr>
              <td>
                <div class="error">
                  <div class="errormessage">Field 1 is required</div>
                  <input class="required text" id="input-mytableform-field1"
                         name="mytableform.field1" required="required"
                         type="text" value=""/>
                </div>
              </td>
            </tr>
          </table>
        </form>
        """, fxml(form(data)))
