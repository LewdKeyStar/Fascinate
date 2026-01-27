from ffmpy import FFmpeg
from argparse import ArgumentParser

import src.parser_namespace

from src.types.VideoInfo import VideoInfo

from src.decl.feature_list import features, prioritized_features
from src.impl.misc_filters import palette_filter

from src.utils.parser_utils import register_feature
from src.utils.filter_utils import chain_filters

from src.utils.name_utils import is_gif, to_output_name
from src.constants import DEFAULT_OUTPUT

def appropriate_filters(args, video_info):

    all_filters = [

        *[
            feature_filter(video_info)
            for feature_filter in prioritized_features()
         ],

        palette_filter() if is_gif(args["output"]) else ""
    ]

    return chain_filters(all_filters)

def appropriate_filter_audio_components(args, video_info):
    # this one doesn't actually use args, but for uniformity's sake...

    all_audio_components = [

        feature_filter(
            video_info,
            seeking_audio_component = True
        )

        for feature_filter in prioritized_features()
    ]

    return chain_filters(all_audio_components)

def any_filters_enabled():
    return any(feature.is_enabled for feature in features)

def any_audio_filters_enabled():
    return any(feature.has_audio_component and feature.is_enabled for feature in features)

def main():
    src.parser_namespace.init_namespace()
    parser = ArgumentParser()

    parser.add_argument("input")
    parser.add_argument("-o", "--output", nargs = "?", default = DEFAULT_OUTPUT)

    for feature in features:
        register_feature(parser, feature)

    # Register the parsed args in a dedicated module,
    # Which then provides utilities to get the value of options,
    # Rather than moving the Namespace object around.

    src.parser_namespace.runtime_namespace = vars(parser.parse_args(namespace = src.parser_namespace.runtime_namespace))
    args = src.parser_namespace.runtime_namespace

    if not any_filters_enabled():
        print("No filters specified, exiting")
        return

    # This has to be done because there is no way to pass a default value generator
    # To ArgumentParser ; only constant values.

    args["output"] = \
        to_output_name(args["input"]) \
        if args["output"] == DEFAULT_OUTPUT \
        else args["output"]

    video_info = VideoInfo(args["input"])

    ff = FFmpeg(
        global_options = "-y",
        inputs = {args["input"]: None},
        outputs = {args["output"]: (
            (
                [
                "-vf", appropriate_filters(
                    args, # Needed for is_gif
                    video_info
                )]
            )
            +
            (
                [
                    "-af", appropriate_filter_audio_components(
                        args, # Not needed, passed for uniformity
                        video_info
                    )
                ]
                if any_audio_filters_enabled()
                else []
            )
        )}
    )

    print(ff.cmd)

    ff.run()

if __name__ == '__main__':
    main()
