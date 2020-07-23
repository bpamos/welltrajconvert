"`.imports` contains essential packages and modules"
import os, pickle, sys

import abc, json, pathlib, inspect
from abc import abstractmethod
from dataclasses import dataclass, field

# External modules
import matplotlib.pyplot as plt, numpy as np, pandas as pd
from pathlib import Path
from pandas import Series, DataFrame
from scipy.ndimage.interpolation import shift
# for utm conversion
import utm

# for type annotations
#from numbers import Number
from typing import Any, Dict, List, Optional
# from typing import Any, AnyStr, Callable, Collection, Dict, Hashable, Iterator, List, Mapping, NewType, Optional
# from typing import Sequence, Tuple, TypeVar, Union