# coding: utf-8
import plumber


Pipe = plumber.Pipe
Pipeline = plumber.Pipeline


class ReportManager:

    def __init__(self, configuration, plumber_pipeline, start=None, end=None):
        self.configuration = configuration
        self.plumber_pipeline_start = start or Pipeline(self.SetupPipe())
        self.plumber_pipeline = plumber_pipeline or Pipeline(self.AnyPipe())
        self.plumber_pipeline_end = end or Pipeline(self.EndPipe())

    def create(self, data):
        transformed_data = self._start(data, rewrap=True)
        transformed_data = self._middle(transformed_data, rewrap=True)
        transformed_data = self._end(transformed_data, rewrap=True)
        return next(transformed_data)

    def _start(self, data):
        transformed_data = self.plumber_pipeline_start.run(data, rewrap=True)
        return next(transformed_data)

    def _middle(self, data):
        transformed_data = self.plumber_pipeline.run(data, rewrap=True)
        return next(transformed_data)

    def _end(self, data):
        transformed_data = self.plumber_pipeline_end.run(data, rewrap=True)
        return next(transformed_data)

    class SetupPipe(Pipe):
        def transform(self, data):
            report = {}
            return data, report

    class AnyPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed

    class EndPipe(Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed
