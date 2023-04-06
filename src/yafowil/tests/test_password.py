from node.utils import UNSET
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.persistence import write_mapping_writer
from yafowil.tests import YafowilTestCase


class TestPassword(YafowilTestCase):

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
