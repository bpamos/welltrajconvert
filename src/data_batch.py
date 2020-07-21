from src.core import *
from src.utils import *
from src.data_object import *

def _path_to_same_str(p_fn):
    "path -> str, but same on nt+posix, for alpha-sort only"
    s_fn = str(p_fn)
    s_fn = s_fn.replace('\\','.')
    s_fn = s_fn.replace('/','.')
    return s_fn

def _get_files(parent, p, f, extensions):
    p = Path(p)#.relative_to(parent)
    if isinstance(extensions,str): extensions = [extensions]
    low_extensions = [e.lower() for e in extensions] if extensions is not None else None
    res = [p/o for o in f if not o.startswith('.')
           and (extensions is None or f'.{o.split(".")[-1].lower()}' in low_extensions)]
    return res



def get_files(path:PathOrStr, extensions:Collection[str]=None, recurse:bool=False, exclude:Optional[Collection[str]]=None,
              include:Optional[Collection[str]]=None, presort:bool=False, followlinks:bool=False)->FilePathList:
    "Return list of files in `path` that have a suffix in `extensions`; optionally `recurse`."
    if recurse:
        res = []
        for i,(p,d,f) in enumerate(os.walk(path, followlinks=followlinks)):
            # skip hidden dirs
            if include is not None and i==0:   d[:] = [o for o in d if o in include]
            elif exclude is not None and i==0: d[:] = [o for o in d if o not in exclude]
            else:                              d[:] = [o for o in d if not o.startswith('.')]
            res += _get_files(path, p, f, extensions)
        if presort: res = sorted(res, key=lambda p: _path_to_same_str(p), reverse=False)
        return res
    else:
        f = [o.name for o in os.scandir(path) if o.is_file()]
        res = _get_files(path, path, f, extensions)
        if presort: res = sorted(res, key=lambda p: _path_to_same_str(p), reverse=False)
        return res


class PreProcessor():
    "Basic class for a processor that will be applied to items at the end of the data block API."

    def __init__(self, ds: Collection = None):  self.ref_ds = ds

    # def process_one(self, item:Any):         return item
    def process(self, ds: Collection):        ds.items = array([self.process_one(item) for item in ds.items])


PreProcessors = Union[PreProcessor, Collection[PreProcessor]]


class ItemList():
    "A collection of items with `__len__` and `__getitem__` with `ndarray` indexing semantics."
    _processor, _square_show_res = None, False

    def __init__(self, items: Iterator, path: PathOrStr = '.', inner_df: Any = None,
                 x: 'ItemList' = None, processor: PreProcessors = None, ignore_empty: bool = False):
        self.path = Path(path)
        self.num_parts = len(self.path.parts)
        self.items, self.x, self.ignore_empty = items, x, ignore_empty
        if not isinstance(self.items, np.ndarray): self.items = array(self.items, dtype=object)
        self.inner_df, self.processor = inner_df, processor
        self.copy_new = ['x', 'path']

    def process(self, processor: PreProcessors = None):
        "Apply `processor` or `self.processor` to `self`."
        if processor is not None: self.processor = processor
        self.processor = listify(self.processor)
        for p in self.processor: p.process(self)
        return self

    def __len__(self) -> int:
        return len(self.items) or 1

    def get(self, i) -> Any:
        "Subclass if you want to customize how to create item `i` from `self.items`."
        return self.items[i]

    def __repr__(self) -> str:
        items = [self[i] for i in range(min(5, len(self.items)))]
        return f'{self.__class__.__name__} ({len(self.items)} items)\n{show_some(items)}\nPath: {self.path}'

    def add(self, items: 'ItemList'):
        self.items = np.concatenate([self.items, items.items], 0)
        if self.inner_df is not None and items.inner_df is not None:
            self.inner_df = pd.concat([self.inner_df, items.inner_df])
        else:
            self.inner_df = self.inner_df or items.inner_df
        return self

    def __getitem__(self, idxs: int) -> Any:
        "returns a single item based if `idxs` is an integer or a new `ItemList` object if `idxs` is a range."
        # idxs = try_int(idxs)
        if isinstance(idxs, Integral):
            return self.get(idxs)
        else:
            return self.new(self.items[idxs], inner_df=index_row(self.inner_df, idxs))

    def new(self, items: Iterator, processor: PreProcessors = None, **kwargs) -> 'ItemList':
        "Create a new `ItemList` from `items`, keeping the same attributes."
        processor = ifnone(processor, self.processor)
        print('in here')
        copy_d = {o: getattr(self, o) for o in self.copy_new}
        print(copy_d)
        kwargs = {**copy_d, **kwargs}
        print(kwargs)
        return self.__class__(items=items, processor=processor, **kwargs)

    @classmethod
    def from_folder(cls, path: PathOrStr, extensions: Collection[str] = None, recurse: bool = True,
                    exclude: Optional[Collection[str]] = None,
                    include: Optional[Collection[str]] = None, presort: Optional[bool] = False, **kwargs) -> 'ItemList':
        """Create an `ItemList` in `path` from the filenames that have a suffix in `extensions`.
        `recurse` determines if we search subfolders."""
        path = Path(path)
        assert path.is_dir() and path.exists(), f"{path} is not a valid directory."
        return cls(get_files(path, extensions, recurse=recurse, exclude=exclude, include=include, presort=presort),
                   path=path, **kwargs)

