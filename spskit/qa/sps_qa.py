# coding: utf-8

import os
import shutil

from spskit.utils.files_utils import unzip_file, delete_file_or_folder
from spskit.qa.article_xml_validator import ArticleXMLValidator
from spskit.qa.article_data_validator import ArticleDataValidator
from spskit.qa.pkg_data_validator import PkgDataValidator
from spskit.qa.sps_xml_normalizer import SPSXMLNormalizer
from spskit.sps.article_data import ArticleData


class PkgReception:

    def __init__(self, configuration):
        self.configuration = configuration
        self.spsxml_normalizer = SPSXMLNormalizer(configuration)

    def receive_package(self, pkg_file_path, destination_path, delete):
        outputs = Outputs(destination_path)
        if os.path.isfile(pkg_file_path) and pkg_file_path.endswith('.zip'):
            package = self.receive_zip(pkg_file_path, outputs.path, delete)
        elif os.path.isdir(pkg_file_path):
            files = [os.path.join(pkg_file_path, f)
                     for f in os.listdir(pkg_file_path)]
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
            self.spsxml_normalizer.normalize(package[prefix]['xml'])
        return package


class Outputs:

    def __init__(self, path):
        self.path = path
        self.scielo_package_path = os.path.join(path, 'scielo_package')
        self.work_path = os.path.join(path, 'work')
        self.src_path = os.path.join(path, 'src')
        self.scielo_package_zips_path = os.path.join(path, 'scielo_package_zips')
        self.pmc_package_path = os.path.join(path, 'pmc_package')
        self.reports_path = os.path.join(path, 'errors')

        for _path in [self.scielo_package_path,
                      self.scielo_package_zips_path,
                      self.pmc_package_path,
                      self.reports_path]:
            if not os.path.isdir(_path):
                os.makedirs(_path)


class ReportFiles(object):

    def __init__(self, xml_name, reports_path, wrk_path=None):
        self.xml_name = xml_name
        self.wrk_path = wrk_path or reports_path
        self.reports_path = reports_path
        if not os.path.isdir(reports_path):
            os.makedirs(reports_path)
        self.ctrl_filename = '{}/{}{}.ctrl.txt'.format(self.wrk_path, self.xml_name)
        self.style_report_filename = '{}{}.rep.html'.format(
            self.reports_path, self.xml_name)
        self.dtd_report_filename = '{}{}.dtd.txt'.format(
            self.reports_path, self.xml_name)
        self.pmc_dtd_report_filename = '{}{}.pmc.dtd.txt'.format(
            self.reports_path, self.xml_name)
        self.pmc_style_report_filename = '{}{}.pmc.rep.html'.format(
            self.reports_path, self.xml_name)
        self.err_filename = '{}{}.err.txt'.format(
            self.reports_path, self.xml_name)
        self.err_filename_html = '{}{}.err.html'.format(
            self.reports_path, self.xml_name)
        self.filename_html = '{}{}.html'.format(
            self.reports_path, self.xml_name)
        self.mkp2xml_report_filename = '{}{}.mkp2xml.txt'.format(
            self.reports_path, self.xml_name)
        self.mkp2xml_report_filename_html = '{}{}.mkp2xml.html'.format(
            self.reports_path, self.xml_name)
        self.data_report_filename = '{}{}.contents.html'.format(
            self.reports_path, self.xml_name)
        self.images_report_filename = '{}{}.images.html'.format(
            self.reports_path, self.xml_name)
        self.xml_structure_validations_filename = '{}{}{}'.format(
            self.reports_path, '/xmlstr-', self.xml_name)
        self.xml_content_validations_filename = '{}{}{}'.format(
            self.reports_path, '/xmlcon-', self.xml_name)
        self.journal_validations_filename = '{}{}{}'.format(
            self.reports_path, '/journal-', self.xml_name)
        self.issue_validations_filename = '{}{}{}'.format(
            self.reports_path, '/issue-', self.xml_name)

    def clean(self):
        for f in [self.err_filename, self.dtd_report_filename,
                  self.style_report_filename, self.pmc_dtd_report_filename,
                  self.pmc_style_report_filename, self.ctrl_filename]:
            delete_file_or_folder(f)


class SPSPackageQA:

    def __init__(self, configuration):
        self.configuration = configuration
        self.article_xml_validator = ArticleXMLValidator(configuration)
        self.article_data_validator = ArticleDataValidator(configuration)
        self.pkg_data_validator = PkgDataValidator(configuration)
        self.pkg_reception = PkgReception(configuration)

    def validate_package(self, pkg_path, outputs_path, delete):
        outputs = Outputs(outputs_path)
        package = self.pkg_reception.receive_package(pkg_path, outputs.path, delete)
        pkg_data_validation_report_content = self._validate_package(package, outputs)
        package['pkg_data_validations'] = pkg_data_validation_report_content
        return package, outputs

    def validate_files(self, files, outputs_path, delete):
        outputs = Outputs(outputs_path)
        package = self.pkg_reception.receive_files(files, outputs.path, delete)
        if len(files) > 1:
            pkg_data_validation_report_content = self._validate_package(package, outputs)
        package['pkg_data_validations'] = pkg_data_validation_report_content
        return package, outputs

    def _validate_package(self, package, outputs):
        for prefix in sorted(package.keys()):
            self._validate_article(package[prefix], ReportFiles(prefix, outputs.reports_path))
        data, pkg_data_validation_report_content = self.pkg_data_validator.validate(package)
        return pkg_data_validation_report_content

    def _validate_article(self, pkg_item, report_files):
        xml_file_path = pkg_item['xml']
        asset_file_paths = pkg_item['assets']
        pkg_item['data'] = ArticleData(xml_file_path)

        self.article_xml_validator.validate(pkg_item['data'], xml_file_path, asset_file_paths, report_files)
        pkg_item['reports'] = report_files
        self.article_data_validator.validate(pkg_item, report_files.xml_content_validations_filename)
