from dataclasses import dataclass

@dataclass(repr = False)
class FeatureParameterRange:
    min: any = None
    max: any = None

    def __repr__(self):
        return (
            f"Range : [{self.min}, {self.max}]"
            if self.min is not None and self.max is not None
            else ''
        )
