def yuva420p_format_filter():
    return "format=yuva420p"

def eq_filter(contrast, brightness, saturation, gamma, gamma_r, gamma_g, gamma_b, gamma_weight):
    return (
        f"eq="
        f"contrast={contrast}:"
        f"brightness={brightness}:"
        f"saturation={saturation}:"
        f"gamma={gamma}:"
        f"gamma_r={gamma_r}:"
        f"gamma_g={gamma_g}:"
        f"gamma_b={gamma_b}:"
        f"gamma_weight={gamma_weight}"
    )

# For GIF management ;
# Without a separate palette for each GIF frame, noticeable quantization noise appears.
# The optimized thing to do would be to have two palettes : one for the normal frames, one for the inverted

def palette_filter():
    return "split[s0][s1];[s0]palettegen=stats_mode=single[p];[s1][p]paletteuse=new=1"

def split_filter(primary_name, secondary_name):
    return f"split[{primary_name}][{secondary_name}]"

def overlay_filter(primary_name, secondary_name):
    return f"[{primary_name}][{secondary_name}]overlay"

def fade_filter(type, start_frame, end_frame, video_duration, n_expression):

    start_frame = max(0, start_frame)
    end_frame = min(end_frame, video_duration)

    def elapsed_time():
        return f"({n_expression} - {start_frame})"

    def duration():
        return f"({end_frame} - {start_frame})"

    def elapsed_time_relative():
        return f"({elapsed_time()} / {duration()})"

    # linear = f"({elapsed_time_relative()})"
    ease_in_out_quad = (
        f"if("
            f"lt({elapsed_time_relative()}, 1/2),"
            f"2 * {elapsed_time_relative()}^2,"
            f"1 - (((-2 * {elapsed_time_relative()} + 2)^2) / 2)"
        f")"
    )

    # Still, that expression must be clamped,
    # because the frame values extend outside the function definition range.
    # # TODO : substitute N for the n_expression when cyclical

    return (
        f"'if("
            f"lt(N, {start_frame}),"
            f"{'p(X,Y)' if type == 'out' else '0'},"
            f"if("
                f"gt(N, {end_frame}),"
                f"{'p(X,Y)' if type == 'in' else '0'},"
                f"p(X,Y)*min(max(0.0, {ease_in_out_quad if type == 'in' else f'1 - {ease_in_out_quad}'}), 1.0)"
            f")"
        f")'"
    )
