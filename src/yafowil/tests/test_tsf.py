from node.tests import NodeTestCase
from yafowil.tsf import DummyTranslationStringFactory


class TestTsf(NodeTestCase):

    def test_tsf(self):
        # Test dummy translation string factory
        _ = DummyTranslationStringFactory('yafowil')
        self.assertEqual(_.domain, 'yafowil')
        self.assertEqual(_('foo'), 'foo')
        self.assertEqual(_('bar', default=u'Bar'), 'Bar')
        self.assertEqual(
            _('baz', default=u'Baz ${bam}', mapping={'bam': 42}),
            'Baz 42'
        )
