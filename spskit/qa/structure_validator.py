# coding: utf-8
from spskit.utils.xml_utils import ValidatedXML


class StructureValidator:

    def __init__(self, configuration):
        self.configuration = configuration

    def validate(self, article_data, xml_filepath, report_file_path):
        validated_xml = ValidatedXML(open(xml_filepath).read())
        with open(report_file_path, 'w') as f:
            f.write(''.join(validated_xml.errors) + '\n' + validated_xml.display(True))
        return validated_xml
