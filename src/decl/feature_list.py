from src.decl.features.custom_features import custom_features
from src.decl.features.ffmpeg_wrapper_features import ffmpeg_wrapper_features
from src.decl.features.frei0r_features import frei0r_features

features = custom_features + ffmpeg_wrapper_features + frei0r_features

# A util function that enforces the priority values given by users at call time.
# Used for the order of feature application, and the order of feature sections in the output name.

def prioritized_features():
    return sorted(
        features,
        key = lambda f: f.priority,
        reverse = True
    )
