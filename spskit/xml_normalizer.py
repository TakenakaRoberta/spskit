# coding: utf-8
import plumber


class XMLNormalizer:

    def __init__(self, configuration):
        self.configuration = configuration

    def normalize(self, data):
        plumber_pipeline = plumber.Pipeline()
        transformed_data = plumber_pipeline.run(data, rewrap=True)
        return next(transformed_data)
