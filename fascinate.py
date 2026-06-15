from ffmpy import FFmpeg
from argparse import ArgumentParser

import src.parser_namespace
from src.parser_namespace import input_property_runtime_value

from src.types.VideoInfo import VideoInfo

from src.decl.feature_list import features, prioritized_features
from src.impl.misc_filters import pad_mp4_filter, palette_filter

from src.utils.parser_utils import register_feature
from src.utils.filter_utils import chain_filters

from src.utils.name_utils import is_mp4, is_gif, to_output_name
from src.constants import DEFAULT_OUTPUT

def appropriate_filters(args):

    all_filters = [

        *[
            feature_filter()
            for feature_filter in prioritized_features()
         ],

        pad_mp4_filter() if is_mp4(args["output"]) else "",

        palette_filter() if is_gif(args["output"]) else ""
    ]

    return chain_filters(all_filters)

def appropriate_filter_audio_components(args):
    # this one doesn't actually use args, but for uniformity's sake...

    all_audio_components = [

        feature_filter(
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

    # Parsed args will be stored in a dedicated module,
    # Which then provides utilities to get the value of options,
    # Rather than moving the Namespace object around.

    src.parser_namespace.init_namespace()

    # But first...

    parser = ArgumentParser()

    parser.add_argument("input")
    parser.add_argument("-o", "--output", nargs = "?", default = DEFAULT_OUTPUT)

    # ...parse just the input path, to gather video info.

    temp_args, unknown_args = parser.parse_known_args(
        namespace = src.parser_namespace.runtime_namespace
    )

    video_info = VideoInfo(
        input_property_runtime_value("input")
    )

    # Then, use it to update the store-maintained namespace.

    src.parser_namespace.update_namespace_with_video_info(video_info)

    # This is necessary because feature options *will* require access to video info.

    # Now, they can be registered,

    for feature in features:
        register_feature(parser, feature)

    # And with that, we can parse everything for real.

    src.parser_namespace.runtime_namespace = parser.parse_args(
        namespace = src.parser_namespace.runtime_namespace
    )

    # TODO : using this "args" local variable is obsolete,
    # Especially with the namespace no longer being permanently stored as a dict,
    # Which makes this call to vars() semantically gross.
    # Think of an alternative.

    args = vars(src.parser_namespace.runtime_namespace)

    if not any_filters_enabled():
        print("No filters specified, exiting")
        return

    # This has to be done because there is no way to pass a default value generator
    # To ArgumentParser ; only constant values.

    args["output"] = \
        to_output_name(args["input"]) \
        if args["output"] == DEFAULT_OUTPUT \
        else args["output"]

    ff = FFmpeg(
        global_options = "-y",
        inputs = {args["input"]: None},
        outputs = {args["output"]: (
            (
                [
                "-vf", appropriate_filters(
                    args, # Needed for is_gif
                )]
            )
            +
            (
                [
                    "-af", appropriate_filter_audio_components(
                        args, # Not needed, passed for uniformity
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
