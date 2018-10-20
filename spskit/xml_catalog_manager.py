# coding: utf-8
"""
XC
usa XMLPackageQA para obter um pacote validado
usa JournalArticlesDataValidator para validar os dados de artigos e journal no contexto de pacote (incluindo os já registrados)
usa RegistrationManager para validar os dados de artigos e journal considerando as regras de gestão da coleção.
"""


from qa.xml_pkg_qa import XMLPackageQA
from registration.registration_manager import RegistrationManager


class XMLCatalogManager:

    def __init__(self, configuration):
        self.configuration = configuration
        self.xml_pkg_qa = XMLPackageQA(configuration)
        self.registration_manager = RegistrationManager(configuration)

    def register_package(self, pkg_file_path, destination_path, delete):
        package = self.xml_pkg_qa.validate_package(pkg_file_path, destination_path, delete)
        self.registration_manager.register(package)
