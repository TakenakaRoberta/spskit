# coding: utf-8
from copy import deepcopy

import plumber


class SPSXML:

    def __init__(self, configuration):
        self.configuration = configuration

    def normalize(self, xml):
        raw, transformed_data = self._plumber_pipeline.run(xml, rewrap=True)
        return transformed_data

    @property
    def _plumber_pipeline(self):
        return plumber.Pipeline(
            self.SetupPipe(),
        )

    class SetupPipe(plumber.Pipe):
        def transform(self, data):
            transformed = data
            raw = data
            return raw, transformed

    class EndPipe(plumber.Pipe):
        def transform(self, data):
            raw, transformed = data
            return raw, transformed
