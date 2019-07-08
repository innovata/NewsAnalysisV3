"""
============================== 핵심일 ==============================
분석 클래스다.
클래스 아니다. 별도 파일일뿐.
실제 일을 하는 파일이다.
뉴스_로딩
뉴스제목/본문을_ETRI_AI_언어분석API_이용해_명사리스트로_변환후_별도_테이블저장
    신버전
    - 뉴스id | col명_분석코드1 | col명_분석코드2 | ...
    - 예) 뉴스id | 뉴스제목_morp | 뉴스본문_morp | 뉴스제목_wsd | 뉴스제목_ner | ...
    구버전
    - 뉴스id | 뉴스제목_명사li | 뉴스본문_명사li
"""
from inews import etri
from ilib import ilist


def 뉴스제목본문_명사li_로딩(query=None, projection=None):
    df = pd.DataFrame(list( db[TBL명].find(query, projection) ))
    dbg.dframe(df, inspect.stack()[0][3])
    return df

def 뉴스제목본문_명사li를_정렬후_문자열로_변환저장():
    """sklearn을 사용하기 위한 목적."""
    df = 뉴스제목본문_명사li_로딩(query=None, projection=None)
    df['뉴스제목_요약'] = df['뉴스제목_명사li'].apply(lambda x: ' '.join(sorted(x)) )
    df = df.loc[:,['뉴스id','뉴스제목_요약']]

        dbg.dframe(df, inspect.stack()[0][3])

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

def 뉴스제목본문을_명사li해야할_뉴스만_걸러서_로딩():
    """
    연구해봐라. -> $nin 으로 간단히 해결되는 것 같은디? -> 삭제 예정?
    이 함수는 이 프로젝트 내에서 전역으로 사용될 수 있을 것 같다.
    함수명은 "두테이블....."
    """
    li1 = list( db['뉴스'].distinct('_id') )
    li2 = list( db[TBL명].distinct('뉴스id') )
    id_li = ilist.difference_list(li1, li2)
    return id_li

def ETRI_AI_언어분석API를_이용해_뉴스제목본문의_명사li를_저장(col='뉴스제목'):
    """
    API 응답결과를 먼저 별도의 테이블에 저장한 후,
    그 테이블로부터 필요한 정보만을 걸러서 작업하는 것이 좋겟다.
    """
    id_li = list( db[TBL명].distinct('뉴스id') )

    query = {'_id':{'$nin':id_li}}
    projection = {'_id':1, col:1}

    df = df.rename(columns={'_id':'뉴스id'})

    #df[col+'_명사li'] = df[col].apply(lambda x: etri.언어분석_API(analzing_text=x, analysisCode='morp'))
    dicli = df.to_dict('records')
    i=1
    dicli_len = len(dicli)
    for d in dicli:
        print('\n' + '-'*60 + '{}/{}'.format(i, dicli_len))
        명사_li = etri.언어분석_API(analzing_text=d[col], analysisCode='morp')
        if len(명사_li) == 0:
            pass
        else:
            d[col+'_명사li'] = 명사_li
            filter = {'뉴스id':d['뉴스id']}
            update = {'$set':d}
            pp.pprint({'filter':filter, 'update':update})
            db[TBL명].update_one(filter=filter, update=update, upsert=True)
        i+=1

def 뉴스XXsrl_WSDNNGli컬럼의_중복제거(col명='뉴스본문srl_WSDNNGli'):
    """
    정렬은 빠르므로 여기서 하지 말것.
    """
    중복제거저장col명 = col명 + '_중복제거'


    query = {col명:{'$ne':None}, 중복제거저장col명:None}
    projection = {'_id':1, col명:1}
    df = mg.find(db명=DB명, tbl명=PARSED_TBL, query=query, projection=projection, 컬럼순서li=[], df보고형태='df')

    df[col명] = df[col명].apply(lambda x: lh.리스트의_중복제거(li=x))
    dicli = df.to_dict('records')

    for d in dicli:
        query = {'_id':d['_id']}
        update = {'$set':{중복제거저장col명:d[col명]}}
        mg.update_one(db명=DB명, tbl명=PARSED_TBL, query=query, update=update, upsert=False, 사전검증=False)

