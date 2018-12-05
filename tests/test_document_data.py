import unittest
import os

from spskit.sps.xml_file import XMLFile
from spskit.sps.xml_content import XMLContent


TEST_PATH = os.path.dirname(os.path.abspath(__file__))
PKG_PATH = os.path.join(TEST_PATH, 'fixtures/markup_xml/scielo_package')

FILE = os.path.join(PKG_PATH, '0034-8910-rsp-48-01-0001.xml')
xml_file = XMLFile(FILE)


class DocumentDataTest(unittest.TestCase):

    def test_document_data_sps_version(self):
        xml_content = '<article specific-use="sps-1.8"/>'
        xml = XMLContent(xml_content, 'name')
        result = xml.document_data.sps_version
        self.assertEqual(result, 'sps-1.8')

    def test_pdf_items(self):
        xml = xml_file
        result = xml.document_data.pdf_items
        self.assertEqual(result, ['0034-8910-rsp-48-01-0001.pdf'])

    def test_node_info(self):
        xml = xml_file
        result = xml.document_data.nodes_info('.//contrib')
        expected = [
            ('/article/front/article-meta/contrib-group/contrib[1]', 1)]
        self.assertEqual(result[0][0], expected[0][0])

    def test_node(self):
        xml = xml_file
        result = xml.document_data.nodes('.//contrib')
        self.assertEqual('Hortale', result[0].findtext('.//surname'))

    def test_xlink_href(self):
        xml = xml_file
        result = xml.document_data.xlink_href
        self.assertIn('http://creativecommons.org/licenses/by-nc/3.0/', result)

    def test_internal_xlink_href(self):
        xml = xml_file
        result = xml.document_data.internal_xlink_href
        self.assertEqual([], result)

    def test_languages(self):
        xml = xml_file
        result = xml.document_data.languages
        self.assertEqual(['en'], result)
