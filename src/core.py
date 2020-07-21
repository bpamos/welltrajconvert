"`.core` contains essential util functions to format and split data"
import csv, os, pickle, sys
import math, matplotlib.pyplot as plt, numpy as np, pandas as pd, random
import abc, collections, hashlib, itertools, json, operator, pathlib

from abc import abstractmethod, abstractproperty
from collections import Counter, defaultdict, namedtuple, OrderedDict
from collections.abc import Iterable, Sized

from dataclasses import dataclass, field, InitVar
from pathlib import Path
from pandas import Series, DataFrame
from scipy.ndimage.interpolation import shift

# for utm conversion
import utm

from numbers import Integral

# for type annotations
from numbers import Number
from typing import Any, AnyStr, Callable, Collection, Dict, Hashable, Iterator, List, Mapping, NewType, Optional
from typing import Sequence, Tuple, TypeVar, Union

# contains essential util functions to format and split data
ListOrItem = Union[Collection[Any],int,float,str]
OptListOrItem = Optional[ListOrItem]
FilePathList = Collection[Path]
PathOrStr = Union[Path,str]
IntsOrStrs = Union[int, Collection[int], str, Collection[str]]
StrList = Collection[str]
OptStrList = Optional[StrList]

def array(a, dtype:type=None)->np.ndarray:
    "Same as `np.array` but also handles generators. `kwargs` are passed to `np.array` with `dtype`."
    if np.int_==np.int32 and dtype is None and is_listy(a) and len(a) and isinstance(a[0],int):
        dtype=np.int64
    return np.array(a, dtype=dtype)


def is1d(a:Collection)->bool:
    "Return `True` if `a` is one-dimensional"
    return len(a.shape) == 1 if hasattr(a, 'shape') else len(np.array(a).shape) == 1


def is_listy(x:Any)->bool: return isinstance(x, (tuple,list))

def chunks(l:Collection, n:int)->Iterable:
    "Yield successive `n`-sized chunks from `l`."
    for i in range(0, len(l), n): yield l[i:i+n]

def listify(p:OptListOrItem=None, q:OptListOrItem=None):
    "Make `p` listy and the same length as `q`."
    if p is None: p=[]
    elif isinstance(p, str):          p = [p]
    elif not isinstance(p, Iterable): p = [p]
    #Rank 0 tensors in PyTorch are Iterable but don't have a length.
    else:
        try: a = len(p)
        except: p = [p]
    n = q if type(q)==int else len(p) if q is None else len(q)
    if len(p)==1: p = p * n
    assert len(p)==n, f'List len mismatch ({len(p)} vs {n})'
    return list(p)



def df_names_to_idx(names:IntsOrStrs, df:DataFrame):
    "Return the column indexes of `names` in `df`."
    if not is_listy(names): names = [names]
    if isinstance(names[0], int): return names
    return [df.columns.get_loc(c) for c in names]

def index_row(a:Union[Collection,pd.DataFrame,pd.Series], idxs:Collection[int])->Any:
    "Return the slice of `a` corresponding to `idxs`."
    if a is None: return a
    if isinstance(a,(pd.DataFrame,pd.Series)):
        res = a.iloc[idxs]
        if isinstance(res,(pd.DataFrame,pd.Series)): return res.copy()
        return res
    return a[idxs]



def show_some(items:Collection, n_max:int=5, sep:str=','):
    "Return the representation of the first  `n_max` elements in `items`."
    if items is None or len(items) == 0: return ''
    res = sep.join([f'{o}' for o in items[:n_max]])
    if len(items) > n_max: res += '...'
    return res

class ItemBase():
    "Base item type in the fastai library."
    def __init__(self, data:Any): self.data=self.obj=data
    def __repr__(self)->str: return f'{self.__class__.__name__} {str(self.data)}'
    def show(self, ax:plt.Axes, **kwargs):
        "Subclass this method if you want to customize the way this `ItemBase` is shown on `ax`."
        ax.set_title(str(self))
    def __eq__(self, other): return recurse_eq(self.data, other.data)

def recurse_eq(arr1, arr2):
    if is_listy(arr1): return is_listy(arr2) and len(arr1) == len(arr2) and np.all([recurse_eq(x,y) for x,y in zip(arr1,arr2)])
    else:              return np.all(np.atleast_1d(arr1 == arr2))


def range_of(x):
    "Create a range from 0 to `len(x)`."
    return list(range(len(x)))