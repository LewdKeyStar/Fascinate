from src.parser_namespace import input_property_runtime_value

def video_time(string):

    def seconds_to_frame_number(seconds):
        fps = input_property_runtime_value("fps")
        return round(fps * seconds)

    seconds_value = None

    # A valid video_time value is either (from most complex to simplest) :

    # A. A timestamp string,
    # Either in the format "[XX:]YY:ZZ.ff" or "[XXh][YYm][ZZ.ffs]"

    if ":" in string or any(sep in string for sep in ["h", "m", "s"]):

        # ...but not both !

        if ":" in string and any(sep in string for sep in ["h", "m", "s"]):

            raise ValueError("video_time : Mixed timestamp format")

        if ":" in string:

            timestamp_components = list(reversed(string.split(':')))

        else:

            hour_component, remainder = (
                string.split("h") if "h" in string else ("0", string)
            )

            minute_component, remainder = (
                remainder.split("m") if "m" in remainder else ("0", remainder)
            )

            second_component = remainder.removesuffix("s")

            timestamp_components = [
                second_component,
                minute_component,
                hour_component
            ]

        # we're gonna stop at hours. I think it's fine.

        if len(timestamp_components) > 3:

            raise ValueError("video_time : Timestamps over a day are not supported")

        try:

            timestamp_components[0] = float(timestamp_components[0]) # seconds can be floats,

            # the other components are ints.

            for i, other_timestamp_component in enumerate(timestamp_components[1:]):
                timestamp_components[i+1] = int(other_timestamp_component)

        except:

            raise ValueError("video_time : Invalid video timestamp value")

        timestamp_component_multipliers = [
            1,
            60,
            3600
        ]

        seconds_value = sum(
            timestamp_component * timestamp_component_multiplier
            for (timestamp_component, timestamp_component_multiplier)
            in zip(timestamp_components, timestamp_component_multipliers)
        )


    # B. A float amount of seconds

    elif "." in string:

        float_literal = string.removesuffix("s")

        try:
            seconds_value = float(float_literal)
        except:
            raise ValueError("video_time : Invalid seconds value")

    # Or C. a frame number, which has to be a valid positive int.

    else:

        try:
            int(string)
        except:
            raise ValueError("video_time : Invalid frame number")

    # --------------------------------------------------------------------------

    # In the end, all those cases are collapsed back into a frame value.

    frame_number = (
        seconds_to_frame_number(seconds_value)
        if seconds_value is not None
        else int(string)
    )

    if frame_number < 0 :

        raise ValueError("video_time : Time provided was negative")

    elif frame_number > input_property_runtime_value("duration"):

        raise ValueError("video_time : Time provided is greater than video duration")

    return frame_number

def coordinate(string, axis):

    try:
        value = float(string)
    except:
        raise ValueError("coordinate : non-float value provided")

    # FIXME : we need to allow default values outside the sensible range,
    # For the purposes of signaling in crop coordinates.
    # It can either be None or a negative number,
    # And the latter, though problematic, is preferable,
    # Since it will be handled fine by FFMPEG.

    # if value < 0:
    #
    #     raise ValueError("coordinate : negative coordinate provided")

    if value > 1:

        return round(value)

    else:

        width, height = map(int, input_property_runtime_value("resolution").split("x"))

        return (
            value * width
            if axis == "x"
            else value * height
        )

def x_coordinate(string):

    return coordinate(string, axis = "x")

def y_coordinate(string):

    return coordinate(string, axis = "y")

def x_dimension(string):

    return x_coordinate(string)

def y_dimension(string):

    return y_coordinate(string)
