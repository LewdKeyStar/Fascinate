from src.constants import UINT32_MAX

from src.types.settings.FeatureEnableSetting import FeatureEnableSetting
from src.types.settings.FeatureSettingRange import FeatureSettingRange

from src.parser_namespace import runtime_value, is_enabled_at_runtime

from src.decl.utils.common_decl_utils import percentage_format

from math import modf

# A declarative list of filter enable settings,
# And the respective conditions for which they are considered "active".
# For use in output naming and reflective feature calls.

enable_settings: list[FeatureEnableSetting] = [
    FeatureEnableSetting(
        name = "start_at",
        include_in_filename = lambda feature_name, value: value > 0,
        special_shorthand = "s"
    ),

    FeatureEnableSetting(
        name = "end_at",
        include_in_filename = lambda feature_name, value: value < UINT32_MAX,
        special_shorthand = "e",
        default = UINT32_MAX
    ),

    FeatureEnableSetting(
        name = "every",
        include_in_filename = lambda feature_name, value: value > 1,
        special_shorthand = "n",
        default = 1
    ),

    FeatureEnableSetting(
        name = "pause",
        include_in_filename = lambda feature_name, value: value > 0
    ),

    FeatureEnableSetting(
        name = "active",
        include_in_filename = lambda feature_name, value: value > 0
    ),

    FeatureEnableSetting(
        name = "invert_pause",
        type = bool,
        include_in_filename = lambda feature_name, value: value,
        default = False
    ),

    # If a syncing BPM is provided, the "pause" and "active" options are ignored.

    # FIXME : This is not very clean ; ideally it should be impossible to provided them together.
    # However argparse has deprecated nesting argument groups, such that something like :
    # [[-p -a] | [-bpm -bap]]
    # Cannot be done.
    # The only alternative would be subcommands :
    # fascinate [pause-mode [-p -a] | bpm-mode [-bpm -bap]]
    # which is not feasible since the same "subcommand" could be invoked multiple times, one for each filter...

    FeatureEnableSetting(
        name = "bpm",
        special_shorthand = "bpm",
        type = float,

        include_in_filename = lambda feature_name, value: value > 0,

        value_format = lambda feature_name, value: (
            int(value) if modf(value)[0] == 0
            else value
        )
    ),

    FeatureEnableSetting(
        name = "bpm_active_percent",
        type = float,
        unit = "%",

        range = FeatureSettingRange(0.0, 1.0),
        default = 0.5,

        include_in_filename = lambda feature_name, value: (
            runtime_value(feature_name, "bpm") > 0
        ),

        value_format = lambda feature_name, value: percentage_format(value)
    ),

    FeatureEnableSetting(
        name = "random",
        special_shorthand = "rand",
        type = bool,

        default = False,

        include_in_filename = lambda feature_name, value: value
    ),

    FeatureEnableSetting(
        name = "random_seed",
        special_shorthand = "seed",
        type = int,

        include_in_filename = lambda feature_name, value: (
            is_enabled_at_runtime(feature_name, "random")
        )
    ),

    FeatureEnableSetting(
        name = "random_probability",
        special_shorthand = "prob",
        type = float,

        unit = "%",

        range = FeatureSettingRange(0.0, 1.0),
        default = 0.5,

        include_in_filename = lambda feature_name, value: (
            is_enabled_at_runtime(feature_name, "random")
        ),

        value_format = lambda feature_name, value: percentage_format(value)
    )
]
