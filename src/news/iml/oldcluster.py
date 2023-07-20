
import pandas as pd
from datetime import datetime
import numpy as np
import __sklearn as skl
from pandas.io.json import json_normalize

TBL명 = 'XX_클러스터'
CLST_TBL = 'XX_클러스터'

class Cluster:

    def 단일타겟_단일조건_클러스터(clst_tbl='뉴스', key_col='뉴스id', clst_col='뉴스제목srl_WSDNNGli', sampling=100,  n_cluster_ratio=1/10, algorithm='KMeans'):
        """
        ===== 작업순서 =====
        클러스터 타겟선정
        클러스터링-저장
        """
        clst_trgt_df = 타겟로딩(clst_tbl, key_col, clst_col, sampling, n_clusters, algorithm, dbg_on, 사전검증)
        clsted_trgt_df = 클러스터링(clst_trgt_df, clst_tbl, key_col, clst_col, sampling, algorithm, n_clusters, dbg_on, 사전검증)
        return df

    def 타겟로딩(clst_tbl='뉴스', key_col='뉴스id', clst_col='뉴스제목srl_WSDNNGli', sampling=100, n_clusters=1000, algorithm='KMeans'):
        """
        ============================== 타겟로딩 ==============================
        clst_col
        clsting_col
        clsted_col
        """
        query = {clst_col:{'$ne':None}}
        projection = {'_id':1, key_col:1, clst_col:1}
        df = mg.find(db명=DB명, tbl명=clst_tbl, query=query, projection=projection, 컬럼순서li=[], df보고형태='df')

        print('\n' + '= '*30 + '샘플링')
        df_len = len(df)
        dbl_arr = np.random.random_integers(low=0, high=df_len-1, size=(1, sampling))
        sampling_li = dbl_arr.tolist()[0]
        df = df.iloc[sampling_li, ]
        return df

    def 클러스터링(clst_trgt_df, clst_tbl='뉴스', key_col='뉴스id', clst_col='뉴스제목srl_WSDNNGli', sampling=100, algorithm='KMeans', n_clusters=1000):
        """
        ============================== 자료구조_정의 ==============================
        이 함수를 모듈화 했기 때문에, 자료구조_정의를 이 함수에서 해야 한다.
        """
        print('\n' + '= '*30 + '자료구조_정의')
        clst결과_dic = {
            'clst_tbl':clst_tbl,
            'key_col':key_col,
            'clst_col':clst_col,
            'sampling':sampling,
            'n_clusters':n_clusters,
            'algorithm':algorithm,
            'KeyidLabel_dicli':None,
        }
        pp.pprint({'clst결과_dic':clst결과_dic})
        clst_trgt_df = clst_trgt_df.loc[:, [key_col, clst_col]]
        """
        ============================== clst_ColValue_dtype_검사조작 ==============================
        """
        clst_trgt_df = clst_ColValue_dtype_검사조작(clst_trgt_df, clst_col)
        if clst_trgt_df is None: return None
        """
        ============================== 클러스터 ==============================
        label_li = plot_gmm_v2(df)
        label_li = plot_gmm_selection_v2(df)
        """
        print('\n' + '= '*30 + '클러스터')
        df = clst_trgt_df.copy()
        label_li = skl.unsupervised_doc_clustering(dataset_data=df[clst_col], n_clusters=n_clusters, algorithm=algorithm)
        df['label'] = label_li
        clsted_trgt_df = df.copy()
        clsted_df = clsted_trgt_df.loc[:, [key_col, 'label']]
        """
        ============================== 클러스터_결과보고 ==============================
        #return None
        """
        print('\n' + '= '*30 + '클러스터_결과보고')
        g = clsted_df.groupby('label').count().sort_values(key_col, ascending=False)
        print(g)
        """
        ============================== 클러스터_결과저장 ==============================
        뉴스 테이블과 그로부터 파생된 다른 테이블 간의 "key_col" 이 다르기 때문에, 원본인 뉴스 테이블의 "_id" 컬럼명을 변경해주도록 한다.
        -> 즉, 원본 테이블의 "_id" 컬럼명은 일반적이기 때문에 명시적인 컬러명(예 : keyid)으로 변경한다.
        """
        print('\n' + '= '*30 + '클러스터_결과저장')
        clsted_df = clsted_df.rename(columns={key_col:'keyid'})
        clst결과_dic['KeyidLabel_dicli'] = clsted_df.to_dict('records')
        clst결과_dic['실행시간sec'] = (datetime.now() - 시작시간).total_seconds()
        mg.insert_one(db명=DB명, tbl명=TBL명, dic=clst결과_dic, 사전검증=사전검증)
        return clsted_trgt_df

    def clst_ColValue_dtype_검사조작(df, clst_col):
        clst_ColValue_dtype = type(list(df[clst_col])[0])
        pp.pprint({'clst_ColValue_dtype':clst_ColValue_dtype})
        if clst_ColValue_dtype is str:
            return df
        elif clst_ColValue_dtype is list:
            s = datetime.now()
            df[clst_col] = df[clst_col].apply(lambda x: ' '.join(x))
            pp.pprint({'실행시간_sec':(datetime.now() - s).total_seconds()})
            return df
        else:
            print('\n 클러스터 clst_col의  값은 문자열이어야 한다.\n')
            return None

    def 다중타겟_다중조건_클러스터(클러스터타겟_tpli, 샘플링기준_tpNum=4, sampling_li=list(range(1000, 11000, 1000)), n_cluster_ratio=1/10, algorithm_li=['MiniBatchKMeans', 'KMeans']):
        """
        샘플링기준_tpNum : 클러스터타겟_tpli 중 샘플링 기준이 될 튜플번호
        n_cluster_ratio : 클러스터수와 샘플수의 비율. sampling * n_cluster_ratio = n_clusters
        -> 1000 * 1/10 = 100
        -> 1000 * 1/5 = 200
        조건 하나당 실행시간 : 3620.60371
        총 조건 100개의 실행시간 : 3620.605005

        ============================== 클러스터_타겟조합_튜플리스트_정의 ==============================
        클러스터타겟_tpli : 클러스터_타겟조합_튜플리스트, (clst_tbl, key_col, clst_col)

        print('\n' + '='*60 + '클러스터_타겟조합_튜플리스트_정의')
        클러스터타겟_tpli = [
            ('뉴스' ,'_id', '뉴스제목'),
            ('뉴스' ,'_id', '뉴스본문'),

            ('뉴스_ETRI언어분석' ,'뉴스id', '뉴스제목srl_WSDNNGli'),
            ('뉴스_ETRI언어분석' ,'뉴스id', '뉴스본문srl_WSDNNGli'),
            ('뉴스_ETRI언어분석' ,'뉴스id', '뉴스본문srl_WSDNNGli_중복제거'),
        ]
        algorithm_li = ['MiniBatchKMeans', 'KMeans']
        sampling_li = list(range(1000, 11000, 1000))
        """
        """
        ============================== 3차원_Loop ==============================
        샘플링 숫자에 따라 타겟의 뉴스id가 변화하기 때문에 샘플링 루프를 먼저 돌아야 한다.
        """
        시작시간 = datetime.now()

        클러스터타겟_tpli_len = len(클러스터타겟_tpli)
        샘플링기준_tp = 클러스터타겟_tpli[샘플링기준_tpNum]
        algorithm_li_len = len(algorithm_li)
        sampling_li_len = len(sampling_li)

        cond_cnt = 1
        i=1
        for sampling in sampling_li:
            print('\n' + '- '*30 + '{}/{}, sampling:{}'.format(i, sampling_li_len, sampling))
            """
            ============================== 뉴스id_기반_고정타겟_샘플링 ==============================
            샘플링기준tbl명 = '뉴스_ETRI언어분석'
            샘플링기준id명 = '뉴스id'
            샘플링기준col명 = '뉴스본문srl_WSDNNGli_중복제거'
            """
            print('\n' + '= '*30 + '뉴스id_기반_고정타겟_샘플링')

            샘플링기준tbl명 = 샘플링기준_tp[0]
            샘플링기준id명 = 샘플링기준_tp[1]
            샘플링기준col명 = 샘플링기준_tp[2]

            query = {샘플링기준col명:{'$ne':None}}
            projection = {샘플링기준id명:1}
            df = mg.find(db명=DB명, tbl명=샘플링기준tbl명, query=query, projection=projection, 컬럼순서li=[], df보고형태='df')

            df_len = len(df)
            dbl_arr = np.random.random_integers(low=0, high=df_len-1, size=(1, sampling))
            sampling_li = dbl_arr.tolist()[0]
            df = df.iloc[sampling_li, ]

            뉴스id_li = list(df['뉴스id'])
            #print(뉴스id_li)
            print('\n len(뉴스id_li) : ', len(뉴스id_li))

            n_clusters = int(round(sampling * n_cluster_ratio, 0)) if sampling >= 20 else 2
            print('\n n_clusters :', n_clusters)

            j=1
            for algorithm in algorithm_li:
                print('\n' + '- '*30 + '{}/{}, {}'.format(j, algorithm_li_len, algorithm))
                k=1
                for tp in 클러스터타겟_tpli:
                    print('\n' + '- '*30 + '{}/{}, {}:{}'.format(k, 클러스터타겟_tpli_len, tp[0], tp[2]))
                    조건별_시작시간 = datetime.now()
                    print('\n' + '= '*30 + '고정된_샘플링으로_조건별_문서로딩')

                    clst_tbl = tp[0]
                    key_col = tp[1]
                    clst_col = tp[2]

                    query = {key_col:{'$in':뉴스id_li}, clst_col:{'$ne':None}}
                    projection = {key_col:1, clst_col:1}
                    clst_trgt_df = mg.find(db명=DB명, tbl명=clst_tbl, query=query, projection=projection, 컬럼순서li=[], df보고형태='df')

                    클러스터링(clst_trgt_df, clst_tbl, key_col, clst_col, sampling, algorithm, n_clusters, dbg_on, 사전검증)

                    print('\n 조건 하나당 실행시간 :', (datetime.now() - 조건별_시작시간).total_seconds())
                    cond_cnt+=1
                    #return None

                    k+=1
                j+=1
            i+=1

        print('\n 총 조건 {}개의 실행시간 :'.format(cond_cnt-1), (datetime.now() - 시작시간).total_seconds())

