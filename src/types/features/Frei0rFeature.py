from dataclasses import dataclass

from src.types.features.Feature import Feature

@dataclass
class Frei0rFeature(Feature):

    # Override
    @property
    def feature_filter(self):
        # All frei0r filters share the same impl function.
        # This is because ffmpeg uses a single frei0r filter,
        # With the name of the desired effect as an argument.
        return getattr(self.impl_module, f"frei0r_filter")

    # Override
    def feature_filterstr(self, video_info, audio = False):

        if audio == True:
            raise ValueError("Audio component required from frei0r feature")

        # frei0r filters are implemented by the frei0r lib, not us.
        # They will not take setting values or video info.
        # However, they do need their own name, so the effect name can be given to ffmpeg.

        return self.feature_filter(
            self.name,

            *[
                self.get_param_value(param.name)
                for param in self.parameters
            ],
        )
