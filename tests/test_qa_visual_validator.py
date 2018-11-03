import unittest
import os

import time
from spskit.utils.files_utils import delete_file_or_folder


from spskit.qa.visual_validator import VisualValidator


FIXTURES_PATH = os.path.dirname(os.path.abspath(__file__))


class VisualValidatorTest(unittest.TestCase):

    def _write_xml(self, content):
        with open('file.xml', 'wb') as f:
            f.write(content.encode('utf-8'))

    def _read_file(self, file_path):
        with open(file_path, 'rb') as f:
            content = f.read().decode('utf-8')
        return content

    def test_gerar_html(self):
        self.validator = VisualValidator({})
        self.xml_filepath = os.path.join(FIXTURES_PATH, 'fixtures/0034-8910-rsp-48-01-0001.xml')
        new_files = self.validator.validate(self.xml_filepath)
        self.assertEqual(
            set(new_files),
            set(
                [os.path.join(FIXTURES_PATH, 'fixtures/0034-8910-rsp-48-01-0001.pt.html'),
                 os.path.join(FIXTURES_PATH, 'fixtures/0034-8910-rsp-48-01-0001.en.html')
                ]
            )
        )
