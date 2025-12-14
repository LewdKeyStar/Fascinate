from ffmpy import FFmpeg
from argparse import ArgumentParser

from src.utils.ffprobe_utils import (
    get_resolution,
    get_fps
)

from src.decl.feature_list import features, prioritized_features
from src.impl.misc_filters import palette_filter

from src.utils.parser_utils import register_feature

from src.utils.name_utils import is_gif, to_output_name
from src.constants import DEFAULT_OUTPUT

def appropriate_filters(args, *, resolution, fps):

    # For SOME reason, this is necessary.
    # If we call locals() in the list comprehension, it produces a KeyError,
    # For either resolution or fps.

    local_dict = locals()

    all_filters = [
        *[
            feature_filter(
                args,
                *[local_dict[supp_arg] for supp_arg in feature_filter.supplemental_arguments]
            )
            for feature_filter in prioritized_features(args)
         ],

        palette_filter() if is_gif(args.input) else ""
    ]

    return ",".join([
        filter for filter in all_filters if filter != ""
    ])

def main():
    parser = ArgumentParser()

    parser.add_argument("input")
    parser.add_argument("-o", "--output", nargs = "?", default = DEFAULT_OUTPUT)

    for feature in features:
        register_feature(parser, feature)

    args = parser.parse_args()

    # This has to be done because there is no way to pass a default value generator
    # To ArgumentParser ; only constant values.

    args.output = \
        to_output_name(args) \
        if args.output == DEFAULT_OUTPUT \
        else args.output

    ff = FFmpeg(
        global_options = "-y",
        inputs = {args.input: None},
        outputs = {args.output: [
            "-c:a", "copy", # this cannot be done for video, so transcoding WILL occur
            # because there is no way for ffmpeg to reference the input codec in the filter chain...
            "-vf", appropriate_filters(
                args,
                resolution = get_resolution(args.input),
                fps = get_fps(args.input)
            )
        ]}
    )

    print(ff.cmd)

    ff.run()

if __name__ == '__main__':
    main()
