"""
pip를 통해 설치해야할 패키지들.

임시사용법 :
from inews.libs import dbg

정상사용법 :
import idebug as dbg
"""
import os
from inews import PKG_PATH
PJTS_PATH = os.path.dirname(PKG_PATH)
import sys
sys.path.append(f"{PKG_PATH}/idebug")
sys.path.append(f"{PKG_PATH}/idatetime")
