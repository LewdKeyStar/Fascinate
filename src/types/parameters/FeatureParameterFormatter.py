from dataclasses import dataclass

from src.types.abstract.options.FeatureOptionFormatter import FeatureOptionFormatter

@dataclass(repr = False)
class FeatureParameterFormatter(FeatureOptionFormatter):

    @property
    def param(self):
        return self.option

    @property
    def param_value(self):
        return self.option_value

    def _include_in_filename(self):
        return self.param.include_in_filename(self.param_value)

    def _unit(self):
        return self.param.unit(self.param_value)

    def _value_format(self):
        return self.param.value_format(self.param_value)