class ClusterLoader:
    """
    방법.1 : 클러스터TBL_로딩
    방법.2 : 타겟자료로 검색해서 그에 대응하는 원본자료를 덧붙인다.
    """
    def XX_클러스터_검색로딩(clst_tbl=None, clst_col=None, algorithm=None, sampling=None, n_clusters=None, meta_only=False):
        """
        clst_df = ML.cluster.XX_클러스터_검색로딩(clst_tbl=clst_tbl, clst_col=clst_col, algorithm=algorithm, sampling=sampling, n_clusters=n_clusters)
        clst_df = ML.cluster.XX_클러스터_검색로딩(clst_tbl='뉴스_ETRI언어분석', clst_col='뉴스본문srl_WSDNNGli', algorithm='KMeans', sampling=10000, n_clusters=2000)
        """
        query = {}
        if clst_tbl is not None: query.update({'clst_tbl':clst_tbl})
        if clst_col is not None: query.update({'clst_col':clst_col})
        if algorithm is not None: query.update({'algorithm':algorithm})
        if sampling is not None: query.update({'sampling':sampling})
        if n_clusters is not None: query.update({'n_clusters':n_clusters})
        #query = {'clst_tbl':clst_tbl, 'clst_col':clst_col, 'algorithm':algorithm, 'sampling':sampling, 'n_clusters':n_clusters}
        #print('\n 훈련자료의 조건 :')
        #pp.pprint(query)

        projection = {'KeyidLabel_dicli':0} if meta_only==True else None
        df = mg.find(db명=DB명, tbl명=TBL명, query=query, projection=projection, 컬럼순서li=[], df보고형태='df')

        if len(df) is not 0:
            df = df.drop_duplicates(subset=['clst_tbl','clst_col','algorithm','sampling','n_clusters'], keep='last')
        print('\n df.dtypes :\n', df.dtypes)
        print(df)
        return df

    def 다중타겟_다중조건_별_클러스터_결과_비교분석용_로딩():
        df = XX_클러스터_검색로딩(clst_tbl=None, clst_col=None, algorithm=None, sampling=None, n_clusters=None)
        df = KeyidLabel_dicli_json_normalize(df)
        return df

    def XX_클러스터_id검색로딩(clst_id, meta_only=False):
        """
        clst_id : 객체. ObjectId('5b952d6bdc958f4c8d0f0a7a')
        from bson.objectid import ObjectId
        """
        query = {'클러스터id':clst_id}
        projection = {'KeyidLabel_dicli':0} if meta_only==True else None
        clf_df = mg.find(db명=DB명, tbl명=CLST_TBL, query=query, projection=projection, 컬럼순서li=[], df보고형태='df')
        return clf_df

    def Trainset_로딩(clst_tbl, clst_col, algorithm, sampling, n_clusters):

        """
        XX_클러스터_검색로딩 -> clst_df
        클러스터_결과를_json_normalize -> clsted_df
        클러스터된_원본자료_로딩 -> df
        원본자료에_라벨을_결합 -> train_df
        unclustered_원본자료를_로딩 -> test_df

        ===== 사용법 =====
        train_df, 클러스터id, test_df = ML.cluster.Trainset_로딩(clst_tbl='뉴스_ETRI언어분석', clst_col='뉴스본문srl_WSDNNGli', algorithm='KMeans', sampling=10000, n_clusters=2000)
        """
        clst_df = XX_클러스터_검색로딩(clst_tbl, clst_col, algorithm, sampling, n_clusters, meta_only=False)
        dicli = clst_df.to_dict('records')
        d = dicli[0]


        clsted_df = KeyidLabel_dicli_json_normalize(clst_df).loc[:, ['keyid', 'label']]
        """
        ============================== 클러스터된_원본자료_로딩 ==============================
        """
        print('\n' + '= '*30 + '클러스터된_원본자료_로딩')
        keyid_li = list(clsted_df['keyid'])
        query = {d['key_col']:{'$in':keyid_li}}
        projection = {'_id':0, d['key_col']:1, d['clst_col']:1}
        df = mg.find(db명=DB명, tbl명=d['clst_tbl'], query=query, projection=projection, 컬럼순서li=[], df보고형태='df')
        print('\n df.dtypes :\n', df.dtypes)
        pp.pprint({'len(df)':len(df)})
        # 테이블 Handler 처리 대상 표시
        if len(df) == 0:
            query = {'_id':d['_id']}
            update = {'$set':{'키컬럼_문제발생TF':True}}
            mg.update_one(db명=DB명, tbl명=TBL명, query=query, update=update, upsert=False)
        else:
            print(len(df))
        #return None

        """
        ============================== 원본자료에_라벨을_결합 ==============================
        keyid명을 '뉴스id'명으로 변경해야되나? 말아야되나? -> keyid로 모두 통일
        """
        print('\n' + '= '*30 + '원본자료에_라벨을_결합')
        train_df = df.join(clsted_df.set_index('keyid'), on=d['key_col'])
        print('\n train_df.dtypes :\n', train_df.dtypes)
        pp.pprint({'len(train_df)':len(train_df)})
        if dbg_on == False: print('\n train_df.iloc[:1,] :\n',train_df.iloc[:1,])
        """
        ============================== clst_col_dtype_검사조작 ==============================
        """
        print('\n' + '= '*30 + 'clst_col_dtype_검사조작')
        FirstValue_dtype = type(list( train_df[clst_col] )[0])
        pp.pprint({'clst_col_1st_value_dtype':FirstValue_dtype})
        if FirstValue_dtype is str:
            pass
        elif FirstValue_dtype is list:
            s = datetime.now()
            train_df[clst_col] = train_df[clst_col].apply(lambda x: ' '.join(x))
            pp.pprint({'실행시간_sec':(datetime.now() - s).total_seconds()})
        else:
            print('\n clstclst_col의 값은 문자열/리스트 여야 한다.\n')
        """
        ============================== unclustered_원본자료를_로딩 ==============================
        불필요한듯?

        분류기를 대비한 방어코드 -> d['clst_col']:{'$ne':None}
        print('\n' + '= '*30 + 'unclustered_원본자료를_로딩')
        keyid_li = list(clst_df['keyid'])
        query = {d['key_col']:{'$nin':keyid_li}, d['clst_col']:{'$ne':None}}
        projection = {'_id':0, d['key_col']:1, d['clst_col']:1}

        test_df = mg.find(db명=DB명, tbl명=d['clst_tbl'], query=query, projection=projection, 컬럼순서li=[], df보고형태='df')
        print('\n test_df.dtypes :\n', test_df.dtypes)
        pp.pprint({'len(test_df)':len(test_df)})
        """
        return train_df

    def KeyidLabel_dicli_json_normalize(df):
        """
        XX_클러스터TBL의 KeyidLabel_dicli을 json_normalize 한다. 이때, 메타컬럼을 선택적으로 선택할 수 있다.
        기본 컬럼 : keyid, label
        추가 컬럼 :

        df : XX_클러스터 테이블에서 로딩한 df.

        meta_cols_선택
        ### _id 생성 원인
        : 뉴스TBL 이외의 다른 TBL의 경우 _id 컬럼도 저장되어 있다. Join을 위해 여기서 삭제한다.
        """

        col_li = list(df.columns)
        col_li.remove('KeyidLabel_dicli')
        col_li.remove('_id')
        pp.pprint({'meta_cols':col_li})

        dicli = df.to_dict('records')
        clst_df = json_normalize(data=dicli, record_path='KeyidLabel_dicli', meta=col_li, meta_prefix=None, record_prefix=None, errors='raise', sep='.')
        print('\n clst_df.dtypes :\n', clst_df.dtypes)
        pp.pprint({'len(clst_df)':len(clst_df)})
        return clst_df

