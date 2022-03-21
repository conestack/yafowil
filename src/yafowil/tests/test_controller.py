from yafowil.base import factory
from yafowil.controller import Controller
from yafowil.tests import fxml
from yafowil.tests import YafowilTestCase
import yafowil.common
import yafowil.compound  # noqa


class TestController(YafowilTestCase):

    def test_controller(self):
        # Dummy context
        class Context(object):
            value = 'hello world'
        context = Context()

        # Dummy getter
        def getter(widget, data):
            return data.request.context.value

        # Create Widget tree
        form = factory(
            u'form',
            name='testform',
            props={
                'action': 'http://fubar.com'
            })
        form['field1'] = factory(
            'text',
            value=getter)
        form['field2'] = factory(
            'text',
            value='',
            props={
                'required': True
            })

        # Define action ``handler``
        def handler(widget, data):
            self.handler_result = 'handler called "%s"' % '.'.join(widget.path)

        # Define action ``next``
        def next(request):
            return 'next return value'

        # Indicate widget to be an ``action`` definition by setting ``action``
        # attribute to widget properties. ``expression``, ``handler`` and
        # ``next`` are action referring properties
        props = {
            'action': 'save',
            'expression': True,
            'handler': handler,
            'next': next,
            'label': 'Save',
            'skip': False,
        }

        # Add save action
        form['save'] = factory('submit', props=props)

        # Add cancel action. In this case we want the form processing to be
        # skipped and just the next action to be performed
        props = {
            'action': 'cancel',
            'expression': True,
            'handler': None,
            'next': next,
            'label': 'Cancel',
            'skip': True,
        }
        form['cancel'] = factory('submit', props=props)

        # Check widget tree
        self.assertEqual(form.treerepr().split('\n'), [
            "<class 'yafowil.base.Widget'>: testform",
            "  <class 'yafowil.base.Widget'>: field1",
            "  <class 'yafowil.base.Widget'>: field2",
            "  <class 'yafowil.base.Widget'>: save",
            "  <class 'yafowil.base.Widget'>: cancel",
            ""
        ])

        # Dummy request
        class Request(dict):
            context = None

        Request.context = context
        request = Request()

        # Render form with empty request
        data = form.extract(request)
        self.checkOutput("""
        <form action="http://fubar.com" enctype="multipart/form-data"
              id="form-testform" method="post" novalidate="novalidate">
          <input class="text" id="input-testform-field1" name="testform.field1"
                 type="text" value="hello world"/>
          <input class="required text" id="input-testform-field2"
                 name="testform.field2" required="required" type="text"
                 value=""/>
          <input id="input-testform-save" name="action.testform.save"
                 type="submit" value="Save"/>
          <input id="input-testform-cancel" name="action.testform.cancel"
                 type="submit" value="Cancel"/>
        </form>
        """, fxml(form(data)))

        # Create controller for form
        controller = Controller(form, request)

        # If action is not triggered, or ``action['next']`` is not set,
        # ``Controller.next`` is ``None``
        self.assertEqual(controller.next, None)

        # An empty request does not trigger validation failures
        self.assertFalse(controller.error)

        # Provide empty required field and it fails!
        request['testform.field2'] = ''
        controller = Controller(form, request)
        self.assertTrue(controller.error)

        # Provide required field and all is fine
        request['testform.field2'] = '1'
        controller = Controller(form, request)
        self.assertFalse(controller.error)

        # Trigger save action without required field
        request['testform.field2'] = ''
        request['action.testform.save'] = '1'
        controller = Controller(form, request)
        self.assertTrue(controller.error, True)
        self.assertTrue(controller.performed, True)

        # Trigger save action with valid input
        request['testform.field2'] = '1'
        controller = Controller(form, request)
        self.assertEqual(self.handler_result, 'handler called "testform"')
        self.handler_result = None
        self.assertEqual(controller.next, 'next return value')
        self.assertFalse(controller.error)
        self.assertTrue(controller.performed)

        # Render the form performed
        self.checkOutput("""
        <form action="http://fubar.com" enctype="multipart/form-data"
              id="form-testform" method="post" novalidate="novalidate">
          <input class="text" id="input-testform-field1" name="testform.field1"
                 type="text" value="hello world"/>
          <input class="required text" id="input-testform-field2"
                 name="testform.field2" required="required" type="text"
                 value="1"/>
          <input id="input-testform-save" name="action.testform.save"
                 type="submit" value="Save"/>
          <input id="input-testform-cancel" name="action.testform.cancel"
                 type="submit" value="Cancel"/>
        </form>
        """, fxml(controller.rendered))

        # Trigger cancel action. performing is skipped
        del request['action.testform.save']
        request['action.testform.cancel'] = '1'
        controller = Controller(form, request)
        self.assertEqual(controller.next, 'next return value')
        self.assertFalse(controller.performed)

        # Render form not performed
        self.checkOutput("""
        <form action="http://fubar.com" enctype="multipart/form-data"
              id="form-testform" method="post" novalidate="novalidate">
          <input class="text" id="input-testform-field1" name="testform.field1"
                 type="text" value="hello world"/>
          <input class="required text" id="input-testform-field2"
                 name="testform.field2" required="required" type="text"
                 value=""/>
          <input id="input-testform-save" name="action.testform.save"
                 type="submit" value="Save"/>
          <input id="input-testform-cancel" name="action.testform.cancel"
                 type="submit" value="Cancel"/>
        </form>
        """, fxml(controller.rendered))

        # Try recursive lookup of actions
        form = factory(
            u'form',
            name='testform',
            props={
                'action': 'http://fubar.com'
            })
        form['level1'] = factory(
            'submit',
            props={
                'action': 'l1action'
            })
        form['fieldset'] = factory('fieldset')
        form['fieldset']['level2'] = factory(
            'submit',
            props={
                'action': 'l2action'
            })
        form['fieldset']['subset'] = factory('fieldset')
        form['fieldset']['subset']['level3'] = factory(
            'submit',
            props={
                'action': 'l3action'
            })
        controller = Controller(form, {})
        self.assertEqual(len(controller.actions), 3)
        self.assertEqual(controller.actions[0].name, 'level1')
        self.assertEqual(controller.actions[1].name, 'level2')
        self.assertEqual(controller.actions[2].name, 'level3')
