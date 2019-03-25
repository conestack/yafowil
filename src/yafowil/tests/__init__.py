from __future__ import print_function
from node.tests import NodeTestCase
from yafowil.base import factory
from yafowil.compat import IS_PY2
import lxml.etree as etree
import sys
import unittest
import yafowil.common
import yafowil.compound
import yafowil.persistence
import yafowil.table


if not IS_PY2:
    from importlib import reload


class YafowilTestCase(NodeTestCase):

    def setUp(self):
        super(YafowilTestCase, self).setUp()
        factory.clear()
        reload(yafowil.persistence)
        reload(yafowil.common)
        reload(yafowil.compound)
        reload(yafowil.table)


def fxml(xml):
    et = etree.fromstring(xml)
    return etree.tostring(et, pretty_print=True).decode('utf-8')


def pxml(xml):
    print(fxml(xml))


def test_suite():
    from yafowil.tests import test_base
    from yafowil.tests import test_common
    from yafowil.tests import test_compound
    from yafowil.tests import test_controller
    from yafowil.tests import test_persistence
    from yafowil.tests import test_resources
    from yafowil.tests import test_table
    from yafowil.tests import test_tsf
    from yafowil.tests import test_utils

    suite = unittest.TestSuite()

    suite.addTest(unittest.findTestCases(test_base))
    suite.addTest(unittest.findTestCases(test_common))
    suite.addTest(unittest.findTestCases(test_compound))
    suite.addTest(unittest.findTestCases(test_controller))
    suite.addTest(unittest.findTestCases(test_persistence))
    suite.addTest(unittest.findTestCases(test_resources))
    suite.addTest(unittest.findTestCases(test_table))
    suite.addTest(unittest.findTestCases(test_tsf))
    suite.addTest(unittest.findTestCases(test_utils))

    return suite


def run_tests():
    from zope.testrunner.runner import Runner

    runner = Runner(found_suites=[test_suite()])
    runner.run()
    sys.exit(int(runner.failed))


if __name__ == '__main__':
    run_tests()
