from node.base import AttributedNode
from node.utils import UNSET
from odict import odict
from yafowil.base import factory
from yafowil.persistence import attribute_writer
from yafowil.persistence import node_attribute_writer
from yafowil.persistence import write_mapping_writer
from yafowil.tests import YafowilTestCase
import uuid
import yafowil.loader  # noqa


class TestPersistence(YafowilTestCase):

    def test_persistence(self):
        # Test ``attribute_writer``
        form = factory(
            'form',
            name='form',
            props={
                'persist_writer': attribute_writer
            })
        form['my_field'] = factory(
            'text',
            props={
                'persist': True
            })
        data = form.extract(request={
            'form.my_field': 'value'
        })
        self.assertEqual(data.persist_writer, attribute_writer)

        class AttributeModel(object):
            my_field = UNSET

        model = AttributeModel()
        data.write(model)
        self.assertEqual(model.my_field, 'value')

        # Test ``write_mapping_writer``
        form.attrs['persist_writer'] = write_mapping_writer
        data = form.extract(request={
            'form.my_field': 'value'
        })
        self.assertEqual(data.persist_writer, write_mapping_writer)

        model = dict()
        data.write(model)
        self.assertEqual(sorted(model.items()), [('my_field', 'value')])

        # Test ``node_attribute_writer``
        form.attrs['persist_writer'] = node_attribute_writer
        data = form.extract(request={
            'form.my_field': 'value'
        })
        self.assertEqual(data.persist_writer, node_attribute_writer)

        model = AttributedNode()
        data.write(model)
        self.assertEqual(sorted(model.attrs.items()), [('my_field', 'value')])

        # If ``recursiv`` flag is ``False``, don't dig into child data
        form.attrs['persist_writer'] = write_mapping_writer
        data = form.extract(request={
            'form.my_field': 'value'
        })
        self.checkOutput("""
        <RuntimeData form, value=<UNSET>, extracted=odict(...) at ...>
          <RuntimeData form.my_field, value=<UNSET>, extracted='value' at ...>
        """, data.treerepr())

        model = dict()
        data.write(model, recursiv=False)
        self.assertEqual(sorted(model.items()), [])

        # By default persitence ``target`` is taken from widget ``name``.
        # Widgets can persist to different ``target`` as well
        form['my_field'].attrs['persist_target'] = 'my_other_field'
        data = form.extract(request={
            'form.my_field': 'value'
        })
        model = dict()
        data.write(model)
        self.assertEqual(sorted(model.items()), [('my_other_field', 'value')])

        form['my_field'].attrs['persist_target'] = 'my_field'

        # We can override persist writers for specific widgets
        form['my_other_field'] = factory(
            'text',
            props={
                'persist': True,
                'persist_writer': attribute_writer
            })

        class MixedModel(dict):
            my_other_field = UNSET

        data = form.extract(request={
            'form.my_field': 'value',
            'form.my_other_field': 'other value'
        })
        model = MixedModel()
        data.write(model)

        self.assertEqual(model.my_other_field, 'other value')
        self.assertEqual(sorted(model.items()), [('my_field', 'value')])

        del form['my_other_field']

        # We can also persist extracted from compound
        form['compound'] = factory(
            'compound',
            props={
                'persist': True,
            })
        form['compound']['f1'] = factory(
            'text',
            props={
                'persist': False
            })
        form['compound']['f2'] = factory(
            'text',
            props={
                'persist': False
            })

        data = form.extract(request={
            'form.my_field': 'value',
            'form.compound.f1': 'f1',
            'form.compound.f2': 'f2'
        })
        model = dict()
        data.write(model)
        self.assertEqual(sorted(model.items()), [
            ('compound', odict([('f1', 'f1'), ('f2', 'f2')])),
            ('my_field', 'value')
        ])

        # We can call write on children of runtime data. ``writer`` must be
        # passed in if ``persist_writer`` is not provide via widget
        model = dict()
        with self.assertRaises(ValueError) as arc:
            data['my_field'].write(model)
        self.assertEqual(
            str(arc.exception),
            'No persistence writer found for "form.my_field"'
        )

        data['my_field'].write(model, writer=write_mapping_writer)
        self.assertEqual(sorted(model.items()), [('my_field', 'value')])

        # Structural children work as usual
        del form['compound'].attrs['persist']
        form['compound'].attrs['structural'] = True
        form['compound']['f1'].attrs['persist'] = True
        form['compound']['f2'].attrs['persist'] = True
        data = form.extract(request={
            'form.my_field': 'value',
            'form.compound.f1': 'f1',
            'form.compound.f2': 'f2'
        })
        model = dict()
        data.write(model)
        self.assertEqual(sorted(model.items()), [
            ('f1', 'f1'),
            ('f2', 'f2'),
            ('my_field', 'value')
        ])

        # Widgets with no persis flag set gets ignored
        form['compound']['f2'].attrs['persist'] = False
        data = form.extract(request={
            'form.my_field': 'value',
            'form.compound.f1': 'f1',
            'form.compound.f2': 'f2'
        })
        model = dict()
        data.write(model)
        self.assertEqual(
            sorted(model.items()),
            [('f1', 'f1'), ('my_field', 'value')]
        )

        form['compound']['f2'].attrs['persist'] = True

        # In conjunction with ``datatype`` and ``emptyvalue`` we have fancy
        # convenience for single model bound forms
        form['my_field'].attrs['datatype'] = int
        form['my_field'].attrs['emptyvalue'] = UNSET
        form['compound']['f1'].attrs['datatype'] = float
        form['compound']['f2'].attrs['datatype'] = uuid.UUID

        data = form.extract(request={
            'form.my_field': '',
            'form.compound.f1': '1.0',
            'form.compound.f2': 'c6b19794-dc9e-4a98-920d-182a9ec07b7a'
        })
        model = dict()
        data.write(model)
        self.assertEqual(sorted(model.items()), [
            ('f1', 1.0),
            ('f2', uuid.UUID('c6b19794-dc9e-4a98-920d-182a9ec07b7a')),
            ('my_field', UNSET)
        ])

        # When trying to persist data containing errors we get a runtime error
        data = form.extract(request={
            'form.my_field': '',
            'form.compound.f1': 'a',
            'form.compound.f2': 'c6b19794-dc9e-4a98-920d-182a9ec07b7a'
        })
        self.assertTrue(data.has_errors)

        with self.assertRaises(RuntimeError) as arc:
            data.write(dict())
        msg = 'Attempt to persist data which failed to extract'
        self.assertEqual(str(arc.exception), msg)
