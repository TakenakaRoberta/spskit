import unittest
import os


from spskit.qa.structure_validator import StructureValidator


THIS_PATH = os.path.dirname(os.path.abspath(__file__))


class StructureValidatorTest(unittest.TestCase):

    def _write_xml(self, content):
        with open('file.xml', 'wb') as f:
            f.write(content.encode('utf-8'))

    def _read_file(self, file_path):
        with open(file_path, 'rb') as f:
            content = f.read().decode('utf-8')
        return content

    def setUp(self):
        self.validator = StructureValidator({})
        self.xml_filepath = 'file.xml'
        self.report_file_path = 'file.txt'

    def tearDown(self):
        for f in ['file.xml', 'file.txt']:
            if os.path.isfile(f):
                os.unlink(f)

    def test_validate_with_error(self):
        article_data = '1.8'
        self._write_xml('<article>')
        result = self.validator.validate(article_data, self.xml_filepath, self.report_file_path)
        report_content = self._read_file(self.report_file_path)
        self.assertIn(
            'Premature end of data in tag article line 1',
            report_content
        )
        self.assertFalse(result)

    def test_validate_valid(self):
        xml = '<article specific-use="1.8"/>'
        article_data = '1.8'
        self._write_xml(xml)
        result = self.validator.validate(article_data, self.xml_filepath, self.report_file_path)
        report_content = self._read_file(self.report_file_path)
        self.assertTrue(result)
        self.assertEqual(report_content, '')
