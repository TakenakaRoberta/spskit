# coding: utf-8
from spskit.utils.report_manager import ReportManager, Pipe, Pipeline


"""
usa os dados de artigos e journal já registrados
etc

"""


class PkgDataValidator:

    def __init__(self, configuration):
        self.configuration = configuration
        self.report_manager = ReportManager(configuration, self._plumber_pipeline)

    def validate(self, data):
        data, report = self.report_manager.create(data)
        return data, report

    @property
    def _plumber_pipeline(self):
        return Pipeline(self.SetupPipe(), self.EndPipe())

    class SetupPipe(Pipe):

        def transform(self, data):
            report = {}
            return data, report

    class EndPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

