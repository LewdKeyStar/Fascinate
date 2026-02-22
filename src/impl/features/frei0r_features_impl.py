def frei0r_filter(
    name,
    *parameters
):

    formatted_params = [
        ("y" if param is True else "n") if type(param) == bool
        else str(param)
        for param in parameters
    ]

    param_string = f":filter_params={'|'.join(formatted_params)}"

    return (
        f"frei0r=filter_name={name}"
        f"{param_string if len(parameters) > 0 else ''}"
    )
