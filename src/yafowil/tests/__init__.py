import lxml.etree as etree
import unittest


def fxml(xml):
    et = etree.fromstring(xml)
    return etree.tostring(et, pretty_print=True)


def pxml(xml):
    print fxml(xml)


def test_suite():
    from yafowil.tests import test_base
    from yafowil.tests import test_common
    from yafowil.tests import test_compound
    from yafowil.tests import test_controller
    from yafowil.tests import test_persistence
    from yafowil.tests import test_resources
    from yafowil.tests import test_table
    from yafowil.tests import test_tsf

    suite = unittest.TestSuite()

    suite.addTest(unittest.findTestCases(test_base))
    suite.addTest(unittest.findTestCases(test_common))
    suite.addTest(unittest.findTestCases(test_compound))
    suite.addTest(unittest.findTestCases(test_controller))
    suite.addTest(unittest.findTestCases(test_persistence))
    suite.addTest(unittest.findTestCases(test_resources))
    suite.addTest(unittest.findTestCases(test_table))
    suite.addTest(unittest.findTestCases(test_tsf))

    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(test_suite())
