# coding: utf-8

import os


def display_text(text):
    return text


_ = display_text


def evaluate_xml_path(xml_path):
    error = None
    sgm_xml = None
    xml_list = None

    if xml_path is None:
        error = _('Missing XML location. ')
    elif os.path.isfile(xml_path):
        name, ext = os.path.splitext(xml_path)
        if ext == '.xml':
            if name.endswith('.sgm'):
                sgm_xml = xml_path
            else:
                xml_list = [xml_path]
        else:
            error = _('Invalid file. XML file required. ')
    elif os.path.isdir(xml_path):
        xml_list = [os.path.join(xml_path, item)
                    for item in os.listdir(xml_path)
                    if item.endswith('.xml') and not item.endswith('.sgm.xml')]
        if len(xml_list) == 0:
            error = _('Invalid folder. Folder must have XML files. ')
    else:
        error = _('Invalid XML location. ')
    return sgm_xml, xml_list, error


