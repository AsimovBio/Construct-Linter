import functools
import operator


def flatten(nested_list):
    return functools.reduce(operator.iconcat, nested_list, [])
