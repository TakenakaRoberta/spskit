from spskit.utils import xml_utils
from spskit.utils.files_utils import FileInfo


def parse_issue(issue):
    number = None
    suppl = None
    compl = None
    if issue is not None:
        parts = [part for part in issue.strip().lower().split(' ') if part != '']
        if len(parts) == 1:
            # suppl or n
            if parts[0].startswith('sup'):
                suppl = parts[0]
            else:
                number = parts[0]
        elif len(parts) == 2:
            #n suppl or suppl s or n pr
            if parts[0].startswith('sup'):
                suppl = parts[1]
            elif parts[1].startswith('sup'):
                number, suppl = parts
            else:
                number, compl = parts
        elif len(parts) == 3:
            # n suppl s
            number, _type, value = parts
            if _type.startswith('sup'):
                suppl = value
            else:
                compl = value
    if suppl is not None:
        if suppl.startswith('sup'):
            suppl = '0'
    return (number, suppl, compl)


class ArticleData:

    def __init__(self, file_path):
        self.file_info = FileInfo(file_path)
        self.xml = xml_utils.XML(open(file_path).read())
        self._get_article_location()

    def nodes(self, xpath):
        elements = []
        if self.xml.tree:
            for node in self.xml.tree.findall(xpath):
                elements.append((self.xml.tree.getpath(node), node))
        return elements

    @property
    def sps_version(self):
        return self.xml.tree.getroot().get('sps')

    @property
    def xlink_href(self):
        return [node.get('{http://www.w3.org/1999/xlink}href')
                for node in self.nodes('.//*[@{http://www.w3.org/1999/xlink}href]') or []
                ]

    @property
    def internal_xlink_href(self):
        return [item for item in self.xlink_href if '/' not in item]

    @property
    def languages(self):
        nodes = self.nodes('.//article') + self.nodes('.//sub-article')
        languages = [node.get('{http://www.w3.org/XML/1998/namespace}lang')
                     for node in nodes]
        return [languages[0]] + [item for item in languages[1:] if item != languages[0]]

    @property
    def article_meta(self):
        return self.xml.find('.//article-meta')

    @property
    def journal_meta(self):
        return self.xml.find('.//journal-meta')

    def _get_article_location(self):
        self.volume = self.article_meta.findtext('volume')
        self.issue = self.article_meta.findtext('issue')
        self.number, self.suppl, self.compl = parse_issue(self.issue)
        self.fpage = self.article_meta.findtext('fpage')
        self.lpage = self.article_meta.findtext('lpage')
        self.fpage_seq = None if self.fpage is None else self.fpage.get('seq')
        self.elocation_id = self.article_meta.findtext('elocation-id')
        self.doi = self.article_meta.findtext('article-id[@pub-id-type="doi"]')
        self.publisher_article_id = self.article_meta.findtext('article-id[@pub-id-type="publisher-id"]')
        self.e_issn = self.journal_meta.findtext('issn[@pub-type="epub"]')
        self.print_issn = self.journal_meta.findtext('issn[@pub-type="ppub"]')
