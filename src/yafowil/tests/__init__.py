from __future__ import print_function
from importlib import reload
from node.tests import NodeTestCase
from yafowil import button
from yafowil import checkbox
from yafowil import common
from yafowil import compound
from yafowil import datatypes
from yafowil import email
from yafowil import field
from yafowil import file
from yafowil import hidden
from yafowil import lines
from yafowil import number
from yafowil import password
from yafowil import persistence
from yafowil import proxy
from yafowil import search
from yafowil import select
from yafowil import table
from yafowil import tag as tag_module
from yafowil import text
from yafowil import textarea
from yafowil import url
from yafowil.base import factory
from yafowil.utils import Tag
import lxml.etree as etree
import sys
import unittest


class YafowilTestCase(NodeTestCase):

    def setUp(self):
        super(YafowilTestCase, self).setUp()
        factory.push_state()
        factory.clear()
        reload(button)
        reload(checkbox)
        reload(common)
        reload(compound)
        reload(datatypes)
        reload(email)
        reload(field)
        reload(file)
        reload(hidden)
        reload(lines)
        reload(number)
        reload(password)
        reload(persistence)
        reload(proxy)
        reload(search)
        reload(select)
        reload(table)
        reload(tag_module)
        reload(text)
        reload(textarea)
        reload(url)

    def tearDown(self):
        factory.pop_state()
        super(YafowilTestCase, self).tearDown()


def fxml(xml):
    et = etree.fromstring(xml)
    return etree.tostring(et, pretty_print=True).decode('utf-8')


def wrapped_fxml(value):
    return fxml(u'<div>' + value + u'</div>')


tag = Tag(lambda msg: msg)


def test_suite():
    from yafowil.tests import test_base
    from yafowil.tests import test_button
    from yafowil.tests import test_checkbox
    from yafowil.tests import test_common
    from yafowil.tests import test_compound
    from yafowil.tests import test_controller
    from yafowil.tests import test_datatypes
    from yafowil.tests import test_email
    from yafowil.tests import test_field
    from yafowil.tests import test_file
    from yafowil.tests import test_hidden
    from yafowil.tests import test_lines
    from yafowil.tests import test_number
    from yafowil.tests import test_password
    from yafowil.tests import test_persistence
    from yafowil.tests import test_proxy
    from yafowil.tests import test_resources
    from yafowil.tests import test_search
    from yafowil.tests import test_select
    from yafowil.tests import test_table
    from yafowil.tests import test_tag
    from yafowil.tests import test_text
    from yafowil.tests import test_textarea
    from yafowil.tests import test_tsf
    from yafowil.tests import test_url
    from yafowil.tests import test_utils

    suite = unittest.TestSuite()

    suite.addTest(unittest.findTestCases(test_base))
    suite.addTest(unittest.findTestCases(test_button))
    suite.addTest(unittest.findTestCases(test_checkbox))
    suite.addTest(unittest.findTestCases(test_common))
    suite.addTest(unittest.findTestCases(test_compound))
    suite.addTest(unittest.findTestCases(test_controller))
    suite.addTest(unittest.findTestCases(test_datatypes))
    suite.addTest(unittest.findTestCases(test_email))
    suite.addTest(unittest.findTestCases(test_field))
    suite.addTest(unittest.findTestCases(test_file))
    suite.addTest(unittest.findTestCases(test_hidden))
    suite.addTest(unittest.findTestCases(test_lines))
    suite.addTest(unittest.findTestCases(test_number))
    suite.addTest(unittest.findTestCases(test_password))
    suite.addTest(unittest.findTestCases(test_persistence))
    suite.addTest(unittest.findTestCases(test_proxy))
    suite.addTest(unittest.findTestCases(test_resources))
    suite.addTest(unittest.findTestCases(test_search))
    suite.addTest(unittest.findTestCases(test_select))
    suite.addTest(unittest.findTestCases(test_table))
    suite.addTest(unittest.findTestCases(test_tag))
    suite.addTest(unittest.findTestCases(test_text))
    suite.addTest(unittest.findTestCases(test_textarea))
    suite.addTest(unittest.findTestCases(test_tsf))
    suite.addTest(unittest.findTestCases(test_url))
    suite.addTest(unittest.findTestCases(test_utils))

    return suite


def run_tests():
    from zope.testrunner.runner import Runner

    runner = Runner(found_suites=[test_suite()])
    runner.run()
    sys.exit(int(runner.failed))


if __name__ == '__main__':
    run_tests()
