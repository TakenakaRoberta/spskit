import unittest
import os

import time
from spskit.utils.files_utils import delete_file_or_folder

from spskit.sps.article_data import ArticleData
from spskit.qa.assets_validator import AssetsValidator


FIXTURES_PATH = os.path.dirname(os.path.abspath(__file__))


class AssetsValidatorTest(unittest.TestCase):

    def _write_xml(self, content):
        with open('file.xml', 'wb') as f:
            f.write(content.encode('utf-8'))

    def _read_file(self, file_path):
        with open(file_path, 'rb') as f:
            content = f.read().decode('utf-8')
        return content

    def setUp(self):
        #self.xml = '<article lang="pt"><body><graphic xlink:href="f01.jpg"/><graphic xlink:href="f02.jpg"/></body><sub-article lang="en"/></article>'
        #self.asset_files = ['f01.jpg', 'f02.jpg', 'file.pdf', 'file-en.pdf']
        #self.report_path = 'report.txt'
        self.article_data = ArticleData(self.xml)
        self.validator = AssetsValidator({})

    def test_report_content(self):
        content = self.validator.report_content(
            ['f01.jpg', 'f02.jpg'],
            ['f01.jpg', 'f02.jpg', 'file.pdf', 'file-en.pdf'],
            'xlink:href not found')
        self.assertIn('file.pdf', content)
        self.assertIn('file-en.pdf', content)
        self.assertNotIn('f01.jpg', content)
        self.assertNotIn('f02.jpg', content)
