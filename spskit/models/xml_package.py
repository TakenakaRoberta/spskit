from spskit.models.manifest import Manifest


class XMLPackage:

    def __init__(self, id: str = None, manifest: dict = None):
        assert any([id, manifest])
        self.manifest = manifest or Manifest.new(id)

    def id(self):
        return self.manifest.get("id", "")

    def created(self):
        return self.manifest.get("created", "")

    def updated(self):
        return self.manifest.get("updated", "")

    @property
    def manifest(self):
        return deepcopy(self._manifest)

    @manifest.setter
    def manifest(self, value: dict):
        self._manifest = value

    @property
    def name(self):
        return Manifest.get_metadata(self.manifest, "name", {})

    @name.setter
    def name(self, value: str):
        try:
            value = str(value)
        except (TypeError, ValueError):
            raise TypeError(
                "cannot set name with value " '"%s": value must be str' % value
            ) from None
        self.manifest = Manifest.set_metadata(self._manifest, "name", value)

    @property
    def xml_file(self):
        return Manifest.get_metadata(self.manifest, "xml_file", {})

    @xml_file.setter
    def xml_file(self, value: str):
        try:
            value = str(value)
        except (TypeError, ValueError):
            raise TypeError(
                "cannot set xml_file with value " '"%s": value must be str' % value
            ) from None
        self.manifest = Manifest.set_metadata(self._manifest, "xml_file", value)

    @property
    def related_files(self):
        return Manifest.get_metadata(self.manifest, "related_files", [])

    @related_files.setter
    def related_files(self, value: list):
        try:
            value = list(value)
        except (TypeError, ValueError):
            raise TypeError(
                "cannot set related_files with value " '"%s": value must be list' % value
            ) from None
        self.manifest = Manifest.set_metadata(self._manifest, "related_files", value)
