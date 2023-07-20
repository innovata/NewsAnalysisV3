
<!-- #============================================================ -->
## Cluster
<!-- #============================================================ -->

### 1. 용어 정의.

    clst_tbl : 클러스터할 테이블명

    clst_col : 액션을 수행할 대상 컬럼명 --> 반드시 값이 문자열이어야 한다.

    key_col : id 이외에 키값으로 사용할 컬렴명. 예) 뉴스id

    타겟자료 : 타겟 테이블의 타겟 컬럼과 id

    clst_trgt_df : 클러스터할 df

    clst_df : XX_클러스터 테이블에 저장/로딩 할 df

    sampling : 샘플링 수

    n_clusters : 분류(카테고리, label)의 개수

    algorithm : 클러스터 알고리즘


### 2. 자료구조.

    id                  object

    clst_tbl               object

    key_col                object

    clst_col               object

    sampling              int64

    n_clusters            int64

    algorithm            object

    KeyidLabel_dicli     object

    실행시간sec             float64


### 3. 클러스터 방법

2가지.
- 1. 뉴스XX를 직접 클러스터
- 2. ETRI언어분석 결과중 명사만 추출해 요약문을 만들어 클러스터.

유사도를 어떻게 계산해서 숫자로 표현할 것인가? 일단 해봐?
- 사용된 단어의 매칭율

### 3. 고민할 문제

클러스터 알고리즘별 / 클러스터 시행시점별로 결과가 달라진다?? 헐?

### 4. 교훈

언어분석 파싱 결과인 리스트를 클러스터링을 위해 문자열로 변환해서 테이블에 저장할 필요 없다. 과정도 복잡하고.
아래 결과를 보면 속도가 그렇게 오래 걸리지 않는다.

"clst_ColValue_dtype_검사조작" 이함수를 참조해라.

    {'clst_ColValue_dtype': <class 'list'>}

    {'실행시간_sec': 0.009807}







<!-- #============================================================ -->
## Classifier.
<!-- #============================================================ -->

### 1. 용어 정의

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

    clf : classifier, 분류기

    clfed : 분류된

    clfing : 분류할

### 2. 자료구조 : 

#### 2.1 TBL 구조

    id            object  -> 분류id

    클러스터id -> trainsetid

    분류기_알고리즘       object

    KeyidPredict_dicli    object

    실험tbl명       object -> clfed_tbl, prdct_tbl

    실험col명       object -> clf_col


#### 2.2 자료구조

    실험tbl명 = '트위터_유저타임라인' -> 거의 고정

    실험col명 = 'text' -> 거의 고정

    분류기_알고리즘 = MultinomialNB, Perceptron, etc.

    분류예측값li
