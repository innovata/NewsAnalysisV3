
import __sklearn as skl
import pandas as pd
from datetime import datetime
import News as news
import News_
import ML

CLF_TBL = 'XX_분류'
CLF_REPORT_TBL = 'XX_분류결과_분석보고'


def 트윗_분류기():
    트윗_단위분류기(훈련col명='뉴스제목', 분류기_알고리즘='MultinomialNB')
    TBL에_저장된_하나의_문서를_SP_TBL에_풀어헤치기(실험tbl명='트위터_유저타임라인', 실험col명='text', 분류기_알고리즘='MultinomialNB', dbg_on=False, 사전검증=False)


class Classifier:
    """
    "어떤 클러스터"를 사용한 "어떤 훈련자료"를 이용해서 "어떤 분류기"를 훈련시킨다.
    ===== 작업순서 =====
    1. test_df 를 넘겨받는다.
    - 실험자료는 필수 파라미터로 받아야 한다. 왜냐? 실험자료는 경우에 따라 쿼리가 너무 달라서 이 함수에서 처리하기에는 제약사항이 많아져 파라미터가 늘어난다.
    2. 넘겨받은 파라미터로 클러스터를 불러와 그 개수만큼 반복한다.
    - 클러스터 선택정보를 파라미터로 넘겨 받은 만큼 적은 횟수로 반복한다.
    - 즉, 어떤 클러스터를 사용할지 여기서 결정한다. 물론 서비스 모듈에서 결정해서 넘기겠지만, 결정 안해서 넘기면 모든 클러스터에 대해 반복한다.

    3. test_docs과 trainset 모두 갖춰졌으므로 반복하며 분류한다.
    """
    def 뉴스클러스터기준_분류(test_df, 실험tbl명, key_col, 실험col명, 분류기_알고리즘='MultinomialNB', 훈련tbl명='뉴스_ETRI언어분석', 훈련col명='뉴스본문srl_WSDNNGli', algorithm='KMeans', sampling=10000, n_clusters=2000, dbg_on=False, 사전검증=False):
        print('\n' + '='*60 + inspect.stack()[0][3])
        """
        ===== 사용법 =====
        ML.classifier.뉴스클러스터기준_분류(test_df=test_df, 실험tbl명=실험tbl명, 실험col명=실험col명, 분류기_알고리즘=분류기_알고리즘, 훈련tbl명=훈련tbl명, 훈련col명=훈련col명, algorithm=algorithm, sampling=sampling, n_clusters=n_clusters, dbg_on=dbg_on, 사전검증=사전검증)
        훈련tbl명='뉴스_ETRI언어분석', 훈련col명='뉴스본문srl_WSDNNGli', algorithm='KMeans', sampling=10000, n_clusters=2000

        ===== 작업순서 =====
        클러스터_선택_및_반복 -> 훈련자료모음_로딩
        클러스터_호출_및_훈련자료_받기 -> 훈련자료모음_로딩
        분류기_선택_및_훈련
        분류기_예측
        실험자료의 분류예측결과 저장
        """
        #if dbg_on == True: print(설명)
        #입력 = {'tbl명':tbl명, 'clstclst_col':clstclst_col, 'algorithm':algorithm, 'n_clusters':n_clusters}
        #if dbg_on == True: pp.pprint({'입력':입력})

        test_docs = test_df[실험col명]
        #return None
        """
        ============================== 훈련자료모음_로딩 ==============================
        어떤 훈련자료로 분류기를 훈련시킬 것인가?
        """
        import ML_Cluster as cluster
        print('\n' + '= '*30 + '훈련자료모음_로딩')

        clst_meta_df = cluster.XX_클러스터_검색로딩(clst_tbl=훈련tbl명, clst_col=훈련col명, algorithm=algorithm, sampling=sampling, n_clusters=n_clusters, meta_only=True, dbg_on=dbg_on)
        ClstMeta_dicli = clst_meta_df.to_dict('records')
        ClstMeta_dicli_len = len(ClstMeta_dicli)
        i=1
        for d in ClstMeta_dicli:
            print('\n' + '-'*60 + '{}/{}'.format(i, ClstMeta_dicli_len))
            print('--> 클러스터 정보 :\n', d)

            train_df = cluster.Trainset_로딩(clst_tbl=d['clst_tbl'], clst_col=d['clst_col'], algorithm=d['algorithm'], sampling=d['sampling'], n_clusters=d['n_clusters'], dbg_on=dbg_on)
            train_docs = train_df[ d['clst_col'] ]
            train_label = train_df['label']
            """
            ============================== 분류기_선택_훈련_예측 ==============================
            """
            print('\n' + '= '*30 + '분류기_선택_및_훈련')
            if 분류기_알고리즘 == 'MultinomialNB':
                predicted_li = skl.supervised_TextData_classifier(trainset_data=train_docs, trainset_target=train_label, testset_data=test_docs, dbg_on=dbg_on)
            elif 분류기_알고리즘 == 'Perceptron':
                predicted_li = skl.language_train_model(train_docs=train_docs, train_label=train_label, test_docs=test_docs)

            test_df['predicted'] = predicted_li
            print('\n test_df.dtypes :\n', test_df.dtypes)
            pp.pprint({'len(test_df)':len(test_df)})
            #return None
            """
            ============================== 분류기_결과보고 ==============================
            """
            print('\n' + '= '*30 + '분류기_결과보고')
            g = test_df.groupby('predicted').count().sort_values(key_col, ascending=False)
            print(g)
            #return None
            """
            ============================== 분류기_결과저장 ==============================
            insert_one 이라도 데이타가 커서 dbg_on 강제 False
            loop 돌때 test_df 본래의 _id 컬럼명을 여기서 변경하면, 다음 루프에도 영향을 준다.
            """
            print('\n' + '= '*30 + '분류기_결과저장')
            clf결과저장_dic = {
                '실험tbl명':실험tbl명,
                'key_col':key_col,
                '실험col명':실험col명,
                '분류기_알고리즘':분류기_알고리즘,
                '클러스터id':d['_id'],
                'KeyidPredict_dicli':None,
            }
            print('\n clf결과저장_dic :\n', clf결과저장_dic)
            test_df_1 = test_df.loc[:,[key_col, 'predicted']]
            test_df_1 = test_df_1.rename(columns={key_col:'keyid'})
            print('\n test_df_1.dtypes :\n', test_df_1.dtypes)
            clf결과저장_dic['KeyidPredict_dicli'] = test_df_1.to_dict('records')
            mg.insert_one(db명=DB명, tbl명=CLF_TBL, dic=clf결과저장_dic, dbg_on=dbg_on, 사전검증=사전검증)

            i+=1
            #break

    def 뉴스클러스터기준_추가자료_분류(test_df, 실험tbl명, key_col, 실험col명, 분류기_알고리즘='MultinomialNB', 훈련tbl명='뉴스_ETRI언어분석', 훈련col명='뉴스본문srl_WSDNNGli', algorithm='KMeans', sampling=10000, n_clusters=2000, dbg_on=False, 사전검증=False):
        print('\n' + '='*60 + inspect.stack()[0][3])
        """
        고민중.
        """
        #if dbg_on == True: print(설명)
        #입력 = {'tbl명':tbl명, 'clstclst_col':clstclst_col, 'algorithm':algorithm, 'n_clusters':n_clusters}
        #if dbg_on == True: pp.pprint({'입력':입력})

        test_docs = test_df[실험col명]
        #return None
        """
        ============================== 훈련자료모음_로딩 ==============================
        어떤 훈련자료로 분류기를 훈련시킬 것인가?
        """
        import ML_Cluster as cluster
        print('\n' + '= '*30 + '훈련자료모음_로딩')

        clst_meta_df = cluster.XX_클러스터_검색로딩(clst_tbl=훈련tbl명, clst_col=훈련col명, algorithm=algorithm, sampling=sampling, n_clusters=n_clusters, meta_only=True, dbg_on=dbg_on)
        ClstMeta_dicli = clst_meta_df.to_dict('records')
        ClstMeta_dicli_len = len(ClstMeta_dicli)
        i=1
        for d in ClstMeta_dicli:
            print('\n' + '-'*60 + '{}/{}'.format(i, ClstMeta_dicli_len))
            print('--> 클러스터 정보 :\n', d)

            train_df = cluster.Trainset_로딩(clst_tbl=d['clst_tbl'], clst_col=d['clst_col'], algorithm=d['algorithm'], sampling=d['sampling'], n_clusters=d['n_clusters'], dbg_on=dbg_on)
            train_docs = train_df[ d['clst_col'] ]
            train_label = train_df['label']
            """
            ============================== 분류기_선택_훈련_예측 ==============================
            """
            print('\n' + '= '*30 + '분류기_선택_및_훈련')
            if 분류기_알고리즘 == 'MultinomialNB':
                predicted_li = skl.supervised_TextData_classifier(trainset_data=train_docs, trainset_target=train_label, testset_data=test_docs, dbg_on=dbg_on)
            elif 분류기_알고리즘 == 'Perceptron':
                predicted_li = skl.language_train_model(train_docs=train_docs, train_label=train_label, test_docs=test_docs)

            test_df['predicted'] = predicted_li
            print('\n test_df.dtypes :\n', test_df.dtypes)
            pp.pprint({'len(test_df)':len(test_df)})
            #return None
            """
            ============================== 분류기_결과보고 ==============================
            """
            print('\n' + '= '*30 + '분류기_결과보고')
            g = test_df.groupby('predicted').count().sort_values(key_col, ascending=False)
            print(g)
            #return None
            """
            ============================== 분류기_결과의_신규삽입_업뎃_저장 ==============================
            insert_one 이라도 데이타가 커서 dbg_on 강제 False
            loop 돌때 test_df 본래의 _id 컬럼명을 여기서 변경하면, 다음 루프에도 영향을 준다.
            """
            print('\n' + '= '*30 + '분류기_결과의_신규삽입_업뎃_저장')
            clf결과저장_dic = {
                '실험tbl명':실험tbl명,
                'key_col':key_col,
                '실험col명':실험col명,
                '분류기_알고리즘':분류기_알고리즘,
                '클러스터id':d['_id'],
                'KeyidPredict_dicli':None,
            }
            print('\n clf결과저장_dic :\n', clf결과저장_dic)
            test_df_1 = test_df.loc[:,[key_col, 'predicted']]
            test_df_1 = test_df_1.rename(columns={key_col:'keyid'})
            print('\n test_df_1.dtypes :\n', test_df_1.dtypes)
            clf결과저장_dic['KeyidPredict_dicli'] = test_df_1.to_dict('records')



            query = clf결과저장_dic.copy()
            del(query['KeyidPredict_dicli'])
            key_li = list(query.keys())
            projection = {key:1 for key in key_li}
            df_ = mg.find(db명=DB명, tbl명=CLF_TBL, query=query, projection=projection, dbg_on=True, 컬럼순서li=[], df보고형태='df')
            if len(df_) == 0:
                print('분류결과_신규저장')
                mg.update_one(db명=DB명, tbl명=CLF_TBL, dic=clf결과저장_dic, dbg_on=dbg_on, 사전검증=사전검증)
            elif len(df_) == 1:
                print('추가자료_분류결과_업뎃저장')
                뉴스클러스터기준_추가자료_분류결과_업뎃저장(df_)
            else:
                print('그럴리 업자나? XX_분류 테이블 중복제거해라.')
                break
                return None
            i+=1
            break

    def 뉴스클러스터기준_추가자료_분류결과_업뎃저장(df_, test_df):
        dic = df_.to_dict('records')[0]
        query = {'_id':dic['_id']}
        projection = {'_id':0, 'KeyidPredict_dicli':1}
        df = mg.find(db명=DB명, tbl명=CLF_TBL, query=query, projection=projection, dbg_on=True, 컬럼순서li=[], df보고형태='df')

