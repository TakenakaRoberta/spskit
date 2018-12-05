# coding: utf-8

import os
import shutil


from spskit.utils.files_utils import FileInfo
from spskit.sps.xml_file import XMLFile


def destinate_files(files, destination_path, delete):
    _files = []
    for f in files:
        file_path = os.path.join(destination_path, os.path.basename(f))
        shutil.copy(f, file_path)
        _files.append(FileInfo(file_path))
        if delete:
            try:
                os.unlink(f)
            except:
                pass
    return _files


def get_xml_packages(file_info_items):
    xml_prefixes = [f.name_prefix for f in file_info_items if f.ext == '.xml']

    xml_packages = {}
    invalid_files = []

    for file_info in file_info_items:
        prefix = file_info.name_prefix
        if prefix not in xml_prefixes:
            prefix = prefix[:prefix.rfind('-')]
        if prefix in xml_prefixes:
            if xml_packages.get(prefix) is None:
                xml_packages[prefix] = {}
                xml_packages[prefix]['name'] = prefix
                xml_packages[prefix]['xml_file'] = None
                xml_packages[prefix]['related_files'] = []
            if file_info.ext == '.xml':
                xml_packages[prefix]['xml_file'] = file_info.file_path
            else:
                xml_packages[prefix]['related_files'].append(file_info.file_path)
        else:
            invalid_files.append(file_info.file_path)
    xml_packages = [xml_packages[k]
                    for k in sorted(xml_packages.keys())]
    return xml_packages, invalid_files


def get_document_packages(xml_packages):
    document_packages = []
    for xml_pkg in xml_packages:
        files = xml_pkg['related_files']
        xml_pkg['xml'] = XMLFile(xml_pkg['xml_file'])

        assets = []
        attachments = []
        for f in files:
            basename = os.path.basename(f)
            if basename in xml_pkg['xml'].document_data.internal_xlink_href:
                assets.append(f)
            else:
                attachments.append(f)
        xml_pkg['assets'] = assets
        xml_pkg['attachments'] = attachments
        document_packages.append((xml_pkg))
    return document_packages


def receive_files(files, destination_path, delete=False):
    file_info_items = destinate_files(files)
    xml_packages, invalid_files = get_xml_packages(file_info_items)
    document_packages = get_documents_packages(xml_packages)