class Handler:

    def XX_클러스터TBL의_KeyidLabel_dicli의_id명을_keyid로_변경():
        """
        뉴스 테이블로부터 파생된 다른 테이블의 경우, _id와 뉴스id 를 둘다 저장하고 있다.
        따라서 _id 를 keyid로 모두 변경해서는 안된다.
        """
        def _id를_뉴스id로_변경(dicli):
            df = pd.DataFrame(dicli)
            df = df.rename(columns={'뉴스id':'keyid'})
            dicli = df.to_dict('records')
            return dicli


        업뎃col명 = 'KeyidLabel_dicli'
        변경할col명 = '뉴스id'
        수정후col명 = 'keyid'

        query = {'KeyidLabel_dicli':{'$elemMatch': {'뉴스id':{'$ne':None}} }}
        projection = {'_id':1, 업뎃col명:1}
        df = mg.find(db명=DB명, tbl명=TBL명, query=query, projection=projection, 컬럼순서li=[], df보고형태='df')
        #print(df[업뎃col명])
        print(df)
        #print(len(df))
        """
        중간 점검
        df = json_normalize(data=dicli9, record_path='key_col_label_dicli', meta=None, meta_prefix=None, record_prefix=None, errors='raise', sep='.')
        print(len(df))
        df = df.rename(columns={'_id':'뉴스id'})
        dicli91 = df.to_dict('records')
        print(dicli91[0])
        """
        return None
        df[업뎃col명] = df[업뎃col명].apply(_id를_뉴스id로_변경)
        print(df)
        #print( list(df['KeyidLabel_dicli'])[0][0] )
        dicli = df.to_dict('records')
        for d in dicli:
            query = {'_id':d['_id']}
            update = {'$set':{업뎃col명:d[업뎃col명]}}
            mg.update_one(db명=DB명, tbl명=TBL명, query=query, update=update, upsert=False)