class Loader:
    """
    KeyidPredict_dicli 컬럼을 포함해서 로딩할 경우 엄청난 시간이 걸린다. 프로그램이 멈출수도 있다.
    절대로 통째로 로드하지 말것.
    """
    def XX_분류_검색로딩(실험tbl명=None, 실험col명=None, 분류기_알고리즘=None, meta_only=False, dbg_on=False):
        print('\n' + '='*60 + inspect.stack()[0][3])
        """
        ===== 사용법 =====
        #XX_분류_검색로딩(실험tbl명, 실험col명, 분류기_알고리즘, meta_only, dbg_on)
        """
        query = {}
        if 실험tbl명 is not None: query.update({'실험tbl명':실험tbl명})
        if 실험col명 is not None: query.update({'실험col명':실험col명})
        if 분류기_알고리즘 is not None: query.update({'분류기_알고리즘':분류기_알고리즘})
        #print('\n query :')
        #pp.pprint(query)
        projection = {'KeyidPredict_dicli':0} if meta_only == True else None

        clf_df = mg.find(db명=DB명, tbl명=CLF_TBL, query=query, projection=projection, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')
        print('\n clf_df.dtypes :\n', clf_df.dtypes)
        pp.pprint({'len(clf_df)':len(clf_df)})
        return clf_df

    def KeyidPredict_dicli_json_normalize(df, dbg_on=True):
        from pandas.io.json import json_normalize
        print('\n' + '='*60 + inspect.stack()[0][3])
        """
        XX_분류 테이블의 KeyidPredict_dicli을 json_normalize 한다. 이때, 메타컬럼을 선택적으로 선택할 수 있다.
        기본 컬럼 : keyid, predicted

        df : XX_분류 테이블에서 로딩한 df.

        meta_cols_선택

        ===== 사용법 =====
        KeyidPredict_dicli_json_normalize(df, dbg_on)
        """
        col_li = list(df.columns)
        col_li.remove('KeyidPredict_dicli')
        col_li.remove('_id')
        if dbg_on == True: pp.pprint({'meta_cols':col_li})

        dicli = df.to_dict('records')
        clf_df = json_normalize(data=dicli, record_path='KeyidPredict_dicli', meta=col_li, meta_prefix=None, record_prefix=None, errors='raise', sep='.')
        if dbg_on == True: print('\n clf_df.dtypes :\n', clf_df.dtypes)
        if dbg_on == True: pp.pprint({'len(clf_df)':len(clf_df)})
        return clf_df

    def KeyidPredict_dicli_json_normalize_v2(df, dbg_on=False):
        from pandas.io.json import json_normalize
        print('\n' + '='*60 + inspect.stack()[0][3])
        """
        XX_분류 테이블의 KeyidPredict_dicli을 json_normalize 한다. 이때, 메타컬럼을 선택적으로 선택할 수 있다.
        기본 컬럼 : keyid, predicted

        df : XX_분류 테이블에서 로딩한 df.

        meta_cols_선택

        ===== 사용법 =====
        KeyidPredict_dicli_json_normalize(df, dbg_on)
        """
        meta_cols = list(df.columns)
        meta_cols.remove('KeyidPredict_dicli')
        if dbg_on == True: pp.pprint({'meta_cols':meta_cols})

        dicli = df.to_dict('records')
        clf_df = json_normalize(data=dicli, record_path='KeyidPredict_dicli', meta=meta_cols, meta_prefix=None, record_prefix=None, errors='raise', sep='.')
        if dbg_on == True: print('\n clf_df.dtypes :\n', clf_df.dtypes)
        if dbg_on == True: pp.pprint({'len(clf_df)':len(clf_df)})
        return clf_df

    def json_normalized_XX_분류TBL_로딩(dbg_on=False):
        print('\n' + '='*60 + inspect.stack()[0][3])
        df = XX_분류_검색로딩(실험tbl명, 실험col명, 분류기_알고리즘, 클러스터id, dbg_on)
        df = KeyidPredict_dicli_json_normalize(df, dbg_on)
        return df

    def Predicted_Orig_df로딩(실험tbl명, 실험col명, 분류기_알고리즘, 클러스터id, dbg_on=False):
        print('\n' + '='*60 + inspect.stack()[0][3])
        """
        이미 분류작업이 완료된 원본자료와 predicted 값을 결합해서 로딩한다.

        ===== 용어정의 =====
        keyid명 : "KeyidPredict_dicli"컬럼에서 검색할 때 사용할 원본자료의 키id명

        ===== 작업순서 =====
        원본자료의 keyli로 XX_분류TBL에서 검색.
        분류값을 결합.

        ===== 사용법 =====
        predicted_df = ML.classifier.Predicted_Orig_df로딩(실험tbl명='트위터_유저타임라인', 실험col명='text', 분류기_알고리즘='MultinomialNB', 클러스터id=None, dbg_on=False)
        predicted_df = ML.classifier.Predicted_Orig_df로딩(실험tbl명, 실험col명, 분류기_알고리즘, 클러스터id, dbg_on=False)

        elemMatch={'predicted':40}
        """

        query = {'실험tbl명':실험tbl명, '실험col명':실험col명, '분류기_알고리즘':분류기_알고리즘, '클러스터id':클러스터id}
        clf_df = mg.find(db명=DB명, tbl명=CLF_TBL, query=query, projection=None, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')

        clf_dicli = clf_df.to_dict('records')
        d = clf_dicli[0]
        print(d.keys())
        """
        ============================== KeyidPredict_dicli_json_normalize ==============================
        """
        clfied_df = KeyidPredict_dicli_json_normalize(clf_df, dbg_on).loc[:, ['keyid', 'predicted']]
        """
        ============================== 분류된_원본자료_로딩_및_결합 ==============================
        """
        print('\n' + '= '*30 + '분류된_원본자료_로딩')
        keyid_li = list(clfied_df['keyid'])
        query = {d['key_col']:{'$in':keyid_li}}
        #projection = {d['key_col']:1, d['실험col명']:1}
        org_df = mg.find(db명=DB명, tbl명=d['실험tbl명'], query=query, projection=None, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')
        print('\n org_df.dtypes :\n', org_df.dtypes)
        pp.pprint({'len(org_df)':len(org_df)})


        print('\n' + '= '*30 + '원본자료에_결합')
        predicted_df = org_df.join(clfied_df.set_index('keyid'), on=d['key_col'])
        print('\n predicted_df.dtypes :\n', predicted_df.dtypes)

        """
        ============================== 분류된_원본자료_보고 ==============================
        """
        print('\n' + '= '*30 + '분류된_원본자료_보고')
        g_df = predicted_df.loc[:, ['predicted', d['key_col']]]
        print('\n g_df.dtypes :\n', g_df.dtypes)
        if dbg_on == True: print(g_df)
        g = g_df.groupby('predicted').count().sort_values(d['key_col'], ascending=False)
        print('\n Predicted_Grouped_Report :\n', g)
        return predicted_df, g

class Analyzer:

    def 분류결과보고_로딩(predicted_num=2, dbg_on=False):
        """
        ===== 사용법 =====
        ML.classifier.분류결과보고_로딩(predicted_num, dbg_on)
        ML.classifier.분류결과보고_로딩(predicted_num=None, dbg_on=False)
        """
        df = mg.find(db명=DB명, tbl명=CLF_REPORT_TBL, query=None, projection=None, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')
        df = df.rename(columns={'_id':'clf_rpt_id'})
        df['predicted_num'] = df['predicted_li'].apply(lambda x: len(x))
        if predicted_num is not None:
            df = df.sort_values('predicted_num', ascending=False)[:predicted_num]

        return df

    def CLF_TBL자료에_CLST_TBL메타정보를_결합해서_df로딩(dbg_on=False):
        import ML_Cluster as cluster
        """
        predicted_num : 분류값의_분포도, predicted_li 의 개수
        predicted_num = None : CLF_REPORT_TBL의 모든 자료 로딩

        ===== 사용법 =====
        ML.classifier.CLF_TBL자료에_CLST_TBL메타정보를_결합해서_df로딩(predicted_num=None, dbg_on=False)
        """
        clf_rpt_df = 분류결과보고_로딩(predicted_num=None, dbg_on=False)
        uq_clf_id_li = list(clf_rpt_df['clf_id'].unique())
        query = {'_id':{'$in':uq_clf_id_li}}
        projection = {'KeyidPredict_dicli':0}
        clf_df = mg.find(db명=DB명, tbl명=CLF_TBL, query=query, projection=projection, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')
        clf_df = clf_df.rename(columns={'_id':'clf_id', 'key_col':'clf_keycol'})


        uq_clst_id_li = list(clf_df['클러스터id'].unique())
        query = {'_id':{'$in':uq_clst_id_li}}
        projection = {'KeyidLabel_dicli':0}
        clst_df = mg.find(db명=DB명, tbl명=cluster.CLST_TBL, query=query, projection=projection, dbg_on=False, 컬럼순서li=[], df보고형태='df')
        clst_df = clst_df.rename(columns={'_id':'clst_id', 'key_col':'clst_keycol'})
        """
        = = = = = = = = = = = = = = = clst_df에_분류결과보고정보_결합 = = = = = = = = = = = = = = =
        clst_df.dtypes :
        clst_id              object
        algorithm            object
        clst_col             object
        clst_tbl             object
        clst_keycol          object
        n_clusters            int64
        sampling              int64
        실행시간sec             float64
        clf_id               object
        clf_keycol           object
        분류기_알고리즘             object
        실험col명               object
        실험tbl명               object
        clf_rpt_id           object
        predicted_cnt_li     object
        predicted_li         object
        predicted_num         int64
        """
        clst_df = clst_df.join(clf_df.set_index('클러스터id'), on='clst_id')
        #clst_df = clst_df.join(clf_rpt_df.set_index('clf_id'), on='clf_id')
        print('\n clst_df.dtypes :\n', clst_df.dtypes)
        #clst_df = clst_df.sort_values('predicted_num', ascending=False)
        print('\n clst_df_len :\n', len(clst_df))
        #print('\n clst_df :\n', clst_df)
        return clst_df

    def 분류기알고리즘별_표준편차_비교분석():
        df = mg.find(db명=DB명, tbl명=ML.classifier.CLF_TBL, query=None, projection=None, dbg_on=False, 컬럼순서li=[], df보고형태='df')
        df = df.rename(columns={'_id':'clf_id'})
        df = KeyidPredict_dicli_json_normalize_v2(df, dbg_on=True)
        독립변수 = ['클러스터id', '실험col명']
        비교변수 = '분류기_알고리즘'
        grouped = df.groupby(독립변수)
        grouped_len = len(grouped)
        i=1
        dicli = []
        for n, g in grouped:
            print('\n' + '-'*60 + '{}/{}, 독립변수:{}'.format(i, grouped_len, n))
            g = g.assign(keyid_cnt= 1)
            g = g.fillna(0)
            pvt = pd.pivot_table(data=g, values='keyid_cnt', index='predicted', columns=비교변수, aggfunc='sum', fill_value=None, margins=False, dropna=True, margins_name='All')
            pvt = pvt.fillna(0)
            dscb = pvt.describe()
            print('\n dscb :\n', dscb)
            dscb = dscb.T
            print('\n dscb :\n', dscb)
            std = dscb['std']
            std = std.to_dict()
            print('\n std :\n', std)
            dic = {}
            for j in range(len(독립변수)):
                dic[독립변수[j]] = n[j]
            dic.update(std)
            print('\n dic :\n', dic)
            dicli.append(dic)
            i+=1
            #break

        mg.insert_many(db명=DB명, tbl명=inspect.stack()[0][3], dicli=dicli, dbg_on=False, 사전검증=False)

class Reporter:

    def 분류기알고리즘별_표준편차_비교_scatterplot_3D():
        import Translator
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.pyplot as plt
        import numpy as np
        import math
        from matplotlib import rc
        rc('font', family='AppleGothic')
        """
        xs : std of KMeans
        ys : std of MiniBatchKMeans
        zs : 구분해서 보고 싶은 변수.
        """
        projection = {'_id':0}
        df = mg.find(db명=DB명, tbl명='분류기알고리즘별_표준편차_비교분석', query=None, projection=projection, dbg_on=False, 컬럼순서li=[], df보고형태='df')
        df = Translator.term_translator(df)
        df['test_column'] = df['test_column'].str.replace('text', 'tweet_text')
        df['clst_id_num'] = df.index

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        X = 'Perceptron'
        Y = 'MultinomialNB'
        Z = 'clst_id_num'
        colors = ['r', 'g', 'b', 'y', 'c']
        markers = ['o', '^', 's', '*', '+']
        grouped = df.groupby('test_column')

        grouped_len = len(grouped)
        i=0
        for n, g in grouped:
            print('\n' + '-'*60 + '{}/{}, n:{}'.format(i, grouped_len, n))
            print(g)

            xs = list(g[X])
            ys = list(g[Y])
            zs = list(g[Z])
            c = colors[i]
            m = markers[i]
            ax.scatter(xs, ys, zs, zdir='z', c=c, marker=m)
            i+=1

        ax.set_xlabel(X + '_std')
        ax.set_ylabel(Y + '_std')
        ax.set_zlabel(Z)

        ax.legend(labels=list(df['test_column'].unique()), loc='upper right', bbox_to_anchor=(1, 1), fontsize='x-small')
        plt.show()

    def 분류기알고리즘별_표준편차_비교결과로_어떤_클러스터_분류기_조합이_가장효과적인가():
        import Translator

        df = mg.find(db명=DB명, tbl명='분류기알고리즘별_표준편차_비교분석', query=None, projection=None, dbg_on=False, 컬럼순서li=[], df보고형태='df')
        df_1 = df[250:300]
        df_1['clst_id_num'] = df_1.index
        df_2 = df_1.loc[:, ['clst_id_num', '클러스터id']]
        uq_clst_id = list(df_2['클러스터id'].unique())

        query = {'_id':{'$in':uq_clst_id}}
        projection = {'KeyidLabel_dicli':0}
        df1 = mg.find(db명=DB명, tbl명='XX_클러스터', query=query, projection=projection, dbg_on=False, 컬럼순서li=[], df보고형태='df')
        df1 = df1.rename(columns={'_id':'clst_id'})

        df1 = df1.join(df_2.set_index('클러스터id'), on='clst_id')
        df1 = Translator.term_translator(df1)
        df1 = df1.sort_values(by='clst_id_num', ascending=False)
        print(df1)
        return df_1, df1

class Handler:

    def XX_분류의_클러스터id_업뎃(clst_tbl='뉴스_ETRI언어분석', clst_col='뉴스본문srl_WSDNNGli', algorithm='KMeans', sampling=10000, n_clusters=2000):
        from ML_Cluster import CLST_TBL
        #projection = {'_id':1}
        dicli = mg.find(db명=DB명, tbl명=CLF_TBL, query=None, projection=None, dbg_on=True, 컬럼순서li=[], df보고형태='dicli')
        return None

        query = {'clst_tbl':clst_tbl, 'clst_col':clst_col, 'algorithm':algorithm, 'sampling':sampling, 'n_clusters':n_clusters}
        print('\n 훈련자료의 조건 :')
        pp.pprint(query)
        dicli_1 = mg.find(db명=DB명, tbl명=CLST_TBL, query=query, projection=None, dbg_on=False, 컬럼순서li=[], df보고형태='dicli')
        클러스터id = dicli_1[0]['_id']

        query = {'_id':dicli[0]['_id']}
        update = {'$set':{'클러스터id':클러스터id}}
        mg.update_one(db명=DB명, tbl명=CLF_TBL, query=query, update=update, upsert=False, dbg_on=True, 사전검증=False)

    def XX_분류TBL의_클러스터_중복제거(dbg_on=True):
        clf_df = XX_분류_검색로딩(실험tbl명=None, 실험col명=None, 분류기_알고리즘=None, meta_only=True, dbg_on=False)
        df = clf_df[ clf_df.duplicated(subset=['실험tbl명', 'key_col', '실험col명', '분류기_알고리즘', '클러스터id'], keep='first') ]
        id_li = list(df['_id'])
        print(id_li)
        query = {'_id':{'$in':id_li}}
        mg.delete_many(db명=DB명, tbl명=CLF_TBL, query=query, dbg_on=False, 사전검증=False)

    def 특정_실험tbl명에_대해_통째로_삭제():
        """
        신규 데이터에 대해 분류해서 추가업뎃하기 보다, 기존 분류된 데이터를 삭제하고
        """
