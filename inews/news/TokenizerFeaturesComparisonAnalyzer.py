# 오픈 패키지
import inspect
import pprint
pp = pprint.PrettyPrinter(indent=2)
import sys

import pandas as pd

# 나의 패키지
sys.path.append('/Users/sambong/p/lib/')
from __nltk import 토큰화_기능비교_보고

# 프로젝트 라이브러리



"""
============================== 핵심일 ==============================
"""

def 뉴스제목_토큰화_기능비교():
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbg_on)
    inputs = dbg.inputs(inspect.currentframe(), dbg_on)
    """
    """
    

    query = {'뉴스제목':{'$regex':'박근혜'}}
    df = 뉴스_로딩(query=None)

    토큰화_기능비교(df=df, 분석할_컬럼명='뉴스제목')


if __name__ == '__main__':
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbg_on)
    inputs = dbg.inputs(inspect.currentframe(), dbg_on)
    뉴스제목_토큰화_기능비교()
