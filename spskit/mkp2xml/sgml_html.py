# coding=utf-8

import os
import shutil

from bs4 import BeautifulSoup
from utils.fs_utils import FileInfo


class SGMLHTML(object):

    def __init__(self, html_file_path):
        self.sgml_html_info = FileInfo(html_file_path)

    @property
    def content(self):
        return self.bs.prettify()

    @content.setter
    def content(self, value):
        self.bs = BeautifulSoup(value, 'lxml')

    @property
    def images_path(self):
        path = None
        for item in os.listdir(self.sgml_html_info.path):
            _path = os.path.join(self.sgml_html_info.path, item)
            if os.path.isdir(_path) and item.startswith(self.sgml_html_info.name):
                path = _path
                break
        if path is None:
            path = self.create_html_images(self.sgml_html_info.path, self.sgml_html_info.name)
        if path is None:
            path = self.sgml_html_info.path
        return path

    @property
    def href_items(self):
        #[graphic href=&quot;?a20_115&quot;]</span><img border=0 width=508 height=314
        #src="a20_115.temp_arquivos/image001.jpg"><span style='color:#33CCCC'>[/graphic]
        return [elem
                for elem in self.bs.find_all('img')
                if elem.get('src') is not None
                ]
