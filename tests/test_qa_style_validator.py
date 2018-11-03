import unittest
import os


from spskit.qa.style_validator import StyleValidator


THIS_PATH = os.path.dirname(os.path.abspath(__file__))
FIXTURES_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class StyleValidatorTest(unittest.TestCase):

    def _write_xml(self, content):
        with open('file.xml', 'wb') as f:
            f.write(content.encode('utf-8'))

    def _read_file(self, file_path):
        with open(file_path, 'rb') as f:
            content = f.read().decode('utf-8')
        return content

    def setUp(self):
        self.validator = StyleValidator({})
        self.xml_filepath = 'file.xml'
        self.report_file_path = 'file.txt'

    def tearDown(self):
        for f in ['file.xml', 'file.txt']:
            if os.path.isfile(f):
                os.unlink(f)

    def _validate_with_error(self, xml, error_msg):
        sps_version = '1.8'
        self._write_xml(xml)
        result = self.validator.validate(sps_version, self.xml_filepath, self.report_file_path)
        report_content = self._read_file(self.report_file_path)
        self.assertIn(
            error_msg,
            report_content
        )
        self.assertFalse(result)

    def test_validate_absence_of_sps_version(self):
        xml = '<article/>'
        error_msg = 'cannot get the SPS version from /article/@specific-use'
        self._validate_with_error(xml, error_msg)

    def test_validate_invalid_sps_version_error(self):
        xml = '<article specific-use="1.8"/>'
        error_msg = 'version "1.8" is not currently supported'
        self._validate_with_error(xml, error_msg)

    def test_validate_absence_of_doctype(self):
        xml = '<article specific-use="sps-1.8"/>'
        error_msg = 'cannot get the DOCTYPE declaration'
        self._validate_with_error(xml, error_msg)

    def test_validate_(self):
        xml = '<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.1 20151215//EN" "https://jats.nlm.nih.gov/publishing/1.1/JATS-journalpublishing1.dtd"><article specific-use="sps-1.8"/>'
        error_msg = 'Missing attribute article-type'
        self._validate_with_error(xml, error_msg)


"""
    def test_validate_xml(self):
        xml = self._read_file(THIS_PATH+'/fixtures/0034-8910-rsp-48-01-0001.xml')
        error_msg = 'Missing attribute article-type'
        self._validate_with_error(xml, error_msg)

    def test_validate(self):
        xml = THIS_PATH+'/fixtures/0034-8910-rsp-48-01-0001.xml'
        result = self.validator.validate('1.8', xml, self.report_file_path)
        self.assertTrue(result)
"""
