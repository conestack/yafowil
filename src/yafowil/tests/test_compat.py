from node.tests import NodeTestCase
from yafowil import compat
import warnings


class TestCompat(NodeTestCase):

    def deprecated_value(self, name):
        with warnings.catch_warnings(record=True) as log:
            warnings.simplefilter('always')
            value = getattr(compat, name)
        self.assertEqual(len(log), 1)
        self.assertTrue(issubclass(log[0].category, DeprecationWarning))
        self.assertTrue(str(log[0].message).startswith(f'{name}: '))
        return value

    def test_constants(self):
        self.assertFalse(self.deprecated_value('IS_PY2'))
        self.assertIs(self.deprecated_value('BYTES_TYPE'), bytes)
        self.assertIs(self.deprecated_value('STR_TYPE'), str)
        self.assertIs(self.deprecated_value('UNICODE_TYPE'), str)
        self.assertIs(self.deprecated_value('LONG_TYPE'), int)
        self.assertEqual(self.deprecated_value('ITER_TYPES'), (list, tuple))
