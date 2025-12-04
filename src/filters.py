from os.path import splitext

def invert_filter(strobe_every):
    return f"lutrgb=r=negval:g=negval:b=negval:enable='eq(mod(n, {strobe_every}), 0)'"

# For GIF management ;
# Without a separate palette for each GIF frame, noticeable quantization noise appears.
# The optimized thing to do would be to have two palettes : one for the normal frames, one for the inverted

def palette_filter():
    return "split[s0][s1];[s0]palettegen=stats_mode=single[p];[s1][p]paletteuse=new=1"

def appropriate_filters(input_path, strobe_every):
    return ",".join([
        invert_filter(strobe_every),
        palette_filter() if splitext(input_path)[1].lower() == ".gif" else ""
    ])
