from src.constants import UINT32_MAX

from src.types.FeatureSetting import FeatureSetting

# A declarative list of filter enable settings,
# And the respective conditions for which they are considered "active".
# For use in output naming and reflective feature calls.

enable_settings: list[FeatureSetting] = [
    FeatureSetting(
        name = "start_at",
        active_condition = lambda x: x > 0,
        special_shorthand = "s"
    ),

    FeatureSetting(
        name = "end_at",
        active_condition = lambda x: x < UINT32_MAX,
        special_shorthand = "e",
        default = UINT32_MAX
    ),

    FeatureSetting(
        name = "every",
        active_condition = lambda x: x > 1,
        special_shorthand = "n",
        default = 1
    ),

    FeatureSetting(
        name = "pause",
        active_condition = lambda x: x > 0
    ),

    FeatureSetting(
        name = "active",
        active_condition = lambda x: x > 0
    ),

    FeatureSetting(
        name = "invert_pause",
        type = bool,
        active_condition = lambda x: x,
        default = False
    ),

    # If a syncing BPM is provided, the "pause" and "active" options are ignored.

    # FIXME : This is not very clean ; ideally it should be impossible to provided them together.
    # However argparse has deprecated nesting argument groups, such that something like :
    # [[-p -a] | [-bpm -bap]]
    # Cannot be done.
    # The only alternative would be subcommands :
    # strobify [pause-mode [-p -a] | bpm-mode [-bpm -bap]]
    # which is not feasible since the same "subcommand" could be invoked multiple times, one for each filter...

    FeatureSetting(
        name = "bpm",
        special_shorthand = "bpm",
        type = float,
        active_condition = lambda x: x > 0
    ),

    FeatureSetting(
        name = "bpm_active_percent",
        type = float,
        active_condition = lambda x: x > 0
    )
]

video_settings: list[FeatureSetting] = [
    FeatureSetting(
        name = "alpha",
        type = float,
        special_shorthand = "l",
        default = 1.0
    )
]

settings = enable_settings + video_settings

valid_setting_names = [setting.name for setting in settings]
