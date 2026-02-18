from src.parser_namespace import is_enabled_at_runtime

from math import modf

def conditional_int(value):
    return (
        int(value) if modf(value)[0] == 0
        else value
    )

def percentage_format(value):
    return conditional_int(100*value)

def relative_format(value, feature_name):
    return (
        int(value) if not is_enabled_at_runtime(f"{feature_name}", "relative_mode")
        else percentage_format(value)
    )

def percentage_unit(*, if_is_relative):

    return (
        "%" if is_enabled_at_runtime(f"{if_is_relative}", f"relative_mode")
        else "px"
    )
