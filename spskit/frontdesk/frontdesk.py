# coding: utf-8

import os
import shutil

from .mkp2xml.mkp2sps import SGMLXML2SPSXML
from .qa.sps_qa import SPSPackageQA


def display_text(text):
    return text


_ = display_text


def evaluate_xml_path(xml_path):
    error = None
    sgm_xml = None
    xml_list = None
    outputs_path = None

    if xml_path is None:
        error = _('Missing XML location. ')
    elif os.path.isfile(xml_path):
        dirname = os.path.dirname(xml_path)
        name, ext = os.path.splitext(xml_path)
        if ext == '.xml':
            if name.endswith('.sgm'):
                sgm_xml = xml_path
                dirname = os.path.dirname(dirname)  # work
                outputs_path = os.path.dirname(dirname)  # markup_xml
            else:
                xml_list = [xml_path]
                basename = os.path.basename(dirname)
                if basename == 'scielo_package':
                    outputs_path = os.path.dirname(dirname)
                else:
                    outputs_path = dirname+'_xpm'
        else:
            error = _('Invalid file. XML file required. ')
    elif os.path.isdir(xml_path):
        xml_list = [os.path.join(xml_path, item)
                    for item in os.listdir(xml_path)
                    if item.endswith('.xml') and not item.endswith('.sgm.xml')]
        if len(xml_list) == 0:
            error = _('Invalid folder. Folder must have XML files. ')
        else:
            outputs_path = xml_path+'_xpm'
    else:
        error = _('Invalid XML location. ')
    return sgm_xml, xml_list, error, outputs_path


def execute_xpm(xml_path, configuration, outputs_path=None, acron=None):
    """
    Generate the XML Package or validates the XML files informed by xml_path

    Keyword arguments:
    xml_path -- XML file location or XML files folder location or SGML XML file
    configuration -- configuration
    outputs_path
    """
    sgmlxml_file_path, xml_list, error, _outputs_path = \
        evaluate_xml_path(xml_path)
    if error:
        return False, error

    if sgmlxml_file_path is not None:
        if acron is None:
            raise IOError('Missing acron')
        sgmxml2xml = SGMLXML2SPSXML(configuration)
        pkg_file_path = sgmxml2xml.make(sgmlxml_file_path, acron)

    if xml_list:
        pkg_file_path = os.path.dirname(xml_list[0])

    qa = SPSPackageQA(configuration)
    outputs_path = outputs_path or _outputs_path
    package, outputs = qa.validate_package(
        pkg_file_path, outputs_path, delete=False)
    return True, outputs_path
