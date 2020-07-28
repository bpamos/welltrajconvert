"`.utils` contains essential util functions to format and split data"
from src.imports import *


def if_none(a: Any, b: Any) -> Any:
    "`a` if `a` is not None, otherwise `b`."
    return b if a is None else a


def to_type(a: Any, data_type):
    """
    If item is None, return None, else, convert to an data_type specified
    (ie. np.array, str, int, float, ect..)

    :parameter: a (Any or None)

    :returns: None or data_type(a)
    """
    return None if a is None else data_type(a)


def is_dict(obj):
    """
    Helper function that checks if a given parameter is a dict or not
    """

    if isinstance(obj, dict):
        return True
    else:
        return False

def crs_transformer(crs_out: str, crs_in: str, x: float, y: float):
    """
    takes a two crs and transforms x and y coordinates to latitude and longitude.
    find the crs_in of interst at `https://epsg.io/`

    """
    transformer = Transformer.from_crs(crs_in, crs_out)
    latitude, longitude = transformer.transform(x, y)

    return latitude, longitude