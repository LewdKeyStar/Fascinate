from src.decl.filter_settings_list import settings, valid_setting_names

class FeatureSettingDefaultValues(dict):

    @property
    def provided_setting_names(self):
        return self.keys()

    def __post_init__(self):
        for provided_setting_name in self.provided_setting_names:
            if provided_setting_name not in valid_setting_names:
                raise ValueError("Default value declared for nonexistent setting")