class ClusterAnalyzer:

    def 뉴스제목본문_클러스터의__label_그룹핑개수__보고(clst_col='뉴스제목_요약label'):
        """
        grouped_cnt_byLabel
        clst_col : XXlabel 컬럼명
        """
        query = {clst_col:{'$exists':True}}
        projection = {'_id':0, '뉴스id':1, clst_col:1}
        df = Cluster.뉴스제목본문_클러스터_로딩(query=query, projection=projection)

        g = df.groupby(clst_col).count().sort_values('뉴스id', ascending=False)
        print(g)
        return g

    def 클러스터된_컬럼들_간의_일치여부를_검사(clst_col_li=['뉴스제목label','뉴스제목_요약label'], 퍼센트자릿수=1):
        """
        클러스터된 컬럼들 간의 일치여부를 검사한다.
        일단 두개의 변수만 비교. 3개 이상은 고민해봐라.
        """
        query ={}
        for e in clst_col_li:
            query[e] = {'$exists':True}

        projection = {'_id':0, '뉴스id':1}
        for e in clst_col_li:
            projection[e] = 1

        pp.pprint({'query':query, 'projection':projection})

        df = Cluster.뉴스제목본문_클러스터_로딩(query=query, projection=projection)

        col0 = clst_col_li[0]
        col1 = clst_col_li[1]


        df['뉴스제목_lab일치'] = df[col0].eq(df[col1], level=None, fill_value=None, axis=0)
        df_T = df[ df['뉴스제목_lab일치']==True ]
        df_F = df[ df['뉴스제목_lab일치']==False ]
        df_T_len = len(df_T)
        df_F_len = len(df_F)
        rpt = {
            'len(df_T)':df_T_len,
            'len(df_F)':df_F_len,
        }
        rpt1 = mthr.구성비_비율_보고(n1=df_T_len, n2=df_F_len, portion명='일치율', 소수점자릿수=4, 퍼센트자릿수=퍼센트자릿수)
        rpt.update(rpt1)
        print('\n'+'*'*60+inspect.stack()[0][3])
        pp.pprint(rpt)
        df = df_T.sort_values(col0)
        print(df)
        return df

