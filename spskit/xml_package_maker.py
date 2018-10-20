# coding: utf-8


from qa.sps_qa import SPSPackageQA


class XMLPackageManager:

    def __init__(self, configuration):
        self.configuration = configuration
        self.qa = SPSPackageQA(configuration)

    def validate_package(self, pkg_file_path, destination_path, delete):
        package, outputs = self.qa.validate_package(pkg_file_path, destination_path, delete)
