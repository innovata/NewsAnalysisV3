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
============================== 뉴스 기준 전방위 보고 ==============================
"""
def 화면배치TBL_href와_뉴스원본TBL_뉴스url간의_매핑관계_관찰(dbg_on=False, shown_cnt=1):
    """
    condition_li : 조건튜플 목록 (테이블명, 검사타겟컬럼1, 검사타겟컬럼2, ...)
    """
    condition_li = [
        (lay.TBL명, 'href', '수집일시', '뉴스제목'),
        (RD_TBL명, '뉴스_url', '수집일시', '뉴스_url'),
        (TBL명, '뉴스_url', '수집일시', '뉴스제목')
    ]
    rpt_dicli = []
    for cond in condition_li:
        print('\n' + '-'*60 + ' TBL명:{}, URL컬럼명:{}'.format(cond[0], cond[1]))
        projection = {'_id':1}
        df = mg.find(db명=DB명, tbl명=cond[0], query=None, projection=projection, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')
        url_li = mg.distinct(db명=DB명, tbl명=cond[0], col명=cond[1], query=None, dbg_on=dbg_on, shown_cnt=shown_cnt)
        수집일시_li = mg.distinct(db명=DB명, tbl명=cond[0], col명=cond[2], query=None, dbg_on=dbg_on, shown_cnt=shown_cnt)
        뉴스제목_li = mg.distinct(db명=DB명, tbl명=cond[0], col명=cond[3], query=None, dbg_on=dbg_on, shown_cnt=shown_cnt)
        자료구조_dic = {
            'TBL명':cond[0],
            'URL컬럼명':cond[1],
            '총_doc수':len(df),
            '유일한_URL수':len(url_li),
            '유일한_수집일시수':len(수집일시_li),
            '유일한_뉴스제목수':len(뉴스제목_li),
        }
        rpt_dicli.append(자료구조_dic)

    df = pd.DataFrame(rpt_dicli)
    print(df)
    return df

def 뉴스df_컬럼별_개수():
    print('\n' + '='*60 + inspect.stack()[0][3])

    for col in 뉴스_컬럼순서:
        pp.pprint({col:len(list(df[col].unique()))})

def 특정언론의_뉴스발행수(언론사명_re):
    print('\n' + '='*60 + inspect.stack()[0][3])
    query = {'언론사명':{'$regex':언론사명_re, '$options':'i'}}

    return df

def 언론별_뉴스발행수():
    print('\n' + '='*60 + inspect.stack()[0][3])

    g = df.groupby(누가).count().sort_values('_id',ascending=False)#.query('뉴스_url>1')
    print(g)
    return g

def 클러스터된_뉴스본문에_대해_그루핑개수보고():
    print('\n' + '='*60 + inspect.stack()[0][3])
    df = 뉴스제목본문_클러스터_로딩(query=None, projection=None, dbg_on=False)
    g = df.groupby('뉴스본문label').count()
    dbg._df(df=g, 호출자=inspect.stack()[0][3])

def 특정분류값에_대해_뉴스본문_탐색():
    print('\n' + '='*60 + inspect.stack()[0][3])

    query = {'뉴스본문label':4}
    df = 뉴스제목본문_클러스터_로딩(query=query, projection=None, dbg_on=False)
    뉴스id_li = list(df['뉴스id'])

    query = {'_id':{'$in':뉴스id_li}}
    projection = {'뉴스본문':1}
    df1 = 뉴스_로딩(query=query, projection=projection, dbg_on=False)
    dicli = df1.to_dict('records')
    i=1
    dicli_len = len(dicli)
    for d in dicli:
        print('\n' + '-'*60 + '{}/{}'.format(i, dicli_len))
        s = d['뉴스본문']
        s1 = PCI.stripHTML(h=s, dbg_전문_on=False)
        pp.pprint(s1)
        i+=1
