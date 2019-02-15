# coding: utf-8
"""
XC
usa SPSPackageQA para obter um pacote validado
usa JournalArticlesDataValidator para validar os dados de artigos e journal no contexto de pacote (incluindo os já registrados)
usa RegistrationManager para validar os dados de artigos e journal considerando as regras de gestão da coleção.
"""
import os
import sys
import argparse


from spskit.qa.sps_qa import SPSPackageQA
from spskit.registration.registration_manager import RegistrationManager


class XMLConverter:

    def __init__(self, configuration):
        self.configuration = configuration
        self.qa = SPSPackageQA(configuration)
        self.registration_manager = RegistrationManager(configuration)

    def register_package(self, pkg_file_path, outputs_path, delete):
        package, ouputs = self.qa.validate_package(pkg_file_path, outputs_path, delete)
        report_data = self.registration_manager.register(package)


def get_valid_argument():
    if os.path.isdir('config') and \
       len([f for f in os.listdir('config') if f.endswith('.xc.ini')]) > 0:
        return 'collection'
    return 'xml_package'


if __name__ == '__main__':
    # script, xml_path, acron, INTERATIVE, GENERATE_PMC = read_inputs(args)

    if len(sys.argv) == 1:
        print('Abrir formulario para escolher XML')
    else:

        argument_name = get_valid_argument()
        parser = argparse.ArgumentParser()

        parser.add_argument(argument_name, nargs='?')

        inputs = parser.parse_args()
        if inputs.xml:
            print('input.xml')

        elif inputs.collection:
            print('inputs.collection')

        else:
            print('else')
