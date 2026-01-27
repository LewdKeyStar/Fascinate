from argparse import Namespace

def init_namespace():
    global runtime_namespace
    runtime_namespace = Namespace()

def runtime_value(feature_name, option_name = ""):
    return (
        runtime_namespace[feature_name]
        if option_name == ""
        else runtime_namespace[f"{feature_name}_{option_name}"]
    )

# Boolean truth value alias

def is_enabled_at_runtime(feature_name, option_name = ""):
    return runtime_value(feature_name, option_name)

# Use with great parcimony.

def override_runtime_value(feature_name, option_name, option_value):
    runtime_namespace[f"{feature_name}_{option_name}"] = option_value
