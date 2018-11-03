import os

from spskit.utils.files_utils import FileInfo


class ArticlePackage:

    def __init__(self, xml_file_path):
        self.file_info = FileInfo(xml_file_path)

    def find_files(self):
        _files = {'xml': None, 'files': []}
        for f in os.listdir(self.file_info.dirname):
            file_path = os.path.join(self.file_info.dirname, f)
            file_info = FileInfo(file_path)
            if self.file_info.file_path == file_info.path:
                _files['xml'] = file_path
            elif self.file_info.name_prefix == file_info.name_prefix:
                _files['files'].append(file_path)
            elif file_info.name.startswith(self.file_info.name_prefix + '-'):
                _files['files'].append(file_path)
        return _files


"""
        article_pkg = ArticlePackage(xml_filepath)

        if os.path.isdir(report_file_path):
            dest_path = os.path.join(report_file_path, article_pkg.file_info.basename)
            dest_pkg = ArticlePackage(report_file_path)
        
            delete_file_or_folder(report_file_path)
        else:
            os.makedirs(report_file_path)
"""
