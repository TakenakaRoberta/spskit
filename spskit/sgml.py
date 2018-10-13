# coding: utf-8

import os
import shutil

import plumber

from xml_pkg_qa import XMLPackageQA, Outputs
from xml_transformer import XMLTransformer

"""
markup_xml/scielo_markup
markup_xml/src
markup_xml/work/<basename>/<basename>.sgml.xml
markup_xml/work/<basename>/<images>/

markup_xml/pmc_package
markup_xml/scielo_package
markup_xml/scielo_package_zips
markup_xml/errors

"""

class PackageName(object):

    def __init__(self, doc):
        self.doc = doc
        self.xml_name = doc.xml_name

    def generate(self, acron):
        parts = [self.issn, acron, self.doc.volume, self.issueno, self.suppl, self.last, self.doc.compl]
        return '-'.join([part for part in parts if part is not None and not part == ''])

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
        s = self.doc.volume_suppl or self.doc.number_suppl
        if s is not None:
            s = 's' + s if s != '0' else 'suppl'
        return s

    @property
    def issn(self):
        _issns = [_issn for _issn in [self.doc.e_issn, self.doc.print_issn] if _issn is not None]
        if len(_issns) > 0:
            if self.xml_name[0:9] in _issns:
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
        elif self.doc.number == 'ahead' and self.doc.doi is not None and '/' in self.doc.doi:
            _last = self.doc.doi[self.doc.doi.find('/')+1:].replace('.', '-')
        else:
            _last = self.doc.publisher_article_id
        return _last


class SGMLHTML(object):

    def __init__(self, xml_name, html_filename):
        self.xml_name = xml_name
        self.html_filename = html_filename

    @property
    def html_content(self):
        content = fs_utils.read_file(self.html_filename, encoding.SYS_DEFAULT_ENCODING)
        if '<html' not in content.lower():
            c = content
            for c in content:
                if ord(c) == 0:
                    break
            content = content.replace(c, '')
        return content

    @property
    def html_img_path(self):
        path = None

        html_path = os.path.dirname(self.html_filename)
        html_name = os.path.basename(self.html_filename)
        html_name, ext = os.path.splitext(html_name)
        for item in os.listdir(html_path):
            if os.path.isdir(html_path + '/' + item) and item.startswith(html_name):
                path = html_path + '/' + item
                break
        if path is None:
            path = self.create_html_images(html_path, html_name)
        if path is None:
            path = html_path
        return path

    def create_html_images(self, html_path, html_name):
        #name_image001
        new_html_folder = html_path + '/' + html_name + '_arquivosalt'
        if not os.path.isdir(new_html_folder):
            os.makedirs(new_html_folder)
        for item in os.listdir(html_path):
            if os.path.isfile(html_path + '/' + item) and item.startswith(html_name + '_image'):
                new_name = item[len(html_name)+1:]
                shutil.copyfile(html_path + '/' + item, new_html_folder + '/' + new_name)
        return new_html_folder

    @property
    def unknown_href_items(self):
        #[graphic href=&quot;?a20_115&quot;]</span><img border=0 width=508 height=314
        #src="a20_115.temp_arquivos/image001.jpg"><span style='color:#33CCCC'>[/graphic]
        html_content = self.html_content
        if 'href=&quot;?' in html_content:
            html_content = html_content.replace('href=&quot;?', 'href="?')
        #if '“' in html_content:
        #    html_content = html_content.replace('“', '"')
        #if '”' in html_content:
        #    html_content = html_content.replace('”', '"')
        _items = html_content.replace('href="?', 'href="?--~BREAK~FIXHREF--FIXHREF').split('--~BREAK~FIXHREF--')
        items = [item for item in _items if item.startswith('FIXHREF')]
        img_src = []
        for item in items:
            if 'src="' in item:
                src = item[item.find('src="') + len('src="'):]
                src = src[0:src.find('"')]
                if '/' in src:
                    src = src[src.find('/') + 1:]
                if len(src) > 0:
                    img_src.append(src)
            else:
                img_src.append('None')
        return img_src

    def get_fontsymbols(self):
        r = []
        html_content = self.html_content
        if '[fontsymbol]' in html_content.lower():
            for style in ['italic', 'sup', 'sub', 'bold']:
                html_content = html_content.replace('<' + style + '>', '[' + style + ']')
                html_content = html_content.replace('</' + style + '>', '[/' + style + ']')

            html_content = html_content.replace('[fontsymbol]'.upper(), '[fontsymbol]')
            html_content = html_content.replace('[/fontsymbol]'.upper(), '[/fontsymbol]')
            html_content = html_content.replace('[fontsymbol]', '~BREAK~[fontsymbol]')
            html_content = html_content.replace('[/fontsymbol]', '[/fontsymbol]~BREAK~')

            html_fontsymbol_items = [item for item in html_content.split('~BREAK~') if item.startswith('[fontsymbol]')]
            for item in html_fontsymbol_items:
                item = item.replace('[fontsymbol]', '').replace('[/fontsymbol]', '')
                item = item.replace('<', '~BREAK~<').replace('>', '>~BREAK~')
                item = item.replace('[', '~BREAK~[').replace(']', ']~BREAK~')
                parts = [part for part in item.split('~BREAK~') if not part.endswith('>') and not part.startswith('<')]

                new = ''
                for part in parts:
                    if part.startswith('['):
                        new += part
                    else:

                        for c in part:
                            _c = c.strip()
                            if _c.isdigit() or _c == '':
                                n = c
                            else:
                                try:
                                    n = symbols.get_symbol(c)
                                except:
                                    n = '?'
                            new += n
                for style in ['italic', 'sup', 'sub', 'bold']:
                    new = new.replace('[' + style + ']', '<' + style + '>')
                    new = new.replace('[/' + style + ']', '</' + style + '>')
                r.append(new)
        return r


