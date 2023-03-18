from node.tests import NodeTestCase
from yafowil.tsf import DummyTranslationStringFactory


class TestTsf(NodeTestCase):

    def test_tsf(self):
        # Test dummy translation string factory
        tsf = DummyTranslationStringFactory('yafowil')
        self.assertEqual(tsf.domain, 'yafowil')
        self.assertEqual(tsf('foo'), 'foo')
        self.assertEqual(tsf('bar', default=u'Bar'), 'Bar')
        self.assertEqual(
            tsf('baz', default=u'Baz ${bam}', mapping={'bam': 42}),
            'Baz 42'
        )
