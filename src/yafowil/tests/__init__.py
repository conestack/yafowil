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