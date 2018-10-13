# coding: utf-8

import os
import shutil
import zipfile

from validations.article_data import ArticleData
from validations.article_xml_validator.article_xml_validator import ArticleXMLValidator
from validations.article_data_validator import ArticleDataValidator
from validations.pkg_data_validator import PkgDataValidator
from xml_normalizer import XMLNormalizer


def unzip_file(zip_file_path):
    files = []
    with open(zip_file_path, 'rb') as f:
        z = zipfile.ZipFile(f)
        for name in z.namelist():
            z.extract(name, "./")
            files.append(name)
    return files


class Package:

    def __init__(self, files):
        self.files = files
        self._organize()

    def _organize(self):
        self.organized = {}
        self.invalid_files = []
        for f in self.files:
            basename = os.path.basename(f)
            name, ext = os.path.splitext(basename)
            prefix = None
            if ext == '.xml':
                prefix = name
            elif '-' in name:
                prefix = name[:name.rfind('-')]

            if prefix is None:
                self.invalid_files.append(f)
            else:
                if self.organized.get(prefix) is None:
                    self.organized[prefix] = {}
                    self.organized[prefix]['xml'] = None
                    self.organized[prefix]['assets'] = []
                if ext == '.xml':
                    self.organized[prefix]['xml'] = f
                else:
                    self.organized[prefix]['assets'].append(f)
        for prefix, files in self.organized.items():
            if files.get('xml') is None:
                self.invalid_files.extend(files['assets'])


class PkgReception:

    def __init__(self, configuration):
        self.configuration = configuration
        self.xml_normalizer = XMLNormalizer(configuration)

    def receive_package(self, pkg_file_path, destination_path, delete):
        outputs = Outputs(destination_path)
        if os.path.isfile(pkg_file_path) and pkg_file_path.endswith('.zip'):
            package = self.receive_zip(pkg_file_path, outputs.path, delete)
        elif os.path.isdir(pkg_file_path):
            files = [os.path.join(pkg_file_path, f) for f in os.listdir(pkg_file_path)]
            package = self.receive_files(files, outputs.path, delete)
        elif isinstance(pkg_file_path, list):
            files = pkg_file_path
            package = self.receive_files(files, outputs.path, delete)
        return package

    def receive_zip(self, zip_file_path, destination_path, delete):
        files = unzip_file(zip_file_path)
        return self.receive_files(files, destination_path)

    def receive_files(self, files, destination_path, delete):
        for f in files:
            file_path = os.path.join(destination_path, os.path.basename(f))
            shutil.copy(f, file_path)
            files.append(file_path)

        package = Package(files)
        for prefix in sorted(package.keys()):
            self.xml_normalizer.normalize(package[prefix]['xml'])
        return package


class Outputs:

    def __init__(self, path):
        self.path = path
        self.scielo_package_path = os.path.join(path, 'scielo_package')
        self.scielo_package_zips_path = os.path.join(path, 'scielo_package_zips')
        self.pmc_package_path = os.path.join(path, 'pmc_package')
        self.reports_path = os.path.join(path, 'errors')

        for _path in [self.scielo_package_path,
                      self.scielo_package_zips_path,
                      self.pmc_package_path,
                      self.reports_path]:
            if not os.path.isdir(_path):
                os.makedirs(_path)


class XMLPackageQA:

    def __init__(self, configuration):
        self.configuration = configuration
        self.article_xml_validator = ArticleXMLValidator(configuration)
        self.article_data_validator = ArticleDataValidator(configuration)
        self.pkg_data_validator = PkgDataValidator(configuration)
        self.pkg_reception = PkgReception(configuration)

    def validate_package(self, pkg_path, destination_path, delete):
        outputs = Outputs(destination_path)
        package = self.pkg_reception.receive_package(pkg_path, outputs.path, delete)
        self._validate_package(package)
        return package

    def validate_files(self, files, destination_path, delete):
        outputs = Outputs(destination_path)
        package = self.pkg_reception.receive_files(files, outputs.path, delete)
        self._validate_package(package)
        return package

    def _validate_package(self, package):
        for prefix in sorted(package.keys()):
            self._validate_article(package[prefix])
        self.pkg_data_validator.validate(package)

    def _validate_article(self, pkg_item):
        xml_file_path = pkg_item['xml']
        asset_file_paths = pkg_item['assets']
        pkg_item['data'] = ArticleData(xml_file_path)
        pkg_item['result1'] = self.article_xml_validator.validate(
            xml_file_path,
            asset_file_paths)
        pkg_item['result2'] = self.article_data_validator.validate(pkg_item)
