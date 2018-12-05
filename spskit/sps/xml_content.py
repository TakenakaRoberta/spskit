
from spskit.utils.xml_utils import XML
from spskit.sps.sps_xml import SPSXML
from spskit.sps.document_data import DocumentData


spsxml = SPSXML({})


class XMLContent:

    def __init__(self, content, xml_name):
        self.content = content
        self.xml_name = xml_name

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
