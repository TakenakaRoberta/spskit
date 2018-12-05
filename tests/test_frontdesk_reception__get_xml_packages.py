import unittest
import os

import spskit.frontdesk.reception as reception
from spskit.utils.files_utils import FileInfo


FIXTURES_PATH = os.path.dirname(os.path.abspath(__file__))


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
