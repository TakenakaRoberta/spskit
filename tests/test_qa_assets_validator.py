import unittest
import os

from spskit.sps.document_data import DocumentData
from spskit.qa.assets_validator import AssetsValidator
from spskit.utils.xml_utils import XML


FIXTURES_PATH = os.path.dirname(os.path.abspath(__file__))


class AssetsValidatorTest(unittest.TestCase):

    def setUp(self):
        xml = '<article lang="pt" xmlns:xlink="http://www.w3.org/1999/xlink"><body><graphic xlink:href="f01.jpg"/><graphic xlink:href="f02.jpg"/></body><sub-article lang="en"/></article>'
        self.xml = XML(xml)
        self.asset_files = ['f01.jpg', 'f02.jpg', 'file.pdf', 'file-en.pdf']
        self.report_path = 'report.txt'
        self.document_data = DocumentData(self.xml, 'file')
        self.validator = AssetsValidator({})

    def test_find_items_in_list(self):
        items = [1, 2, 3]
        _list = [4, 4, 5]
        result = self.validator.find_items_in_list(items, _list)
        expected = [], [1, 2, 3]
        self.assertEqual(result, expected)

    def test_find_items_in_list2(self):
        items = [1, 2, 3]
        _list = [2, 3, 5]
        result = self.validator.find_items_in_list(items, _list)
        expected = [2, 3], [1]
        self.assertEqual(result, expected)

    def test_find_items_in_list3(self):
        items = [4, 5]
        _list = [4, 5]
        result = self.validator.find_items_in_list(items, _list)
        expected = [4, 5], []
        self.assertEqual(result, expected)

    def test_find_items_in_list4(self):
        items = [4, 4, 5]
        _list = [1, 2, 3]
        result = self.validator.find_items_in_list(items, _list)
        expected = [], [4, 4, 5]
        self.assertEqual(result, expected)

    def test_find_items_in_list5(self):
        items = [2, 3, 5]
        _list = [1, 2, 3]
        result = self.validator.find_items_in_list(items, _list)
        expected = [2, 3], [5]
        self.assertEqual(result, expected)

    def test_report_content(self):
        items = ['f01.jpg', 'f02.jpg']
        _list = ['f01.jpg', 'f02.jpg', 'file.pdf', 'file-en.pdf']
        header = 'xlink:href not found'
        result = self.validator.report_content(items, _list, header)
        expected = ''
        self.assertEqual(result, expected)

    def test_report_content2(self):
        items = ['f01.jpg', 'f02.jpg', 'file.pdf', 'file-en.pdf']
        _list = ['f01.jpg', 'f02.jpg']
        header = 'xlink:href not found'
        result = self.validator.report_content(items, _list, header)
        self.assertIn('file.pdf', result)
        self.assertIn('file-en.pdf', result)