class CollectingOptimizer:

    def res컬럼에_대한_json_normalizer(dicli):
        from pandas.io.json import json_normalize



        dic = dicli[0]
        pp.pprint({'res_dic의 keys':list(dic.keys())})

        df = json_normalize(data=dicli, record_path='res', meta=['_id','뉴스_url','수집일시'], meta_prefix=None, record_prefix='r_', errors='raise', sep='.')
        df = df.loc[:,['_id','뉴스_url','수집일시','r_text']]
        dbg.dframe(df, caller=inspect.stack()[0][3], 컬럼순서li=[], df보고형태='df')
        dicli = df.to_dict('records')
        dic = dicli[0]
        pp.pprint(dic)
        return dicli

    def ETRI_AI_언어분석_정상완료된_뉴스본문의_길이_보고(타겟col명='뉴스본문', analyzerMethod='srl'):
        언어분석_col명 = 타겟col명 + analyzerMethod + '_res'

        query = {언어분석_col명:{'$elemMatch':{'result':0}}}
        projection = {'_id':1, 언어분석_col명:1}
        dicli = mg.find(db명=DB명, tbl명=PARSING_TBL, query=query, projection=projection, 컬럼순서li=[], df보고형태='dicli')

        df = json_normalize(data=dicli, record_path='res', meta=['_id'], meta_prefix=None, record_prefix='r_', errors='raise', sep='.')

    def ETRI_AI_언어분석_미완료된_뉴스본문의_길이_보고():
        언어분석_col명 = '뉴스본문' + '_' + 'srl'
        query = {언어분석_col명:{'$elemMatch':{'result':-1}}}
        뉴스id_li = mg.distinct(db명=DB명, tbl명=PARSING_TBL, col명='뉴스id', query=query, shown_cnt=1)
        뉴스본문의_길이_보고(뉴스id_li, dbg_on)

    def 뉴스본문의_길이_보고(뉴스id_li):
        query = {'_id':{'$in':뉴스id_li}}
        projection = {'_id':1, '뉴스본문':1}
        dicli = mg.find(db명=DB명, tbl명='뉴스', query=query, projection=projection, 컬럼순서li=[], df보고형태='dicli')
        #df = df.assign(본문크기= lambda x: 0)
        #df['본문크기'] = df['뉴스본문'].apply(lambda x: len(x))
        #df = df.assign(본문크기= lambda x: len(x.뉴스본문))
        for d in dicli:
            if d['뉴스본문'] is None:
                pass
            else:
                d['본문크기'] = len(d['뉴스본문'])
        df = pd.DataFrame(dicli)
        df = df.sort_values('본문크기')
        print('\n'+'*'*60+inspect.stack()[0][3])
        print(df)
        print(df.iloc[:1,])
        pp.pprint(df.iloc[:1,].to_dict('records'))

