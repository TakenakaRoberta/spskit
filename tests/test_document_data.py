import unittest
import os

from spskit.utils.xml_utils import XML
from spskit.sps.document_data import DocumentData


TEST_PATH = os.path.dirname(os.path.abspath(__file__))
PKG_PATH = os.path.join(TEST_PATH, 'fixtures/markup_xml/scielo_package')

FILE = os.path.join(PKG_PATH, '0034-8910-rsp-48-01-0001.xml')
xml_file = XML(FILE)


class DocumentDataTest(unittest.TestCase):

    def setUp(self):
        self.document_data = DocumentData(xml_file, '0034-8910-rsp-48-01-0001')

    def test_document_data_sps_version(self):
        xml_content = '<article specific-use="sps-1.8"/>'
        xml = XML(xml_content)
        self.assertEqual(DocumentData(xml, 'name').sps_version, 'sps-1.8')

    def test_pdf_items(self):
        result = self.document_data.pdf_items
        self.assertEqual(result, ['0034-8910-rsp-48-01-0001.pdf'])

    def test_node_info(self):
        result = self.document_data.nodes_info('.//contrib')
        expected = [
            ('/article/front/article-meta/contrib-group/contrib[1]', 1)]
        self.assertEqual(result[0][0], expected[0][0])

    def test_node(self):
        result = self.document_data.nodes('.//contrib')
        self.assertEqual('Hortale', result[0].findtext('.//surname'))

    def test_xlink_href(self):
        result = self.document_data.xlink_href
        self.assertIn('http://creativecommons.org/licenses/by-nc/3.0/', result)

    def test_internal_xlink_href(self):
        result = self.document_data.internal_xlink_href
        self.assertEqual([], result)

    def test_languages(self):
        result = self.document_data.languages
        self.assertEqual(['en'], result)
