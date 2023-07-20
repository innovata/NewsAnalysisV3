"""
============================== 핵심일 ==============================
클래스다.

===== 용어 정의 =====
훈련자료모음(훈련자료 + 그 분류값) 로딩 -> 뉴스XX와 그로부터 클러스터된 라벨, train_df
훈련자료 : trainset_data, train_docs
훈련분류 : label, target
훈련tbl명 : 클러스터(훈련된) 자료를 보유한 테이블명
훈련col명 : 클러스터(훈련된) 컬럼명
실험자료모음 : test_df
실험자료 : testset_data, test_docs
실험분류 : predicted
실험tbl명 : 분류예측할 자료가 존재하는 테이블명
실험col명 : 분류예측할 컬럼명

SP_TBL : spread_tbl
clf : classifier

===== 자료구조 : TBL 구조 =====
_id            object  -> 조건id
클러스터id -> trainset_id
분류기_알고리즘       object
KeyidPredict_dicli    object
실험tbl명       object
실험col명       object

===== 자료구조 : SP_TBL 구조 =====
_id          object
UTL_id       object  -> 훈련tbl명에 따라 변동
predicted     int64
조건id         object

TBL명 에는 여러 조건을 같이 저장할 때 쓰고,
SP_TBL명 에는 하나의 문서에 포함된 엄청난 데이터를 풀어헤쳐 놓는다.
이유는, 사건별(label / predicted)로 빠르게 로딩하기 위해서다.

===== 자료구조 =====
훈련자료tbl명='뉴스' -> 고정
훈련col명='뉴스제목'
훈련분류tbl명='뉴스_클러스터'
훈련분류col명 = 'label'
클러스터_알고리즘 = 'KMeans'

실험tbl명 = '트위터_유저타임라인' -> 거의 고정
실험col명 = 'text' -> 거의 고정
분류기_알고리즘 = MultinomialNB, Perceptron, etc.
분류예측값li
"""

# 프로젝트 라이브러리
from thenews.__lib__ import *
print('\n' + '# '*5 + sys.modules[__name__].__file__ + ' #'*5)
#doc#print(__doc__)

# 나의 패키지
import __pymongo as mg
import __sklearn as skl

# 오픈 패키지
import pandas as pd
from datetime import datetime

# 모듈 라이브러리
import News as news
import ML

# 전역변수
import News_
#TBL명 = '트위터_분류기_예측결과'
#SP_TBL명 = TBL명 + '_확장'



