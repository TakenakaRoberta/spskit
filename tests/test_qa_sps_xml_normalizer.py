import unittest
import os

from spskit.qa.sps_xml_normalizer import SPSXMLNormalizer
from spskit.utils.xml_utils import XML


def fun(x):
    return x + 1


class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(fun(3), 4)


class SPSXMLNormalizerTest(unittest.TestCase):

    def setUp(self):
        self.normalizer = SPSXMLNormalizer({})

    def test_SetupPipe(self):
        input_content = '<?xml version="1.0" encoding="utf-8"?>\n<article></article>'
        expected = '<?xml version="1.0" encoding="utf-8"?><article/>'
        result = self.normalizer.SetupPipe().transform(input_content)
        self.assertEqual(result[0], input_content)
        self.assertEqual(result[1].text, expected)

    def test_EndPipe(self):
        expected = '<?xml version="1.0" encoding="utf-8"?><article/>'
        xml = XML(expected)
        result = self.normalizer.EndPipe().transform(('<article/>', xml))
        self.assertEqual(result, expected)
