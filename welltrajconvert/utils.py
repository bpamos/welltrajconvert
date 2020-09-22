"`.utils` contains essential util functions to format and split data"
from .base import *


def _get_files(p, fs, extensions=None):
    p = Path(p)
    res = [p / f for f in fs if not f.startswith('.')
           and ((not extensions) or f'.{f.split(".")[-1].lower()}' in extensions)]
    return res


def get_files(path, extensions=None, recurse=True, folders=None, followlinks=True):
    """
    Get all the files in `path` with optional `extensions`,
    optionally with `recurse`, only in `folders`, if specified.
    """
    path = Path(path)
    folders = L(folders)
    extensions = make_set(extensions)
    extensions = {e.lower() for e in extensions}
    if recurse:
        res = []
        for i, (p, d, f) in enumerate(os.walk(path, followlinks=followlinks)):  # returns (dirpath, dirnames, filenames)
            if len(folders) != 0 and i == 0:
                d[:] = [o for o in d if o in folders]
            else:
                d[:] = [o for o in d if not o.startswith('.')]
            if len(folders) != 0 and i == 0 and '.' not in folders: continue
            res += _get_files(p, f, extensions)
    else:
        f = [o.name for o in os.scandir(path) if o.is_file()]
        res = _get_files(path, f, extensions)
    return L(res)


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


def crs_transformer(crs_from: Any, crs_to: Any, x: Any, y: Any) -> tuple:
    """
    Make a CRS Transformer and transform points between two coordinate systems.
    Transform x and y points to latitude and longitude points from input and output projection systems.
    Find the crs_to of interst at `https://epsg.io/`

    :parameter:
    -------
    crs_from: Projection of input data
    crs_to: Projection of output data
    x: (scalar or array (numpy or python)) – Input x coordinate(s).
    y: (scalar or array (numpy or python)) – Input y coordinate(s).

    :return:
    -------
    latitude, longitude: tuple

    :examples:
    -------
    # crs_to and crs_from as str
    >>> crs_from = "EPSG:4326"
    >>> crs_to='epsg:32638'
    >>> x = 759587.93
    >>> y = 3311661.86
    >>> crs_transformer(crs_from,crs_to,x,y)
    (29.899999999974757, 47.68000000020621)

    # alternative, crs_from and crs_to can be ints
    >>> crs_from = 4326
    >>> crs_to=32638
    >>> x = 759587.93
    >>> y = 3311661.86
    >>> crs_transformer(crs_from,crs_to,x,y)
    (29.899999999974757, 47.68000000020621)

    # x,y can be arrays.
    >>> crs_out = "EPSG:4326"
    >>> crs_in='epsg:32638'
    >>> crs_out = 4326
    >>> crs_in= 32638
    >>> x = np.array([759587,759588])
    >>> y = np.array([3311661,3311662])
    >>> crs_transformer(crs_out,crs_in,x,y)
    (array([29.90828684, 29.90829564]), array([47.68851095, 47.68852154]))
    """
    transformer = Transformer.from_crs(crs_to, crs_from)
    latitude, longitude = transformer.transform(x, y)

    return latitude, longitude


def list_of_dicts_to_df(dict_list: dict) -> DataFrame:
    """takes a list of dicts and converts to an appended df"""
    appended_df = pd.DataFrame()
    for i in dict_list:
        df_well_obj = pd.DataFrame(i)
        appended_df = appended_df.append(df_well_obj)
    return appended_df