class Analyzer:

    def 다중타겟_다중조건_별_클러스터_결과_비교():
        import ML
        #import __matplotlib as mpl


        df = ML.cluster.다중타겟_다중조건_별_클러스터_결과_비교분석용_로딩()
        df1 = 클러스터알고리즘별_표준편차_비교분석(df)
        print(df1.dtypes)

    def 클러스터알고리즘별_표준편차_비교분석(df, 독립변수=['sampling', 'n_clusters', 'clst_col'], 뷰어변수='algorithm'):
        """
        독립변수=['sampling', 'n_clusters', 'clst_col']
        """
        grouped = df.groupby(독립변수)
        grouped_len = len(grouped)
        i=1
        dicli = []
        for n, g in grouped:
            print('\n' + '-'*60 + '{}/{}, 독립변수:{}'.format(i, grouped_len, n))
            g = g.assign(keyid_cnt= 1)
            g = g.fillna(0)
            pvt = pd.pivot_table(data=g, values='keyid_cnt', index='label', columns=뷰어변수, aggfunc='sum', fill_value=None, margins=False, dropna=True, margins_name='All')
            #print(pvt.describe())
            dscb = pvt.describe()
            dscb = dscb.T
            std = dscb['std']
            std = std.to_dict()
            #print(std)
            corr = pvt.corr()
            print(corr)

            dic = {}
            for j in range(len(독립변수)):
                dic[독립변수[j]] = n[j]
            dic.update(std)
            #print(dic)
            dicli.append(dic)
            """
            CHAPTER = '클러스터-분류기'
            SUB_CHAPTER = '클러스터 결과에 대한 해석'
            title = 'label별  id 개수 분포 ({}:{}, {}:{}, {}:{})'.format(독립변수[0], n[0], 독립변수[1], n[1], 독립변수[2], n[2])
            f_path = TFM_DATA_PATH + CHAPTER + SUB_CHAPTER + '/' + title
            #mpl.단일창_단일다중_선그래프(df=pvt, title=title, figsize=(10,4))
            #mpl.simple_histo(n_bins, x=pvt[''], f_path)
            """
            i+=1
            #break
        df1 = pd.DataFrame(dicli)
        dicli = df1.to_dict('records')
        mg.insert_many(db명=DB명, tbl명=inspect.stack()[0][3], dicli=dicli)
        return df1

