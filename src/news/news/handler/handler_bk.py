"""
============================== 동기화 작업 ==============================
뉴스 수집 원복자.
화면배치TBL <=> 뉴스_원본TBL

화면배치TBL의 href와 동일한 뉴스원본TBL의 뉴스_url를 가진 문서에
화면배치TBL의 수집일시를 뉴스원본TBL의 수집일시에 업데이트한다.
그러면 싱크되는거지.

뉴스_원본TBL에는 수집일시에 따라 동일한 뉴스_url이 여러개 존재할 필요가 없다.
즉, 뉴스_url = "뉴스"(기사) 그 자체다.
따라서, 뉴스_원본TBL에서 중복제거가 필수다.
수집일시를 순정렬 후 first를 남기고 중복제거한다.

동기화 : 원복, 청소 ...

뉴스_원본TBL의 컬럼은 뉴스_url, 수집일시, r_txt
그 중 뉴스TBL에서 뉴스_url, 수집일시를 복원할 수 있다.
r_txt를 복원 불가능하므로, 뉴스_원본TBL의 r_txt에는 수집시 r_txt가 아예 없는 ""과 구별되도록 "파싱완료" 문자열을 저장하자.

뉴스_원본TBL의 url_li 를 추출
url_li 를 제외한 뉴스TBL의 대상의 dicli을 추출
그 dicli을 뉴스_원본TBL에
"""
# 프로젝트 라이브러리
from thenews.__lib__ import *
print('\n' + '# '*5 + sys.modules[__name__].__file__ + ' #'*5)
#doc#print(__doc__)

# 오픈 패키지
from datetime import datetime, date
import pandas as pd
from pymongo import MongoClient
client = MongoClient()
db = client[DB명]

# 나의 패키지
import __datetime as dth
import __pymongo as mg
import __list as lh

# 모듈 라이브러리
import Layout as lay

# 전역변수
TBL명 = '뉴스'
RD_TBL명 = TBL명 + '_원본'

