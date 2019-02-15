# coding: utf-8

import os
import shutil


from spskit.utils.files_utils import FileInfo
from spskit.models.xml_package import XMLPackage
from spskit.models.document_package import DocumentPackage


def classify_files(received_files, destination_path, delete):
    input_files = []
    for f in received_files:
        file_path = os.path.join(destination_path, os.path.basename(f))
        shutil.copy(f, file_path)
        input_files.append(FileInfo(file_path))
        if delete:
            try:
                os.unlink(f)
            except:
                pass
    return input_files


def group_files_in_xml_packages(file_info_items):
    """
    A partir de uma lista de FileInfo, retorna uma lista de pacotes XML e
    uma lista de arquivos que não fazem parte de nenhum pacote XML
    Param file_info_items: lista de FileInfo
    Retorna (xml_packages, invalid_files)
    """
    xml_prefixes = [f.name_prefix for f in file_info_items if f.ext == ".xml"]

    xml_packages = {}
    invalid_files = []

    for file_info in file_info_items:
        prefix = file_info.name_prefix
        if prefix not in xml_prefixes:
            prefix = prefix[: prefix.rfind("-")]
        if prefix in xml_prefixes:
            if xml_packages.get(prefix) is None:
                xml_packages[prefix] = XMLPackage(prefix)
            if file_info.ext == ".xml":
                xml_packages[prefix].xml_file = file_info.file_path
            else:
                related_files = xml_packages[prefix].related_files
                related_files.append(file_info.file_path)
                xml_packages[prefix].related_files = related_files
        else:
            invalid_files.append(file_info.file_path)
    return xml_packages, invalid_files


def get_document_packages(input_files, destination_path, delete=False):
    file_info_items = classify_files(input_files, destination_path, delete)
    xml_packages, invalid_files = group_files_in_xml_packages(file_info_items)
    document_packages = []
    for prefix, xml_pkg in sorted(xml_packages.items()):
        document_packages.append(DocumentPackage(xml_pkg))
    return document_packages
