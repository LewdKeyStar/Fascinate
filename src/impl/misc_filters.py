# For GIF management ;
# Without a separate palette for each GIF frame, noticeable quantization noise appears.
# The optimized thing to do would be to have two palettes : one for the normal frames, one for the inverted

# FIXME : this should not be in the same file as basic building blocks like overlay and split...

def palette_filter():
    return "split[s0][s1];[s0]palettegen=stats_mode=single[p];[s1][p]paletteuse=new=1"

def split_filter(primary_name, secondary_name):
    return f"split[{primary_name}][{secondary_name}]"

def overlay_filter(primary_name, secondary_name):
    return f"[{primary_name}][{secondary_name}]overlay"
