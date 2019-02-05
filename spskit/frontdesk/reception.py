# coding: utf-8

import os
import shutil


from spskit.utils.files_utils import FileInfo
from spskit.utils.xml_utils import XML
from spskit.sps.document_data import DocumentData


def get_file_info_items(received_files, destination_path, delete):
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


def get_xml_packages(file_info_items):
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
                xml_packages[prefix] = {}
                xml_packages[prefix]["name"] = prefix
                xml_packages[prefix]["xml_file"] = None
                xml_packages[prefix]["related_files"] = []
            if file_info.ext == ".xml":
                xml_packages[prefix]["xml_file"] = file_info.file_path
            else:
                xml_packages[prefix]["related_files"].append(file_info.file_path)
        else:
            invalid_files.append(file_info.file_path)
    xml_packages = [xml_packages[k] for k in sorted(xml_packages.keys())]
    return xml_packages, invalid_files


def get_document_packages(xml_packages):
    """
    A partir de xml_packages (um dicionário de pacotes de XML),
    retorna document_packages (o mesmo dicionário acrescido de ativos digitais,
    dados do documento, arquivos anexos, etc)
    """
    document_packages = []
    for xml_pkg in xml_packages:
        files = xml_pkg["related_files"]
        xml_pkg["xml"] = XML(xml_pkg["xml_file"])
        xml_pkg["data"] = DocumentData(
            xml_pkg["xml"], xml_pkg["xml"].file_info.name_prefix
        )
        assets = []
        attachments = []
        for f in files:
            basename = os.path.basename(f)
            if basename in xml_pkg["data"].internal_xlink_href:
                assets.append(f)
            else:
                attachments.append(f)
        xml_pkg["assets"] = assets
        xml_pkg["attachments"] = attachments
        document_packages.append((xml_pkg))
    return document_packages


def receive_files(input_files, destination_path, delete=False):
    file_info_items = get_file_info_items(
        input_files, destination_path, delete)
    xml_packages, invalid_files = get_xml_packages(file_info_items)
    document_packages = get_documents_packages(xml_packages)
