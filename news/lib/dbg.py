
# 2019.07.12

import inspect
import pprint
pp = pprint.PrettyPrinter(indent=2)
import os
from datetime import datetime
import re
import sys

#============================================================
print(f"{'*'*50} {__name__} | Start.\n\nEnvironment Checking...\n\n")
#============================================================

try:
    dbgon = os.environ['DEBUG_ON']
except Exception as e:
    print(f"Exception : {e}\n=== Guide ===\nIf you want to debug something, setup below :\nexport DEBUG_ON=True")
    dbgon = False
finally:
    print(f"Default Setup : dbgon = {dbgon}")

print(f"\n{'*'*50} {__name__} | End.")

#============================================================
"""Base Code."""
#============================================================

p_hidden = re.compile('^_.*')


def clsattrs(cls, loose=False):
    whoiam = f"{__name__}.{inspect.stack()[0][3]} | cls : {cls.__class__.__name__}"
    try:
        attrs = dir(cls)
        if loose:
            attrs = [e for e in attrs if p_hidden.match(e) is None]
        for attr in attrs:
            v = getattr(cls, attr)
            print(f"{'-'*50} {whoiam}\na : {attr}\nv : {v}\nt : {type(v)}")
            if isinstance(v, dict):
                pp.pprint(v)
    except Exception as e:
        print(f"{'#'*50} {whoiam}\nException : {e}")

def clsdict(cls, loose=False):
    whoiam = f"{__name__}.{inspect.stack()[0][3]} | cls : {cls.__class__.__name__}"
    try:
        dkeys = list(cls.__dict__)
        if loose:
            dkeys = [e for e in dkeys if p_hidden.match(e) is None]
        for k,v in cls.__dict__.items():
            if k in dkeys:
                print(f"{'-'*50} {whoiam}\n{k} : {v}")
                if isinstance(v, dict):
                    pp.pprint(v)
    except Exception as e:
        print(f"{'#'*50} {whoiam}\nException : {e}")



from ilib import inumber

class Loop:
    start_dt = datetime.now()
    count = 0

    def __init__(self, iterable, func):
        self.it = iter(iterable)
        self.len = len(iterable)
        # sefl.itname = iterable.__name__
        self.f = func

    def next(self):
        if hasattr(self.f, '__qualname__'):
            whoiam = f"{self.f.__module__}.{self.f.__qualname__}"
        else:
            whoiam = f"{self.f.__module__}.{self.f.__name__}"
        self.count += 1
        print(f"{'-'*50} {whoiam} ({self.count}/{self.len})")
        # self.it.next()
        next(self.it)
        pass


class Looper:

    def __init__(self, cframe, len, exp_runtime=60):
        self.start_dt = datetime.now()
        self.count = 1
        self.len = len
        self.exp_runtime = exp_runtime
        frameinfo = inspect.getframeinfo(frame=cframe)
        self.caller = f"{frameinfo.filename} | {frameinfo.function}"

    def report(self, addi_info):
        whoiam = f"{'*'*50} {__name__}.{__class__.__qualname__}"
        cum_runtime = (datetime.now() - self.start_dt).total_seconds()
        avg_runtime = cum_runtime / self.count
        leftover_runtime = avg_runtime * (self.len - self.count)
        print(f"{whoiam} | ({self.count}/{self.len})")
        print(f" caller : {self.caller}\n addi_info : {addi_info}")
        tpls = [
            ('누적실행시간', cum_runtime),
            ('잔여실행시간', leftover_runtime),
            ('평균실행시간', avg_runtime),
        ]
        for tpl in tpls:
            timeexp, unit = inumber.convert_timeunit(tpl[1])
            print(f" {tpl[0]} : {timeexp} ({unit})")
        if self.count == self.len:
            if avg_runtime > self.exp_runtime:
                print(f"{whoiam}\n Save the final report into DB.")
        self.count += 1
        return self

def fruntime(f):
    def func_runtime(*args, **kwargs):
        start_dt = datetime.now()
        rv = f(*args, **kwargs)
        runt = (datetime.now() - start_dt).total_seconds()
        timeexp, unit = inumber.convert_timeunit(runt)
        print(f"{'*'*50} {__name__}.{inspect.stack()[0][3]}")
        # if hasattr(f, '__qualname__'):
        #     fname = f"{f.__module__}.{f.__qualname__}"
        # else:
        #     fname = f"{f.__module__}.{f.__name__}"
        print(f"{f.__module__}.{f.__qualname__} : {timeexp} ({unit})")
        return rv
    return func_runtime

def utestfunc(f):
    def func(*args, **kwargs):
        print(f"\n{'='*50} {f.__module__}.{f.__qualname__}")
        start_dt = datetime.now()
        rv = f(*args, **kwargs)
        runt = (datetime.now() - start_dt).total_seconds()
        timeexp, unit = inumber.convert_timeunit(runt)
        print(f"\nTest Runtime : {timeexp} ({unit})")
        return rv
    return func

def objsize(obj, seen=None):
    """Recursively finds size of objects
    https://goshippo.com/blog/measure-real-size-any-python-object/
    """
    whoiam = f"{__name__}.{inspect.stack()[0][3]}"
    print(f"{'*'*50} {whoiam}")
    print(f"type : {type(obj)}")
    print(f"size : {sys.getsizeof(obj)} (bytes)")
    try:
        if hasattr(obj, '__name__'):
            print(f"objname : {obj.__name__}")
    except Exception as e:
        print(f"{'#'*50} {whoiam}\nException : {e}")
    try:
        print(f"len : {len(obj)}")
    except Exception as e:
        print(f"{'#'*50} {whoiam}\nException : {e}")

    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])

def printdf(df, slen=10):
    whoiam = f"{__name__}.{inspect.stack()[0][3]}"
    print(f"{'*'*50} {whoiam}")
    try:
        print(df.info())
        print(f"\ndf[:1].T :\n{df[:1].T}")
        if len(df) > 50:
            print(f"\ndf[:{slen}] :\n{df.head(abs(slen))}")
            print(f"\ndf[{-1*slen}:] :\n{df.tail(abs(slen))}")
        else:
            print(f"\ndf :\n{df}")
        print(f"\ndf[-1:].T :\n{df[-1:].T}")
    except Exception as e:
        print(f"{'#'*50} {whoiam}\nException : {e}")


def printiter(iterable, slen=10):
    print(f"{'*'*50} {__name__}.{inspect.stack()[0][3]}")
    print(f"len(iterable) : {len(iterable)}")
    if len(iterable) > 50:
        print(f"\niterable[:{slen}] :")
        pp.pprint(iterable[:slen])
        print(f"\niterable[{-1*slen}:] :")
        pp.pprint(iterable[-1*slen:])
    else:
        pp.pprint(iterable)
