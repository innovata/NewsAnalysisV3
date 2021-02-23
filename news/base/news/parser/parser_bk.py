"""
============================== 핵심일 ==============================
news TBL 의 뉴스기사의 파싱은 개별 언론사 모듈에서 수행한다.

r_txt 의 r은 response 객체

뉴스_원본 테이블의 쌩데이터를 정규화해서 뉴스 테이블에 저장한다.

뉴스_원본 테이블에 "파싱대상" 컬럼을 새로 추가해서 데이터 접근을 빠르게 도와준다.
- None : 파싱대상여부의 가치판단 이전
- True : 파싱대상여부의 가치판단 후 YES
- False : 파싱대상여부의 가치판단 후 No 또는 파싱완료
"""
# 프로젝트 라이브러리
from thenews.__lib__ import *
print('\n' + '# '*5 + sys.modules[__name__].__file__ + ' #'*5)

# 나의 패키지
import __datetime as dth
import __pymongo as mg
import __list as lh
#import Programming_Collective_Intelligence as PCI

# 프로젝트 라이브러리

# 오픈 패키지
from bs4 import BeautifulSoup

# 전역변수
"""
============================== 파싱타겟 선정 ==============================
현재 3가지 방법
1. 파싱대상컬럼이_True인_대상로딩 -> 파싱대상TF
2. 뉴스URL_중복제거로_tpl로딩 -> URL중복제거
3. load_parsing_news

최종 3번이 가장 효율적
"""

def 파싱할_뉴스원본을_URL중복제거로_선정후_dicli로딩(파싱컬럼명='r_txt', dbg_on=False):
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbg_on)
    inputs = dbg.inputs(inspect.currentframe(), dbg_on)

    tpl = 뉴스URL_중복제거로_tpl로딩(dbg_on, shown_cnt=1)
    파싱할url_li = tpl[2]
    query = {'뉴스_url':{'$in':파싱할url_li}}
    projection = {'_id':1, '뉴스_url':1, 파싱컬럼명:1, '수집일시':1}
    dicli = mg.find(db명=DB명, tbl명=PARSING_TBL, query=query, projection=projection, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='dicli')
    return dicli

def 뉴스URL_중복제거로_tpl로딩(dbg_on=False, shown_cnt=1):
    뉴스원본url_li = mg.distinct(db명=DB명, tbl명=PARSING_TBL, col명='뉴스_url', query=None, dbg_on=dbg_on, shown_cnt=shown_cnt)
    뉴스url_li = mg.distinct(db명=DB명, tbl명=PARSED_TBL, col명='뉴스_url', query=None, dbg_on=dbg_on, shown_cnt=shown_cnt)
    파싱할url_li = lh.리스트1로부터_리스트2를_제거(li1=뉴스원본url_li, li2=뉴스url_li)
    return (뉴스원본url_li, 뉴스url_li, 파싱할url_li)

def 파싱완료True가_아닌_타겟의_query조건별_개수비교_보고(dbg_on=False):
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbg_on)
    inputs = dbg.inputs(inspect.currentframe(), dbg_on)
    """
    결과
      id개수               query
    0  1276  'res':{'$ne':None}
    1   468          'res':None
    2  1744                   _
    """

    query = {'파싱완료':{'$ne':True}, 'res':{'$ne':None}}
    li1 = mg.distinct(db명=DB명, tbl명=PARSING_TBL, col명='_id', query=query, dbg_on=dbg_on, shown_cnt=1)

    query = {'파싱완료':{'$ne':True}, 'res':None}
    li2 = mg.distinct(db명=DB명, tbl명=PARSING_TBL, col명='_id', query=query, dbg_on=dbg_on, shown_cnt=1)

    query = {'파싱완료':{'$ne':True}}
    li3 = mg.distinct(db명=DB명, tbl명=PARSING_TBL, col명='_id', query=query, dbg_on=dbg_on, shown_cnt=1)

    print('\n'+'*'*60+inspect.stack()[0][3])
    dic = {
        'id개수':[len(li1), len(li2), len(li3)],
        'query':["'res':{'$ne':None}", "'res':None", "_"],
        'id_li':[li1, li2, li3]
    }
    df = pd.DataFrame(dic)
    df1 = df.copy()
    del(df1['id_li'])
    print(df1)
    return df

