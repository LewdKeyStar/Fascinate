from math import lcm

# Trigger filter only every n frames.

def enable_every(freq):
    return f"'eq(mod(n, {freq}), 0)'"

# Assuming a filter is enabled every n frames, trigger it only for a certain interval of time,
# Then pause for that same interval and so on.
# This can be generalized to a filter that isn't enabled every n frames,
# Just by defining freq = 1.

def enable_at_interval(freq, interval, should_invert):

    compar_func = "gte" if should_invert else "lt"

    return "1" if interval == 0 \
    else f"'{compar_func}(mod(n, {2*lcm(freq, interval)}), {lcm(freq, interval)})'"

# Utility for the invert_filter.

def strobe_enable_conds(strobe_every, strobe_pause, should_invert_strobe_pause):
    return (
        "enable="
        f'''{
            enable_every(strobe_every)
        }''' '*' f'''{
            enable_at_interval(strobe_every, strobe_pause, should_invert_strobe_pause)
        }'''
    )