"""
============================== Classifier ==============================
"""
def News_Classifier(실험tbl명=News_.PARSED_TBL, key_col='_id', 실험col명='뉴스본문', 분류기_알고리즘='MultinomialNB', 훈련tbl명='뉴스_ETRI언어분석', 훈련col명='뉴스본문srl_WSDNNGli', algorithm='KMeans', sampling=10000, n_clusters=2000, dbg_on=False, 사전검증=False):
    import ML
    print('\n' + '='*60 + inspect.stack()[0][3])
    """
    "어떤 클러스터"를 사용한 "어떤 훈련자료"를 이용해서 "어떤 분류기"를 훈련시킨다.

    ===== 사용법 =====
    News_Classifier(실험tbl명=News_.PARSED_TBL, 실험col명='뉴스본문', 분류기_알고리즘='MultinomialNB', 훈련tbl명=None, 훈련col명=None, algorithm=None, sampling=None, n_clusters=None, dbg_on=False, 사전검증=False)
    News_Classifier(실험tbl명=News_.PARSED_TBL, key_col='_id' 실험col명='뉴스본문', 분류기_알고리즘='MultinomialNB', 훈련tbl명='뉴스_ETRI언어분석', 훈련col명='뉴스본문srl_WSDNNGli', algorithm='KMeans', sampling=10000, n_clusters=2000, dbg_on=False, 사전검증=False)
    훈련tbl명='뉴스_ETRI언어분석', 훈련col명='뉴스본문srl_WSDNNGli', algorithm='KMeans', sampling=10000, n_clusters=2000

    ===== 작업순서 =====
    실험자료 로딩
    머신러닝_분류기_호출
    """
    #
    #입력 = {'tbl명':tbl명, 'clst타겟col명':clst타겟col명, 'algorithm':algorithm, 'n_clusters':n_clusters}
    #


    #clst_df = ML.cluster.XX_클러스터_검색로딩(clst_tbl=훈련tbl명, clst_col=훈련col명, algorithm=algorithm, sampling=sampling, n_clusters=n_clusters, dbg_on=dbg_on)
    query = {실험col명:{'$ne':None}}
    projection = {'_id':1, 실험col명:1}
    test_df = mg.find(db명=DB명, tbl명=실험tbl명, query=query, projection=projection, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')
    ML.classifier.뉴스클러스터기준_분류(test_df=test_df, 실험tbl명=실험tbl명, key_col=key_col, 실험col명=실험col명, 분류기_알고리즘=분류기_알고리즘, 훈련tbl명=훈련tbl명, 훈련col명=훈련col명, algorithm=algorithm, sampling=sampling, n_clusters=n_clusters, dbg_on=dbg_on, 사전검증=사전검증)

    #test_df = 트위터_실험자료_로딩(실험tbl명, 실험col명)
    #ML.classifier.뉴스훈련자료기반_분류(test_df=test_df, 실험tbl명=실험tbl명, 실험col명=실험col명, 분류기_알고리즘=분류기_알고리즘, 훈련tbl명=훈련tbl명, 훈련col명=훈련col명, algorithm=algorithm, sampling=sampling, n_clusters=n_clusters, dbg_on=dbg_on, 사전검증=사전검증)

"""
============================== ClassifierAnalyzer ==============================
"""
def News_Predicted_df_결과저장(실험tbl명, 실험col명, 분류기_알고리즘, dbg_on=False):
    print('\n' + '='*60 + inspect.stack()[0][3])
    """
    ===== 사용법 =====
    News_Predicted_Orig_df로딩(test_tbl='뉴스', test_col='뉴스본문', clf_algorithm='MultinomialNB', dbg_on=False)

    clf_tbl='트위터_유저타임라인', clf_col='text'
    Predicted_Orig_df로딩(실험tbl명, 실험col명, 분류기_알고리즘, 클러스터id, dbg_on=False)
    """
    clf_df = ML.classifier.XX_분류_검색로딩(실험tbl명, 실험col명, 분류기_알고리즘, meta_only=True, dbg_on=dbg_on)
    clf_dicli = clf_df.to_dict('records')
    #d = clf_dicli[0]
    #print(d)
    clf_dicli_len = len(clf_dicli)
    i=1
    for d in clf_dicli:
        print('\n' + '-'*60 + '{}/{}'.format(i, clf_dicli_len))
        predicted_df, g = ML.classifier.Predicted_Orig_df로딩(실험tbl명=d['실험tbl명'], 실험col명=d['실험col명'], 분류기_알고리즘=d['분류기_알고리즘'], 클러스터id=d['클러스터id'], dbg_on=dbg_on)
        """
        ============================== 분류결과_저장 ==============================
        """
        print('\n' + '= '*30 + '분류결과_저장')
        cnt_col = list(g.columns)[0]
        report_dic = {
            'clf_id':d['_id'],
            'predicted_li':list(g.index),
            'predicted_cnt_li':list(g[cnt_col]),
        }
        print('\n report_dic :\n')
        if dbg_on == True: pp.pprint(report_dic)
        mg.insert_one(db명=DB명, tbl명=ML.classifier.CLF_REPORT_TBL, dic=report_dic, dbg_on=dbg_on, 사전검증=False)
        i+=1
        #break
"""
============================== ClassifierLoader ==============================
"""
def News_Predicted_Orig_df로딩(test_tbl='뉴스', test_col='뉴스본문', dbg_on=False):
    print('\n' + '='*60 + inspect.stack()[0][3])
    """
    clf_tbl명='트위터_유저타임라인', clf_col명='text'
    """
    df = ML.classifier.CLF_TBL자료에_CLST_TBL메타정보를_결합해서_df로딩(dbg_on=dbg_on)
    """
    핵심부분은, 어떠한 클러스터-분류기 조합을 선택하는 "dicli[?]" 부분이다.!!
    클러스터-분류기 조합에 따른 분류결과_분석보고.ipynb 를 참고해라
    """
    df = df[ df['실험col명']==test_col ]
    dicli = df.to_dict('records')

    if test_col == '뉴스본문':
        d = dicli[0]
    elif test_col == '뉴스제목':
        d = dicli[1]
    """"""
    predicted_news_df = ML.classifier.Predicted_Orig_df로딩(실험tbl명=d['실험tbl명'], 실험col명=d['실험col명'], 분류기_알고리즘=d['분류기_알고리즘'], 클러스터id=d['clst_id'], dbg_on=dbg_on)
    return predicted_news_df




if __name__ == '__main__':
    print('\n' + '='*60 + sys.modules[__name__].__file__)
    #pp.pprint({'sys.path':sys.path})
    pp.pprint({'dir()':dir()})

    #News_Classifier(실험tbl명=News_.PARSED_TBL, 실험col명='뉴스본문', 분류기_알고리즘='Perceptron', 훈련tbl명=None, 훈련col명=None, algorithm=None, sampling=None, n_clusters=None, dbg_on=False, 사전검증=False)
    #News_Predicted_df_결과저장(실험tbl명=News_.PARSED_TBL, 실험col명='뉴스본문', 분류기_알고리즘='Perceptron', dbg_on=False)
