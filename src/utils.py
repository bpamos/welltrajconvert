from src.imports import *


def ifnone(a:Any,b:Any)->Any:
    "`a` if `a` is not None, otherwise `b`."
    return b if a is None else a

def is_dict(object):
    """
    Helper function that checks if a given parameter is a dict or not
    """

    if isinstance(object, dict):
        return True
    else:
        return False

