from enum import Enum

# TODO : migrate to Python 3.11 to use StrEnum instead
class FeatureParameterApplicableComponent(Enum):
    VIDEO_COMPONENT_ONLY = 1

    AUDIO_COMPONENT_ONLY = 2

    BOTH_COMPONENTS = 3