#
# class DataBatch:
#
#     def __init__(self, data):
#         """
#
#
#         :param directional_survey_data:
#         """
#
#         self.data = data
#
#
#     # def from_df(self: DataFrame, wellId_name: Optional[str] = None, md_name: Optional[str] = None,
#     #             inc_name: Optional[str] = None, azim_name: Optional[str] = None,
#     #             surface_latitude_name: Optional[str] = None,
#     #             surface_longitude_name: Optional[str] = None) -> 'DirectionalSurveyObj':
#     #     """Create a `dataclass_obj` suitable for `DataObject()` from a dataframe.
#     #
#     #     Params:
#     #     None
#     #     #df: Dataframe with well data from single well and all data columns.
#     #
#     #     with data in the following format style
#     #     data = {'wellId': ['well_C', 'well_C', 'well_C'],
#     #     'md': [0., 35., 700.],
#     #     'inc': [0., 10., 14.],
#     #     'azim': [227., 228., 230.],
#     #    'surface_latitude': [29.908294,29.908294,29.908294],
#     #    'surface_longitude':[47.688521,47.688521,47.688521]}
#     #     df = pd.DataFrame(data)
#     #
#     #
#     #     Return:
#     #     dataclass_obj
#     #
#     #     """
#     #     df = self.data
#     #
#     #     # if no column names are specified use 0:5 for dir survey obj
#     #     wellId_name = ifnone(wellId_name, df.columns[0])
#     #     md_name = ifnone(md_name, df.columns[1])
#     #     inc_name = ifnone(inc_name, df.columns[2])
#     #     azim_name = ifnone(azim_name, df.columns[3])
#     #     surface_latitude_name = ifnone(surface_latitude_name, df.columns[4])
#     #     surface_longitude_name = ifnone(surface_longitude_name, df.columns[5])
#     #
#     #     dataclass_obj = DataObject(wellId=df[wellId_name][0],
#     #                                md=np.array(df[md_name]),
#     #                                inc=np.array(df[inc_name]),
#     #                                azim=np.array(df[azim_name]),
#     #                                surface_latitude=df[surface_latitude_name][0],
#     #                                surface_longitude=df[surface_longitude_name][0])
#     #     return dataclass_obj
#
#     def from_df_and_header_values(self: DataFrame, wellId_val: str = 'wellId_example', md_name: Optional[str] = None,
#                                 inc_name: Optional[str] = None, azim_name: Optional[str] = None,
#                                 surface_latitude_val: float = 42.8746,
#                                 surface_longitude_val: float = 74.5698) -> 'DirectionalSurveyObj':
#         """Create a `dataclass_obj` suitable for `DataObject()` from a dataframe.
#
#         Params:
#         df: Dataframe with well data from single well and all data columns.
#
#         Return:
#         dataclass_obj
#
#         """
#
#         df = self.data
#
#         # if no column names are specified use 0:5 for dir survey obj
#         md_name = ifnone(md_name, df.columns[0])
#         inc_name = ifnone(inc_name, df.columns[1])
#         azim_name = ifnone(azim_name, df.columns[2])
#
#         dataclass_obj = DataObject(wellId=wellId_val,
#                                    md=np.array(df[md_name]),
#                                    inc=np.array(df[inc_name]),
#                                    azim=np.array(df[azim_name]),
#                                    surface_latitude=surface_latitude_val,
#                                    surface_longitude=surface_longitude_val)
#         return dataclass_obj