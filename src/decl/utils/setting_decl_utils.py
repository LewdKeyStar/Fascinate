from src.parser_namespace import is_enabled_at_runtime

# value isn't used in these functions,
# But is part of the signature so they can be directly passed as the decl lambdas.

def crop_corner_mode_enabled(feature_name, value):
    return (
        is_enabled_at_runtime(f"{feature_name}", "crop")
        and
        not is_enabled_at_runtime(f"{feature_name}", "crop_center_mode")
    )

def crop_center_mode_enabled(feature_name, value):
    return (
        is_enabled_at_runtime(f"{feature_name}", "crop")
        and
        is_enabled_at_runtime(f"{feature_name}", "crop_center_mode")
    )
