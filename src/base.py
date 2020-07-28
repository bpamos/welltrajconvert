from .imports import *


# TODO: reduce to only what you will really need
def setify(o): return o if isinstance(o, set) else set(L(o))


def _is_array(x): return hasattr(x, '__array__') or hasattr(x, 'iloc')


def _listify(o):
    if o is None: return []
    if isinstance(o, list): return o
    if isinstance(o, str) or _is_array(o): return [o]
    return [o]


class CollBase:
    "Base class for composing a list of `items`"

    def __init__(self, items): self.items = items

    def __len__(self): return len(self.items)

    def __getitem__(self, k): return self.items[list(k) if isinstance(k, CollBase) else k]

    def __setitem__(self, k, v): self.items[list(k) if isinstance(k, CollBase) else k] = v

    def __delitem__(self, i): del (self.items[i])

    def __repr__(self): return self.items.__repr__()

    def __iter__(self): return self.items.__iter__()


class L(CollBase):
    "Behaves like a list of `items` but can also index with list of indices or masks"
    _default = 'items'

    def __init__(self, items=None, *rest, use_list=False):
        if rest: items = (items,) + rest
        if items is None: items = []
        if (use_list is not None) or not _is_array(items):
            items = list(items) if use_list else _listify(items)
        super().__init__(items)
