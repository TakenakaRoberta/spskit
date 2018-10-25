import os

from utils.xml_utils import XML
from utils.xml_transformer import XMLTransformer
from utils.fs_utils import FileInfo
from qa.sps_qa import Outputs


class SGMLXML2SPSXML:

    def __init__(self, configuration):
        self.configuration = configuration

    def make(self, sgmlxml_file_path, acron):
        sgmlxml = SGMLXML(sgmlxml_file_path)
        work_xml_file_path = sgmlxml_file_path.replace('.sgm.xml', '.xml')
        files = ArticleFiles(work_xml_file_path)

        self._sgmlxml2xml(
            sgmlxml_file_path, sgmlxml.sps_version, work_xml_file_path)
        # tiff2jpg (src_path)

    def _sgmlxml2xml(self, sgmlxml_file_path, sps_version, work_xml_file_path):
        xsl_id = 'XSL_{}'.format(sps_version)
        xsl_file_path = self.configuration[xsl_id]
        self.configuration.update({'XSL': xsl_file_path})
        xml_transformer = XMLTransformer(self.configuration)
        xml_transformer.transform(sgmlxml_file_path, work_xml_file_path)


class SGMLXML:

    def __init__(self, file_path):
        self.file_info = FileInfo(file_path)
        self._content = open(self.file_info.file_path, 'rb').read().strip()

    @property
    def xml(self):
        return XML(self.content)

    @property
    def sps_version(self):
        sps = self.xml.getroot().get('sps')
        return sps[4:] if sps.startswith('sps-') else sps

    @property
    def content(self):
        # self.fix_begin_end()
        # self.fix_quotes()
        # self.content = xml_utils.remove_doctype(# self.content)
        # self.insert_mml_namespace_reference()
        # self.identify_href_values()
        # self.insert_xhtml_content()
        # self.replace_fontsymbols()
        # self.fix_styles_names()
        # self.remove_exceding_styles_tags()
        # self.content = # self.fix_begin_end(# self.content)
        # if # self.xml is None:
        #    # self.fix()
        # self.fix_begin_end()
        return self._content

    def fix_begin_end(self):
        _content = self._content
        if '<doc' in _content and '</doc>' in _content:
            if '<!DOCTYPE' in _content:
                doctype = _content[_content.find('<!DOCTYPE'):]
                doctype = doctype[:doctype.find('>')+1]
                _content = _content.replace(doctype+'\n', '')
            if not _content.endswith('</doc>'):
                _content = _content[:_content.rfind('</doc>')+len('</doc>')]
        self._content = _content


class ArticleFiles(object):

    def __init__(self, work_xml_file_path):
        self.work_xml_file_info = FileInfo(work_xml_file_path)
        self.outputs = Outputs(os.path.dirname(
            os.path.dirname(self.xml_file_info.path)))
        self.html_file_info = FileInfo(
            os.path.join(self.xml_file_info.path),
            self.xml_file_info.name+'.temp.htm')
        self.src_xml_file_info = FileInfo(
            os.path.join(
                self.outputs.src_path, self.work_xml_file_info.basename)
        )
