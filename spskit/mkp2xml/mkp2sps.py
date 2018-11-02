import os
import shutil

from bs4 import BeautifulSoup

from spskit.utils.xml_transformer import XMLTransformer
from spskit.utils.files_utils import FileInfo
from spskit.qa.sps_qa import Outputs
from spskit.sps.article_data import ArticleData


from mimetypes import MimeTypes
MIME_TYPES = MimeTypes()


def get_mkp_href_data(elem_name, elem_id, alternative_id):
    suffixes = []
    possibilities = []
    n = ''
    if elem_name == 'equation':
        suffixes.append('frm')
        suffixes.append('form')
        suffixes.append('eq')
        n = get_number_from_element_id(elem_id)
    elif elem_name in ['tabwrap', 'equation', 'figgrp']:
        suffixes.append(elem_name[0])
        suffixes.append(elem_name[0:3])
        n = get_number_from_element_id(elem_id)
    else:
        suffixes.append('img')
        suffixes.append('image')
        alternative_id += 1
        n = str(alternative_id)

    for suffix in suffixes:
        possibilities.append(suffix + n)
        if n != '':
            possibilities.append(suffix + '0' + n)
    return (n, possibilities, alternative_id)


def get_number_from_element_id(element_id):
    n = ''
    i = 0
    is_letter = True
    while i < len(element_id) and is_letter:
        is_letter = not element_id[i].isdigit()
        i += 1
    if not is_letter:
        n = element_id[i-1:]
        if n != '':
            n = str(int(n))
    return n


class SGMLXML2SPSXML:

    def __init__(self, configuration, sgmlxml_file_path, acron):
        self.configuration = configuration
        self.files = RelatedArticleFiles(sgmlxml_file_path)
        self.acron = acron

    def make(self):
        # normaliza sgmlxml
        self.sgmlxml = SGMLXML(self.files.sgmlxml_file_info.file_path)
        self.sgmlxml.fix_content(self.files.sgml_html, self.files)
        with open(self.files.src_sgmlxml_file_info.file_path, 'wb') as f:
            f.write(self.sgmlxml.content)

        # sgmlxml 2 xml
        self._sgmlxml2xml(self.files.src_sgmlxml_file_info.file_path,
                          self.sgmlxml.sps_version,
                          self.files.work_xml_file_info.file_path)

        # normaliza xml
        doc = ArticleData(self.files.work_xml_file_info.file_path)
        new_name = PackageName(doc).get()

        # pacote
        self.spsxml = DraftSPSXML(self.files.work_xml_file_info.file_path)
        replacements = self.spsxml.replace_href_values(new_name+'-')
        self.spsxml.replace_mimetypes()
        with open(self.files.xml_file_info.file_path, 'wb') as f:
            f.write(self.spsxml.content)
        self.files.pack(new_name)
        for k, v in dict(replacements):
            shutil.copyfile(k, os.path.join(self.files.xml_file_info.path, v))

        # relatorio de imagem
        # FIXME

    def _sgmlxml2xml(self, sgmlxml_file_path, sps_version, work_xml_file_path):
        # sgmlxml 2 xml
        xsl_id = 'XSL_{}'.format(sps_version)
        xsl_file_path = self.configuration[xsl_id]
        self.configuration.update({'XSL': xsl_file_path})
        xml_transformer = XMLTransformer(self.configuration)
        xml_transformer.transform(sgmlxml_file_path, work_xml_file_path)


