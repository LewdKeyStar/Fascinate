from math import lcm

def enforce_strobe_every(strobe_every):
    return f"'eq(mod(n, {strobe_every}), 0)'"

def enforce_strobe_pause(strobe_every, strobe_pause, should_invert_strobe_pause):

    compar_func = "gte" if should_invert_strobe_pause else "lt"

    return "1" if strobe_pause == 0 \
    else f"'{compar_func}(mod(n, {2*lcm(strobe_every,strobe_pause)}), {lcm(strobe_every,strobe_pause)})'"

def enable_conds(strobe_every, strobe_pause, should_invert_strobe_pause):
    return (
        "enable="
        f'''{
            enforce_strobe_every(strobe_every)
        }''' '*' f'''{
            enforce_strobe_pause(strobe_every, strobe_pause, should_invert_strobe_pause)
        }'''
    )