class CollectingStatusReporter:

    def 뉴스제목본문_ETRI언어분석_컬렉터_작업현황_보고():
        """
        데이터 크기가 너무 커서, 터미널창도 멈춘다. -> 컬럼별로 각개 분석해야 한다.
        """
        뉴스제목본문_ETRI언어분석_수집완료_현황보고(dbg_on)
        #뉴스제목본문_ETRI언어분석_수집결과를_id비교대조로_검증(dbg_on=dbg_on)

    def 뉴스제목본문_ETRI언어분석_수집완료_현황보고():
        query = {'뉴스제목':{'$ne':None}, '뉴스본문':{'$ne':None}}
        projection = {'_id':1, '뉴스제목_ETRI언어분석_수집완료':1, '뉴스본문_ETRI언어분석_수집완료':1}
        df = mg.find(db명=DB명, tbl명='뉴스', query=query, projection=projection, 컬럼순서li=[], df보고형태='df')
        df = df.fillna('_None')

        #df = df.loc[:,['_id','뉴스본문_ETRI언어분석_수집완료']]
        g1 = df.groupby('뉴스제목_ETRI언어분석_수집완료').count()
        print(g1)

        g2 = df.groupby('뉴스본문_ETRI언어분석_수집완료').count()
        print(g2)
        return (g1, g2)

    def 뉴스제목본문_ETRI언어분석_수집결과를_id비교대조로_검증(db명=DB명, tbl_A='뉴스', col_a='_id', tbl_B=RD_TBL명, col_b='뉴스id', shown_cnt=1):


        mg.테이블A의_컬럼a와_테이블B의_컬럼b_간의_개수비교_보고(db명=db명, tbl_A=tbl_A, col_a=col_a, tbl_B=tbl_B, col_b=col_b, shown_cnt=shown_cnt)

    def 뉴스XX에대한_ETRI언어분석요청결과_현황보고(타겟col명='뉴스본문'):
        from pandas.io.json import json_normalize

        언어분석col명 = 타겟col명 + '_srl'
        projection = {'_id':1, '뉴스id':1, 언어분석col명:1}
        dicli = mg.find(db명=DB명, tbl명=PARSING_TBL, query=None, projection=projection, 컬럼순서li=[], df보고형태='dicli')
        df = json_normalize(data=dicli, record_path='result', meta=['_id','뉴스id',언어분석col명], meta_prefix=None, record_prefix='rslt_', errors='raise', sep='.')
        dbg.dframe(df, caller=inspect.stack()[0][3], 컬럼순서li=[], df보고형태='df')

class ParsingStatusReporter:

    def 뉴스제목본문_ETRI언어분석_파서_작업현황_보고():


        """
        ===== 경고 =====
        한번에 모든 컬럼 로딩 사용하면 CPU 터진다
        """
        #query = {'뉴스제목':{'$ne':None}, '뉴스본문':{'$ne':None}}
        projection = {'_id':1, '뉴스제목srl_res파싱완료':1}
        df = mg.find(db명=DB명, tbl명=PARSING_TBL, query=None, projection=projection, 컬럼순서li=[], df보고형태='df')
        df = df.fillna('_None')
        print(df.dtypes)

        g1 = df.groupby('뉴스제목srl_res파싱완료').count()
        print(g1)

class RD_TBL:

    def 언어분석RDTBL에서_뉴스XX의_개수정보dic(col명='뉴스제목_srl', analyzerMethod='srl'):
        """
        다른 함수로 레벨업 예정.
        """
        query = {col명:{'$elemMatch':{'result':0}}}
        뉴스id_li = mg.distinct(db명=DB명, tbl명=PARSING_TBL, col명='뉴스id', query=query, shown_cnt=10)
        dbg._li(li=뉴스id_li, caller=inspect.stack()[0][3], shown_cnt=10)
        뉴스XX_li = mg.distinct(db명=DB명, tbl명=PARSING_TBL, col명=col명, query=query, shown_cnt=10)
        dbg._li(li=뉴스XX_li, caller=inspect.stack()[0][3], shown_cnt=10)
        dic = {
            'TBL명':RD_TBL명,
            '유일한_뉴스id_개수':len(뉴스id_li),
            '유일한_'+col명+'_개수':len(뉴스XX_li),
        }
        pp.pprint({'dic':dic})
        return dic

