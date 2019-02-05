import unittest
import os

import spskit.frontdesk.reception as reception
from spskit.sps.document_data import DocumentData
from spskit.utils.files_utils import FileInfo
from spskit.utils.xml_utils import XML


TEST_PATH = os.path.dirname(os.path.abspath(__file__))
PKG_PATH = os.path.join(TEST_PATH, 'fixtures/markup_xml/scielo_package')
FIXTURES_PATH = os.path.dirname(os.path.abspath(__file__))


class GetDocumentPackagesTest(unittest.TestCase):

    def get_file_info_items(self, files):
        return [FileInfo(f) for f in files]

    def test_package_file_1(self):
        xml_file_path = os.path.join(PKG_PATH, '0034-8910-rsp-48-01-0001.xml')
        xml_related_files = [
            os.path.join(PKG_PATH, '0034-8910-rsp-48-01-0001.pdf'),
            os.path.join(PKG_PATH, '0034-8910-rsp-48-01-0001-en.pdf'),
        ]
        xml_pkg_items = [
            {
                'xml_file': xml_file_path,
                'related_files': xml_related_files,
            }
        ]
        article_pkg_items = reception.get_document_packages(xml_pkg_items)
        result = article_pkg_items
        xml = XML(xml_file_path)
        expected = [
            {
                'name': '0034-8910-rsp-48-01-0001',
                'xml_file': xml_file_path,
                'content': xml.text,
                'xml': xml,
                'data': DocumentData(xml, 'name'),
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
            result[0]['xml'].text, expected[0]['xml'].text)
        self.assertIsInstance(
            result[0]['data'], DocumentData)


class GetXMLPackagesTest(unittest.TestCase):

    def get_file_info_items(self, files):
        return [FileInfo(f) for f in files]

    def test_package_file_1(self):
        files = ['abc-1234.xml', 'abc-1234-gf01.jpg', 'abc-1234.pdf',
                 'abc-1234-es.pdf', 'a01.sgm.xml']
        xml_pkg, invalid_files = reception.get_xml_packages(
            self.get_file_info_items(files))
        result = xml_pkg
        expected = [
            {'xml_file': 'abc-1234.xml',
             'name': 'abc-1234',
             'related_files':
                ['abc-1234-gf01.jpg', 'abc-1234.pdf', 'abc-1234-es.pdf']}]
        self.assertEqual(result, expected)

        result = invalid_files
        expected = ['a01.sgm.xml']
        self.assertEqual(result, expected)

    def test_package_file_2(self):
        files = ['abc-1234.xml', 'abc-1234-gf01.jpg', 'abc-1234.pdf',
                 'abc-1234-es.pdf']
        xml_pkg, invalid_files = reception.get_xml_packages(
            self.get_file_info_items(files))
        result = xml_pkg
        expected = [
            {'xml_file': 'abc-1234.xml',
             'name': 'abc-1234',
             'related_files':
                ['abc-1234-gf01.jpg', 'abc-1234.pdf', 'abc-1234-es.pdf']}]
        self.assertEqual(result, expected)

        result = invalid_files
        expected = []
        self.assertEqual(result, expected)

    def test_package_file_3(self):
        files = ['abc-1234.xml', 'abc-1234-gf01.jpg', 'abc-1234.pdf',
                 'abc-1234-es.pdf',
                 'abc-1235.xml', 'abc-1235-gf01.jpg', 'abc-1235-gf02.jpg',
                 'abc-1236.xml', 'abc-1236-gf01.jpg', 'abc-1236.pdf',
                 'tubm', 'tubm.txt']
        xml_pkg, invalid_files = reception.get_xml_packages(
            self.get_file_info_items(files))
        result = xml_pkg
        expected = [
            {'xml_file': 'abc-1234.xml',
             'name': 'abc-1234',
             'related_files':
                ['abc-1234-gf01.jpg', 'abc-1234.pdf', 'abc-1234-es.pdf']},
            {'xml_file': 'abc-1235.xml',
             'name': 'abc-1235',
             'related_files':
                ['abc-1235-gf01.jpg', 'abc-1235-gf02.jpg']},
            {'xml_file': 'abc-1236.xml',
             'name': 'abc-1236',
             'related_files':
                ['abc-1236-gf01.jpg', 'abc-1236.pdf']},
        ]
        self.assertEqual(result, expected)

        result = invalid_files
        expected = ['tubm', 'tubm.txt']
        self.assertEqual(result, expected)

    def test_package_file_4(self):
        files = ['abc-1234-gf01.jpg', 'abc-1234.pdf', 'abc-1234-es.pdf']
        xml_pkg, invalid_files = reception.get_xml_packages(
            self.get_file_info_items(files))
        result = xml_pkg
        expected = []
        self.assertEqual(result, expected)

        result = invalid_files
        expected = ['abc-1234-gf01.jpg', 'abc-1234.pdf', 'abc-1234-es.pdf']
        self.assertEqual(result, expected)
