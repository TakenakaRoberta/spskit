import unittest
import os

from spskit.sps.pkg_files import PackageFiles


FIXTURES_PATH = os.path.dirname(os.path.abspath(__file__))


class PackageFilesTest(unittest.TestCase):

    def test_package_file_1(self):
        files = ['abc-1234.xml', 'abc-1234-gf01.jpg', 'abc-1234.pdf',
                 'abc-1234-es.pdf', 'a01.sgm.xml']
        pkg_files = PackageFiles(files)
        result = pkg_files.articles_files
        expected = [
            {'xml': 'abc-1234.xml',
             'related_files':
                ['abc-1234-gf01.jpg', 'abc-1234.pdf', 'abc-1234-es.pdf']}]
        self.assertEqual(result, expected)

        result = pkg_files.invalid_files
        expected = ['a01.sgm.xml']
        self.assertEqual(result, expected)

    def test_package_file_2(self):
        files = ['abc-1234.xml', 'abc-1234-gf01.jpg', 'abc-1234.pdf',
                 'abc-1234-es.pdf']
        pkg_files = PackageFiles(files)
        result = pkg_files.articles_files
        expected = [
            {'xml': 'abc-1234.xml',
             'related_files':
                ['abc-1234-gf01.jpg', 'abc-1234.pdf', 'abc-1234-es.pdf']}]
        self.assertEqual(result, expected)

        result = pkg_files.invalid_files
        expected = []
        self.assertEqual(result, expected)

    def test_package_file_3(self):
        files = ['abc-1234.xml', 'abc-1234-gf01.jpg', 'abc-1234.pdf',
                 'abc-1234-es.pdf',
                 'abc-1235.xml', 'abc-1235-gf01.jpg', 'abc-1235-gf02.jpg', 
                 'abc-1236.xml', 'abc-1236-gf01.jpg', 'abc-1236.pdf',
                 'tubm', 'tubm.txt']
        pkg_files = PackageFiles(files)
        result = pkg_files.articles_files
        expected = [
            {'xml': 'abc-1234.xml',
             'related_files':
                ['abc-1234-gf01.jpg', 'abc-1234.pdf', 'abc-1234-es.pdf']},
            {'xml': 'abc-1235.xml',
             'related_files':
                ['abc-1235-gf01.jpg', 'abc-1235-gf02.jpg']},
            {'xml': 'abc-1236.xml',
             'related_files':
                ['abc-1236-gf01.jpg', 'abc-1236.pdf']},
        ]
        self.assertEqual(result, expected)

        result = pkg_files.invalid_files
        expected = ['tubm', 'tubm.txt']
        self.assertEqual(result, expected)

    def test_package_file_4(self):
        files = ['abc-1234-gf01.jpg', 'abc-1234.pdf', 'abc-1234-es.pdf']
        pkg_files = PackageFiles(files)
        result = pkg_files.articles_files
        expected = []
        self.assertEqual(result, expected)

        result = pkg_files.invalid_files
        expected = ['abc-1234-gf01.jpg', 'abc-1234.pdf', 'abc-1234-es.pdf']
        self.assertEqual(result, expected)
