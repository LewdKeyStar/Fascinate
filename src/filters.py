from src.filter_utils import strobe_enable_conds

def invert_filter(strobe_every, strobe_pause, should_invert_strobe_pause):
    return (
        "lutrgb=r=negval:g=negval:b=negval:"
        f"{strobe_enable_conds(strobe_every, strobe_pause, should_invert_strobe_pause)}"
    )

# For GIF management ;
# Without a separate palette for each GIF frame, noticeable quantization noise appears.
# The optimized thing to do would be to have two palettes : one for the normal frames, one for the inverted

def palette_filter():
    return "split[s0][s1];[s0]palettegen=stats_mode=single[p];[s1][p]paletteuse=new=1"
