# coding: utf-8
from validations.registration_validator import RegistrationValidator


"""
usa os dados de artigos e journal já registrados
validações de artigos duplicados
gerenciamento de exclusão
gerenciamento de inserção
gerenciamento de artigos relacionados 
gerenciamento de aop
gerenciamento de versões
etc

"""


class Registration:

    def __init__(self, configuration):
        self.registration_service = configuration

    def get(self, data):
        return self.registration_service.get(data)

    def save(self, data):
        return self.registration_service.save(data)


class RegistrationManager:

    def __init__(self, configuration):
        self.configuration = configuration
        self.registration = Registration(configuration)
        self.registration_validator = RegistrationValidator(configuration)

    def register(self, package):
        registered_data = self.registration.get(package)
        data, report = self.registration_validator.validate(package, registered_data)
        self.registration.save(data)
        return report
