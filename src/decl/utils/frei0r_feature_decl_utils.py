def frei0r_composite_type(
    string,
    *,
    expected_components_num,
    conversion_op = lambda x: x
):

    if not (
        string.startswith('(')
        and string.endswith(')')
    ):
        # Because argparse catches this error, our own message doesn't actually display,
        # So there's no use in writing one.
        raise ValueError()

    components = string.replace('(', '').replace(')', '').split(',')

    if not len(components) == expected_components_num:
        raise ValueError()

    # The float conversions simply serve to trigger the float conversion error if need be,
    # So that it can bubble up to argparse.
    # The conversion op is for the color type only,
    # so it can be converted from values in range [0, 255]...

    converted_components = [conversion_op(float(component)) for component in components]

    # ...because all composite types have values in range [0, 1], as is canonical for frei0r.
    # Yes. Even color triplets.
    # Please send help.

    for component in converted_components:
        if component < 0 or component > 1:
            raise ValueError()

    return "/".join(components)

def frei0r_composite_type_format(value):

    components = value.split('/')

    return f"({','.join(components)})"

def frei0r_position(string):
    return frei0r_composite_type(
        string,
        expected_components_num = 2
    )

def frei0r_position_format(value):
    return frei0r_composite_type_format(value)

def frei0r_color(string):
    return frei0r_composite_type(
        string,
        expected_components_num = 3,
        conversion_op = lambda x: x / 255
    )

def frei0r_color_format(value):
    return frei0r_composite_type_format(value)
