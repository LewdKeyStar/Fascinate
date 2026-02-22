from src.constants import *

from src.types.features.Frei0rFeature import Frei0rFeature
from src.types.parameters.FeatureParameter import FeatureParameter
from src.types.parameters.FeatureParameterRange import FeatureParameterRange

from src.decl.utils.frei0r_feature_decl_utils import (
    frei0r_position,
    frei0r_position_format,

    frei0r_color,
    frei0r_color_format
)

from src.decl.utils.common_decl_utils import percentage_format

# Advance warning :
# Frei0r numeric parameters are *always* double-precision floats,
# And their canonical user range is *usually* [0, 1].
# However, the filter calculations themselves may often project those values
# onto completely different ranges,
# rendering the overall framework cryptic.

# The lack of documentation means only source code clarifies the meaning of the parameters.
# Where such clarification is obtuse, the user will just have to kind of...guess.

# The provided default values, where applicable,
# May sometimes be self-determined,
# And others be defaults listed by gstreamer (https://gstreamer.freedesktop.org/documentation/frei0r)
# Which is the only extant (non-exhaustive, sometimes divergent in param order or number)
# documentation about frei0r.

frei0r_features: list[Frei0rFeature] = [

    # Regardless of the amount of tests conducted, select0r does nothing.
    # However, unlike other filters with no effect (pixs0r, cartoon, etc.)
    # I choose to comment it rather than not include it,
    # Just because it's such a huge block of parameters,
    # and it would be a pain to rewrite them later when this is inevitably fixed.

    # Frei0rFeature(
    #     name = "select0r",
    #     special_shorthand = "c0",
    #
    #     default_priority = HIGHEST_PRIORITY,
    #
    #     parameters = [
    #         FeatureParameter(
    #             "selected_color",
    #             type = frei0r_color,
    #
    #             default = DEFAULT_SELECT0R_SELECTED_COLOR,
    #
    #             value_format = frei0r_color_format
    #         ),
    #
    #         FeatureParameter(
    #             "invert_selection",
    #             type = bool,
    #             default = DEFAULT_SELECT0R_INVERT_SELECTION
    #         ),
    #
    #         # Those are *probably* percentages,
    #         # But code comments are silent on the matter, so I won't be too sure.
    #
    #         # Also, those are technically deltas for the chosen colorspace,
    #         # But imho it should always be RGB,
    #         # Since frei0r colors aren't supposed to be anything else.
    #
    #         FeatureParameter(
    #             "delta_red",
    #             type = float
    #         ),
    #
    #         FeatureParameter(
    #             "delta_green",
    #             type = float
    #         ),
    #
    #         FeatureParameter(
    #             "delta_blue",
    #             type = float
    #         ),
    #
    #         FeatureParameter(
    #             "slope",
    #             special_shorthand = "sl",
    #             type = float
    #         ),
    #
    #         # This parameter dictates the space used for the [0, 1]
    #         # converted value of each triplet member.
    #         # Translation : even though frei0r only allows for RGB color,
    #         # This plugin allows us to choose another.
    #         # This is almost certainly a bad idea.
    #
    #         FeatureParameter(
    #             "selection_subspace",
    #             special_shorthand = "sub",
    #             type = float
    #         ),
    #
    #         # Same for those last three. NO idea what they stand for.
    #
    #         FeatureParameter(
    #             "subspace_shape",
    #             special_shorthand = "sha",
    #             type = float
    #         ),
    #
    #         FeatureParameter(
    #             "edge_mode",
    #             type = float
    #         ),
    #
    #         FeatureParameter(
    #             "operation",
    #             special_shorthand = "op",
    #             type = float
    #         )
    #     ]
    # ),

    Frei0rFeature(
        name = "nosync0r",
        special_shorthand = "y0",

        default_priority = HIGHEST_PRIORITY,

        parameters = [

            # This is a percentage.
            # Note that 0% and 100% are equivalent.

            FeatureParameter(
                "hsync",
                type = float,

                range = FeatureParameterRange(0, 1),

                unit = "%",
                value_format = percentage_format
            ),

            # The vsync parameter is registered in source, but does nothing.

            # FeatureParameter(
            #     "vsync",
            #     type = float
            # )
        ]
    ),

    Frei0rFeature(
        name = "sobel",
        special_shorthand = "s0",

        default_priority = HIGHER_PRIORITY
    ),

    Frei0rFeature(
        name = "threshold0r",
        special_shorthand = "th0",

        default_priority = HIGHER_PRIORITY,

        # This is a value from [0, 255] mapped to [0, 1].

        parameters = [
            FeatureParameter(
                "threshold",
                type = float,
                range = FeatureParameterRange(0, 1),
                default = 1
            )
        ]
    ),

    Frei0rFeature(
        name = "cluster",
        special_shorthand = "r0",

        parameters = [

            # This is a pseudo-int.
            # It is not a range mapped to [0, 1],
            # rather all int values should be valid.

            FeatureParameter(
                "amount",
                special_shorthand = "m",
                type = float
            ),

            # However, it's not clear how this parameter ranges.

            FeatureParameter(
                "weight",
                type = float
            )
        ]
    ),

    Frei0rFeature(
        name = "rgbnoise",
        special_shorthand = "n0",

        default_priority = HIGHER_PRIORITY,

        # No conversion is performed on this parameter,
        # So supposedly, anything goes.

        parameters = [
            FeatureParameter(
                "amount",
                special_shorthand = "m",
                type = float,
                default = DEFAULT_RGB_NOISE_AMOUNT
            )
        ]
    ),

    Frei0rFeature(
        name = "dither",
        special_shorthand = "dh0",

        default_priority = HIGHER_PRIORITY,

        # Same as rgb noise, no conversion is performed.
        # This is particularly striking for the matrix ID,
        # Which *should* refer to an index into an array of magic matrices,
        # And thus be a pseudo-int.

        parameters = [
            FeatureParameter(
                "levels",
                special_shorthand = "lvl",
                type = float,
                default = DEFAULT_DITHER_LEVELS
            ),

            FeatureParameter(
                "matrixid",
                special_shorthand = "mid",
                type = float,
                default = DEFAULT_DITHER_MATRIX_ID
            )
        ]
    ),

    Frei0rFeature(
        name = "pixeliz0r",
        special_shorthand = "x0",

        default_priority = HIGHER_PRIORITY,

        parameters = [

            # These are, predictably, percentages of the frame dimensions.

            FeatureParameter(
                "block_height",
                type = float,

                range = FeatureParameterRange(0, 1),
                default = DEFAULT_PIXELIZ0R_BLOCK_HEIGHT,

                unit = "%",
                value_format = percentage_format
            ),

            FeatureParameter(
                "block_width",
                type = float,

                range = FeatureParameterRange(0, 1),
                default = DEFAULT_PIXELIZ0R_BLOCK_WIDTH,

                unit = "%",
                value_format = percentage_format
            ),

            # If this is set to true, the alpha channel is passed unchanged,
            # Rather than averaged over the pixel area.

            FeatureParameter(
                "passthrough_alpha",
                type = bool,
                default = DEFAULT_PIXELIZ0R_PASSTHROUGH_ALPHA
            )
        ]
    ),

    Frei0rFeature(
        name = "sharpness",
        special_shorthand = "sh0",

        # These values are collapsed

        parameters = [

            # From [0, 1] to [-1.5, 3.5]

            FeatureParameter(
                "amount",
                special_shorthand = "m",

                type = float,

                range = FeatureParameterRange(0, 1),
                default = DEFAULT_SHARPNESS_AMOUNT
            ),

            # From [0, 1] to [3.0, 11.0]

            FeatureParameter(
                "size",
                special_shorthand = "z",

                type = float,

                range = FeatureParameterRange(0, 1),
                default = DEFAULT_SHARPNESS_SIZE
            )
        ]
    ),

    Frei0rFeature(
        name = "vertigo",
        special_shorthand = "v0",

        parameters = [

            # This value is kept as-is.
            # This is strange.

            FeatureParameter(
                "phase_increment",
                type = float,
                default = DEFAULT_VERTIGO_PHASE_INCREMENT
            ),

            # This value is multiplied by 5.

            FeatureParameter(
                "zoom_rate",
                type = float,
                default = DEFAULT_VERTIGO_ZOOM_RATE
            )

            # No ranges are given.
        ]
    ),


    Frei0rFeature(
        name = "distort0r",
        special_shorthand = "d0",

        parameters = [

            # The amplitude is not scaled.

            FeatureParameter(
                "amplitude",
                special_shorthand = "amp",
                type = float,
                default = DEFAULT_DISTORT0R_AMPLITUDE
            ),

            # The frequency is scaled to [0, 200].
            # This means the default frequency is, reasonably enough, 1Hz.

            FeatureParameter(
                "frequency",
                special_shorthand = "freq",
                type = float,
                default = DEFAULT_DISTORT0R_FREQUENCY
            ),

            FeatureParameter(
                "use_velocity",
                special_shorthand = "vy",
                type = bool,
                default = DEFAULT_DISTORT0R_USE_VELOCITY
            ),

            # Similarly, velocity is scaled to [9, 2],
            # So the default velocity is in effect 1.

            FeatureParameter(
                "velocity",
                type = float,
                default = DEFAULT_DISTORT0R_VELOCITY
            )
        ],
    ),

    Frei0rFeature(
        name = "perspective",
        special_shorthand = "p0",

        # All perspective params are positions 2-uples.
        # frei0r normally accepts those as "X / Y", which is an awfully uncommon format,
        # So I added some sugar on top to make it "(X, Y)" instead.
        # (Quotes sadly needed, thanks to ffmpeg's special character parsing.)

        # Of course, those coordinates are, quite transparently, percentages of the frame dimensions.

        parameters = [
            FeatureParameter(
                "top_left",
                type = frei0r_position,
                default = DEFAULT_PERSPECTIVE_TOP_LEFT,

                value_format = frei0r_position_format
            ),

            FeatureParameter(
                "top_right",
                type = frei0r_position,
                default = DEFAULT_PERSPECTIVE_TOP_RIGHT,

                value_format = frei0r_position_format
            ),

            FeatureParameter(
                "bottom_left",
                type = frei0r_position,
                default = DEFAULT_PERSPECTIVE_BOTTOM_LEFT,

                value_format = frei0r_position_format
            ),

            FeatureParameter(
                "bottom_right",
                type = frei0r_position,
                default = DEFAULT_PERSPECTIVE_BOTTOM_RIGHT,

                value_format = frei0r_position_format
            )
        ]
    ),

    Frei0rFeature(
        name = "glow",
        special_shorthand = "w0",

        parameters = [

            # The blur value is divided by 20.
            # A default of zero seems fine.

            FeatureParameter(
                "blur",
                type = float
            )
        ]
    ),

    Frei0rFeature(
        name = "softglow",
        special_shorthand = "sw0",

        # None of those parameters are scaled.
        # This is strange.

        parameters = [
            FeatureParameter(
                "blur",
                special_shorthand = "br",
                type = float,
                default = DEFAULT_SOFTGLOW_BLUR
            ),

            FeatureParameter(
                "brightness",
                type = float,
                default = DEFAULT_SOFTGLOW_BRIGHTNESS
            ),

            FeatureParameter(
                "sharpness",
                special_shorthand = "sh",
                type = float,
                default = DEFAULT_SOFTGLOW_SHARPNESS
            ),

            FeatureParameter(
                "blur_blend",
                type = float,
                default = DEFAULT_SOFTGLOW_BLUR_BLEND
            )
        ]
    ),

    Frei0rFeature(
        name = "scanline0r",
        special_shorthand = "l0"

        # Where there should be parameters describing the scanlines,
        # In practice there are none, which makes it an on/off switch.
    ),

    Frei0rFeature(
        name = "glitch0r",
        special_shorthand = "g0",

        parameters = [

            # Those first three are percentages, specifically :

            # Raw (=>percentage chance),

            FeatureParameter(
                "glitch_frequency",
                type = float,

                range = FeatureParameterRange(0, 1),
                default = DEFAULT_GLITCH0R_GLITCH_FREQUENCY,

                unit = "%",
                value_format = percentage_format
            ),

            # Of the frame height,

            FeatureParameter(
                "block_height",
                type = float,

                range = FeatureParameterRange(0, 1),
                default = DEFAULT_GLITCH0R_BLOCK_HEIGHT,

                unit = "%",
                value_format = percentage_format
            ),

            # Of the frame width ;

            FeatureParameter(
                "shift_intensity",
                type = float,

                range = FeatureParameterRange(0, 1),
                default = DEFAULT_GLITCH0R_SHIFT_INTENSITY,

                unit = "%",
                value_format = percentage_format
            ),

            # And this one is scaled from a 0-1 float to a rounded 0-5 int.

            FeatureParameter(
                "color_glitching_intensity",
                type = float,

                range = FeatureParameterRange(0, 1),
                default = DEFAULT_GLITCH0R_COLOR_GLITCHING_INTENSITY
            )
        ]
    )
]
