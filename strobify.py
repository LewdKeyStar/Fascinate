from os.path import splitext
from ffmpy import FFmpeg
from argparse import ArgumentParser

from src.filters import (
    invert_filter,
    palette_filter,
    
    appropriate_filters
)

DEFAULT_OUTPUT = "default" # This is just a placeholder, not an actual filename.
DEFAULT_STROBE_EVERY = 2

def to_output_name(input_path, strobe_every):
    input_name, input_ext = splitext(input_path)
    return input_name+f"strobe_every_{strobe_every}"+input_ext

def main():
    parser = ArgumentParser()

    parser.add_argument("input")
    parser.add_argument("-o", "--output", nargs = "?", default = DEFAULT_OUTPUT)
    parser.add_argument("-n", "--every", type = int, nargs = "?", default = DEFAULT_STROBE_EVERY)

    args = parser.parse_args()

    # This has to be done because there is no way to pass a default value generator
    # To ArgumentParser ; only constant values.

    args.output = \
        to_output_name(args.input, args.every) \
        if args.output == DEFAULT_OUTPUT \
        else args.output

    ff = FFmpeg(
        global_options = "-y",
        inputs = {args.input: None},
        outputs = {args.output: [
            "-c:a", "copy", # this cannot be done for video, so transcoding WILL occur
            # because there is no way for ffmpeg to reference the input codec in the filter chain...
            "-vf", appropriate_filters(args.input, args.every)
        ]}
    )

    print(ff.cmd)

    ff.run()

if __name__ == '__main__':
    main()
