from dataclasses import dataclass

from src.types.abstract.Shortenable import Shortenable
from src.types.FeatureParameterRange import FeatureParameterRange

# This is a class for feature-specific parameters, which are unique to this feature,
# As opposed to FeatureSetting.

@dataclass
class FeatureParameter(Shortenable):
    name: str
    default: any = 0
    unit: str = ""
    type: any = int

    range: FeatureParameterRange = FeatureParameterRange()
    desc: str = ""

    @property
    def help(self):
        return f"{self.desc} {self.range}"
