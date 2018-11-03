# coding: utf-8
from spskit.utils.xml_utils import ValidatedXML


class StructureValidator:

    def __init__(self, configuration):
        self.configuration = configuration

    def validate(self, article_data, xml_filepath, report_file_path):
        content = ''
        with open(xml_filepath, 'rb') as f:
            content = f.read().decode('utf-8')

        validated_xml = ValidatedXML(content)
        content = ''
        if len(validated_xml.errors) > 0:
            content = '\n'.join(validated_xml.errors)
            content += '\n' + validated_xml.display(True)
        with open(report_file_path, 'wb') as f:
            f.write(content.encode('utf-8'))
        return len(content) == 0
