
import io,operator,sys,os,re,mimetypes,csv,itertools,json,shutil,glob,pickle,tarfile,collections
import hashlib,itertools,types,inspect,functools,random,time,math,bz2,typing,numbers,string


from copy import copy,deepcopy
from pathlib import Path
from collections import OrderedDict,defaultdict,Counter,namedtuple
from collections.abc import Iterable,Iterator,Generator,Sequence
from typing import Union,Optional

# External modules
from pandas.api.types import is_categorical_dtype,is_numeric_dtype
from numpy import array,ndarray


# def is_coll(o):
#     "Test whether `o` is a collection (i.e. has a usable `len`)"
#     #Rank 0 tensors in PyTorch do not have working `len`
#     return hasattr(o, '__len__') and getattr(o,'ndim',1)