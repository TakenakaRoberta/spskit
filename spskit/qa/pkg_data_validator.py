# coding: utf-8
import plumber

"""
usa os dados de artigos e journal já registrados
etc

"""


class PkgDataValidator:

    def __init__(self, configuration):
        self.configuration = configuration

    def validate(self, data):
        data, report = self._plumber_pipeline.run(data, rewrap=True)
        return data, report

    @property
    def _plumber_pipeline(self):
        return plumber.Pipeline(
            self.SetupPipe(),
            self.EndPipe())

    class SetupPipe(plumber.Pipe):
        def transform(self, data):
            report = {}
            return data, report

    class EndPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed
