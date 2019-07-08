
import os
print(f"\n os.getcwd() :\n{os.getcwd()}")
PJT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"\n PJT_PATH :\n{PJT_PATH}")
print(f"\n package_path :\n{os.path.abspath(__file__)}")
DATA_PATH = f"{os.path.abspath(__file__)}/data"
import sys
print(f"\n sys.modules[__name__].__file__ :\n{sys.modules[__name__].__file__}")
