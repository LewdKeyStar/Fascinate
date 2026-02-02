from src.types.settings.FilterLessFeatureVideoSetting import FilterLessFeatureVideoSetting
from src.types.settings.FeatureSettingRange import FeatureSettingRange
from src.types.settings.FeatureSettingChoices import FeatureSettingChoices

from src.constants import VALID_FADE_FUNCTIONS, DEFAULT_FADE_FUNCTION

from src.parser_namespace import is_enabled_at_runtime

from src.decl.utils.common_decl_utils import (
    percentage_format,
    relative_format,
    percentage_unit
)

from src.decl.utils.setting_decl_utils import (
    crop_corner_mode_enabled,
    crop_center_mode_enabled
)

filterless_video_settings: list[FilterLessFeatureVideoSetting] = [

    FilterLessFeatureVideoSetting(
        name = "fade_in_function",
        type = str,
        choices = FeatureSettingChoices(VALID_FADE_FUNCTIONS),
        default = DEFAULT_FADE_FUNCTION,

        include_in_filename = lambda feature_name, value: (
            is_enabled_at_runtime(f"{feature_name}", "fade_in")
            or
            is_enabled_at_runtime(f"{feature_name}", "fade_cyclical")
        )
    ),

    FilterLessFeatureVideoSetting(
        name = "fade_out_function",
        type = str,
        choices = FeatureSettingChoices(VALID_FADE_FUNCTIONS),
        default = DEFAULT_FADE_FUNCTION,

        include_in_filename = lambda feature_name, value: (
            is_enabled_at_runtime(f"{feature_name}", "fade_out")
            or
            is_enabled_at_runtime(f"{feature_name}", "fade_cyclical")
        )
    ),

    # The number of frames in a non-synced cyclical fade between the in and out phase,
    # where the filter stays at full opacity.

    FilterLessFeatureVideoSetting(
        name = "fade_cyclical_peak",
        include_in_filename = lambda feature_name, value: value > 0
    ),

    # The number of frames separating two full in-out cycles of a non-synced cyclical fade.

    FilterLessFeatureVideoSetting(
        name = "fade_cyclical_trough",
        include_in_filename = lambda feature_name, value: value > 0
    ),

    # Sync a cyclical fade a to a feature's active period.
    # If this is enabled, the fade in, fade out, peak and trough values are ignored.

    FilterLessFeatureVideoSetting(
        name = "fade_cyclical_sync",
        type = bool,
        default = False,
        include_in_filename = lambda feature_name, value: value
    ),

    # These percentages are used instead, with peak and trough deduced from them.

    FilterLessFeatureVideoSetting(
        name = "fade_cyclical_sync_in_percent",
        type = float,
        unit = "%",

        range = FeatureSettingRange(0.0, 1.0),
        default = 0.5,

        include_in_filename = lambda feature_name, value: (
            is_enabled_at_runtime(f"{feature_name}", "fade_cyclical_sync")
        ),

        value_format = lambda feature_name, value: percentage_format(value)
    ),

    FilterLessFeatureVideoSetting(
        name = "fade_cyclical_sync_out_percent",
        type = float,
        unit = "%",

        range = FeatureSettingRange(0.0, 1.0),
        default = 0.5,

        include_in_filename = lambda feature_name, value: (
            is_enabled_at_runtime(f"{feature_name}", "fade_cyclical_sync")
        ),

        value_format = lambda feature_name, value: percentage_format(value)
    ),

    FilterLessFeatureVideoSetting(
        name = "crop_top",
        special_shorthand = "crt",
        type = float,

        default = -1,

        unit = lambda feature_name, value: (
            percentage_unit(if_is_relative = f"{feature_name}_crop")
        ),

        value_format = lambda feature_name, value: (
            relative_format(value, feature_name = f"{feature_name}_crop")
        ),

        include_in_filename = crop_corner_mode_enabled
    ),

    FilterLessFeatureVideoSetting(
        name = "crop_bottom",
        special_shorthand = "crb",
        type = float,

        default = -1,

        unit = lambda feature_name, value: (
            percentage_unit(if_is_relative = f"{feature_name}_crop")
        ),

        value_format = lambda feature_name, value: (
            relative_format(value, feature_name = f"{feature_name}_crop")
        ),

        include_in_filename = crop_corner_mode_enabled
    ),

    FilterLessFeatureVideoSetting(
        name = "crop_left",
        special_shorthand = "crl",
        type = float,

        default = -1,

        unit = lambda feature_name, value: (
            percentage_unit(if_is_relative = f"{feature_name}_crop")
        ),

        value_format = lambda feature_name, value: (
            relative_format(value, feature_name = f"{feature_name}_crop")
        ),

        include_in_filename = crop_corner_mode_enabled
    ),

    FilterLessFeatureVideoSetting(
        name = "crop_right",
        special_shorthand = "crr",
        type = float,

        default = -1,

        unit = lambda feature_name, value: (
            percentage_unit(if_is_relative = f"{feature_name}_crop")
        ),

        value_format = lambda feature_name, value: (
            relative_format(value, feature_name = f"{feature_name}_crop")
        ),

        include_in_filename = crop_corner_mode_enabled
    ),

    FilterLessFeatureVideoSetting(
        name = "crop_center_x",
        special_shorthand = "crx",
        type = float,

        default = -1,

        unit = lambda feature_name, value: (
            percentage_unit(if_is_relative = f"{feature_name}_crop")
        ),

        value_format = lambda feature_name, value: (
            relative_format(value, feature_name = f"{feature_name}_crop")
        ),

        include_in_filename = crop_center_mode_enabled
    ),

    FilterLessFeatureVideoSetting(
        name = "crop_center_y",
        special_shorthand = "cry",
        type = float,

        default = -1,

        unit = lambda feature_name, value: (
            percentage_unit(if_is_relative = f"{feature_name}_crop")
        ),

        value_format = lambda feature_name, value: (
            relative_format(value, feature_name = f"{feature_name}_crop")
        ),

        include_in_filename = crop_center_mode_enabled
    ),

    FilterLessFeatureVideoSetting(
        name = "crop_width",
        special_shorthand = "crw",
        type = float,

        default = -1,

        unit = lambda feature_name, value: (
            percentage_unit(if_is_relative = f"{feature_name}_crop")
        ),

        value_format = lambda feature_name, value: (
            relative_format(value, feature_name = f"{feature_name}_crop")
        ),

        include_in_filename = crop_center_mode_enabled
    ),

    FilterLessFeatureVideoSetting(
        name = "crop_height",
        special_shorthand = "crh",
        type = float,

        default = -1,

        unit = lambda feature_name, value: (
            percentage_unit(if_is_relative = f"{feature_name}_crop")
        ),

        value_format = lambda feature_name, value: (
            relative_format(value, feature_name = f"{feature_name}_crop")
        ),

        include_in_filename = crop_center_mode_enabled
    ),

    FilterLessFeatureVideoSetting(
        name = "crop_edge_fade",
        special_shorthand = "cref",

        include_in_filename = lambda feature_name, value: (
            is_enabled_at_runtime(f"{feature_name}", "crop")
            and
            value > 0
        )
    ),

    FilterLessFeatureVideoSetting(
        name = "crop_center_mode",
        special_shorthand = "crcm",
        type = bool,
        default = False,

        include_in_filename = False
    ),

    FilterLessFeatureVideoSetting(
        name = "crop_relative_mode",
        special_shorthand = "crrm",
        type = bool,
        default = False,

        include_in_filename = False
    ),
]
