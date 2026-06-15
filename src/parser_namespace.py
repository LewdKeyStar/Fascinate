from argparse import Namespace

from dataclasses import fields

def init_namespace():
    global runtime_namespace
    runtime_namespace = Namespace()

def update_namespace_with_video_info(video_info):

    for info_field in fields(video_info):

        info_field_name = info_field.name

        runtime_namespace[info_field_name] = getattr(video_info, info_field_name)

def runtime_value(feature_name, option_or_property_name):

    return (

        # Used to determine if a feature is active.

        runtime_namespace[feature_name]
        if option_or_property_name == ""

        # Used to get feature-independent runtime info,
        # e.g. video info (resolution, fps, etc.)

        else runtime_namespace[option_or_property_name]
        if feature_name == ""

        else runtime_namespace[f"{feature_name}_{option_or_property_name}"]
    )

# More explicit aliases for the rest of the codebase.

def option_runtime_value(feature_name, option_name):

    return runtime_value(feature_name, option_name)

def input_property_runtime_value(input_property_name):

    return runtime_value("", input_property_name)

# Boolean truth value alias.
# Option name may be blank, when a feature is testing its own enabled status.

def is_enabled_at_runtime(feature_name, option_name = ""):
    return runtime_value(feature_name, option_name)

# Use with great parcimony.

def override_runtime_value(feature_name, option_name, option_value):
    runtime_namespace[f"{feature_name}_{option_name}"] = option_value
