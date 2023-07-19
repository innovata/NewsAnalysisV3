"""
============================== 핵심일 ==============================
===== 사용법 =====
from thenews.news import report
report.collector.f()
report.parser.f() 
"""
# 프로젝트 라이브러리
from thenews.__lib__ import *
print('\n' + '# '*5 + sys.modules[__name__].__file__ + ' #'*5)
#doc#print(__doc__)

# 나의 패키지
import __datetime as dth
import __pymongo as mg
import __list as lh
from __requests import human_req_get

# 프로젝트 라이브러리
import Layout

# 오픈 패키지
from datetime import datetime, date
import pandas as pd

# 전역변수
from News_ import *

"""
============================== 시간추이 ==============================
"""
def 사건번호별_언론사별_뉴스발행수_시간추이(df, EventNum_li):
    import __matplotlib as mpl
    import Report
    print('\n' + '='*60 + inspect.stack()[0][3])

    EventNum_li_len = len(EventNum_li)
    i=1
    for EventNum in EventNum_li:
        print('\n' + '-'*60 + '{}/{}, EventNum:{}'.format(i, EventNum_li_len, EventNum))
        df1 = df[ df['predicted']==EventNum ]

        data = Report.pivot_TimeResampled_data(df1, idx_col='입력일시', clmn_col='언론사명', rsp_period='24H', agg='sum')
        data_ = Report.시간축_맞추기(data)
        mpl.단일창_단일다중_선그래프(df=data_, title='사건번호 {}에 대한 언론사별 뉴스발행 수 시간추이'.format(EventNum), figsize=(12,4))
        i+=1
#        break
