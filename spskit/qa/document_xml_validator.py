# coding: utf-8
from spskit.qa.assets_validator import AssetsValidator
from spskit.qa.structure_validator import StructureValidator
from spskit.qa.style_validator import StyleValidator
from spskit.qa.visual_validator import VisualValidator


class DocumentXMLValidator:

    def __init__(self, configuration):
        self.configuration = configuration
        self.assets_validator = AssetsValidator(self.configuration)
        self.dtd_validator = StructureValidator(self.configuration)
        self.style_validator = StyleValidator(self.configuration)
        self.html_validator = VisualValidator(self.configuration)

    def validate(self, article_data, xml_filepath, xml_assets, report_files):
        if self.dtd_validator.validate(
                article_data, xml_filepath, report_files.dtd_report_filename):
            self.assets_validator.validate(
                article_data, xml_filepath, xml_assets, report_files.err_filename)
            self.style_validator.validate(
                article_data, xml_filepath, report_files.style_report_filename)
            self.html_validator.validate(xml_filepath)
