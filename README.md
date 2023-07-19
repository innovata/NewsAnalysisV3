<!-- #============================================================ -->
# NewsAnalysis v3
<!-- #============================================================ -->

UPV 대학원 석사 졸업 논문 최종버전


<!-- #============================================================ -->
## Intro | 개요
<!-- #============================================================ -->






<!-- #============================================================ -->
## Algorithms used in this project 
<!-- #============================================================ -->

1. K-Means Clustering

2. MeansShift Clustering 

3. Linear Model Perceptron Classification 

    sklearn.linear_model.Perceptron




<!-- #============================================================ -->
## Packages.
<!-- #============================================================ -->

### ETRI

1. 일반정보
- Open API 서비스 : http://aiopen.etri.re.kr/service_api.php
    - 언어 분석 API
    - 어휘관계 분석 API
    - 질문 분석 API
    - 음성인식 API


- 말뭉치 공개 서비스 : http://aiopen.etri.re.kr/service_corpus.php

2. 어휘 정보 API (http://aiopen.etri.re.kr:8000/WiseWWN/Word)

    "argument": {
        "word": “YOUR_WORD”
    }

3. 어휘 관계분석 API (http://aiopen.etri.re.kr:8000/WiseWWN/WordRel)

    "argument": {
        “first_word”: “FIRST_YOUR_WORD”,
        “first_sense_id”: “FIRST_WORD_SENSE_ID”,#첫 번째 어휘의 의미 코드
        “second_word”: “SECOND_YOUR_WORD”,
        “second_sense_id”: “SECOND_WORD_SENSE_ID”#두 번째 어휘의 의미 코드
    }

4. 동음이의어 정보 API (http://aiopen.etri.re.kr:8000/WiseWWN/Homonym)

    "argument": {
        "word": “YOUR_WORD”
    }

5. 다의어 정보 API (http://aiopen.etri.re.kr:8000/WiseWWN/Polysemy)

    "argument": {
        "word": “YOUR_WORD”
    }

6. 언어 분석 API (http://aiopen.etri.re.kr/doc_language.php)


언어 분석 API는 요청된 자연어 문장의 분석된 결과를 JSON 형태의 Text 데이터로 반환합니다.

형태소 분석 : “morp”,

어휘의미 분석 (동음이의어 분석) : “wsd”

어휘의미 분석 (다의어 분석) : “wsd_poly”

개체명 인식 : “ner”

의존 구문 분석 : “dparse”

의미역 인식 : “srl”

분석 명 | 분석 코드 | 포함되는 내용

형태소 분속 | morp |	형태소 분석 결과

어휘의미 분석(동음이의어) | wsd | 형태소 분석 결과, 어휘의미 분석 결과 (동음이의어 분석)

(동음이의어에 대한 상세정보 조회는 동음이의어 정보 API 사용)

어휘의미 분석(다의어) | wsd_poly | 형태소 분석 결과, 어휘의미 분석 결과 (다의어 분석)

(다의어에 대한 상세정보 조회는 다의어 정보 API 사용)

개체명 인식 | ner | 형태소 분석 결과, 어휘의미 분석 결과 (동음이의어 분석), 개체명 인식 결과

의존 구문 분석 | dparse | 형태소 분석 결과, 어휘의미 분석 결과 (동음이의어 분석), 개체명 인식 결과, 의존 구문 분석 결과

의미역 인식 | srl | 형태소 분석 결과, 어휘의미 분석 결과 (동음이의어 분석), 개체명 인식 결과, 의존 구문 분석 결과, 의미역 인식 
결과

### 어휘관계분석_API [lexicalRelation_analysis_api]

http://aiopen.etri.re.kr/doc_language.php
