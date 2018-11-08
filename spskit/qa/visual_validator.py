# coding: utf-8
import os


class VisualValidator:

    def __init__(self, configuration):
        self.configuration = configuration

    def validate(self, xml_filepath):
        dirname = os.path.dirname(xml_filepath)
        name = os.path.basename(xml_filepath)
        name, ext = os.path.splitext(name)
        files = set(os.listdir(dirname))
        files = [f
                 for f in files
                 if not (f.startswith(name) and f.endswith('.html'))]

        cmd = 'htmlgenerator {}  --nochecks --js {} --css {} --print_css {}'.format(
                xml_filepath,
                self.configuration.get('SITE_JS_PATH', 'js_path'),
                self.configuration.get('SITE_CSS_PATH', 'css_path'),
                self.configuration.get('SITE_PRINT_CSS_PATH', 'print_css_path'),
            )
        os.system(cmd)

        _files = set(os.listdir(dirname))
        new_files = _files - set(files)
        html_files = []
        for f in new_files:
            file_path = os.path.join(dirname, f)
            html_files.append(file_path)
        return html_files