class TBL:

    def 언어분석TBL_각컬럼_유일값_보고(db명=DB명, tbl명=PARSING_TBL, col_li=None, shown_cnt=1):


        보고제외할col_li = []
        mg.TBL_자료구조_보고(db명=db명, tbl명=tbl명, 보고제외할col_li=보고제외할col_li, 컬럼순서li=[], df보고형태='df')

    def 언어분석TBL에서_뉴스XX의_개수정보dic(col명='뉴스제목_요약', analyzerMethod='srl'):
        query = {col명:{'$not':None}}
        뉴스id_li = mg.distinct(db명=DB명, tbl명=PARSING_TBL, col명='뉴스id', query=query, shown_cnt=10)
        dbg._li(li=뉴스id_li, caller=inspect.stack()[0][3], shown_cnt=10)
        뉴스XX_li = mg.distinct(db명=DB명, tbl명=PARSING_TBL, col명=col명, query=query, shown_cnt=10)
        dbg._li(li=뉴스XX_li, caller=inspect.stack()[0][3], shown_cnt=10)
        dic = {
            'TBL명':TBL명,
            '유일한_뉴스id_개수':len(뉴스id_li),
            '유일한_'+언어분석된col명+'_개수':len(뉴스XX_li),
        }
        pp.pprint({'dic':dic})
        return dic

    def 언어분석TBL의_컬럼별_개수보고(col_li=['뉴스본문_요약','뉴스제목_요약','뉴스제목_명사li']):

        for col in col_li:
            print('\n' + '-'*60 + '컬럼명:{}'.format(col))
            if type(col) is list:
                print('if type(col) is list:')
            else:
                mg.distinct(db명=DB명, tbl명=PARSED_TBL, col명=col, query=None, shown_cnt=1)

class ETRILangAnalysisCollectingStatusReporter:
    """ETRI언어분석 수집현황 보고"""
    def RD_TBL에서_ETRI언어분석수집이_정상완료된_뉴스idli로딩(타겟col명='뉴스제목', analyzerMethod='srl', shown_cnt=1):


        """
        result 값 의미 : 0 = 정상, -1 = 오류
        """


        언어분석_col명 = 타겟col명 + '_' + analyzerMethod
        query = {언어분석_col명:{'$elemMatch':{'result':0}}}
        뉴스id_li = mg.distinct(db명=DB명, tbl명=PARSING_TBL, col명='뉴스id', query=query, shown_cnt=shown_cnt)
        return 뉴스id_li

    #def 뉴스TBL에서_뉴스XXETRI언어분석수집완료True인_대상

    def ETRI언어분석수집할_뉴스XX가_몇개인지_보고(타겟col명='뉴스제목', analyzerMethod='srl', shown_cnt=1):


        """
        ETRI언어분석수집할_타겟선정 방법1
        """


        query = {타겟col명:{'$exists':1}}
        id_li = mg.distinct(db명=DB명, tbl명='뉴스', col명='_id', query=query, shown_cnt=shown_cnt)
        뉴스id_li = ETRI언어분석수집이_정상완료된_뉴스id_li(타겟col명, analyzerMethod, dbg_on, shown_cnt)
        분석수집할_뉴스id_li = ilist.difference_list(li1=id_li, li2=뉴스id_li)

        print('\n'+'*'*60+inspect.stack()[0][3])
        dicli = [
            {'TBL명':'뉴스', '타겟col명':타겟col명, '뉴스id_개수':len(id_li)},
            {'TBL명':RD_TBL명, '타겟col명':타겟col명, '뉴스id_개수':len(뉴스id_li), '분석수집할_뉴스id_li':len(분석수집할_뉴스id_li)},
        ]
        df = pd.DataFrame(dicli)
        dbg.dframe(df, caller=inspect.stack()[0][3], 컬럼순서li=[], df보고형태='df')
        print(df)
        return 분석수집할_뉴스id_li

    def ETRI언어분석수집할_뉴스XX가_몇개인지_보고(뉴스XX='뉴스본문', analyzerMethod='srl', shown_cnt=1):
        from LangAnalysis_Collector import ETRI언어분석수집할_뉴스XX가_몇개인지_보고
        ETRI언어분석수집할_뉴스XX가_몇개인지_보고(뉴스XX, analyzerMethod, dbg_on, shown_cnt)

    def 뉴스XX에_대해_뉴스TBL_언어분석원본TBL_언어분석TBL의_개수를_보고(col명='뉴스제목', analyzerMethod='srl'):
        언어분석파싱된col명 = col명 + '_요약'
        언어분석TBL에서_뉴스XX의_개수정보dic(col명=언어분석파싱된col명, analyzerMethod='srl')
