from src.types.settings.FilterBearingFeatureVideoSetting import FilterBearingFeatureVideoSetting
from src.types.settings.FeatureSettingRange import FeatureSettingRange

from src.decl.utils.common_decl_utils import percentage_format

filter_bearing_video_settings: list[FilterBearingFeatureVideoSetting] = [
    FilterBearingFeatureVideoSetting(
        name = "alpha",
        special_shorthand = "l",
        type = float,
        unit = "%",

        requires_overlay = True,

        range = FeatureSettingRange(0.0, 1.0),
        default = 1.0,

        include_in_filename = lambda feature_name, value: value < 1.0,

        value_format = lambda feature_name, value: percentage_format(value)
    ),

    FilterBearingFeatureVideoSetting(
        name = "fade_in",
        include_in_filename = lambda feature_name, value: value > 0,

        requires_overlay = True,

        video_settings_used_in_setting_filter = ["fade_in_function"],

        enable_settings_used_in_setting_filter = [
            "start_at",
            "pause",
            "invert_pause"
        ],

        video_info_used_in_setting_filter = ["duration"]
    ),

    FilterBearingFeatureVideoSetting(
        name = "fade_out",
        include_in_filename = lambda feature_name, value: value > 0,

        requires_overlay = True,

        video_settings_used_in_setting_filter = ["fade_out_function"],

        enable_settings_used_in_setting_filter = ["end_at"],

        video_info_used_in_setting_filter = ["duration"]
    ),

    FilterBearingFeatureVideoSetting(
        name = "fade_cyclical",
        type = bool,

        requires_overlay = True,

        own_value_used_in_setting_filter = False,

        video_settings_used_in_setting_filter = [
            "fade_in",
            "fade_out",
            "fade_in_function",
            "fade_out_function",
            "fade_cyclical_peak",
            "fade_cyclical_trough",
            "fade_cyclical_sync",
            "fade_cyclical_sync_in_percent",
            "fade_cyclical_sync_out_percent"
        ],

        enable_settings_used_in_setting_filter = [
            "start_at",
            "end_at",
            "pause",
            "active",
            "invert_pause"
        ],

        video_info_used_in_setting_filter = ["duration"],

        default = False,
        include_in_filename = lambda feature_name, value: value
    ),

    FilterBearingFeatureVideoSetting(
        name = "crop",
        special_shorthand = "cr",
        type = bool,

        requires_overlay = True,

        own_value_used_in_setting_filter = False,

        video_settings_used_in_setting_filter = [
            "crop_top", "crop_bottom", "crop_left", "crop_right",

            "crop_center_x", "crop_center_y",
            "crop_width", "crop_height",

            "crop_edge_fade",

            "crop_center_mode", "crop_relative_mode"
        ],

        video_info_used_in_setting_filter = ["resolution"],

        default = False,
        include_in_filename = lambda feature_name, value: value
    )
]
