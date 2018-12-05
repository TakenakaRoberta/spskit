import os

from spskit.utils.xml_utils import XML
from spskit.sps.sps_xml import SPSXML
from spskit.sps.document_data import DocumentData
from spskit.utils.files_utils import FileInfo


spsxml = SPSXML({})


class XMLFile:

    def __init__(self, xml_file_path):
        file_info = FileInfo(xml_file_path)
        self.xml_file_path = xml_file_path
        self.xml_name = file_info.name_prefix
        self.content = self.file_content

    @property
    def file_content(self):
        if os.path.isfile(self.xml_file_path):
            with open(self.xml_file_path, 'rb') as fp:
                content = fp.read().decode('utf-8')
            return content

    @property
    def content(self):
        return self.xml.text

    @content.setter
    def content(self, content):
        self.xml = XML(content)

    @property
    def sps_xml(self):
        return spsxml.normalize(self.xml)

    @property
    def document_data(self):
        return DocumentData(self.sps_xml, self.xml_name)
