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

    suite = unittest.TestSuite()

    suite.addTest(unittest.findTestCases(test_base))
    suite.addTest(unittest.findTestCases(test_common))
    suite.addTest(unittest.findTestCases(test_compound))

    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(test_suite())
