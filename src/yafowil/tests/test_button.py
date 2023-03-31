from yafowil.base import factory
from yafowil.tests import YafowilTestCase


class TestButton(YafowilTestCase):

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
                'expression': lambda w, d: False,
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

    def test_button_blueprint(self):
        # Render button element
        widget = factory(
            'button',
            name='SAVE',
            props={
                'action': True,
                'text': 'Button text',
            })
        self.assertEqual(
            widget(),
            '<button id="input-SAVE" name="action.SAVE" type="submit">'
            'Button text</button>'
        )

        # If expression is or evaluates to False, skip rendering
        widget = factory(
            'button',
            name='SAVE',
            props={
                'action': True,
                'text': 'Button text',
                'expression': False,
            })
        self.assertEqual(widget(), '')

        widget = factory(
            'button',
            name='SAVE',
            props={
                'action': True,
                'text': 'Button text',
                'expression': lambda w, d: False,
            })
        self.assertEqual(widget(), '')

        # Generic HTML5 Data
        widget = factory(
            'button',
            name='SAVE',
            props={
                'action': True,
                'text': 'Button text',
                'data': {'foo': 'bar'},
            })
        self.assertEqual(
            widget(),
            """<button data-foo='bar' id="input-SAVE" name="action.SAVE" """
            """type="submit">Button text</button>"""
        )

        # Button specific attrs
        widget = factory(
            'button',
            name='SAVE',
            props={
                'action': True,
                'text': 'Button text',
                'form': 'my-parent-for',
                'formaction': 'alternative-action',
                'formenctype': 'text/plain',
                'formmethod': 'post',
                'formnovalidate': "1",
                'formtarget': "_blank",
            })
        self.assertEqual(
            widget(),
            '<button form="my-parent-for" formaction="alternative-action" '
            'formenctype="text/plain" formmethod="post" formnovalidate="1" '
            'formtarget="_blank" id="input-SAVE" name="action.SAVE" '
            'type="submit">Button text</button>'
        )

        # Custom button name if action not defined
        widget = factory(
            'button',
            name='BUTTON',
            props={
                'text': 'Button text',
                'action': False,
                'name': 'custom_button_action'
            })
        self.assertEqual(
            widget(),
            '<button id="input-BUTTON" name="custom_button_action" '
            'type="submit">Button text</button>'
        )
