from src.constants import DEFAULT_FADE_FUNCTION

from src.impl.utils.enable_settings_utils import effective_feature_start

def fade_cyclical_sync_values(
    feature_pause,
    feature_active,
    fade_cyclical_sync_in_percent,
    fade_cyclical_sync_out_percent
):

    if feature_active == 0:
        feature_active = feature_pause

    fade_in_duration = fade_cyclical_sync_in_percent * feature_active
    fade_out_duration = fade_cyclical_sync_out_percent * feature_active
    fade_out_cyclical_peak = feature_active - (fade_in_duration + fade_out_duration)
    fade_out_cyclical_trough = feature_pause

    return (
        fade_in_duration,
        fade_out_duration,
        fade_out_cyclical_peak,
        fade_out_cyclical_trough
    )

def fade_filter(
    type,

    start_frame,
    end_frame,

    video_duration,

    n_expression,
    fade_function,
    cyclical_offset
):

    # In the case of a cyclical fade, the modulo calculations can only work
    # if the start offset is subtracted from the fade bounds.
    # This does not impact the end result,
    # because the feature is invisible before the start offset,
    # and the n expression is arranged so that the start offset is congruent to zero.

    start_frame = max(0, start_frame) - cyclical_offset
    end_frame = min(end_frame, video_duration) - cyclical_offset

    def elapsed_time():
        return f"({n_expression} - {start_frame})"

    def duration():
        return f"({end_frame} - {start_frame})"

    def elapsed_time_relative():
        return f"({elapsed_time()} / {duration()})"

    linear = l = f"({elapsed_time_relative()})"
    ease_out = eo = (
        f"(1 - (1 - {elapsed_time_relative()})^2)"
    )
    ease_in_out = eio = (
        f"if("
            f"lt({elapsed_time_relative()}, 1/2),"
            f"2 * {elapsed_time_relative()}^2,"
            f"1 - (((-2 * {elapsed_time_relative()} + 2)^2) / 2)"
        f")"
    )

    chosen_fade_function = locals()[fade_function]

    # The fade expression must be clamped,
    # because the frame values extend outside the function definition range.
    # In other words, we're defining a function domain.

    return (
        f"'if("
            f"lt({n_expression}, {start_frame}),"
            f"{'p(X,Y)' if type == 'out' else '0'},"
            f"if("
                f"gt({n_expression}, {duration() if type == 'in' and n_expression != 'N' else end_frame}),"
                f"{'p(X,Y)' if type == 'in' else '0'},"
                f"p(X,Y)*min(max(0.0, {chosen_fade_function if type == 'in' else f'1 - {chosen_fade_function}'}), 1.0)"
            f")"
        f")'"
    )

    # I really, really don't know why duration() has to replace the end frame
    # only on a CYCLICAL fadein rather than all fadeins period.
    # But that's how it works. If duration() is used on a non-cyclical fadein, it breaks.

# Note :
# The default argument values are for passing to the non-cyclical fade in and out filters.

def fade_in_filter_generic(
    *,

    fade_in_duration = 0,
    fade_out_duration = 0,

    fade_in_function = DEFAULT_FADE_FUNCTION,

    fade_cyclical = False,

    fade_cyclical_peak = 0,
    fade_cyclical_trough = 0,

    fade_cyclical_sync = False,
    fade_cyclical_sync_in_percent = 0,
    fade_cyclical_sync_out_percent = 0,

    feature_start_at = 0,
    feature_pause = 0,
    feature_active = 0,
    feature_invert_pause = 0,

    video_duration = 0
):

    if fade_cyclical_sync and feature_pause == 0:
        raise ValueError("Synced cyclical fade set with no pause cycle to sync to")

    if fade_cyclical and not fade_cyclical_sync and fade_out_duration == 0:
        raise ValueError("Non-synced cyclical fade set with no fadeout duration")

    actual_feature_start = effective_feature_start(
        feature_start_at,
        feature_pause,
        feature_invert_pause
    )

    fade_in_start_at = actual_feature_start

    if fade_cyclical_sync:
        (
            fade_in_duration,
            fade_out_duration,
            fade_cyclical_peak,
            fade_cyclical_trough
        ) = fade_cyclical_sync_values(
            feature_pause,
            feature_active,
            fade_cyclical_sync_in_percent,
            fade_cyclical_sync_out_percent
        )

    # The total time of an in-out cycle.
    # In the case of a non-cyclical fade, peak is irrelevant.
    total_fade_time = fade_in_duration + (fade_cyclical_peak) + fade_out_duration

    return (
        f'''format=argb,geq=r='p(X,Y)':a={fade_filter(
            type = "in",
            start_frame = fade_in_start_at,
            end_frame = fade_in_start_at + fade_in_duration,
            video_duration = video_duration,
            n_expression = (
                "N" if not fade_cyclical
                else f"mod(N - {actual_feature_start}, {total_fade_time + fade_cyclical_trough})"
            ),
            fade_function = fade_in_function,
            cyclical_offset = actual_feature_start if fade_cyclical else 0
        )}'''
    )

def fade_out_filter_generic(
    *,

    fade_out_duration = 0,
    fade_in_duration = 0,

    fade_out_function = DEFAULT_FADE_FUNCTION,

    fade_cyclical = False,

    fade_cyclical_peak = 0,
    fade_cyclical_trough = 0,

    fade_cyclical_sync = False,
    fade_cyclical_sync_in_percent = 0,
    fade_cyclical_sync_out_percent = 0,

    feature_start_at = 0,
    feature_end_at = 0,
    feature_pause = 0,
    feature_active = 0,
    feature_invert_pause = 0,

    video_duration = 0
):

    if fade_cyclical_sync and feature_pause == 0:
        raise ValueError("Synced cyclical fade set with no pause cycle to sync to")

    if fade_cyclical and not fade_cyclical_sync and fade_in_duration == 0:
        raise ValueError("Non-synced cyclical fade set with no fadein duration")

    actual_feature_start = effective_feature_start(
        feature_start_at,
        feature_pause,
        feature_invert_pause
    )

    if fade_cyclical_sync:
        (
            fade_in_duration,
            fade_out_duration,
            fade_cyclical_peak,
            fade_cyclical_trough
        ) = fade_cyclical_sync_values(
            feature_pause,
            feature_active,
            fade_cyclical_sync_in_percent,
            fade_cyclical_sync_out_percent
        )

    # The total time of an in-out cycle.
    # In the case of a non-cyclical fade, peak is irrelevant.
    # FIXME : honestly, duplicating this seems like the lesser of two evils.
    total_fade_time = fade_in_duration + (fade_cyclical_peak) + fade_out_duration

    fade_out_end_at = (
        feature_end_at if not fade_cyclical
        else actual_feature_start + total_fade_time # = fade_in_start_at + total_fade_time
    )

    # The min between end frame and duration has to preemptively happen here,
    # Otherwise the start frame is incorrect.
    return (
        f'''format=argb,geq=r='p(X,Y)':a={fade_filter(
            type = "out",
            start_frame = min(fade_out_end_at, video_duration) - fade_out_duration,
            end_frame = fade_out_end_at,
            video_duration = video_duration,
            n_expression = (
                "N" if not fade_cyclical
                else f"mod(N - {actual_feature_start}, {total_fade_time + fade_cyclical_trough})"
            ),
            fade_function = fade_out_function,
            cyclical_offset = actual_feature_start if fade_cyclical else 0
        )}'''
    )
