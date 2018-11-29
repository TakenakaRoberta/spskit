
from spskit.utils.files_utils import FileInfo


class PackageFiles:

    def __init__(self, any_files):

        self.articles_files = any_files

    @property
    def articles_files(self):
        return self._organized

    @articles_files.setter
    def articles_files(self, any_files):
        files = [FileInfo(f) for f in any_files]
        xml_prefixes = [f.name_prefix for f in files if f.ext == '.xml']

        self._organized = {}
        self.invalid_files = []

        for file_info in files:
            prefix = file_info.name_prefix
            if prefix not in xml_prefixes:
                prefix = prefix[:prefix.rfind('-')]
            if prefix in xml_prefixes:
                if self._organized.get(prefix) is None:
                    self._organized[prefix] = {}
                    self._organized[prefix]['xml'] = None
                    self._organized[prefix]['related_files'] = []
                if file_info.ext == '.xml':
                    self._organized[prefix]['xml'] = file_info.file_path
                else:
                    self._organized[prefix]['related_files'].append(file_info.file_path)
            else:
                self.invalid_files.append(file_info.file_path)
        self._organized = list(self._organized.values())
