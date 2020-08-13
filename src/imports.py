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

# for crs transformation
from pyproj import CRS
from pyproj import Transformer

# for type annotations
from typing import Any, Dict, List, Optional, Union, Collection


PathOrStr = Union[Path,str]
IntsOrStrs = Union[int, Collection[int], str, Collection[str]]