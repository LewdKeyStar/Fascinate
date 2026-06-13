from argparse import Namespace

from dataclasses import fields

def init_namespace():
    global runtime_namespace
    runtime_namespace = Namespace()

def update_namespace_with_video_info(video_info):

    for info_field in fields(video_info):

        info_field_name = info_field.name

        runtime_namespace[info_field_name] = getattr(video_info, info_field_name)

def runtime_value(feature_name, option_name = ""):
    return (

        # Used to determine if a feature is active.

        runtime_namespace[feature_name]
        if option_name == ""

        # Used to get feature-independent runtime info,
        # e.g. video info (resolution, fps, etc.)

        else runtime_namespace[option_name]
        if feature_name == ""

        else runtime_namespace[f"{feature_name}_{option_name}"]
    )

# Boolean truth value alias

def is_enabled_at_runtime(feature_name, option_name = ""):
    return runtime_value(feature_name, option_name)

# Use with great parcimony.

def override_runtime_value(feature_name, option_name, option_value):
    runtime_namespace[f"{feature_name}_{option_name}"] = option_value
