# coding: utf-8
import plumber


"""
usa os dados de artigos e journal já registrados
etc

"""


class RegistrationValidator:

    def __init__(self, configuration):
        self.configuration = configuration

    def validate(self, package, registered_data):
        data = package, registered_data
        data, report = self._run(data)
        return report

    def _run(self, data):
        return plumber.Pipeline(
            self.SetupPipe(),
            self.EndPipe()
        ).run(data, rewrap=True)

    class SetupPipe(plumber.Pipe):
        def transform(self, data):
            report = {}
            return data, report

    class EndPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed
