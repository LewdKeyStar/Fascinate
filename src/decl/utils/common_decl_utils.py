from src.parser_namespace import (
    is_enabled_at_runtime,
    input_property_runtime_value
)

from math import modf

def conditional_int(value):
    return (
        int(value) if modf(value)[0] == 0
        else value
    )

def percentage_format(value):
    return conditional_int(100*value)

def x_percentage_format(value):
    width = int(input_property_runtime_value("resolution").split("x")[0])
    return percentage_format(value / width)

def y_percentage_format(value):
    height = int(input_property_runtime_value("resolution").split("x")[1])
    return percentage_format(value / height)
