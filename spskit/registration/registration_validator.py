# coding: utf-8
from utils.report_manager import ReportManager, Pipe, Pipeline


"""
usa os dados de artigos e journal já registrados
etc

"""


class RegistrationValidator:

    def __init__(self, configuration):
        self.configuration = configuration
        self.report_manager = ReportManager(configuration)

    def validate(self, package, registered_data):
        data = package, registered_data
        package, registered_data, report = self.report_manager.create(data, self._plumber_pipeline)
        return report

    @property
    def _plumber_pipeline(self):
        return Pipeline(self.SetupPipe(), self.SetupPipe())

    class SetupPipe(Pipe):

        def transform(self, data):
            report = {}
            return data, report
