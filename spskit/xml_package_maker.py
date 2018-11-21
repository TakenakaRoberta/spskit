# coding: utf-8

import sys
import argparse
from .mkp2xml.mkp2sps import SGMLXML2SPSXML
from .qa.sps_qa import SPSPackageQA
from .frontdesk import evaluate_xml_path, display_text


_ = display_text


def execute_xpm(xml, configuration, outputs_path):
    sgmlxml_file_path, xml_list, errors = evaluate_xml_path(xml)
    if len(errors) > 0:
        return False, errors

    if sgmlxml_file_path is not None:
        sgmxml2xml = SGMLXML2SPSXML(configuration)
        pkg_file_path, outputs_path = sgmxml2xml.make(
            sgmlxml_file_path, inputs.acron)

    xpm = XMLPackageManager(configuration)
    xpm.validate_package(pkg_file_path, outputs_path, delete=False)
    return True, outputs_path


class XMLPackageManager:

    def __init__(self, configuration):
        self.configuration = configuration
        self.qa = SPSPackageQA(configuration)

    def validate_package(self, pkg_file_path, outputs_path, delete):
        package, outputs = self.qa.validate_package(
            pkg_file_path, outputs_path, delete)


if __name__ == '__main__':
    # script, xml_path, acron, INTERATIVE, GENERATE_PMC = read_inputs(args)

    if len(sys.argv) == 1:
        print('Abrir formulario para escolher XML')
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument('xml')
        parser.add_argument('acron', nargs='?')
        parser.add_argument('-auto', action="store_true", default=False)
        parser.add_argument('-pmc', action="store_true", default=False)

        inputs = parser.parse_args()
        result, outputs = execute_xpm(inputs.xml, configuration, outputs_path)
        if result is False:
            print('\n'.join(outputs))
        else:
            print(outputs)
