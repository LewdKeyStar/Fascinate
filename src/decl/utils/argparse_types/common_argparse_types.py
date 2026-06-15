from src.parser_namespace import input_property_runtime_value

def video_time(string):

    def seconds_to_frame_number(seconds):
        fps = input_property_runtime_value("fps")
        return round(fps * seconds)

    seconds_value = None

    if string.endswith("s") or "." in string:

        float_literal = string.removesuffix("s")

        try:
            seconds_value = float(float_literal)
        except:
            raise ValueError("video_time : Invalid seconds value")

    elif ":" in string: # timestamp string

        timestamp_components = list(reversed(string.split(':')))

        # we're gonna stop at hours. I think it's fine.

        if len(timestamp_components) > 3:

            raise ValueError("video_time : Timestamps over a day are not supported")

        try:

            timestamp_components[0] = float(timestamp_components[0]) # seconds can be floats,

            print("Past first component")

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

    else: # frame number. has to be a valid positive int.

        try:
            int(string)
        except:
            raise ValueError("video_time : Invalid frame number")

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
