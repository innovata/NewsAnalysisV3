"""
============================== 핵심일 ==============================
일시적 별도 작업이다.
뉴스TBL에 존재하지않고 언어분석_원본TBL에만 존재하는 뉴스id를 가진 문서삭제


===== 단축용어 가이드 =====
LangAnalysis 모듈/클래스? 에서 다음과 같이 사용하자.
뉴스제목본문_ETRI언어분석_원본TBL -> 언어분석_원본TBL
뉴스제목본문_ETRI언어분석TBL -> 언어분석TBL
분석수집타겟col명 -> 타겟col명
"""
import __pymongo as mg
import __list as lh
import __ETRI_AI as etri
from LangAnalysis_ import *




"""
============================== 뉴스TBL <=> 언어분석_원본TBL ==============================
"""
def 뉴스TBL에_존재하지않고_언어분석_원본TBL에만_존재하는_뉴스id을_가진_문서삭제(dbg_on=False, 사전검증=False, shown_cnt=1):
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbg_on)
    inputs = dbg.inputs(inspect.currentframe(), dbg_on)

    tbl_A = '뉴스'
    col_a = '_id'
    tbl_B = '뉴스제목본문_ETRI언어분석_원본'
    col_b = '뉴스id'

    집합_A = mg.distinct(db명=DB명, tbl명=tbl_A, col명=col_a, query=None, dbg_on=dbg_on, shown_cnt=shown_cnt)
    query = {col_b:{'$nin':집합_A}}
    차집합_B = mg.distinct(db명=DB명, tbl명=tbl_B, col명=col_b, query=query, dbg_on=dbg_on, shown_cnt=shown_cnt)

    if dbg_on == True: dbg._li(li=차집합_B, caller=inspect.stack()[0][3], shown_cnt=1)
    query = {col_b:{'$in':차집합_B}}
    mg.delete_many(db명=DB명, tbl명=tbl_B, query=query, dbg_on=dbg_on, 사전검증=사전검증)


"""
============================== LangAnalysis_ParserSynchronizer ==============================
함수다. 클래스 아니다. 별도 파일일뿐.
실제 일을 하는 파일이다.

수집된 언어분석 결과를 여러방법으로 파싱해보자.
    - 명사리스트를 추출후 컬럼추가저장
    - 또 뭐?
"""

def TBL의_뉴스id가_RDTBL에도_존재한다면_파싱완료는_True여야한다(타겟col명, analyzerMethod='srl', subMethod='WSD', texttype='NNG', dbg_on=False):
    파싱타겟col명 = 타겟col명 + analyzerMethod + '_res'
    파싱저장col명 = 타겟col명 + analyzerMethod + '_' + subMethod + texttype + 'li'
    파싱완료col명 = 타겟col명 + analyzerMethod + '_res' + '파싱완료'

    query = {파싱저장col명:{'$ne':None}}
    뉴스id_li = mg.distinct(db명=DB명, tbl명=TBL명, col명='뉴스id', query=query, dbg_on=dbg_on, shown_cnt=1)
    query = {'뉴스id':{'$in':뉴스id_li}, 파싱타겟col명:{'$ne':None}}
    뉴스id_RD_li = mg.distinct(db명=DB명, tbl명=RD_TBL명, col명='_id', query=None, dbg_on=dbg_on, shown_cnt=1)
    #projection = {'_id':1}
    #df = mg.find(db명=DB명, tbl명=RD_TBL명, query=None, projection=projection, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')
    print(len(뉴스id_RD_li))

    query = {'_id':{'$in':뉴스id_RD_li}}
    update = {'$set':{파싱완료col명:True}}
    mg.update_many(db명=DB명, tbl명=RD_TBL명, query=query, update=update, upsert=False, dbg_on=dbg_on, 사전검증=False)

def 뉴스XX_언어분석TBL_id조사():
    id_li = mg.distinct(db명=DB명, tbl명=TBL명, col명='_id', query=None, dbg_on=True, shown_cnt=1)
    id_li1 = lh.리스트의_중복제거(li=id_li)

def RD_TBL의_뉴스id_중복조사(dbg_on=False):
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbg_on)
    inputs = dbg.inputs(inspect.currentframe(), dbg_on)
    뉴스id_li = mg.distinct(db명=DB명, tbl명=RD_TBL명, col명='뉴스id', query=None, dbg_on=dbg_on, shown_cnt=1)
    lh.리스트의_중복제거(li=뉴스id_li)
