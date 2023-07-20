"""
============================== 핵심일 ==============================
===== 사용법 =====
from thenews.news.report.collector import *

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

# 전역변수

# 나의 패키지

# 오픈 패키지

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
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbg_on)
    inputs = dbg.inputs(inspect.currentframe(), dbg_on)
    """
    뉴스_컬렉터_작업현황_보고
    report.collector.
    """
    뉴스_수집완료TN_현황보고(dbg_on)
    화면배치TBL과_뉴스원본TBL간의_공통컬럼_각각에_대해_유일값_개수비교_보고()
    res컬럼의_None_NotNone_분포현황_보고(dbg_on)
    res컬럼이_NotNone인_문서의_URL분포현황_보고(dbg_on)


def collected_true(dbg_on=True):
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbg_on)
    inputs = dbg.inputs(inspect.currentframe(), dbg_on)
    from thenews import news
    """
    =====  =====
    뉴스_수집완료TN_현황보고
    True or None
    ===== 사용법 =====
    report.collected_true()
    ===== 작업순서 =====
    """
    A = '화면배치TBL에서 수집완료 컬럼을 로딩'
    B = '그룹-카운트'

    tbl = db[news.TBL]
    projection = {'_id':1, '수집완료':1}
    cursor = tbl.find(projection=projection)
    df = pd.DataFrame(list(cursor))

    df = df.fillna('_None')
    dbg.df_structure(df)

    g = df.groupby('수집완료').count()
    print("\n df.groupby('수집완료').count() :\n\n {}".format(g))
    return g


def compare_unique_values_of_shared_col(dbg_on=False):
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbg_on)
    inputs = dbg.inputs(inspect.currentframe(), dbg_on)
    from thenews import layout
    from thenews import news
    import __pymongo as mg
    """
    화면배치TBL과_뉴스원본TBL간의_공통컬럼_각각에_대해_유일값_개수비교_보고
    공통컬럼의 의미
    화면배치TBL : _id -> 뉴스_원본TBL : 화면배치id
    화면배치TBL : href -> 뉴스_원본TBL : 뉴스_url
    화면배치TBL : 수집일시 -> 뉴스_원본TBL : 수집일시
    ===== 사용법 =====
    report.compare_unique_values_of_shared_col()
    """
    컬럼tpl_li = [
        ('_id', '화면배치id'),
        ('href', '뉴스_url'),
        ('수집일시', '수집일시')
    ]
    tbl_a = layout.TBL#'화면배치'
    col_a = '_id'
    tbl_b = news.TBL#'뉴스_원본'
    col_b = '화면배치id'
    for tpl in 컬럼tpl_li:
        col_a = tpl[0]
        col_b = tpl[1]
        mg.테이블A의_컬럼a와_테이블B의_컬럼b_간의_개수비교_보고(db=db, tbl_a=tbl_a, col_a=col_a, tbl_b=tbl_b, col_b=col_b, dbg_on=dbg_on)


def res컬럼의_None_NotNone_분포현황_보고(dbg_on=False):
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbg_on)
    inputs = dbg.inputs(inspect.currentframe(), dbg_on)
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
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbg_on)
    inputs = dbg.inputs(inspect.currentframe(), dbg_on)
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
============================== News_Analyzer_ResError ==============================
"""
def 뉴스_원본TBL_r_txt내용중_서비스이용제한_문구포함된df():
    import re
    query = {'r_txt':{'$regex':'날씨', '$options':1}}
    df = mg.find(db명=DB명, tbl명=PARSING_TBL, query=None, projection=None, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')
    df = df[ df['r_txt'].str.contains(pat='제한', case=False, flags=re.IGNORECASE, na=None, regex=True) ]
