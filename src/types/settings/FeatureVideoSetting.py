from dataclasses import dataclass, field
from collections.abc import Callable

from src.types.settings.FeatureSetting import FeatureSetting

@dataclass(kw_only = True)
class FeatureVideoSetting(FeatureSetting):
    enabled: Callable[[any], bool] = lambda x: True

    requires_overlay: bool = False

    enable_settings_used_in_setting_filter: list[str] = field(default_factory = list)
    video_info_used_in_setting_filter: list[str] = field(default_factory = list)

    def __post_init__(self):
        self.enabled = self.include_in_filename
