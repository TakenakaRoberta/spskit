import unittest
import os


from spskit.qa.visual_validator import VisualValidator


FIXTURES_PATH = os.path.dirname(os.path.abspath(__file__))


class VisualValidatorTest(unittest.TestCase):

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
