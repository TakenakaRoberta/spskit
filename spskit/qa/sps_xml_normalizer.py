# coding: utf-8
import plumber
from spskit.utils.xml_utils import XML


class SPSXMLNormalizer:

    def __init__(self, configuration):
        self.configuration = configuration

    def normalize(self, xml_content):
        transformed_data = self._plumber_pipeline.run(
            xml_content,
            rewrap=True)
        return transformed_data

    @property
    def _plumber_pipeline(self):
        return plumber.Pipeline(
            self.SetupPipe(),
            self.EndPipe()
        )

    class SetupPipe(plumber.Pipe):
        def transform(self, data):
            xml_content = data
            sps_xml = XML(xml_content)
            return xml_content, sps_xml

    class EndPipe(plumber.Pipe):
        def transform(self, data):
            xml_content, sps_xml = data
            return sps_xml.text
