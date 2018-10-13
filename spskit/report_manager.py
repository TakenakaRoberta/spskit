# coding: utf-8
import plumber


Pipe = plumber.Pipe
Pipeline = plumber.Pipeline


class ReportManager:

    def __init__(self, configuration):
        self.configuration = configuration

    def create(self, data, plumber_pipeline):
        transformed_data = plumber_pipeline.run(data, rewrap=True)
        return next(transformed_data)