class DraftSPSXML:

    def __init__(self, file_path):
        self.file_info = FileInfo(file_path)
        self.content = open(file_path, 'rb').read()

    @property
    def bs(self):
        return self._bs

    @property
    def content(self):
        return self.bs.prettify()

    @content.setter
    def content(self, value):
        self._bs = BeautifulSoup(value, 'lxml')

    def replace_mimetypes(self):
        for elem in self.bs.find_all(attrs={'mimetype': not None}):
            f = elem['mimetype']
            if 'replace' in f:
                f = f.replace('replace', '')
                result = MIME_TYPES.guess_type(f)
                elem['mimetype'] = result[0] or ''
                if '/' in result:
                    m, ms = result.split('/')
                    elem['mimetype'] = m
                    elem['mime-subtype'] = ms

    def replace_href_values(self, new_name):
        replacements = []
        for elem in self.bs.find_all(attrs={'xlink:href': not None}):
            if not ':' in elem['xlink:href']:
                previous = elem['xlink:href']
                f = FileInfo(previous)
                new = f.basename.replace(self.file_info.name_prefix, new_name)
                elem['xlink:href'] = new
                replacements.append((previous, new))
        return replacements


class SGMLXML:

    def __init__(self, file_path):
        self.file_info = FileInfo(file_path)
        self.content = self._fix_begin_end(
            open(self.file_info.file_path, 'rb').read().strip())

        self.FONT_SYMBOLS = {}
        for item in open('symbols.tsv').readlines():
            k, v = item.strip().split('\t')
            self.FONT_SYMBOLS[k] = v

    @property
    def bs(self):
        return self._bs

    @property
    def content(self):
        return self.bs.prettify()

    @content.setter
    def content(self, value):
        self._bs = BeautifulSoup(value, 'lxml')

    @property
    def sps_version(self):
        sps = self.bs.find('doc').get('sps')
        return sps[4:] if sps.startswith('sps-') else sps

    def fix_content(self, sgml_html, files):
        self._fix_quotes()
        self._fix_graphic_href_values(sgml_html, files)
        self._insert_xhtml_content(files.outputs.src_path)
        self._insert_mml_namespace_reference()
        self._replace_fontsymbols()
        self._fix_style()
        self.content = self._fix_begin_end(self.content)

    def _fix_begin_end(self, content):
        _content = content
        if '<doc' in _content and '</doc>' in _content:
            if '<!DOCTYPE' in _content:
                doctype = _content[_content.find('<!DOCTYPE'):]
                doctype = doctype[:doctype.find('>')+1]
                _content = _content.replace(doctype+'\n', '')
            if not _content.endswith('</doc>'):
                _content = _content[:_content.rfind('</doc>')+len('</doc>')]
        return _content

    def _fix_quotes(self):
        self.content = self.bs.prettify()

    def _insert_mml_namespace_reference(self):
        ns = "https://www.w3.org/1998/Math/MathML"
        doc = self.bs.find('doc')
        if 'mml:' in self.content and doc.get('xmlns:mml') is None:
            doc['xmlns:mml'] = ns

    def _fix_graphic_href_values(self, sgml_html, files):
        self.replaced = []
        self.not_found = []
        href_elements = []
        for elem in self.bs.find_all('graphic'):
            if elem.get('href', '').startswith('?'+self.file_info.name):
                href_elements.append(elem)
        alternative_id = 0
        for elem_graphic, elem_img in zip(href_elements, sgml_html.img_elements):
            if elem_img.get('src') is None:
                elem_graphic.decompose()
            else:
                elem_name = elem.parent.name
                elem_id = elem.parent.get('id')
                found, alternative_id = files.get_file(
                    elem_name, elem_id, alternative_id)
                file_info = None
                if len(found) == 0:
                    file_path = sgml_html.img_src_paths.get(elem_img['src'])
                    if file_path is not None:
                        file_info = FileInfo(file_path)
                else:
                    file_info = found[0]
                if file_info is None:
                    self.not_found.append(
                        (elem_name, elem_id, files.digital_asset_file_paths))
                else:
                    new_href = os.path.join(file_info.path, file_info.name)
                    self.replaced.append((elem_name, elem_id, new_href))
                    elem['href'] = file_info.file_path

    def _insert_xhtml_content(self, src_path):
        self.replaced = []
        self.not_found = []
        for elem in self.bs.find_all('xhtml'):
            href = elem.get('href')
            if href is None:
                body = HTML(os.path.join(src_path, href)).body
                if body:
                    elem.string = body
                    elem.extract()

    def _replace_fontsymbols(self):
        for symb in self.bs.find_all('fontsymbol'):
            symb.string = self.FONT_SYMBOLS.get(symb.text)
            symb.extract()

    def _fix_styles(self):
        self._fix_styles_names()
        self._remove_exceding_styles_tags()

    def _fix_styles_names(self):
        content = self.content
        for style in ['italic', 'bold', 'sup', 'sub']:
            s = '<' + style + '>'
            e = '</' + style + '>'
            content = content.replace(s.upper(), s).replace(e.upper(), e)
        self.content = content

    def _remove_exceding_styles_tags(self):
        content = self.content
        previous = ''
        while previous != content:
            previous = content
            for style in ['italic', 'bold', 'sup', 'sub']:
                content = self.__remove_exceding_style_tag(style, content)
        self.content = content

    def __remove_exceding_style_tag(self, style, content):
        s = '<' + style + '>'
        e = '</' + style + '>'
        content = content.replace(e + s, '')
        content = content.replace(e + ' ' + s, ' ')
        return content


