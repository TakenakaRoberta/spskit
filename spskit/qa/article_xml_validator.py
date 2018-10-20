# coding: utf-8
from qa.assets_validator import AssetsValidator
from qa.structure_validator import StructureValidator
from qa.style_validator import StyleValidator
from qa.visual_validator import VisualValidator


class ArticleXMLValidator:

    def __init__(self, configuration):
        self.configuration = configuration
        self.assets_validator = AssetsValidator(self.configuration)
        self.dtd_validator = StructureValidator(self.configuration)
        self.style_validator = StyleValidator(self.configuration)
        self.html_validator = VisualValidator(self.configuration)

    def validate(self, article_data, xml_filepath, xml_assets, report_files):
        self.dtd_validator.validate(xml_filepath, report_files.dtd_report_filename)
        self.assets_validator.validate(article_data, xml_filepath, xml_assets, report_files.err_filename)
        self.style_validator.validate(xml_filepath, report_files.style_report_filename)
        self.html_validator.validate(xml_filepath, xml_assets, report_files.filename_html)
