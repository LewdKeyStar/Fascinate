def frei0r_composite_type_format(value):

    components = value.split('/')

    return f"({','.join(components)})"

def frei0r_position_format(value):
    return frei0r_composite_type_format(value)

def frei0r_color_format(value):
    return frei0r_composite_type_format(value)
