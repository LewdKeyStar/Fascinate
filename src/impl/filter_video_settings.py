from src.impl.misc_filters import fade_filter

def alpha_filter(alpha):
    return (
        f"format=argb,colorchannelmixer=aa={alpha}"
    )

def fade_in_filter(fade_duration, start_at, video_duration, n_expression = "N"):
    return (
        f'''format=argb,geq=r='p(X,Y)':a={fade_filter(
            type = "in",
            start_frame = start_at,
            end_frame = start_at + fade_duration,
            video_duration = video_duration,
            n_expression = n_expression
        )}'''
    )

def fade_out_filter(fade_duration, end_at, video_duration, n_expression = "N"):
    # The min between end frame and duration has to preemptively happen here,
    # Otherwise the start frame is incorrect.
    return (
        f'''format=argb,geq=r='p(X,Y)':a={fade_filter(
            type = "out",
            start_frame = min(end_at, video_duration) - fade_duration,
            end_frame = end_at,
            video_duration = video_duration,
            n_expression = n_expression
        )}'''
    )
