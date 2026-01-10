# Python doesn't have this and it drives me insane

def array_find(array, test):
    return next((x for x in array if test(x)), None)
