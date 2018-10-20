# coding: utf-8
"""
XC
usa SPSPackageQA para obter um pacote validado
usa JournalArticlesDataValidator para validar os dados de artigos e journal no contexto de pacote (incluindo os já registrados)
usa RegistrationManager para validar os dados de artigos e journal considerando as regras de gestão da coleção.
"""


from qa.sps_qa import SPSPackageQA
from registration.registration_manager import RegistrationManager


class XMLConverter:

    def __init__(self, configuration):
        self.configuration = configuration
        self.qa = SPSPackageQA(configuration)
        self.registration_manager = RegistrationManager(configuration)

    def register_package(self, pkg_file_path, destination_path, delete):
        package, ouputs = self.qa.validate_package(pkg_file_path, destination_path, delete)
        report_data = self.registration_manager.register(package)
