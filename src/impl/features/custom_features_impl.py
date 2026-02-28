from src.impl.utils.enable_settings_utils import interval_total_length

from src.constants import (
    DEFAULT_ZOOM_CENTER_X, DEFAULT_ZOOM_CENTER_Y,
    DEFAULT_INTERSPERSE_UNSCALED_X, DEFAULT_INTERSPERSE_UNSCALED_Y,
    VALID_AXES, VALID_COLORS,
    TRANSPARENT_FFMPEG_COLOR
)

from src.impl.utils.feature_utils import yuva420p_format_filter

# Yucky !
# This shouldn't need to be here, but we need it for intersperse :
# - get_resolution to center the unscaled movie,
# - get_duration for its extend option.

from src.utils.ffprobe_utils import (
    get_resolution,
    get_duration
)

def shake_filter(
    shake_axis,

    shake_amplitude,
    shake_frequency,
    shake_dampen,

    shake_blur_radius,

    start_shake_at,

    shake_pause,
    shake_active,

    fps
):

    def t_modulo_interval():
        interval = interval_total_length(shake_pause, shake_active)/fps
        modulo = interval if round(interval) >= 1 else 1 # = modulo every second
        # we could also to a half-second, or a certain fraction of the FPS...

        # FIXME : replace with effective_feature_start ?
        # This doesn't seem to cause problems here somehow...
        return f'mod(t-{start_shake_at/fps},{modulo})'

    return (
        f"split[orig][moving];"
        f"[moving]dblur=angle={'0' if shake_axis == 'x' else '90'}"
        f":radius={shake_blur_radius}[moving_blurred];"
        f"[orig][moving_blurred]overlay={shake_axis}='"
        f"exp(-{shake_dampen}*{t_modulo_interval()})"
        f"*{shake_amplitude}*sin(2*PI*{shake_frequency}*{t_modulo_interval()})'"
    )

def zoom_filter(
    zoom_factor,
    zoom_center_x,
    zoom_center_y,

    zoom_relative_mode,

    res,
    fps
):

    if zoom_center_x == DEFAULT_ZOOM_CENTER_X:
        zoom_center_x = "(iw / 2)" if not zoom_relative_mode else 0.5

    if zoom_center_y == DEFAULT_ZOOM_CENTER_Y:
        zoom_center_y = "(ih / 2)" if not zoom_relative_mode else 0.5

    if zoom_relative_mode:
        zoom_center_x = f"({str(zoom_center_x)}*iw)"
        zoom_center_y = f"({str(zoom_center_y)}*ih)"

    return (
        f"zoompan=s={res}:fps={fps}:"
        f"z={zoom_factor}:d=1:"
        f"x={zoom_center_x} - {zoom_center_x}/zoom:y={zoom_center_y} - {zoom_center_y}/zoom"
    )

def frame_randomizer_filter(
    frame_randomizer_max_frames,
    frame_randomizer_seed
):
    return (
        f"random=frames={frame_randomizer_max_frames}:"
        f"seed={frame_randomizer_seed}"
    )

def afterimages_filter(
    afterimages_amount,
    afterimages_delay,

    afterimages_start_white,
    afterimages_extend,

    afterimages_alpha
):

    def amount_range():
        return range(1, afterimages_amount + 1)

    def overlay_step(i):
        return (
            f"overlay_step{i}"
            if i > 0
            else "before_afterimages_pre"
        )

    # If the individual afterimage overlays are enabled during their tpad interval (while they're transparent-white)
    # And the format isn't changed to a compatible one like yuva420p,
    # It results in a "fade in from white" effect.
    # This is undesirable in most cases, but can be neat sometimes, which is why it's an option.

    def pre_format():
        return (
            f"{yuva420p_format_filter()},"
            if not afterimages_start_white
            else ''
        )

    def hide_when_white(i):
        return (
            f"=enable='gte(n, {i*afterimages_delay})'"
            if not afterimages_start_white
            else ''
        )

    def conditional_extend(should_extend):
        return f"shortest={'0' if afterimages_extend else '1'}"

    return (
        f"{pre_format()}"
        f"split={afterimages_amount+2}[before_afterimages_pre][before_afterimages_post]{''.join([f'[clone{i}]' for i in amount_range()])};"
        f'''{''.join([
            f"[clone{i}]tpad=start={i*afterimages_delay}:color={TRANSPARENT_FFMPEG_COLOR}[afterimage{i}];"
            f"[afterimage{i}]format=argb,colorchannelmixer=aa={afterimages_alpha}[afterimage{i}_alpha];"
            f"[{overlay_step(i-1)}][afterimage{i}_alpha]overlay{hide_when_white(i)}:{conditional_extend()}[{overlay_step(i)}];"
            for i in amount_range()
        ])}'''
        f"[before_afterimages_post][{overlay_step(afterimages_amount)}]overlay={conditional_extend()}"
    )

def speed_change_filter(
    speed_change_factor
):

    return (
        f"setpts={1/speed_change_factor}*PTS"
    )

