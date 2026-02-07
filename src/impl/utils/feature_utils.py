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
