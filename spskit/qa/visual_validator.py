# coding: utf-8
import os

class VisualValidator:

    def __init__(self, configuration):
        self.configuration = configuration

    def validate(self, article_data, xml_filepath, xml_assets, report_file_path):
        cmd = 'htmlgenerator {} {} -js {} -css {}'.format(
                xml_filepath,
                report_file_path,
                self.configuration.get('SITE_JS_PATH', 'js_path'),
                self.configuration.get('SITE_CSS_PATH', 'css_path'),
                self.configuration.get('SITE_PRINT_CSS_PATH', 'print_css_path'),
            )
        os.system(cmd)
