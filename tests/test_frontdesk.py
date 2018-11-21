import unittest
import os

from spskit import frontdesk


_ = frontdesk.display_text


THIS_PATH = os.path.dirname(os.path.abspath(__file__))
FIXTURES_PATH = os.path.join(THIS_PATH, 'fixtures')


class EvaluateXMLPathTest(unittest.TestCase):

    def setUp(self):
        self.txt_filename = os.path.join(FIXTURES_PATH, '0034-8910-rsp-48-01-0001.en.html')
        self.sgml_filename = os.path.join(FIXTURES_PATH, '0034-8910-rsp-48-01-0001.sgm.xml')
        self.xml_filename = os.path.join(FIXTURES_PATH, '0034-8910-rsp-48-01-0001.xml')

    def test_missing_xml_location(self):
        sgm_xml, xml_list, error = frontdesk.evaluate_xml_path(None)
        self.assertEqual(error, _('Missing XML location. '))
        self.assertIsNone(xml_list)
        self.assertIsNone(sgm_xml)

    def test_sgml_filename(self):
        sgm_xml, xml_list, error = frontdesk.evaluate_xml_path(
            self.sgml_filename)
        self.assertIsNone(xml_list)
        self.assertIsNone(error)
        self.assertEqual(self.sgml_filename, sgm_xml)

    def test_xml_filename(self):
        sgm_xml, xml_list, error = frontdesk.evaluate_xml_path(
            self.xml_filename)
        self.assertEqual(xml_list, [os.path.join(FIXTURES_PATH, '0034-8910-rsp-48-01-0001.xml')])
        self.assertIsNone(sgm_xml)
        self.assertIsNone(error)

    def test_required_xml_file(self):
        sgm_xml, xml_list, error = frontdesk.evaluate_xml_path(
            self.txt_filename)
        self.assertIsNone(sgm_xml)
        self.assertIsNone(xml_list)
        self.assertEqual(
            error,
            _('Invalid file. XML file required. '))

    def test_invalid_folder(self):
        sgm_xml, xml_list, error = frontdesk.evaluate_xml_path(
            os.path.join(FIXTURES_PATH, 'invalid_folder'))
        self.assertIsNone(sgm_xml)
        self.assertEqual(xml_list, [])
        self.assertEqual(
            error,
            _('Invalid folder. Folder must have XML files. ')
        )

    def test_xml_list(self):
        sgm_xml, xml_list, error = frontdesk.evaluate_xml_path(FIXTURES_PATH)
        self.assertIsNone(sgm_xml)
        self.assertEqual(xml_list, [self.xml_filename])
        self.assertIsNone(error)

    def test_invalid_location(self):
        sgm_xml, xml_list, error = frontdesk.evaluate_xml_path('unknown')
        self.assertIsNone(sgm_xml)
        self.assertIsNone(xml_list)
        self.assertEqual(
            error,
            _('Invalid XML location. ')
        )
