from node.tests import NodeTestCase
from unittest import mock
from yafowil import tsf
from yafowil.tsf import DummyTranslationStringFactory
import importlib
import os
import sys
import types


def fake_module(name, **attrs):
    module = types.ModuleType(name)
    module.__dict__.update(attrs)
    return module


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

    def tsf_outside_test_run(self, modules):
        """Reload ``yafowil.tsf`` without ``TESTRUN_MARKER`` and with
        ``modules`` patched into ``sys.modules``, return the chosen ``TSF``.
        """
        environ = {
            key: value for key, value in os.environ.items()
            if key != 'TESTRUN_MARKER'
        }
        try:
            with mock.patch.dict(os.environ, environ, clear=True), \
                    mock.patch.dict(sys.modules, modules):
                importlib.reload(tsf)
                return tsf.TSF
        finally:
            importlib.reload(tsf)

    def test_tsf_outside_test_run_prefers_pyramid(self):
        factory = mock.Mock()
        self.assertIs(self.tsf_outside_test_run({
            'pyramid': fake_module('pyramid'),
            'pyramid.i18n': fake_module(
                'pyramid.i18n',
                TranslationStringFactory=factory
            )
        }), factory)

    def test_tsf_outside_test_run_falls_back_to_zope(self):
        factory = mock.Mock()
        self.assertIs(self.tsf_outside_test_run({
            'pyramid.i18n': None,
            'zope.i18nmessageid': fake_module(
                'zope.i18nmessageid',
                MessageFactory=factory
            )
        }), factory)

    def test_tsf_outside_test_run_falls_back_to_dummy(self):
        factory = self.tsf_outside_test_run({
            'pyramid.i18n': None,
            'zope.i18nmessageid': None
        })
        self.assertEqual(factory.__name__, 'DummyTranslationStringFactory')
