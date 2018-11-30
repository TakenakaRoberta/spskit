

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
                xml_packages[prefix]['xml'] = None
                xml_packages[prefix]['related_files'] = []
            if file_info.ext == '.xml':
                xml_packages[prefix]['xml'] = file_info.file_path
            else:
                xml_packages[prefix]['related_files'].append(file_info.file_path)
        else:
            invalid_files.append(file_info.file_path)
    xml_packages = [xml_packages[k]
                    for k in sorted(xml_packages.keys())]
    return xml_packages, invalid_files
