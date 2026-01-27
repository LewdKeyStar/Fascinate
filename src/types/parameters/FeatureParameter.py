from dataclasses import dataclass

from typing import Callable

from src.types.abstract.options.FeatureOption import FeatureOption
from src.types.parameters.FeatureParameterApplicableComponent import FeatureParameterApplicableComponent

# This is a class for feature-specific parameters, which are unique to this feature,
# As opposed to FeatureSetting.
# In practice, though, almost their entire implementation is the same.

@dataclass
class FeatureParameter(FeatureOption):

    value_format: Callable = lambda x: x

    applicable_component: FeatureParameterApplicableComponent = (
        FeatureParameterApplicableComponent.VIDEO_COMPONENT_ONLY
    )
