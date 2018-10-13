# coding: utf-8
from validations.article_xml_validator.assets_validator import AssetsValidator
from validations.article_xml_validator.structure_validator import StructureValidator
from validations.article_xml_validator.style_validator import StyleValidator
from validations.article_xml_validator.visual_validator import VisualValidator


class ArticleXMLValidator:

    def __init__(self, configuration):
        self.configuration = configuration
        self.assets_validator = AssetsValidator(self.configuration)
        self.dtd_validator = StructureValidator(self.configuration)
        self.style_validator = StyleValidator(self.configuration)
        self.html_validator = VisualValidator(self.configuration)

    def validate(self, xml_filepath, xml_assets):
        assets_report = self.assets_validator.validate(xml_filepath, xml_assets)
        dtd_report = self.dtd_validator.validate(xml_filepath)
        style_report = self.style_validator.validate(xml_filepath)
        html_report = self.html_validator.validate(xml_filepath, xml_assets)

        return assets_report, dtd_report, style_report, html_report