def speed_change_filter_audio_component(
    speed_change_factor,
    speed_change_preserve_pitch,
    speed_change_preserve_formants
):

    return (
        f"rubberband=tempo={speed_change_factor}:"
        f"pitch={speed_change_factor if not speed_change_preserve_pitch else 1}:"
        f"transients=mixed:"
        f"detector=percussive:"
        f"phase=independent:"
        f"window=short:"
        f"smoothing=on:"
        f"formant={'shifted' if not speed_change_preserve_formants else 'preserved'}:"
        f"pitchq=quality:"
        f"channels=together"
    )

# FIXME : seek_point doesn't work, NO MATTER WHAT. It just doesn't seek.
# I wonder if this is a recently introduced bug,
# Or just an old one that goes unsolved,
# if only just because people consider the movie filter to be bad practice.

# TODO : it might be impossible to also add the overlay's audio,
# Unless we resort to filter_complex.

def intersperse_filter(
    intersperse_source,

    intersperse_scale,
    intersperse_unscaled_x,
    intersperse_unscaled_y,
    intersperse_relative_mode,

    intersperse_start_frame,
    intersperse_start_delay,
    intersperse_loop,
    intersperse_extend,

    intersperse_alpha,

    res,
    fps,
    duration
):

    def conditional_scale():
        return (
            (
                f"[over]scale=size={res}[over_scaled];"
                f"[over_scaled]"
            )
            if intersperse_scale
            else '[over]'
        )

    width, height = map(int, res.split("x"))

    if intersperse_unscaled_x == DEFAULT_INTERSPERSE_UNSCALED_X:
        intersperse_unscaled_x = (
            width / 2
            if not intersperse_relative_mode
            else 0.5
        )

    if intersperse_unscaled_y == DEFAULT_INTERSPERSE_UNSCALED_Y:
        intersperse_unscaled_y = (
            height / 2
            if not intersperse_relative_mode
            else 0.5
        )

    if intersperse_relative_mode:

        intersperse_unscaled_x *= width
        intersperse_unscaled_y *= height

    movie_width, movie_height = map(int, get_resolution(intersperse_source).split("x"))

    # Because these are X/Y params for the overlay, they concern the top left corner,
    # Not the center.
    # For the same reason, their lowest value is 0.
    # This means that the center cannot be brought closer to 0.25* the main video's dimensions,
    # No matter what we do.
    # Ah well. Not like this is gonna be used a lot.

    overlay_x = intersperse_unscaled_x - (movie_width / 2) if not intersperse_scale else 0
    overlay_y = intersperse_unscaled_y - (movie_height / 2) if not intersperse_scale else 0

    # This is simpler than calculating the number of loops.
    # Note, however, that it ONLY works with the setpts hack below,
    # Otherwise, the ffmpeg process never terminates!

    def loop_count():

        return (
            "0" if intersperse_loop
            else "1"
        )

    # The hack in question, graciously provided by :
    # >> https://superuser.com/questions/1093507/loop-a-video-overlay-with-ffmpeg <<

    # Okay, so convert the frame number to seconds, and then...
    # ...I have *no idea* what TB does here.

    # The ffmpeg docs refer to it as a "time base".
    # Does that mean it converts the (cyclical) second timestamps of the secondary input
    # Into monotonic timestamps based on those of the main input (the "base" input) ?
    # That's my best guess. We don't have another explanation.
    # Whatever the case, it works, so let's not complain.

    def setpts_loop_hack():
        return "setpts=N/FRAME_RATE/TB"

    # shortest=1 will freeze the main video if the interspersed movie terminates.
    # This seems to mean that, without any such indication from the ffmpeg docs,
    # shortest overrides BOTH eof_action and repeatlast.

    # To avoid this, shortest is only triggered, not only if extend is false
    # (which is the default, as is appropriate for us)
    # but if the interspersed movie also DOES extend beyond the main vid,
    # At which point it doesn't run the risk of terminating early and freezing it.

    movie_duration = get_duration(intersperse_source)
    padded_movie_duration = movie_duration + intersperse_start_delay

    is_movie_shorter = padded_movie_duration < duration

    def conditional_extend():
        return f"shortest={'0' if intersperse_extend or is_movie_shorter else '1'}"

    return (
        f"null[main];"
        f"movie=filename={intersperse_source}:"
        f"seek_point={intersperse_start_frame / fps}:"
        f"loop={loop_count()}[over];"
        f"{conditional_scale()}"
        f"tpad=start={intersperse_start_delay}:color={TRANSPARENT_FFMPEG_COLOR}[over_padded];"
        f"[over_padded]format=argb,colorchannelmixer=aa={intersperse_alpha}[over_alpha];"
        f"[over_alpha]{setpts_loop_hack()}[over_adjusted];"
        f"[main][over_adjusted]overlay="
        f"x={overlay_x}:y={overlay_y}:"
        f"eof_action=pass:repeatlast=0:{conditional_extend()}"
    )
