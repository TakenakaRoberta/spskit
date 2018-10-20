# coding: utf-8
import plumber


class SPSXMLNormalizer:

    def __init__(self, configuration):
        self.configuration = configuration

    def normalize(self, data):
        transformed_data = self._plumber_pipeline.run(data, rewrap=True)
        return next(transformed_data)

    @property
    def _plumber_pipeline(self):
        return plumber.Pipeline(self.SetupPipe(), self.EndPipe())

    class SetupPipe(plumber.Pipe):

        def transform(self, data):
            report = {}
            return data, report

    class EndPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed
