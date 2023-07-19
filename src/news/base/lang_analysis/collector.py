"""
ETRI언어분석 수집타겟 선정
ETRI언어분석 수집
ETRI언어분석 수집완료 업뎃

뉴스제목/본문을_ETRI_AI_언어분석API_이용해_명사리스트로_변환후_별도_테이블저장
    신버전
    - 뉴스id | col명_분석코드1 | col명_분석코드2 | ...
    - 예) 뉴스id | 뉴스제목_morp | 뉴스본문_morp | 뉴스제목_wsd | 뉴스제목_ner | ...
    구버전
    - 뉴스id | 뉴스제목_명사li | 뉴스본문_명사li
"""
import etri
import __list as lh
import Programming_Collective_Intelligence as PCI
"""
============================== ETRI언어분석 수집타겟 선정 ==============================
두가지 방법
1. 리스트1에서 리스트2를 제거한다.
2. 리스트2를 찾고, 리스트2를 제외한 리스트1을 디비에서 찾는다.
어느 방법이 더 빠른가? 아마도 2 같다.

수집완료False : ETRI 언어분석 수집완료 여부 컬럼명 -> 뉴스XX_ETRI언어분석_수집완료
타겟col명 : ETRI 언어분석할 컬럼명
ETRI_AI_언어분석할_뉴스TBL의_타겟dicli
===== 작업순서 =====
뉴스TBL의 "뉴스XX_ETRI언어분석_수집완료" 컬럼을 None -> False 강제변경 해야하나? 굳이?
"""
def 수집완료True가_아닌_타겟선정(타겟col명='뉴스본문'):
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbg_on)
    inputs = dbg.inputs(inspect.currentframe(), dbg_on)
    """
    아직 TargetHandler 별도 파일로 분리할 정도로 함수가 많거나 코드 줄이 길지 않다.
    이상한 건,
    1. 뉴스TBL에 URL은 다른데, 뉴스제목/본문의 내용이 완전 같거나
    2. 뉴스본문 내용이 아예 없는 (None) 문서들이 존재한다는 것이다.
    왜지?
    """


    수집완료col명 = 타겟col명 + '_ETRI언어분석_수집완료'

    query = {수집완료col명:{'$ne':True}, 타겟col명:{'$ne':None}}
    projection = {'_id':1, 타겟col명:1}
    df = mg.find(db명=DB명, tbl명='뉴스', query=query, projection=projection, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')
    return df

def 타겟의_중복제거(df, 타겟col명='뉴스본문'):
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbg_on)
    inputs = dbg.inputs(inspect.currentframe(), dbg_on)
    """
    """

    df = df.sort_values(타겟col명, ascending=True)
    pp.pprint({'중복제거 전':len(df)})
    df = df.drop_duplicates(subset=[타겟col명], keep='first', inplace=False)
    pp.pprint({'중복제거 후':len(df)})

    dicli = df.to_dict('records')
    if dbg_on == True: dbg._li(li=dicli, caller=inspect.stack()[0][3], shown_cnt=1)
    return dicli

"""
============================== ETRI언어분석 수집 ==============================
"""
def ETRI언어분석_수집(타겟col명='뉴스본문', analyzerMethod='srl', 사전검증=False):
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbg_on)
    inputs = dbg.inputs(inspect.currentframe(), dbg_on)
    """
    ===== 주의 =====
    뉴스id 불러오는 부분 수정필요.
    RD_TBL명 에 upsert=True를 사용해야 한다. 왜냐?
    : ETRI 언어분석 응답결과가 result=-1 일수도 있기 때문에 이것을 다시 업데이트 해야한다.

    ===== 작업순서 =====
    API 응답결과를 먼저 별도의 테이블에 저장한 후,
    그 테이블로부터 필요한 정보만을 걸러서 작업하는 것이 좋겟다.

    res_js의 경우 MongDB $elemMatch 검색을 위해 [res_js]처럼 dicli으로 변환하는 것이 좋다.

    ===== 경고 =====
    다음 코드는 한줄이나, 오류 발생시 ETRI API 호출제한수를 소진시키는 단점이 있다.
    따라서 사용하지마라.
    df[col명+'_명사li'] = df[col명].apply(lambda x: ETRI.언어분석_API(analzing_text=x, analysisCode='morp'))
    """
    #

    df = 수집완료True가_아닌_타겟선정(타겟col명, dbg_on)
    dicli = 타겟의_중복제거(df, 타겟col명, dbg_on)
    #return None

    dicli_len = len(dicli)
    i=1
    for d in dicli:
        print('\n' + '-'*60 + '{}/{}'.format(i, dicli_len))
        ETRI_res_result = ETRI언어분석_단위수집(d, 타겟col명, analyzerMethod, dbg_on, 사전검증)
        if ETRI_res_result == False:
            print('if ETRI_res_result == False:')
            break
        i+=1
        #break #단위테스트용.

def ETRI언어분석_단위수집(뉴스dic, 타겟col명, analyzerMethod, 사전검증=False):
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbg_on)
    inputs = dbg.inputs(inspect.currentframe(), dbg_on)
    """
    ===== 중요 =====
    upsert=True
    """
    #

    d = 뉴스dic.copy()
    res_js = etri.lang_analysis.api(analzing_text=d[타겟col명], analysisCode=analyzerMethod, dbg_on=dbg_on)
    #res_js = '더미'
    if res_js['result'] == -1:
        if 'Daily amount Limit has been exceed' in res_js['reason']:
            return False
        else:
            pass
    else:
        언어분석col명 = 타겟col명 + analyzerMethod + '_res'
        doc_dic = {
            '뉴스id':d['_id'],
            언어분석col명:[res_js],
            '수집일시':datetime.now()
        }
        query = {'뉴스id':d['_id']}
        update = {'$set': doc_dic}
        mg.update_one(db명=DB명, tbl명=PARSING_TBL, query=query, update=update, upsert=True, dbg_on=dbg_on, 사전검증=사전검증)
        수집된_타겟col에_대해_수집완료컬럼을_True로_업뎃(타겟col명, d, dbg_on, 사전검증)
        Parser.ETRI언어분석_수집파싱_커넥터(doc_dic, 타겟col명, analyzerMethod, 사전검증=False)

def UnitTest_ETRI언어분석_단위수집(타겟col명='뉴스본문', analyzerMethod='srl', dbg_on=True, 사전검증=True):
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbg_on)
    inputs = dbg.inputs(inspect.currentframe(), dbg_on)

    dicli = 수집완료True가_아닌_타겟선정(타겟col명, dbg_on)
    dic = dicli[0]
    ETRI언어분석_단위수집(dic, 타겟col명, analyzerMethod, dbg_on, 사전검증)


"""
============================== ETRI언어분석 수집완료 업뎃 ==============================
"""
def 수집된_타겟col에_대해_수집완료컬럼을_True로_업뎃(타겟col명, dic, 사전검증=False):
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbg_on)
    inputs = dbg.inputs(inspect.currentframe(), dbg_on)
    입력 = {'타겟col명':타겟col명, 'dic':dic, '사전검증':사전검증}


    수집완료col명 = 타겟col명 + '_ETRI언어분석_수집완료'

    #query = {'_id':dic['_id']}
    query = {타겟col명:dic[타겟col명]}
    update = {'$set': {수집완료col명:True} }
    mg.update_many(db명=DB명, tbl명='뉴스', query=query, update=update, upsert=False, dbg_on=dbg_on, 사전검증=사전검증)
