# 오픈 패키지
import sys

# 나의 패키지
sys.path.append('/Users/sambong/p/lib/')
from default_openModule_for_everyNewFile import *

import load
from __nltk import 트윗_단어빈도수_보고

# 프로젝트 라이브러리
from thenews.__lib__ import *


# 모듈 라이브러리

"""
============================== 핵심일 : 용어정의 ==============================
"""

def 뉴스제목의_단어빈도수_보고():
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbg_on)
    inputs = dbg.inputs(inspect.currentframe(), dbg_on)
    """
    """
    


    li = list(df['뉴스제목'])
    트윗_단어빈도수_보고(li)


if __name__ == '__main__':
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbg_on)
    inputs = dbg.inputs(inspect.currentframe(), dbg_on)
    pp.pprint({'sys.path':sys.path})
    pp.pprint({'dir()':dir()})
    뉴스제목의_단어빈도수_보고()
