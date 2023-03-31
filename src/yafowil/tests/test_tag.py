from yafowil.base import factory
from yafowil.tests import YafowilTestCase


class TestTag(YafowilTestCase):

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
