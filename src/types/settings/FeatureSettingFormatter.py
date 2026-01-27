from dataclasses import dataclass

from src.types.abstract.options.FeatureOptionFormatter import FeatureOptionFormatter

@dataclass(repr = False)
class FeatureSettingFormatter(FeatureOptionFormatter):

    @property
    def setting(self):
        return self.option

    @property
    def setting_value(self):
        return self.option_value

    def _include_in_filename(self):
        return self.setting.include_in_filename(self.feature.name, self.setting_value)

    def _unit(self):
        return self.setting.unit(self.feature.name, self.setting_value)

    def _value_format(self):
        return self.setting.value_format(self.feature.name, self.setting_value)
