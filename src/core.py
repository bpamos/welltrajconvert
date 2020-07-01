import math, matplotlib.pyplot as plt, numpy as np, pandas as pd, random
import abc, collections, hashlib, itertools, json, operator, pathlib


from dataclasses import dataclass, field, InitVar
from pathlib import Path
from pandas import Series, DataFrame
from scipy.ndimage.interpolation import shift

# for utm conversion
import utm

# for type annotations
from numbers import Number
from typing import Any, AnyStr, Callable, Collection, Dict, Hashable, Iterator, List, Mapping, NewType, Optional
from typing import Sequence, Tuple, TypeVar, Union

# contains essential util functions to format and split data
PathOrStr = Union[Path,str]