"""
============================== News_CollectorSynchronizer : 수집완료 컬럼 ==============================
"""
def 화면배치TBL의_수집일시를_뉴스원본TBL에_업뎃(dbg_on=False, 사전검증=False):
    print('\n' + '='*60 + inspect.stack()[0][3])

    projection = {'_id':1, 'href':1, '수집일시':1}
    df = mg.find(db명=DB명, tbl명='화면배치', query=None, projection=projection, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')
    df = df.sort_values(['href', '수집일시'])
    df = df.drop_duplicates(subset=['href'], keep='first', inplace=False)
    dicli = df.to_dict('records')
    dicli_len = len(dicli)
    i=1
    for d in dicli:
        print('\n' + '-'*60 + '{}/{}, 수집일시:{}'.format(i, dicli_len, d['수집일시']))
        query = {'뉴스_url':d['href']}
        update = {'$set':{'수집일시':d['수집일시'], '화면배치id':d['_id']}}
        mg.update_many(db명=DB명, tbl명=PARSING_TBL, query=query, update=update, upsert=True, dbg_on=dbg_on, 사전검증=사전검증)
        #break
        i+=1

    if dbg_on == True:
        print('\n' + '='*60 + inspect.stack()[0][3]+'_검증')
        query = {'화면배치id':d['_id']}
        projection = {'_id':1, '화면배치id':1, '수집일시':1, '뉴스_url':1}
        dicli = mg.find(db명=DB명, tbl명=PARSING_TBL, query=query, projection=projection, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='dicli')

def 뉴스_원본TBL에_있는_뉴스url이_화면배치TBL에도_있다면_수집완료True_업뎃(dbg_on=False, 사전검증=False):
    print('\n' + '='*60 + inspect.stack()[0][3])

    뉴스url_li = mg.distinct(db명=DB명, tbl명=PARSING_TBL, col명='뉴스_url', query=None, dbg_on=dbg_on, shown_cnt=1)

    query = {'href':{'$in':뉴스url_li}}
    update = {'$set':{'수집완료':True}}
    mg.update_many(db명=DB명, tbl명=COLLECTING_TBL, query=query, update=update, upsert=False, dbg_on=dbg_on, 사전검증=사전검증)

"""
============================== 뉴스TBL의_중복 ==============================
왜 중복이 발생하는지 collector를 조져라.
"""
def 뉴스url과_뉴스제목의_중복현황():
    projection = {'_id':1, '뉴스_url':1, '뉴스제목':1}
    df = mg.find(db명=DB명, tbl명=PARSED_TBL, query=None, projection=projection, dbg_on=False, 컬럼순서li=[], df보고형태='df')

    group_li = [['뉴스_url', '뉴스제목'], ['뉴스제목', '뉴스_url']]
    for gr in group_li:
        print('\n' + '= '*30 + 'by=', gr)
        g = df.groupby(by=gr, axis=0, level=None, as_index=True, sort=True, group_keys=True, squeeze=False, observed=False)
        g = g.count().sort_values('_id')
        g = g[ g['_id'] > 1 ]
        print(g)
        print('\n len(g) : ',len(g))

    subset_li = [['뉴스제목', '뉴스_url'], ['뉴스_url'], ['뉴스제목']]
    for ss in subset_li:
        print('\n' + '= '*30 + 'subset=', ss)
        print('\n len(df) 원자료 : ',len(df))
        df1 = df[ df.duplicated(subset=ss, keep='last') ]
        print('\n len(df) 중복자료 : ',len(df1))


def TBL에서_뉴스url과_뉴스제목의_조합중복은_반드시_제거한다(dbg_on=False, 사전검증=False):
    import LangAnalysis as lanl
    """
    뉴스TBL에서 삭제된 id는 관련 테이블에서도 삭제 대상이다.
    뉴스_ETRI언어분석_원본, 뉴스_ETRI언어분석,
    """
    projection = {'_id':1, '뉴스_url':1, '뉴스제목':1}
    df = mg.find(db명=DB명, tbl명=PARSED_TBL, query=None, projection=projection, dbg_on=False, 컬럼순서li=[], df보고형태='df')

    df1 = df[ df.duplicated(subset=['뉴스제목', '뉴스_url'], keep='last') ]
    제거id_li = list(df1['_id'])

    query = {'_id':{'$in':제거id_li}}
    mg.delete_many(db명=DB명, tbl명=PARSED_TBL, query=query, dbg_on=dbg_on, 사전검증=사전검증)

    query = {'뉴스id':{'$in':제거id_li}}
    mg.delete_many(db명=DB명, tbl명=lanl.TBL명, query=query, dbg_on=dbg_on, 사전검증=사전검증)
    mg.delete_many(db명=DB명, tbl명=lanl.RD_TBL명, query=query, dbg_on=dbg_on, 사전검증=사전검증)

"""
============================== 뉴스_원본TBL의 중복 ==============================
href <=> 뉴스_url
- 화면배치_원본, 화면배치, 뉴스_원본 테이블은 수집일시에 따라 같은 url이 중복되어 저장된다.
수집일시까지 따져서 중복이 발생한다면 말이 되지만...
"""
def 화면배치TBL에_존재하지_않는_URL은_뉴스원본TBL에_존재할수_없다(dbg_on=False, 사전검증=False):
    """
    ===== 작업순서 =====
    화면배치TBL에서 유일한 href 목록을 로딩
    href_li에 존재하지 않는 뉴스원본TBL의 뉴스_url 목록을 로딩
    뉴스_url_li에 해당하는 _id로 문서 삭제
    """
    href_li = mg.distinct(db명=DB명, tbl명=COLLECTING_TBL, col명='href', query=None, dbg_on=dbg_on, shown_cnt=1)
    query = {'뉴스_url':{'$nin':href_li}}
    projection = {'_id':1, '뉴스_url':1}
    df = mg.find(db명=DB명, tbl명=PARSED_TBL, query=query, projection=projection, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')

    df_len = len(df)
    pp.pprint({'df_len':df_len})
    if df_len == 0:
        print('\n 정상. 화면배치TBL에_존재하지_않는_URL은_뉴스원본TBL에_존재하지 않는다. \n')
    else:
        삭제할_미존재_뉴스url에_해당하는_id_li = list(df['_id'])
        query = {'_id':{'$in':삭제할_미존재_뉴스url에_해당하는_id_li}}
        mg.delete_many(db명=DB명, tbl명=PARSING_TBL, query=query, dbg_on=dbg_on, 사전검증=사전검증)


def 뉴스_원본의_중복현황():
    projection = {'_id':1, '뉴스_url':1, '수집일시':1}
    df = mg.find(db명=DB명, tbl명=PARSING_TBL, query=None, projection=projection, dbg_on=False, 컬럼순서li=[], df보고형태='df')

    subset_li = [['뉴스_url'], ['뉴스_url', '수집일시']]
    for ss in subset_li:
        print('\n' + '= '*30 + 'subset=', ss)
        print('\n len(df) 원자료 : ',len(df))
        df1 = df[ df.duplicated(subset=ss, keep='last') ]
        print('\n len(df) 중복자료 : ',len(df1))


def 화면배치TBL의_href와_뉴스원본TBL의_뉴스url간의_개수비교_보고(db명=DB명, tbl_A='화면배치', col_a='href', tbl_B='뉴스_원본', col_b='뉴스_url', dbg_on=False, shown_cnt=1):
    print('\n' + '='*60 + inspect.stack()[0][3])

    href_li, 뉴스url_li, 개수차이 = mg.테이블A의_컬럼a와_테이블B의_컬럼b_간의_개수비교_보고(db명=db명, tbl_A=tbl_A, col_a=col_a, tbl_B=tbl_B, col_b=col_b, dbg_on=dbg_on, shown_cnt=shown_cnt)
    return (href_li, 뉴스url_li, 개수차이)

"""
============================== res 컬럼 ==============================
"""

def res컬럼값_데이터타입이_float64인_문서_보고(dbg_on=False):
    print('\n' + '='*60 + inspect.stack()[0][3])
    """
    """
    query = {'res':{'$elemMatch':{'encoding':'utf-8'}}}
    #projection = {'_id':0,'res':1, 'r_txt':1}
    df1 = mg.find(db명=DB명, tbl명=PARSING_TBL, query=query, projection=None, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')

    dicli = df1.to_dict('records')
    print(df1.iloc[:1,])
    pp.pprint({'dicli[:1]':dicli[:1]})
    pp.pprint({'len(df1)':len(df1)})
    print(df1.dtypes)

"""
============================== 종합 ==============================
"""

def 뉴스수집모듈의_두테이블간_컬럼들의_개수비교보고(dbg_on=False, shown_cnt=1):
    """
    condition_li : 조건튜플 목록 (테이블명, 검사타겟컬럼1, 검사타겟컬럼2, ...)
    결론
    유일한 URL 개수만 서로 동기화되었다면 좋다.
    doc총개수, 유일한 수집일수는 화면배치TBL이 더 많은게 당연하다.
    수집일수는 마이크로초까지 다루기 때문이다.
    """
    condition_li = [
        (lay.TBL명, 'href', '수집일시'),
        (RD_TBL명, '뉴스_url', '수집일시'),
    ]
    rpt_dicli = []
    for cond in condition_li:
        print('\n' + '-'*60 + ' TBL명:{}, URL컬럼명:{}'.format(cond[0], cond[1]))
        projection = {'_id':1}
        df = mg.find(db명=DB명, tbl명=cond[0], query=None, projection=projection, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')
        url_li = mg.distinct(db명=DB명, tbl명=cond[0], col명=cond[1], query=None, dbg_on=dbg_on, shown_cnt=shown_cnt)
        수집일시_li = mg.distinct(db명=DB명, tbl명=cond[0], col명=cond[2], query=None, dbg_on=dbg_on, shown_cnt=shown_cnt)
        자료구조_dic = {
            'TBL명':cond[0],
            'URL컬럼명':cond[1],
            '총_doc수':len(df),
            '유일한_URL수':len(url_li),
            '유일한_수집일시수':len(수집일시_li),
        }
        rpt_dicli.append(자료구조_dic)

    df = pd.DataFrame(rpt_dicli)
    print(df)
    return df

"""
============================== News_ParserSynchronizer ==============================
"""

def 뉴스TBL을_뉴스_원본TBL로_복원(dbg_on=False):
    url_li = mg.distinct(db명=DB명, tbl명=PARSING_TBL, col명='뉴스_url', query=None, dbg_on=False, shown_cnt=10)

    query = {'뉴스_url':{'$nin':url_li}}
    projection = {'_id':0, '뉴스_url':1, '수집일시':1}
    dicli = mg.find(db명=DB명, tbl명=PARSED_TBL, query=query, projection=projection, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='dicli')
    #"""
    dicli_len = len(dicli)
    i=1
    for d in dicli:
        print('\n' + '-'*60 + '{}/{}'.format(i, dicli_len))
        query = {'뉴스_url':d['뉴스_url']}
        update = {'$set':{'수집일시':d['수집일시'], 'r_txt':'파싱완료'}}
        mg.update_one(db명=DB명, tbl명=PARSING_TBL, query=query, update=update, upsert=True, dbg_on=False)
        #break
        i+=1
    #"""

#def 뉴스_원본TBL과_뉴스TBL간의_특정컬럼값_동기화(col명='뉴스_원본id', dbg_on=False):

def 뉴스원본id가_존재하지_않는_뉴스TBL의_문서(dbg_on=False):
    query = {'뉴스_원본id':None}
    df = mg.find(db명=DB명, tbl명=PARSED_TBL, query=query, projection=None, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')

def 뉴스TBL에는_중복된_뉴스원본id가_존재할수_없다(dbg_on=False, 사전검증=False):
    """
    ===== 작업순서 =====
    """
    projection = {'_id':1, '뉴스_원본id':1}
    df = mg.find(db명=DB명, tbl명=PARSED_TBL, query=None, projection=projection, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')
    TF_srs = df.duplicated(subset=['뉴스_원본id'], keep='first')
    df = df[ TF_srs ]
    df_len = len(df)
    pp.pprint({'df_len':df_len})
    if df_len == 0:
        print('if len(df) == 0: -> {} 는 중복없음.'.format('뉴스_원본id'))
    else:
        삭제할_중복된_뉴스원본id에_해당하는_id_li = list(df['_id'])
        query = {'_id':{'$in':삭제할_중복된_뉴스원본id에_해당하는_id_li}}
        mg.delete_many(db명=DB명, tbl명=PARSED_TBL, query=query, dbg_on=dbg_on, 사전검증=사전검증)

def 뉴스원본TBL의_뉴스url과_뉴스TBL의_뉴스url간의_개수비교_보고(db명=DB명, tbl_A='뉴스_원본', col_a='뉴스_url', tbl_B='뉴스', col_b='뉴스_url', dbg_on=False, shown_cnt=1):
    print('\n' + '='*60 + inspect.stack()[0][3])

    tpl = mg.테이블A의_컬럼a와_테이블B의_컬럼b_간의_개수비교_보고(db명=db명, tbl_A=tbl_A, col_a=col_a, tbl_B=tbl_B, col_b=col_b, dbg_on=dbg_on, shown_cnt=shown_cnt)
    #뉴스원본url_li, 뉴스url_li, 개수차이
    return tpl

def 뉴스파싱모듈의_두테이블간_컬럼들의_개수비교보고(dbg_on=False, shown_cnt=1):
    """
    condition_li : 조건튜플 목록 (테이블명, 검사타겟컬럼1, 검사타겟컬럼2, ...)
    두 테이블 : RD_TBL, TBL
    결론
    두 테이블은 1:1 관계다. 뉴스원본TBL에서 가져온 모든 컬럼정보는 뉴스TBL과 동일해야 한다.
    """
    condition_li = [
        (RD_TBL명, '뉴스_url', '수집일시', '_id'),
        (TBL명, '뉴스_url', '수집일시', '뉴스_원본id'),
    ]
    rpt_dicli = []
    for cond in condition_li:
        print('\n' + '-'*60 + ' TBL명:{}, URL컬럼명:{}'.format(cond[0], cond[1]))
        projection = {'_id':1}
        df = mg.find(db명=DB명, tbl명=cond[0], query=None, projection=projection, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')
        url_li = mg.distinct(db명=DB명, tbl명=cond[0], col명=cond[1], query=None, dbg_on=dbg_on, shown_cnt=shown_cnt)
        수집일시_li = mg.distinct(db명=DB명, tbl명=cond[0], col명=cond[2], query=None, dbg_on=dbg_on, shown_cnt=shown_cnt)
        뉴스원본id_li = mg.distinct(db명=DB명, tbl명=cond[0], col명=cond[3], query=None, dbg_on=dbg_on, shown_cnt=shown_cnt)
        자료구조_dic = {
            'TBL명':cond[0],
            'URL컬럼명':cond[1],
            '총_doc수':len(df),
            '유일한_URL수':len(url_li),
            '유일한_수집일시수':len(수집일시_li),
            '뉴스_원본id':len(뉴스원본id_li),
        }
        rpt_dicli.append(자료구조_dic)

    df = pd.DataFrame(rpt_dicli)
    print(df)
    return df

"""
============================== News_ParserTarget... ==============================
"""
import Programming_Collective_Intelligence as PCI
import __pymongo as mg

def 임시__뉴스본문의_HTML태그를_일괄제거업뎃(dbg_on=False, 사전검증=False):

    projection = {'_id':1, '뉴스본문':1}
    df = mg.find(db명=DB명, tbl명=PARSED_TBL, query=None, projection=projection, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')
    df = df.fillna('_')
    df = df[ df['뉴스본문'] != '_' ]
    #return df
    df['뉴스본문'] = df['뉴스본문'].apply(lambda x: PCI.stripHTML(h=x, dbg_on=dbg_on) )

    dicli = df.to_dict('records')
    dicli_len = len(dicli)
    i=1
    for d in dicli:
        print('\n' + '-'*60 + '{}/{}'.format(i, dicli_len))
        query = {'_id':d['_id']}
        update = {'$set':{'뉴스본문':d['뉴스본문']}}
        mg.update_one(db명=DB명, tbl명=PARSED_TBL, query=query, update=update, upsert=False, dbg_on=dbg_on, 사전검증=사전검증)
        i+=1

def 파싱대상_선정(파싱컬럼명, dbg_on=False):
    print('\n' + '='*60 + inspect.stack()[0][3])
    """
    """

    입력 = {'파싱컬럼명':파싱컬럼명, 'dbg_on':dbg_on}


    query = {파싱컬럼명:{'$exists':1}}
    id_li = mg.distinct(db명=DB명, tbl명=PARSING_TBL, col명='_id', query=query, dbg_on=dbg_on)

    query = {'_id':{'$nin':id_li}}
    projection = {'_id':1, 파싱컬럼명:1}
    df = 뉴스_로딩(query=query, projection=projection, dbg_on=dbg_on)

    dicli = df.to_dict('records')
    return dicli

def 태그제거(dicli, 파싱컬럼명, dbg_on):
    dicli_len = len(dicli)
    i=1
    for d in dicli:
        print('\n' + '-'*60 + '{}/{}'.format(i, dicli_len))
        s = d[파싱컬럼명]
        s1 = PCI.stripHTML(h=s, dbg_on=False)
        if dbg_on == True: pp.pprint(s1)
        d[파싱컬럼명] = s1
        i+=1
    return dicli

def 저장(dicli):
    dicli_len = len(dicli)
    i=1
    for d in dicli:
        print('\n' + '-'*60 + '{}/{}'.format(i, dicli_len))
        query = {}
        update = {'$set':d}
        if dbg_on == True: pp.pprint({'query':query, 'update':update})
        #db[TBL명].update_one(filter=query, update=update, upsert=True)

def 뉴스본문의_HTML태그_제거(파싱컬럼명='뉴스본문', dbg_on=False):
    print('\n' + '='*60 + inspect.stack()[0][3])
    """
    ===== 작업순서 =====
    파싱할 대상 선정
    - 파싱완료된 뉴스id를 로딩하고, 그걸을 제외한 대상만 뉴스 테이블에서 로딩한다.
    파싱
    - 태그제거
    별도 테이블에 저장
    """

    입력 = {'파싱컬럼명':파싱컬럼명}


    dicli = 파싱대상_선정(파싱컬럼명, dbg_on)
    dicli = 태그제거(dicli, 파싱컬럼명, dbg_on)
    저장(dicli)
