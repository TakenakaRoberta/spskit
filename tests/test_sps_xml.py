import unittest

from spskit.sps.sps_xml import SPSXML
from spskit.sps.xml_content import XMLContent


def fun(x):
    return x + 1


class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(fun(3), 4)


class SPSXMLTest(unittest.TestCase):

    def setUp(self):
        self.sps_xml = SPSXML({})

    def test_SetupPipe(self):
        input_content = '<?xml version="1.0" encoding="utf-8"?>\n<article></article>'
        xmlcontent = XMLContent(input_content, 'name')
        result = self.sps_xml.SetupPipe().transform(xmlcontent.xml)
        self.assertEqual(result[0], xmlcontent.xml)
        self.assertEqual(result[1], xmlcontent.xml)
