"""
============================== 핵심일 ==============================
함수다. 클래스 아니다. 별도 파일일뿐.
실제 일을 하는 파일이다.

수집된 언어분석 결과를 여러방법으로 파싱해보자.
    - 명사리스트를 추출후 컬럼추가저장
    - 또 뭐?
"""
import __ETRI_AI as etri
import __list as lh
from LangAnalysis_ import *
from pandas.io.json import json_normalize


class Parser:

    def parse_etri_langanalysis(타겟col명='뉴스제목', analyzerMethod='srl', subMethod='WSD', texttype='NNG'):
        """ETRI언어분석_파싱
        ===== 작업순서 =====
        파싱타겟 선정
        파싱->저장
        파싱완료 True 업뎃

        ===== 고려사항 =====
        API 응답결과를 먼저 별도의 테이블에 저장한 후,
        그 테이블로부터 필요한 정보만을 걸러서 작업하는 것이 좋겟다.

        ===== 규칙 =====
        뉴스_ETRI언어분석TBL에 저장할 컬럼명 작성규칙 :
        '뉴스제목srl_res' -> '뉴스제목srl_WSDNNGli'

        뉴스_ETRI언어분석_원본TBL에 업뎃할 컬럼명 작성규칙 :
        '뉴스제목srl_res' -> '뉴스제목srl_res파싱완료'
        """
        파싱타겟col명 = 타겟col명 + analyzerMethod + '_res'
        파싱저장col명 = 타겟col명 + analyzerMethod + '_' + subMethod + texttype + 'li'
        파싱완료col명 = 타겟col명 + analyzerMethod + '_res' + '파싱완료'

        뉴스id_li = choose_parsing_targets(파싱타겟col명, 파싱완료col명)
        뉴스id_li_len = len(뉴스id_li)
        i=1
        for 뉴스id in 뉴스id_li:
            print('\n' + '-'*60 + '{}/{}'.format(i, 뉴스id_li_len))
            unitparse_etri_langanalysis(뉴스id, 파싱타겟col명, 파싱저장col명, subMethod, texttype)
            update_parsed_True(뉴스id, 파싱완료col명)
            i+=1
            if UnitTest == True: break
            else: pass

    def choose_parsing_targets(파싱타겟col명, 파싱완료col명):
        query = {
            파싱타겟col명:{'$elemMatch':{'result':0}},
            파싱완료col명:{'$ne':True}}
        뉴스id_li = mg.distinct(db명=DB명, tbl명=PARSING_TBL, col명='뉴스id', query=query, shown_cnt=1)
        return 뉴스id_li

    def unitparse_etri_langanalysis(뉴스id, 파싱타겟col명, 파싱저장col명, subMethod, texttype):
        """ETRI언어분석_단위파싱
        # 여기서 잘라 하위 함수로.
        dic = dicli[0][파싱타겟col명][0]['return_object']
        df = json_normalize(data=dic, record_path='sentence', meta=None, meta_prefix=None, record_prefix=None, errors='raise', sep='.')

        df = df.loc[:,[subMethod]]
        dicli = df.to_dict('records')
        df = json_normalize(data=dicli, record_path=subMethod, meta=None, meta_prefix=None, record_prefix=None, errors='raise', sep='.')
        df = df[ df['type']==texttype ]
        print(df)
        text_li = list(df['text'])
        pp.pprint({'text_li':text_li})

        query = {'뉴스id':뉴스id}
        update = {'$set':{파싱저장col명:text_li}}
        mg.update_one(db명=DB명, tbl명=PARSED_TBL, query=query, update=update, upsert=True, 사전검증=사전검증)
        """
        query = {'뉴스id':뉴스id, 파싱타겟col명:{'$elemMatch':{'result':0}}}
        projection = {'_id':0, '뉴스id':1, 파싱타겟col명:1}
        dicli = mg.find(db명=DB명, tbl명=PARSING_TBL, query=query, projection=projection, 컬럼순서li=[], df보고형태='dicli')
        dicli = dicli[0][파싱타겟col명]

    def save_parsed_unit(dicli, 뉴스id, 파싱타겟col명, 파싱저장col명, subMethod, texttype):
        """
        뉴스id가 뉴스제목, 본문 기타등등에 여러번 사용될 수 있으므로,
        즉, 어떨땐 신규 문서추가, 어떨땐 기존 문서에 컬럼 추가 할 수 있으므로,
        insert_one 이 아닌 update_one(upsert=True) 이다.
        """
        dic = dicli[0]['return_object']
        df = json_normalize(data=dic, record_path='sentence', meta=None, meta_prefix=None, record_prefix=None, errors='raise', sep='.')

        df = df.loc[:,[subMethod]]
        dicli = df.to_dict('records')
        df = json_normalize(data=dicli, record_path=subMethod, meta=None, meta_prefix=None, record_prefix=None, errors='raise', sep='.')
        df = df[ df['type']==texttype ]
        print(df)
        text_li = list(df['text'])
        pp.pprint({'text_li':text_li})

        query = {'뉴스id':뉴스id}
        update = {'$set':{파싱저장col명:text_li}}
        mg.update_one(db명=DB명, tbl명=PARSED_TBL, query=query, update=update, upsert=True, 사전검증=사전검증)

    def update_parsed_True(뉴스id, 파싱완료col명):
        query = {'뉴스id':뉴스id}
        update = {'$set':{파싱완료col명:True}}
        mg.update_one(db명=DB명, tbl명=PARSING_TBL, query=query, update=update, upsert=False, 사전검증=사전검증)

    def ETRI언어분석_수집파싱_커넥터(doc_dic, 타겟col명, analyzerMethod, subMethod='WSD', texttype='NNG'):


        """
        이 함수의 존재 목적은, 언어분석 수집시에 파싱까지 한번에 할 수 있도록 하기 위함이다.
        왜냐하면, 언어분석 파싱에 엄청난 시간이 걸린다.
        예를 들어, ------8138/12812 이 정도 파싱하는데만 12시간 걸렸다. 시발.
        커넥터의 목적은, 수집함수에서 직접 "ETRI언어분석_단위파싱" 를 호출하기엔
        파라미터 동기화가 직접적이지 않아, 이를 해결하기 위함이다.
        수집 파트 파라미터 :
        - 뉴스dic, 타겟col명, analyzerMethod, doc_dic
        파싱 파트 파라미터 :
        -dicli, 뉴스id, 파싱타겟col명, 파싱저장col명, subMethod, texttype

        dicli = [res_js] <- doc_dic[언어분석col명]
        뉴스id = doc_dic['뉴스id']
        파싱타겟col명 = 타겟col명 + analyzerMethod + '_res' = 언어분석col명
        강제주입
        subMethod <- 'WSD'
        texttype <- 'NNG'
        파싱저장col명 = 타겟col명 + analyzerMethod + '_' + subMethod + texttype + 'li'
        파싱완료col명 = 타겟col명 + analyzerMethod + '_' + subMethod + texttype + '파싱완료'
        """
        파싱타겟col명 = 타겟col명 + analyzerMethod + '_res'
        파싱저장col명 = 타겟col명 + analyzerMethod + '_' + subMethod + texttype + 'li'
        파싱완료col명 = 타겟col명 + analyzerMethod + '_' + subMethod + texttype + '파싱완료'
        dicli = doc_dic[파싱타겟col명]
        뉴스id = doc_dic['뉴스id']

        save_parsed_unit(dicli, 뉴스id, 파싱타겟col명, 파싱저장col명, subMethod, texttype)
        update_parsed_True(뉴스id, 파싱완료col명)

