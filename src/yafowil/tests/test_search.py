from node.utils import UNSET
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.tests import YafowilTestCase


class TestSearch(YafowilTestCase):

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