"""
결과 -> 중복 없음.
리스트의_중복제거
{'중복제거 전': 14434}
{'중복제거 후': 14434}
"""

def 뉴스TBL과_RD_TBL간의_뉴스id를_비교대조(dbg_on=True):
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbg_on)
    inputs = dbg.inputs(inspect.currentframe(), dbg_on)

    뉴스TBL_ids = mg.distinct(db명=DB명, tbl명='뉴스', col명='_id', query=None, dbg_on=dbg_on, shown_cnt=1)
    RD_TBL_ids = mg.distinct(db명=DB명, tbl명=RD_TBL명, col명='뉴스id', query=None, dbg_on=dbg_on, shown_cnt=1)

    뉴스TBL_차집합_ids = lh.리스트1로부터_리스트2를_제거(li1=뉴스TBL_ids, li2=RD_TBL_ids)
    RD_TBL_차집합_ids = lh.리스트1로부터_리스트2를_제거(li1=RD_TBL_ids, li2=뉴스TBL_ids)
    교집한_ids = lh.리스트1과_리스트2의_교집합을_찾기(li1=뉴스TBL_ids, li2=RD_TBL_ids)
    dic = {
        'len(뉴스TBL_차집합_ids)':len(뉴스TBL_차집합_ids),
        'len(RD_TBL_차집합_ids)':len(RD_TBL_차집합_ids),
        'len(교집한_ids)':len(교집한_ids),
    }
    print('\n'+'*'*60+inspect.stack()[0][3])
    pp.pprint(dic)


    dic1 = {
        'ids명':['뉴스TBL_차집합_ids','RD_TBL_차집합_ids','교집한_ids'],
        'id_li':[뉴스TBL_차집합_ids, RD_TBL_차집합_ids, 교집한_ids],
        'ids_len':[len(뉴스TBL_차집합_ids), len(RD_TBL_차집합_ids), len(교집한_ids)]
    }
    df = pd.DataFrame(dic1)
    함수명 = inspect.stack()[0][3]
    dbg._df(df, caller=함수명, 컬럼순서li=[], df보고형태='df')
    mg.insert_many(db명=DB명, tbl명=함수명, dicli=df.to_dict('records'), dbg_on=dbg_on, 사전검증=False)
"""
결과
뉴스TBL과_RD_TBL간의_뉴스id를_비교대조
'len(뉴스TBL_차집합_ids)': 1499,
'len(RD_TBL_차집합_ids)': 2782,
'len(교집한_ids)': 11652,
"""
#def 뉴스TBL과_RD_TBL간의_뉴스id를_비교대조TBL_로딩():

def RD_TBL_차집합_ids에_해당하는_RD_TBL의_내용보기(dbg_on=True):
    tbl명 = '뉴스TBL과_RD_TBL간의_뉴스id를_비교대조'
    query = {'ids명':'RD_TBL_차집합_ids'}
    dicli = mg.find(db명=DB명, tbl명=tbl명, query=query, projection=None, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='dicli')
    RD_TBL_차집합_idli = dicli[0]['id_li']

    query = {'_id':{'$in':RD_TBL_차집합_idli}}
    dicli = mg.find(db명=DB명, tbl명='뉴스', query=query, projection=None, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='dicli')


def RD_TBL에서_뉴스XX의_뉴스id가_존재하면_뉴스TBL에_수집완료True를_업뎃(타겟col명='뉴스제목', analyzerMethod='srl', dbg_on=False, shown_cnt=1, 사전검증=False):
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbg_on)
    inputs = dbg.inputs(inspect.currentframe(), dbg_on)
    뉴스id_li = RD_TBL에서_ETRI언어분석수집이_정상완료된_뉴스idli로딩(타겟col명=타겟col명, analyzerMethod=analyzerMethod, dbg_on=dbg_on, shown_cnt=shown_cnt)

    수집완료col명 = 타겟col명 +'_ETRI언어분석_수집완료'
    query = {'_id':{'$in':뉴스id_li}}
    update = {'$set':{수집완료col명:True}}
    mg.update_many(db명=DB명, tbl명='뉴스', query=query, update=update, upsert=False, dbg_on=dbg_on, 사전검증=사전검증)

    print('\n'+'*'*60+inspect.stack()[0][3]+'_검증')
    query = {'_id':{'$in':뉴스id_li}, 수집완료col명:True}
    mg.find(db명=DB명, tbl명='뉴스', query=query, projection=None, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')
