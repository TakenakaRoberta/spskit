# coding: utf-8

import os
import shutil

import plumber


from spskit.utils.file_utils import FileInfo
import spskit.sps.pkg_files as package


class Reception:

    def __init__(self, configuration):
        self.configuration = configuration

    def receive_files(self, files, destination_path, delete=False):
        data = files, destination_path, delete
        data = self._plumber_pipeline.run(data, rewrap=True)

    @property
    def _plumber_pipeline(self):
        return plumber.Pipeline(
            self.receive_files_pipe(),
            self.get_xml_packages_pipe(),
            self.get_article_packages_pipe(),
            self.endPipe()
        )

    class receive_files_pipe(plumber.Pipe):
        def transform(self, data):
            files, destination_path, delete = data
            _files = []
            for f in files:
                file_path = os.path.join(destination_path, os.path.basename(f))
                shutil.copy(f, file_path)
                _files.append(FileInfo(file_path))
                if delete:
                    try:
                        os.unlink(f)
                    except:
                        pass
            return _files

    class EndPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class get_xml_packages_pipe(plumber.Pipe):
        def transform(self, data):
            file_info_items = data
            xml_packages, invalid_files = package.get_xml_packages(file_info_items)
            return xml_packages, invalid_files

    class get_article_packages_pipe(plumber.Pipe):
        def transform(self, data):
            xml_packages, invalid_files = data
            pkg_articles = package.get_articles_packages(xml_packages)
            return pkg_articles, invalid_files