class HTML:

    def __init__(self, file_path):
        self.file_path = file_path

    def body(self):
        if os.path.isfile(self.file_path):
            return BeautifulSoup(
                open(self.file_path, 'rb').read(), 'lxml').body


class SGMLHTML(object):

    def __init__(self, file_path):
        self.file_info = FileInfo(file_path)

    @property
    def content(self):
        return self.bs.prettify()

    @content.setter
    def content(self, value):
        self.bs = BeautifulSoup(value, 'lxml')

    @property
    def img_file_paths(self):
        images = []
        for item in os.listdir(self.file_info.path):
            _path = os.path.join(self.file_info.path, item)
            if os.path.isdir(_path) and item.startswith(self.file_info.name):
                images = [os.path.join(_path, f) for f in os.listdir(_path)]
                break
        if len(images) == 0:
            images = self._alternative_img_file_paths()
        return images

    @property
    def _alternative_img_file_paths(self):
        # name_image001
        images = []
        for item in os.listdir(self.file_info.path):
            file_path = os.path.join(self.file_info.path, item)
            if item.startswith(self.file_info.name + '_image') and \
               os.path.isfile(file_path):
                images.append(file_path)
        return images

    @property
    def img_elements(self):
        #[graphic href=&quot;?a20_115&quot;]</span><img border=0 width=508 height=314
        #src="a20_115.temp_arquivos/image001.jpg"><span style='color:#33CCCC'>[/graphic]
        content = self.content.replace('[graphic', '<graphic>[graphic')
        self.content = content.replace('[/graphic]', '[/graphic]</graphic>')
        images = []
        for graphic in self.bs.find_all('graphic'):
            for img in self.bs.find_all('img'):
                if img.get('src') is not None:
                    images.append(img)
        content = self.content.replace('<graphic>', '')
        self.content = content.replace('</graphic>', '')
        return images

    @property
    def img_src_paths(self):
        items = {}
        for img in self.img_elements:
            src = img['src']
            file_path = [f for f in self.img_file_paths if f.endswith(src)]
            if file_path:
                items[src] = file_path
        return items


