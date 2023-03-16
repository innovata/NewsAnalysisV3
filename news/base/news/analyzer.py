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
============================== 수집현황 보고 ==============================
"""
def 뉴스_컬렉터_작업현황_보고(dbg_on=False):
    print('\n' + '@'*60 + inspect.stack()[0][3])

    뉴스_수집완료TN_현황보고(dbg_on)
    화면배치TBL과_뉴스원본TBL간의_공통컬럼_각각에_대해_유일값_개수비교_보고()
    res컬럼의_None_NotNone_분포현황_보고(dbg_on)
    res컬럼이_NotNone인_문서의_URL분포현황_보고(dbg_on)

def 뉴스_수집완료TN_현황보고(dbg_on=False):
    print('\n' + '@'*60 + inspect.stack()[0][3])
    """
    True or None
    ===== 작업순서 =====
    화면배치TBL에서 수집완료 컬럼을 로딩
    그룹-카운트
    """

    projection = {'_id':1, '수집완료':1}
    df = mg.find(db명=DB명, tbl명=COLLECTING_TBL, query=None, projection=projection, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')
    df = df.fillna('_None')
    print(df.dtypes)

    g = df.groupby('수집완료').count()
    print(g)
    return g

def 화면배치TBL과_뉴스원본TBL간의_공통컬럼_각각에_대해_유일값_개수비교_보고(db명=DB명, tbl_A='화면배치', col_a='_id', tbl_B='뉴스_원본', col_b='화면배치id', dbg_on=False, shown_cnt=1):
    print('\n' + '@'*60 + inspect.stack()[0][3])
    """
    공통컬럼의 의미
    화면배치TBL : _id -> 뉴스_원본TBL : 화면배치id
    화면배치TBL : href -> 뉴스_원본TBL : 뉴스_url
    화면배치TBL : 수집일시 -> 뉴스_원본TBL : 수집일시
    """
    컬럼tpl_li = [
        ('_id', '화면배치id'),
        ('href', '뉴스_url'),
        ('수집일시', '수집일시')
    ]
    for tpl in 컬럼tpl_li:
        col_a = tpl[0]
        col_b = tpl[1]
        mg.테이블A의_컬럼a와_테이블B의_컬럼b_간의_개수비교_보고(db명=db명, tbl_A=tbl_A, col_a=col_a, tbl_B=tbl_B, col_b=col_b, dbg_on=dbg_on, shown_cnt=shown_cnt)

def res컬럼의_None_NotNone_분포현황_보고(dbg_on=False):
    print('\n' + '@'*60 + inspect.stack()[0][3])
    """
    """
    query = {'res':None}
    projection = {'_id':1}
    df1 = mg.find(db명=DB명, tbl명=PARSING_TBL, query=query, projection=projection, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')

    query = {'res':{'$ne':None}}
    projection = {'_id':1}
    df2 = mg.find(db명=DB명, tbl명=PARSING_TBL, query=query, projection=projection, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')

    rpt_dic = {
        'res = None 인 문서 개수':len(df1),
        'res = Not None 인 문서 개수':len(df2),
    }

    pp.pprint(rpt_dic)

def res컬럼이_NotNone인_문서의_URL분포현황_보고(dbg_on=False):
    print('\n' + '@'*60 + inspect.stack()[0][3])
    """
    URL를 파싱하고 URI, 서비스함수, 쿼리스트링별 등등 다각도로 분석할 필요가 있을까?
    """

    query = {'res':{'$ne':None}}
    projection = {'_id':1, '뉴스_url':1}
    df = mg.find(db명=DB명, tbl명=PARSING_TBL, query=query, projection=projection, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')

    g = df.groupby('뉴스_url').count().sort_values('_id', ascending=False)
    print(g)
    return g


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

"""
============================== News_Analyzer_ResError ==============================
"""

def 뉴스_원본TBL_r_txt내용중_서비스이용제한_문구포함된df():
    import re
    query = {'r_txt':{'$regex':'날씨', '$options':1}}
    df = mg.find(db명=DB명, tbl명=PARSING_TBL, query=None, projection=None, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')
    df = df[ df['r_txt'].str.contains(pat='제한', case=False, flags=re.IGNORECASE, na=None, regex=True) ]


if __name__ == '__main__':
    print('\n' + '='*60 + sys.modules[__name__].__file__)

    """
    mg.TBL_자료구조_보고(db명=DB명, tbl명='화면배치', col_uq=False, 보고제외할col_li=[])
    mg.TBL_자료구조_보고(db명=DB명, tbl명='뉴스_원본', col_uq=False, 보고제외할col_li=['res'])
    mg.TBL_자료구조_보고(db명=DB명, tbl명='뉴스', col_uq=False, 보고제외할col_li=['res'])
    """


    #뉴스_컬렉터_작업현황_보고(dbg_on=False)
    """
    res컬럼이_NotNone인_문서의_URL분포현황_보고(dbg_on=False)
    res컬럼의_None_NotNone_분포현황_보고(dbg_on=False)
    #뉴스_파싱완료_현황보고(dbg_on=False)
    """

    #뉴스_파서_작업현황_보고(dbg_on=False)
    """
    """
    보고용_뉴스df_기초검사_및_청소후_로딩()
