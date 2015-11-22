# -*- coding: utf-8 -*-
from interlude import interact
from pprint import pprint
import doctest
import lxml.etree as etree
import unittest


optionflags = \
    doctest.NORMALIZE_WHITESPACE | \
    doctest.ELLIPSIS | \
    doctest.REPORT_ONLY_FIRST_FAILURE


TESTFILES = [
    'tsf.rst',
    'utils.rst',
    'base.rst',
    'common.rst',
    'compound.rst',
    'controller.rst',
    'persistence.rst',
    'table.rst',
    'resources.rst',
]


def fxml(xml):
    et = etree.fromstring(xml)
    return etree.tostring(et, pretty_print=True)


def pxml(xml):
    print fxml(xml)


def test_suite():
    return unittest.TestSuite([
        doctest.DocFileSuite(
            filename,
            optionflags=optionflags,
            globs={'interact': interact,
                   'pprint': pprint,
                   'pxml': pxml},
        ) for filename in TESTFILES
    ])


if __name__ == '__main__':                                  #pragma NO COVER
    unittest.main(defaultTest='test_suite')                 #pragma NO COVER
