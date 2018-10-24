from utils.xml_utils import XML
from utils.xml_transformer import XMLTransformer
from utils.fs_utils import FileInfo


class SGMLXML2SPSXML:

    def __init__(self, configuration):
        self.configuration = configuration

    def make(self, sgmlxml_file_path, acron):
        sgmlxml = SGMLXML(sgmlxml_file_path)
        xml_file_path = sgmlxml_file_path.replace('.sgm.xml', '.xml')
        self._sgmlxml2xml(sgmlxml, xml_file_path)

    def _sgmlxml2xml(self, sgmlxml, xml_file_path):
        xsl_id = 'XSL_{}'.format(sgmlxml.sps_version)
        xsl_file_path = self.configuration[xsl_id]
        self.configuration.update({'XSL': xsl_file_path})
        xml_transformer = XMLTransformer(self.configuration)
        xml_transformer.transform(sgmlxml.file_path, xml_file_path)


class SGMLXML:

    def __init__(self, file_path):
        self.file_info = FileInfo(file_path)
        self.xml = XML(self.content)

    @property
    def sps_version(self):
        sps = self.xml.getroot().get('sps')
        return sps[4:] if sps.startswith('sps-') else sps

    @property
    def content(self):
        _content = open(self.file_info.file_path, 'rb').read().strip()
        if '<doc' in _content and '</doc>' in _content:
            if '<!DOCTYPE' in _content:
                doctype = _content[_content.find('<!DOCTYPE'):]
                doctype = doctype[:doctype.find('>')+1]
                _content = _content.replace(doctype+'\n', '')
            if not _content.endswith('</doc>'):
                _content = _content[:_content.rfind('</doc>')+len('</doc>')]
            return _content
