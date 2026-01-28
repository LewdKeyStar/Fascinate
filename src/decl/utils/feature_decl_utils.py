import src.constants

from src.types.parameters.FeatureParameter import FeatureParameter
from src.types.parameters.FeatureParameterRange import FeatureParameterRange

def eq_filter_parameters(suffix):

    param_name_list = [
        "contrast",
        "brightness",
        "saturation",
        "gamma",
        "gamma_r",
        "gamma_g",
        "gamma_b",
        "gamma_weight"
    ]

    return [
        FeatureParameter(
            name,
            special_shorthand = "sat" if name == "saturation" else None, # avoid conflict with start_at
            type = float,
            range = FeatureParameterRange(
                getattr(src.constants, f"MIN_EQ_{name.upper()}_{suffix}"),
                getattr(src.constants, f"MAX_EQ_{name.upper()}_{suffix}")
            ),
            default = getattr(src.constants, f"DEFAULT_EQ_{name.upper()}_{suffix}")
        )

        for name in param_name_list
    ]