class ClusterPreparation:
    """
    수집된 언어분석 결과를 여러방법으로 파싱해보자.
    - 명사리스트를 추출후 컬럼추가저장
    - 또 뭐?
    """
    def 임시__RD_TBL의_뉴스제목_srl컬럼을_리스트타입으로_변경(변경할_col명='뉴스제목_srl'=False):
        query = {변경할_col명:{'$exists':1}}
        projection = {'뉴스id':1, 변경할_col명:1}
        dicli = mg.find(db명=DB명, tbl명=PARSING_TBL, query=query, projection=projection, 컬럼순서li=[], df보고형태='dicli')
        dicli_len = len(dicli)
        i=1
        for d in dicli:
            print('\n' + '-'*60 + '{}/{}'.format(i, dicli_len))
            if 변경할_col명 in d.keys():
                pp.pprint({'type(d[변경할_col명])':type(d[변경할_col명])})
                if type(d[변경할_col명]) is dict:
                    query = {'뉴스id':d['뉴스id']}
                    update = {'$set': {변경할_col명: [d[변경할_col명]] } }
                    mg.update_one(db명=DB명, tbl명=PARSING_TBL, query=query, update=update, upsert=False, 사전검증=사전검증)
                elif type(d[변경할_col명]) is list:
                    pass
                else:
                    pass
            i+=1

    def 뉴스제목본문_명사li를_정렬후_문자열로_변환저장():
        """sklearn을 사용하기 위한 목적."""
        df = 뉴스제목본문_명사li_로딩(query=None, projection=None=False)
        df['뉴스제목_요약'] = df['뉴스제목_명사li'].apply(lambda x: ' '.join(sorted(x)) )
        df = df.loc[:,['뉴스id','뉴스제목_요약']]
        if dbg_on == True:
            dbg._df(df, inspect.stack()[0][3], df보고형태='dic')

        dicli = df.to_dict('records')
        i=1
        dicli_len = len(dicli)
        for d in dicli:
            print('\n' + '-'*60 + '{}/{}'.format(i, dicli_len))
            query = {'뉴스id':d['뉴스id']}
            update = {'$set':{'뉴스제목_요약':d['뉴스제목_요약']}}
            pp.pprint({'query':query, 'update':update})
            db[TBL명].update_one(filter=query, update=update, upsert=False)
            i+=1

    def 언어분석결과중_명사li_추출(js):
        dicli = js['return_object']['sentence'][0]['WSD']
        df = pd.DataFrame(dicli)
        df = df.query("type=='NNG'")
        li = list(df['text'])
        pp.pprint({'명사li':li if len(li)<20 else 'li'})
        return li

    def 뉴스XX에_대해_명사li요약(col명='뉴스본문', analyzerMethod='srl'=False):
        """
        ===== 주의 =====
        sklearn cluster 결과의 정확도를 높이기 위해,
            - 리스트를 정렬한다.
            - 리스트 중복제거한다 --> 진짜 필요한가?
        """
        파싱col명 = col명 + '_' + analyzerMethod
        요약col명 = col명 + '_요약'

        dicli = 뉴스_언어분석_RD로딩(파싱col명=파싱col명, 컬럼순서li=[], df보고형태='dicli')

        dicli_len = len(dicli)
        i=1
        for d in dicli:
            print('\n' + '-'*60 + '{}/{}'.format(i, dicli_len))
            morp_dicli = d[파싱col명]['return_object']['sentence']['morp']
            df = pd.DataFrame(morp_dicli)
            df = df.query('type=="NNG"')
            print(df)
            i+=1
            break
            li = sorted(li)
            li = lh.리스트의_중복제거(li)
            요약_str = ' '.join(li)
            pp.pprint({'요약_str':요약_str})
            return 요약_str

    def 파싱대상_로딩(파싱컬럼명, 요약컬럼명, 방법='전체'):
        """
        파싱할 대상 선정 방법은 기본 "전체"이고, 아니면 "선별"적이다.
        리턴은 뉴스id와 파싱컬럼 2개를 포함한 dicli 타입이다.
        """
        if 방법 == '전체':
            query = {파싱컬럼명:{'$elemMatch':{'result':0}}}
        else:
            query = {파싱컬럼명:{'$elemMatch':{'result':0}}, 요약컬럼명:{'$exists':0}}
            #뉴스_언어분석_distinct로딩(col명='뉴스id', query=query=False)
        projection = {'_id':0, '뉴스id':1, 파싱컬럼명:1}
        df = 뉴스_언어분석_로딩(query=query, projection=projection)

        if len(df) == 0:
            print('if len(df) == 0:')
        else:
            dicli = df.to_dict('records')
            return dicli

    def 뉴스_언어분석_srl파싱(핵심대상='뉴스제목', analyzerMethod='srl'):
        """
        ===== 용어정의 =====
        파싱대상 : 뉴스제목/뉴스본문 등 "핵심대상"
        analyzerMethod : ETRI_AI 언어분석API 호출시 사용했던 분석방법명

        ===== 작업순서 =====
        파싱할 대상 선정
            - 뉴스_언어분석API_로딩
            - 선별적 로딩 : 이미 파싱완료한 것은 제외
        파싱
        저장
        """
        파싱컬럼명 = 핵심대상 + '_' + analyzerMethod
        요약컬럼명 = 핵심대상 + '_요약'
        dicli = 파싱대상_로딩(파싱컬럼명, 요약컬럼명, 방법='선별')
        if dicli is None:
            print('if dicli is None:')
        else:
            i=1
            dicli_len = len(dicli)
            for d in dicli:
                print('\n' + '-'*60 + '{}/{}'.format(i, dicli_len))
                js = d[파싱컬럼명][0]
                dbg._json(js=js, caller=inspect.stack()[0][3])
                li = 언어분석결과중_명사li_추출(js)
                뉴스XX요약_str = 뉴스XX_요약(li)

                d[요약컬럼명] = 뉴스XX요약_str
                del(d[파싱컬럼명])
                query = {'뉴스id':d['뉴스id']}
                update = {'$set':d}
                pp.pprint({'query':query, 'update':update})
                db[TBL명].update_one(filter=query, update=update, upsert=True)
                i+=1
