# coding: utf-8
import plumber


class SPSXML:

    def __init__(self, configuration):
        self.configuration = configuration

    def normalize(self, xml):
        transformed_data = self._plumber_pipeline.run(
            xml,
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
            xml = data
            return xml

    class EndPipe(plumber.Pipe):
        def transform(self, data):
            xml = data
            return xml