class RelatedArticleFiles(object):

    def __init__(self, sgmlxml_file_path):
        self.sgmlxml_file_info = FileInfo(sgmlxml_file_path)

        work_xml_file_path = sgmlxml_file_path.replace('.sgm.xml', '.xml')
        self.work_xml_file_info = FileInfo(work_xml_file_path)

        self.name_prefix = self.work_xml_file_info.name_prefix
        if 'v' == self.name_prefix[3] and \
           self.name_prefix.startswith('a') and \
           self.name_prefix[1:3].isdigit():
            self.name_prefix = self.name_prefix[:3]

        self.outputs = Outputs(os.path.dirname(
            os.path.dirname(self.sgmlxml_file_info.path)))

        self.html_file_info = FileInfo(
            os.path.join(self.sgmlxml_file_info.path),
            self.sgmlxml_file_info.name+'.temp.htm')

        self.src_xml_file_info = FileInfo(
            os.path.join(
                self.outputs.src_path, self.work_xml_file_info.basename)
        )
        self.src_sgmlxml_file_info = FileInfo(
            os.path.join(
                self.outputs.src_path, self.sgmlxml_file_info.basename)
        )
        self.digital_asset_file_paths = [
            os.path.join(self.src_xml_file_info.path, f)
            for f in os.listdir(self.src_xml_file_info.path)
            if f.startswith(self.name_prefix)]

        self.sgml_html = SGMLHTML(self.html_file_info.file_path)

        self.digital_asset_file_paths.extend(self.sgml_html.image_file_paths)
        self.digital_asset_file_info_items = {}
        for f in self.digital_asset_file_paths:
            f_info = FileInfo(f)
            suffix = f_info.name[len(self.name_prefix):]
            if suffix not in self.digital_asset_file_info_items.keys():
                self.digital_asset_file_info_items[suffix] = []
            self.digital_asset_file_info_items[suffix].append(f_info)

    @property
    def xml_file_info(self):
        return FileInfo(self.xml_file_path)

    @property
    def xml_file_path(self):
        return self._xml_file_path

    @xml_file_path.setter
    def xml_file_path(self, new_name):
        self._xml_file_path = os.path.join(
            self.outputs.scielo_package_path, new_name+'.xml')

    def tiff2jpg(self):
        # MISSING tiff2jpg (src_path)
        pass

    def get_file(self, elem_name, elem_id, alternative_id):
        found = []
        number, suffixes, alternative_id = get_mkp_href_data(
            elem_name, elem_id, alternative_id)
        for suffix in suffixes:
            f = self.digital_asset_file_info_items.get(suffix)
            if f is not None:
                found.extend(f)
        f = self.digital_asset_file_info_items.get(elem_id)
        if f is not None:
            found.extend(f)
        return (found, alternative_id)

    def pack(self, new_name):
        for f in self.digital_asset_file_paths:
            basename = os.path.basename(f)
            basename = basename.replace(self.name_prefix, new_name+'-')
            if '-.' in basename:
                basename = basename.replace('-.', '.')
            shutil.copyfile(f, os.path.join(self.outputs.scielo_package_path, basename))


class PackageName(object):

    def __init__(self, acron, doc):
        self.acron = acron
        self.doc = doc
        self.xml_name = doc.xml_name

    def get(self):
        parts = [self.issn, self.acron,
                 self.doc.volume, self.issueno, self.suppl,
                 self.last, self.doc.compl]
        return '-'.join(
            [part for part in parts if part is not None and not part == ''])

    @property
    def issueno(self):
        _issueno = self.doc.number
        if _issueno:
            if _issueno == 'ahead':
                _issueno = '0'
            if _issueno.isdigit():
                if int(_issueno) == 0:
                    _issueno = None
                else:
                    n = len(_issueno)
                    if len(_issueno) < 2:
                        n = 2
                    _issueno = _issueno.zfill(n)
        return _issueno

    @property
    def suppl(self):
        s = self.doc.suppl
        if s is not None:
            s = 's' + s if s != '0' else 'suppl'
        return s

    @property
    def issn(self):
        _issns = [_issn
                  for _issn in [self.doc.e_issn, self.doc.print_issn]
                  if _issn is not None]
        if len(_issns) > 0:
            if self.xml_name and self.xml_name[0:9] in _issns:
                _issn = self.xml_name[0:9]
            else:
                _issn = _issns[0]
        return _issn

    @property
    def last(self):
        if self.doc.fpage is not None and self.doc.fpage != '0':
            _last = self.doc.fpage
            if self.doc.fpage_seq is not None:
                _last += self.doc.fpage_seq
        elif self.doc.elocation_id is not None:
            _last = self.doc.elocation_id
        elif self.doc.number == 'ahead' and \
                self.doc.doi and '/' in self.doc.doi:
            _last = self.doc.doi[self.doc.doi.find('/')+1:].replace('.', '-')
        else:
            _last = self.doc.publisher_article_id
        return _last
