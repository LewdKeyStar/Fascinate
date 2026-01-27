from dataclasses import dataclass

from typing import Callable

from src.types.abstract.options.FeatureOption import FeatureOption

# This class is for options shared across all features :
# Enable conditions, alpha, fade parameters, etc.

@dataclass
class FeatureSetting(FeatureOption):
    value_format: Callable = lambda x, y : y
