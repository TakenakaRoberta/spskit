
from spskit.utils.xml_utils import XML
from spskit.sps.sps_xml import SPSXML
from spskit.sps.document_data import DocumentData


sps_xml = SPSXML({})


class XMLContent:

    def __init__(self, xml_content, xml_name):
        self.xml_content = xml_content
        self.xml_name = xml_name

    @property
    def xml(self):
        return XML(self.xml_content)

    @property
    def sps_xml(self):
        return sps_xml.normalize(self.xml)

    @property
    def document_data(self):
        return DocumentData(self.sps_xml, self.xml_name)
