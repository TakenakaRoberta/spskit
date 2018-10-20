from utils import xml_utils


class ArticleData:

    def __init__(self, file_path):
        self.xml_name = os.path.basename(file_path)
        self.xml_name, ext = os.path.splitext(self.xml_name)
        self.file_path = file_path
        self.xml = xml_utils.XML(open(file_path).read())

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

