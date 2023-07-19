"""
============================== 핵심일 ==============================
클래스다.
여러 파일로부터 모은 함수의 집합체이다.

데이터가 많아질수록, 모든 컬럼을 한번에 로딩하는 개수작을 하지마라.

다음 동기화 서브클래스를 참조할 것.
- News_CollectorSynchronizer
- News_ParserSynchronizer

뉴스제목본문_분석
    - ETRI 분석
        - morpheme 분석
    - sklearn 분석
        - cluster 분석

"""
# 프로젝트 라이브러리
from thenews.__lib__ import *
print('\n' + '# '*5 + sys.modules[__name__].__file__ + ' #'*5)
#doc#print(__doc__)

# 나의 패키지
import __pymongo as mg

# 프로젝트 라이브러리
import Layout as lay

# 오픈 패키지
import pandas as pd

# 전역변수
from News_ import *

# 모듈 내부 클래스들
#import News_Collector as _collector


def 보고용_뉴스df_기초검사_및_청소후_로딩(dbg_on=False):
    import News_Classifier as classifier
    import Cleaner
    """
    분류된 뉴스 자료 로딩
    기초 검사 및 청소
    """
    df, g = classifier.News_Predicted_Orig_df로딩(test_tbl='뉴스', test_col='뉴스본문', dbg_on=dbg_on)
    df = df.rename(columns={'_id':'news_id'})
    df = Cleaner.보고용df에_불필요한_수집파싱완료_원본id_컬럼삭제(df=df)
    df = Cleaner.df컬럼들에_대한_중복처리(df=df, subset=['뉴스_url','뉴스제목','뉴스본문'], action='제거')
    return df

"""
============================== 파싱현황 보고 ==============================
"""

def 뉴스_파서_작업현황_보고(dbg_on=False):
    print('\n' + '@'*60 + inspect.stack()[0][3])

    뉴스_파싱완료TN_분포현황보고(dbg_on)

def 뉴스_파싱완료TN_분포현황보고(dbg_on=False):
    print('\n' + '@'*60 + inspect.stack()[0][3])

    projection = {'_id':1, '파싱완료':1}
    df = mg.find(db명=DB명, tbl명=PARSING_TBL, query=None, projection=projection, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')
    df = df.fillna('_None')
    print(df.dtypes)

    g = df.groupby('파싱완료').count()
    print(g)
    return g
