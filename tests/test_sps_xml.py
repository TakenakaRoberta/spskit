import unittest

from spskit.sps.sps_xml import SPSXML
from spskit.utils.xml_utils import XML


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
        xml = XML(input_content)
        result = self.sps_xml.SetupPipe().transform(xml)
        self.assertEqual(result[0], xml)
        self.assertEqual(result[1], xml)
