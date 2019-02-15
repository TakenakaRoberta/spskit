import os
from spskit.xml_utils import XML
from spskit.sps.document_data import DocumentData


class DocumentPackage:

    def __init__(self, xml_package):
        self.xml_package = xml_package
        self._assets = []
        self._attachments = []
        for f in self.xml_package.related_files:
            basename = os.path.basename(f)
            if basename in self.document_data.internal_xlink_href:
                self._assets.append(f)
            else:
                self._attachments.append(f)

    @property
    def xml(self):
        if self._xml is None:
            self._xml = XML(self.xml_package.xml_file)
        return self._xml

    @property
    def assets(self):
        return self._assets

    @property
    def attachments(self):
        return self._attachments

    @property
    def document_data(self):
        if self._document_data is None:
            self._document_data = DocumentData(
                self.xml, self.xml.file_info.name_prefix
            )
        return self._document_data
