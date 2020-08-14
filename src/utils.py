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


def crs_transformer(crs_out: str, crs_in: str, x: float, y: float):
    """
    takes a two crs and transforms x and y coordinates to latitude and longitude.
    find the crs_in of interst at `https://epsg.io/`

    """
    transformer = Transformer.from_crs(crs_in, crs_out)
    latitude, longitude = transformer.transform(x, y)

    return latitude, longitude


def list_of_dicts_to_df(dict_list):
    """takes a list of dicts and converts to a appended df"""
    appended_df = pd.DataFrame()
    for i in dict_list:
        df_well_obj = pd.DataFrame(i)
        appended_df = appended_df.append(df_well_obj)
    return appended_df