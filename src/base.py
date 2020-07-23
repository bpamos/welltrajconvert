from .imports import *

def setify(o): return o if isinstance(o,set) else set(L(o))

def _rm_self(sig):
    sigd = dict(sig.parameters)
    sigd.pop('self')
    return sig.replace(parameters=sigd.values())

class FixSigMeta(type):
    "A metaclass that fixes the signature on classes that override __new__"
    def __new__(cls, name, bases, dict):
        res = super().__new__(cls, name, bases, dict)
        if res.__init__ is not object.__init__: res.__signature__ = _rm_self(inspect.signature(res.__init__))
        return res

class NewChkMeta(FixSigMeta):
    "Metaclass to avoid recreating object passed to constructor"
    def __call__(cls, x=None, *args, **kwargs):
        if not args and not kwargs and x is not None and isinstance(x,cls):
            x._newchk = 1
            return x

        res = super().__call__(*((x,) + args), **kwargs)
        res._newchk = 0
        return res

def _is_array(x): return hasattr(x,'__array__') or hasattr(x,'iloc')

def _listify(o):
    if o is None: return []
    if isinstance(o, list): return o
    if isinstance(o, str) or _is_array(o): return [o]
    return [o]

class CollBase:
    "Base class for composing a list of `items`"
    def __init__(self, items): self.items = items
    def __len__(self): return len(self.items)
    def __getitem__(self, k): return self.items[list(k) if isinstance(k,CollBase) else k]
    def __setitem__(self, k, v): self.items[list(k) if isinstance(k,CollBase) else k] = v
    def __delitem__(self, i): del(self.items[i])
    def __repr__(self): return self.items.__repr__()
    def __iter__(self): return self.items.__iter__()


class L(CollBase, metaclass=NewChkMeta):
    "Behaves like a list of `items` but can also index with list of indices or masks"
    _default='items'
    def __init__(self, items=None, *rest, use_list=False, match=None):
        if rest: items = (items,)+rest
        if items is None: items = []
        if (use_list is not None) or not _is_array(items):
            items = list(items) if use_list else _listify(items)
        if match is not None:
            if is_coll(match): match = len(match)
            if len(items)==1: items = items*match
            else: assert len(items)==match, 'Match length mismatch'
        super().__init__(items)


