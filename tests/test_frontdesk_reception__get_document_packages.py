import unittest
import os

import spskit.frontdesk.reception as reception
from spskit.utils.xml_utils import XML
from spskit.utils.files_utils import FileInfo
from spskit.sps.document_data import DocumentData


TEST_PATH = os.path.dirname(os.path.abspath(__file__))
PKG_PATH = os.path.join(TEST_PATH, 'fixtures/markup_xml/scielo_package')


class ArticlePackagesTest(unittest.TestCase):

    def get_file_info_items(self, files):
        return [FileInfo(f) for f in files]

    def test_package_file_1(self):
        xml_file = os.path.join(PKG_PATH, '0034-8910-rsp-48-01-0001.xml')
        xml_related_files = [
            os.path.join(PKG_PATH, '0034-8910-rsp-48-01-0001.pdf'),
            os.path.join(PKG_PATH, '0034-8910-rsp-48-01-0001-en.pdf'),
        ]
        xml_pkg_items = [
            {
                'xml_file': xml_file,
                'related_files': xml_related_files,
            }
        ]
        article_pkg_items = reception.get_document_packages(xml_pkg_items)
        result = article_pkg_items
        with open(xml_file, 'rb') as fp:
            xmlcontent = fp.read().decode('utf-8')
        xml = XML(xmlcontent)
        expected = [
            {
                'xml_file': xml_file,
                'content': xmlcontent,
                'xml': xml,
                'data': DocumentData(xml),
                'related_files': xml_related_files,
                'assets': [],
                'attachments': xml_related_files
            }
        ]
        self.assertEqual(
            result[0]['xml_file'], expected[0]['xml_file'])
        self.assertEqual(
            result[0]['related_files'], expected[0]['related_files'])
        self.assertEqual(
            result[0]['assets'], expected[0]['assets'])
        self.assertEqual(
            result[0]['attachments'], expected[0]['attachments'])
        self.assertEqual(
            result[0]['xml'], expected[0]['xml'])
        self.assertEqual(
            result[0]['content'], expected[0]['content'])
        self.assertEqual(
            result[0]['data'], expected[0]['data'])