"""
============================== 파싱완료 업뎃 ==============================
"""
def 뉴스TBL에_뉴스URL이_존재하면_뉴스원본TBL의_파싱완료를_True로_일괄업뎃(dbg_on=False, shown_cnt=1, 사전검증=False):
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbg_on)
    inputs = dbg.inputs(inspect.currentframe(), dbg_on)
    """
    """

    입력 = {'shown_cnt':shown_cnt, '사전검증':사전검증}


    query = {'뉴스_url':{'$exists':1}}
    뉴스url_li = mg.distinct(db명=DB명, tbl명=PARSED_TBL, col명='뉴스_url', query=query, dbg_on=dbg_on, shown_cnt=shown_cnt)

    query = {'뉴스_url':{'$in':뉴스url_li}}
    update = {'$set':{'파싱완료':True}}
    mg.update_many(db명=DB명, tbl명=PARSING_TBL, query=query, update=update, upsert=False, dbg_on=dbg_on, 사전검증=사전검증)
"""
============================== 파싱_제어 ==============================
"""
def 뉴스_단위파싱(뉴스_dic, dbg_on=False, 사전검증=False):
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbg_on)
    inputs = dbg.inputs(inspect.currentframe(), dbg_on)
    """
    뉴스자료구조를 별도로 정의하는 이유는, 뉴스_dic에서 직접 'r_text' 키를 제거할 수가 없어서다.
    """
    d = 뉴스_dic.copy()
    뉴스자료구조 = {
        '뉴스_원본id':d['_id'],
        '뉴스_url':d['뉴스_url'],
        '수집일시':d['수집일시'],
    }

    뉴스_dic = res컬럼에_대한_json_normalizer(뉴스_dic, dbg_on)

    if 'naver' in d['뉴스_url']:
        뉴스자료구조 = 네이버_파싱(뉴스자료구조=뉴스자료구조, 뉴스_dic=뉴스_dic, dbg_on=dbg_on, 사전검증=사전검증)
    elif 'daum' in d['뉴스_url']:
        print('\n\n 임마 ! daum 파서 만들어라 씨빠로마. \n\n')
    else:
        print('\n\n 임마 ! 빨리 핵심대상별로 파서 만들어라 씨빠로마. \n\n')
        뉴스자료구조 = {}

    if len(뉴스자료구조) == 0:
        print('if len(뉴스자료구조) == 0:')
    else:
        mg.insert_one(db명=DB명, tbl명=PARSED_TBL, dic=뉴스자료구조, dbg_on=dbg_on, 사전검증=사전검증)
        update_parsing_complete(dic=뉴스_dic, dbg_on=dbg_on, 사전검증=사전검증)

def res컬럼에_대한_json_normalizer(dic, dbg_on=False):
    from pandas.io.json import json_normalize
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbg_on)
    inputs = dbg.inputs(inspect.currentframe(), dbg_on)

    pp.pprint({'res_dic의 keys':list(dic.keys())})

    df = json_normalize(data=[dic], record_path='res', meta=['_id','뉴스_url','수집일시'], meta_prefix=None, record_prefix='r_', errors='raise', sep='.')
    df = df.loc[:,['_id','뉴스_url','수집일시','r_text']]
    if dbg_on == True: dbg._df(df, caller=inspect.stack()[0][3], 컬럼순서li=[], df보고형태='df')
    dicli = df.to_dict('records')
    dic = dicli[0]
    if dbg_on == True: pp.pprint(dic)
    return dic

def UnitTest_뉴스_단위파싱(dbg_on=True, 사전검증=True):
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbg_on)
    inputs = dbg.inputs(inspect.currentframe(), dbg_on)

    query = {'파싱완료':{'$ne':True}}
    projection = {'_id':1, '뉴스_url':1, '수집일시':1, 'res':1}
    dicli = mg.find_limit(db명=DB명, tbl명=PARSING_TBL, query=query, projection=projection, limit_cnt=1, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='dicli')
    if len(dicli) == 0:
        print('if len(dicli) == 0:')
    else:
        d = dicli[0]
        뉴스_단위파싱(d, dbg_on, 사전검증)
