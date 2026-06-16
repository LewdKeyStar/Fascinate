from src.constants import *

from src.types.features.CustomFeature import CustomFeature

from src.types.features.FeatureCombineMode import FeatureCombineMode

from src.types.parameters.FeatureParameter import FeatureParameter
from src.types.parameters.FeatureParameterApplicableComponent import FeatureParameterApplicableComponent
from src.types.parameters.FeatureParameterRange import FeatureParameterRange
from src.types.parameters.FeatureParameterChoices import FeatureParameterChoices

from src.types.settings.FeatureSettingDefaultValues import FeatureSettingDefaultValues

from src.parser_namespace import option_runtime_value

from src.decl.utils.argparse_types.common_argparse_types import (
    video_time,
    x_coordinate,
    y_coordinate
)

from src.decl.utils.common_decl_utils import (
    x_percentage_format,
    y_percentage_format
)

from os.path import sep

custom_features: list[CustomFeature] = [
    CustomFeature(
        name = "speed_change",

        default_priority = HIGHEST_PRIORITY,

        has_audio_component = True,

        can_receive_enable_settings = False,
        can_receive_video_settings = False,

        combine_mode = FeatureCombineMode.REPLACE,

        parameters = (
            FeatureParameter(
                "factor",
                applicable_component = FeatureParameterApplicableComponent.BOTH_COMPONENTS,
                type = float,
                default = DEFAULT_SPEED_CHANGE_FACTOR
            ),
            FeatureParameter(
                "preserve_pitch",
                applicable_component = FeatureParameterApplicableComponent.AUDIO_COMPONENT_ONLY,
                type = bool,
                default = DEFAULT_SPEED_CHANGE_PRESERVE_PITCH
            ),
            FeatureParameter(
                "preserve_formants",
                applicable_component = FeatureParameterApplicableComponent.AUDIO_COMPONENT_ONLY,
                type = bool,
                default = DEFAULT_SPEED_CHANGE_PRESERVE_FORMANTS
            )
        )
    ),

    CustomFeature(
        name = "afterimages",

        default_priority = HIGHER_PRIORITY,

        special_shorthand = "afi",

        combine_mode = FeatureCombineMode.PRE_MERGED,

        default_setting_values = FeatureSettingDefaultValues({
            "alpha": DEFAULT_AFTERIMAGES_ALPHA
        }),

        parameters = (
            FeatureParameter(
                "amount",
                special_shorthand = "m",
                default = DEFAULT_AFTERIMAGES_AMOUNT
            ),

            FeatureParameter(
                "delay",
                type = video_time,
                default = DEFAULT_AFTERIMAGES_DELAY
            ),

            FeatureParameter(
                "start_white",
                special_shorthand = "w",
                type = bool,
                default = DEFAULT_AFTERIMAGES_START_WHITE
            ),

            FeatureParameter(
                "extend",
                special_shorthand = "xt",
                type = bool,
                default = DEFAULT_AFTERIMAGES_EXTEND
            )
        ),

        settings_used_in_filter = ["alpha"]

    ),

    CustomFeature(
        name = "shake",

        default_priority = LOWEST_PRIORITY,

        special_shorthand = "ss",

        parameters = [
            FeatureParameter(
                "axis",
                special_shorthand = "ax",
                type = str,
                choices = FeatureParameterChoices(VALID_AXES),
                default = DEFAULT_SHAKE_AXIS
            ),
            FeatureParameter(
                "amplitude",
                special_shorthand = "amp",
                default = DEFAULT_SHAKE_AMPLITUDE,
                unit = "px"
            ),
            FeatureParameter(
                "frequency",
                type = float,
                default = DEFAULT_SHAKE_FREQUENCY,
                unit = "hz"
            ),
            FeatureParameter("dampen", type = float, default = DEFAULT_SHAKE_DAMPEN),
            FeatureParameter("blur_radius", type = int, default = DEFAULT_SHAKE_BLUR)
        ],

        video_info_used_in_filter = ["fps"],
        settings_used_in_filter = ["start_at", "pause", "active"]
    ),

    CustomFeature(
        name = "zoom",

        default_priority = LOWEST_PRIORITY,

        combine_mode = FeatureCombineMode.OVERLAY,

        default_setting_values = FeatureSettingDefaultValues({
            "alpha": DEFAULT_ZOOM_ALPHA
        }),

        parameters = [
            FeatureParameter(
                "factor",
                type = float,
                range = FeatureParameterRange(MIN_ZOOM_FACTOR, MAX_ZOOM_FACTOR),
                default = DEFAULT_ZOOM_FACTOR,
            ),

            FeatureParameter(
                "center_x",
                special_shorthand = "x",

                type = x_coordinate,

                default = DEFAULT_ZOOM_CENTER_X,

                unit = "%",

                value_format = x_percentage_format
            ),

            FeatureParameter(
                "center_y",
                special_shorthand = "y",

                type = y_coordinate,

                default = DEFAULT_ZOOM_CENTER_Y,

                unit = "%",

                value_format = y_percentage_format
            )
        ],

        video_info_used_in_filter = ["resolution", "fps"]
    ),

    CustomFeature(
        name = "intersperse",
        special_shorthand = "isp",

        # Because of how the movie filter works, this filter has to pre-merge its alpha.
        combine_mode = FeatureCombineMode.PRE_MERGED,

        parameters = [

            FeatureParameter(
                "source",
                special_shorthand = "so",
                type = str,

                # This means not specifying the source will lead to an error.
                default = "",

                value_format = lambda value: value.replace(sep, "+")
            ),

            FeatureParameter(
                "scale",
                special_shorthand = "sc",

                type = bool,
                default = DEFAULT_INTERSPERSE_SCALE
            ),

            FeatureParameter(
                "unscaled_x",
                special_shorthand = "x",

                type = x_coordinate,
                default = DEFAULT_INTERSPERSE_UNSCALED_X,

                unit = "%",

                value_format = x_percentage_format
            ),

            FeatureParameter(
                "unscaled_y",
                special_shorthand = "y",

                type = y_coordinate,
                default = DEFAULT_INTERSPERSE_UNSCALED_Y,

                unit = "%",

                value_format = y_percentage_format
            ),

            # This parameter is for use with the seek_point option of movie,
            # Reading the stream only from the given frame.
            # However, seek_point does not work,
            # so in effect, this parameter does nothing.

            FeatureParameter(
                "start_frame",
                type = int
            ),

            # This parameter time-pads the interspersed movie for the given amount of frames.
            # This allows for a start_at that actually starts on frame 0 of the movie.

            FeatureParameter(
                "start_delay",
                type = int
            ),

            FeatureParameter(
                "loop",
                special_shorthand = "lp",
                type = bool,
                default = DEFAULT_INTERSPERSE_LOOP
            ),

            FeatureParameter(
                "extend",
                special_shorthand = "xt",
                type = bool,
                default = DEFAULT_INTERSPERSE_EXTEND
            )
        ],

        settings_used_in_filter = ["alpha"],

        video_info_used_in_filter = ["resolution", "fps", "duration"]
    )
]
