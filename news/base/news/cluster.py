"""
============================== 핵심일 ==============================
클래스다.

===== 자료구조 : 테이블 구조 =====
뉴스id
타겟col명_클러스터-알고리즘

뉴스id
뉴스제목_miniKmeans
뉴스제목_명사요약_miniKmeans

===== 용어 정의 =====
n_clusters : 분류명의 개수
액션 : 함수의 일.
예) 액션 -> clst

타겟tbl명 : 클러스터할 테이블명
타겟col명 : 액션을 수행할 대상 컬럼명 --> 반드시 값이 문자열이어야 한다.
키col : _id, 뉴스id 등의 키컬렴명
타겟자료 : 타겟 테이블의 타겟 컬럼과 _id

===== 클러스터 방법 =====
2가지.
- 1. 뉴스XX를 직접 클러스터
- 2. ETRI언어분석 결과중 명사만 추출해 요약문을 만들어 클러스터.

유사도를 어떻게 계산해서 숫자로 표현할 것인가? 일단 해봐?
- 사용된 단어의 매칭율
"""

# 프로젝트 라이브러리
from thenews.__lib__ import *
print('\n' + '# '*5 + sys.modules[__name__].__file__ + ' #'*5)
#doc#print(__doc__)

# 오픈 패키지
import pandas as pd
from datetime import datetime

# 나의 패키지
import __pymongo as mg
import numpy as np
import __sklearn as skl
import __math_report as mthr

# 모듈 라이브러리
import ML

# 백도어
import News_ as news_

# 전역변수


"""
============================== 뉴스_클러스터 ==============================
"""
def 뉴스_다중타겟_다중조건_클러스터():
    print('\n' + '='*60 + inspect.stack()[0][3])
    """
    조건 하나당 실행시간 : 3620.60371
    총 조건 100개의 실행시간 : 3620.605005
    """
    시작시간 = datetime.now()

    print('\n' + '='*60 + '클러스터_타겟조합_튜플리스트_정의')
    클러스터타겟_tpli = [
        ('뉴스' ,'_id', '뉴스제목'),
        ('뉴스' ,'_id', '뉴스본문'),

        ('뉴스_ETRI언어분석' ,'뉴스id', '뉴스제목srl_WSDNNGli'),
        ('뉴스_ETRI언어분석' ,'뉴스id', '뉴스본문srl_WSDNNGli'),
        ('뉴스_ETRI언어분석' ,'뉴스id', '뉴스본문srl_WSDNNGli_중복제거'),
    ]
    sampling_li = list(range(1000, 2000, 1000))
    algorithm_li = ['MiniBatchKMeans', 'KMeans']

    ML.cluster.다중타겟_다중조건_클러스터(클러스터타겟_tpli=클러스터타겟_tpli, 샘플링기준_tpNum=4, sampling_li=sampling_li, n_cluster_ratio=1/15, algorithm_li=algorithm_li)

"""
============================== News_ClusterJoiner ==============================
"""
def 뉴스id로_뉴스원본자료를_결합해서_df로딩(df1, col명='뉴스제목', dbg_on=False):
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbg_on)
    inputs = dbg.inputs(inspect.currentframe(), dbg_on)
    """
    뉴스 제목/본문을 특정해서 결합시킬 때 사용한다.
    """
    """
    ============================== 뉴스id를_추출해_뉴스TBL의_원본컬럼의_자료로딩 ==============================
    원본col명 : 뉴스제목srl_WSDNNGli -> 뉴스제목
    tbl명을 "뉴스" 로 특정할 건인가? 아니면, "d['타겟tbl명']" 를 사용할 것인가.
    """
    print('\n' + '= '*30 + '뉴스id를_추출해_뉴스TBL의_원본컬럼정보를_로딩 -> df2')
    if '_id' in list(df1.columns): del(df1['_id'])

    뉴스id_li = list(df1['뉴스id'])
    query = {'_id':{'$in':뉴스id_li}}
    projection = {'_id':1, col명:1}
    df2 = mg.find(db명=DB명, tbl명=news_.TBL명, query=query, projection=projection, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')
    if dbg_on == True: print('\n df2.dtypes :\n', df2.dtypes)

    """
    ============================== 덧붙임 ==============================
    """
    print('\n' + '= '*30 + '덧붙임 -> df3')
    df3 = df2.join(df1.set_index('뉴스id'), on='_id')
    if dbg_on == True: print('\n df3.dtypes :\n', df3.dtypes)
    if dbg_on == True: pp.pprint({'len(df3)':len(df3)})
    if dbg_on == True: print('\n df3.iloc[:1,]\n', df3.iloc[:1,])

    return df3

"""
============================== 클러스터완료 현황보고 ==============================
클러스터는 문서의 수가 많아질수록 다시 해야 하는 경우이므로,
클러스터완료 여부는 저장할 필요없다. 따라서 보고도 필요없다.
"""



if __name__ == '__main__':
    print('\n' + '='*60 + sys.modules[__name__].__file__)
    #pp.pprint({'sys.path':sys.path})
    #pp.pprint({'dir()':dir()})

    sampling = 5000 # 10 보다 큰수를 넣는게 당연하지...
    n_clusters = int(round(sampling / 10, 0)) if sampling >= 20 else 2
    뉴스_다중타겟_다중조건_클러스터()
    #ML.cluster.단일조건_뉴스_클러스터(타겟tbl명='뉴스', 키col명='_id', 타겟col명='뉴스제목', algorithm='KMeans', sampling=sampling, n_clusters=n_clusters, dbg_on=False, 사전검증=False)


    #clst결과로_뉴스원본자료를_결합해서_df로딩(타겟tbl명='뉴스_ETRI언어분석', 타겟col명='뉴스제목srl_WSDNNGli', algorithm='KMeans', sampling=10000, dbg_on=False)

    #뉴스_클러스터TBL의_뉴스TBL에_대한_KeyidLabel_dicli의_id명을_keyid로_변경()