class Reporter:

    def 클러스터알고리즘별_표준편차_비교_scatterplot_3D():
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

        df = mg.find(db명=DB명, tbl명='클러스터알고리즘별_표준편차_비교분석', query=None, projection=None, 컬럼순서li=[], df보고형태='df')
        df = df.assign(std_sum= lambda x: x.KMeans + x.MiniBatchKMeans)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        X = 'KMeans'
        Y = 'MiniBatchKMeans'
        Z = 'sampling'

        # For each set of style and range settings, plot n random points in the box
        # defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
        """
        clst_cols = list(df['clst_col'].unique())
        clst_col_num = list(range(len(clst_cols)))
        clst_col_dic = {col:num for col, num in zip(clst_cols, clst_col_num)}
        #print(clst_col_dic)
        clst_col_df = pd.DataFrame({
            'clst_col_':list(df['clst_col'].unique()),
            'color':['r', 'g', 'b', 'y', 'c'],
            'marker':['o', '^', 's', '*', '+'],
        })
        """

        colors = ['r', 'g', 'b', 'y', 'c']
        markers = ['o', '^', 's', '*', '+']
        grouped = df.groupby('clst_col')
        #dicli = df.to_dict('records')
        grouped_len = len(grouped)
        i=0
        for n, g in grouped:
        #for d in dicli:
            print('\n' + '-'*60 + '{}/{}, n:{}'.format(i, grouped_len, n))
            """
            df1 = g.copy()
            df1 = df1.assign(color= lambda x: clst_col_dic[x.clst_col])
            df1 = df1.assign(marker= lambda x: clst_col_dic[x.clst_col])
            g = g.join(clst_col_df.set_index('clst_col_'), on='clst_col')
            """
            print(g)

            xs = list(g[X])
            ys = list(g[Y])
            zs = list(g[Z])
            scales = list(g['n_clusters'])
            print('scales :\n', scales)
            scales = [e / 10 for e in scales]
            #scales = [math.log10(e) * 10 for e in scales]
            print('scales :\n', scales)
            c = colors[i]
            m = markers[i]
            ax.scatter(xs, ys, zs, zdir='z', s=scales, c=c, marker=m)
            i+=1

        ax.set_xlabel(X + '_std')
        ax.set_ylabel(Y + '_std')
        ax.set_zlabel(Z)

        df = Translator.term_translator(df)
        ax.legend(labels=list(df['clustered_column'].unique()), loc='upper right', bbox_to_anchor=(1, 1), fontsize='x-small')
        plt.show()

    def Create_2D_bar_graphs_in_different_planes(Xs, Ys, Zs):
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.pyplot as plt
        import numpy as np
        """
        # Generate the random data for the y=k 'layer'.
        xs = np.arange(20)
        ys = np.random.rand(20)
        """

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        colors = ['r', 'g', 'b', 'y', 'c']
        yticks = [4, 3, 2, 1, 0]
        for c, k in zip(colors, yticks):
            print('\n' + '-'*60 + 'c:{}, k:{}'.format(c, k))
            # Generate the random data for the y=k 'layer'.

            print('bar_left : {}\n'.format(len(Xs)), Xs)

            print('bar_height {}:\n'.format(len(Ys)), Ys)

            # You can provide either a single color or an array with the same length as
            # xs and ys. To demonstrate this, we color the first bar of each set cyan.
            cs = [c] * len(Xs)

            # Plot the bar graph given by xs and ys on the plane y=k with 80% opacity.
            ax.bar(left=Xs, height=Ys, zs=k, zdir='y', color=cs, alpha=0.8)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # On the y axis let's only label the discrete values that we have data for.
        ax.set_yticks(yticks)

        plt.show()