class SGMLXMLFilesPkg:

    def __init__(self, sgmlxml_file_path):
        dirname = os.path.dirname(sgmlxml_file_path)
        basename = os.path.basename(sgmlxml_file_path)
        work_dirname = os.path.dirname(dirname)
        self.root_path = os.path.dirname(work_dirname)

        self.outputs = Outputs(self.root_path)

        name, ext = os.path.splitext(basename)
        name, ign = os.path.splitext(name)
        if name[0] == 'a' and name[3] == 'v':
            name = name[:3]
        self.prefix = name

        self.work_images_path = os.path.join(dirname, 'images')
        self.src_path = os.path.join(self.root_path, 'src')

        self.html_filename = self.input_path + '/' + self.prefix + '.temp.htm'
        if not os.path.isfile(self.html_filename):
            self.html_filename += 'l'
        self.xml_file_path = os.path.join(self.root_path, 'xml_file')
        self.destination_path = self.root_path

    def get_src_files(self):
        self.src_files = []
        for basename in os.listdir(self.src_path):
            if basename.startswith(self.prefix):
                suffix = basename[len(self.prefix):]
                if not suffix[0].isdigit():
                    self.src_files.append(os.path.join(self.src_path, basename))
                else:
                    print(basename)

    def get_work_images_files(self):
        self.src_files = []
        for basename in os.listdir(self.src_path):
            if basename.startswith(self.prefix):
                suffix = basename[len(self.prefix):]
                if not suffix[0].isdigit() or suffix[0:2] == '00':
                    self.src_files.append(os.path.join(self.src_path, basename))
                else:
                    print(basename)


class SGMLXML2XML:

    def __init__(self, configuration):
        self.configuration = configuration
        self.sgmlxml_normalizer = SGMLXMLNormalizer(configuration)
        self.xml_transformer = XMLTransformer(configuration)
        self.xml_pkg_qa = XMLPackageQA(configuration)

    def pack(self, sgmlxml_file_path):
        sgmlxml_pkg = SGMLXMLFilesPkg(sgmlxml_file_path)
        self._normalize_sgmlxml(sgmlxml_pkg)
        self._sgmlxml2xml(sgmlxml_pkg)
        self._normalize_xmlsgmlxml_pkg()

    def _normalize_sgmlxml(self, sgmlxml_pkg):
        data, reports = self.sgmlxml_normalizer.normalize(sgmlxml_pkg)
        return data, reports

    def _sgmlxml2xml(self, sgmlxml_pkg):
        # alem de gerar o xml sps
        # renomear os ativos digitais e o xml
        # renomear os ativos digitais dentro do xml
        # gerar relatorio de origem das images
        self.xml_transformer.transform(sgmlxml_pkg.new_sgmlxml, sgmlxml_pkg.xml_filename)

    def _normalize_xml(self, sgmlxml_pkg):
        files = sgmlxml_pkg.xml_files
        destination_path = sgmlxml_pkg.outputs.path
        self.xml_pkg_qa.validate_files(files, destination_path, delete=False)


class SGMLXMLNormalizer:

    def __init__(self, configuration):
        self.configuration = configuration

    def normalize(self, data):
        plumber_pipeline = plumber.Pipeline()
        transformed_data = plumber_pipeline.run(data, rewrap=True)
        return next(transformed_data)

    #         self.replace_mimetypes()
