

from inews import models
import requests
from bs4 import BeautifulSoup
import pandas as pd
import idebug as dbg
import inspect

import people as ppl
from twitter import usertimeline
from pandas.io.json import json_normalize
import re



def 유저정보에_국회의원정보를_결합(dbg_on=False, return_type='all', 사전검증=False):
    """기초 데이터 로딩"""
    #pp.pprint({'ppl.assem.ASS_TBL명':ppl.assem.ASS_TBL명})
    projection = {'_id':0, '이름':1, '정당명':1}
    df1 = mg.find(db명=DB명, tbl명=ppl.assem.ASS_TBL명, query=None, projection=projection, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')
    #print(df1)

    #pp.pprint({'ppl.info.TBL명':ppl.info.TBL명})
    projection = {'_id':0, '이름':1, '직업':1}
    df2 = mg.find(db명=DB명, tbl명=ppl.info.TBL명, query=None, projection=projection, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')
    #print(df2)

    query = {'user_relation':'friend'}
    df = mg.find(db명=DB명, tbl명=TBL명, query=query, projection=None, dbg_on=dbg_on, 컬럼순서li=[], df보고형태='df')


    """트위터_유저TBL 기본청소"""
    df['json_dump'] = df['json_dump'].apply(lambda x: json.loads(x))
    df['json_dump'] = df['json_dump'].apply(lambda x: [x])
    dicli = df.to_dict('records')
    df = json_normalize(data=dicli, record_path='json_dump', meta=['수집일시', 'user_relation'], meta_prefix=None, record_prefix=None, errors='raise', sep='.')

    """불필요 컬럼 제거."""
    print(len(list(df.columns)))
    df = df.dropna(axis=1, how='any', thresh=None, subset=None, inplace=False)
    print(len(list(df.columns)))

    """
    print('\n'+'= '*30+'결합')
    국회의원현황TBL의 이름은 3글자인데, 트위터 이름은 사족이 많다.
    따라서 join 함수는 안 통한다.
    df = df.join(df1.set_index('이름'), on='name')
    #print(df.dtypes)
    """

    """트위터_유저 정보에 국회의원 이름이 regex 매치되면 정당명을 추가"""
    dicli_1 = df1.to_dict('records')
    dicli = df.to_dict('records')
    for d1 in dicli_1:
        for d in dicli:
            rs = re.search(pattern=d1['이름'], string=d['name'], flags=0)
            if rs is None:
                pass
            else:
                d['정당명'] = d1['정당명']
                d['직업'] = '국회의원'

    df = pd.DataFrame(dicli)
    #print(df.dtypes)
    #print(list(df['정당명'].unique()))

    """트위터_유저 정보에 인물정보의 이름이 regex 매치되면 직업을 추가"""
    dicli_2 = df2.to_dict('records')
    dicli = df.to_dict('records')
    for d2 in dicli_2:
        for d in dicli:
            rs = re.search(pattern=d2['이름'], string=d['name'], flags=0)
            if rs is None: pass
            else: d['직업'] = d2['직업']

    df = pd.DataFrame(dicli)
    #print(df.dtypes)

    """직업별 인원수 분포현황보고"""
    df9 = df.fillna(value={'직업':'_None'}, method=None, axis=None, inplace=False, limit=None, downcast=None)
    g = df9.groupby('직업').count().sort_values('name', ascending=False)
    g = g.loc[:,['name']]
    print(g)


    """트위터 수집할 타겟 name | screen_name 과 추가된 정보를 저장"""
    df0 = df.loc[:,['name','screen_name','정당명','직업']]
    #df0 = df0.fillna(value='_None', method=None, axis=None, inplace=False, limit=None, downcast=None)
    df0 = df0.where((pd.notnull(df0)), None)
    #print(df0.dtypes)
    dicli_0 = df0.to_dict('records')
    mg.insert_many(db명=DB명, tbl명=usertimeline.CORE_TRGT_TBL, dicli=dicli_0, dbg_on=dbg_on, 사전검증=사전검증)


    """국회의원 / 비국회의원 분포현황보고"""
    df9 = df.fillna(value={'정당명':'_None'}, method=None, axis=None, inplace=False, limit=None, downcast=None)
    print(list(df9['정당명'].unique()))
    df91 = df9[ df9['정당명'] != '_None' ]
    df92 = df9[ df9['정당명'] == '_None' ]
    #df1 = df.query('정당명 != "_None" ')
    #df2 = df.query('정당명 = "_None" ')
    dic = {
        '총 유저 수':len(df9),
        '국회의원 df91 수':len(df91),
        '비국회의원 df92 수':len(df92),
    }
    pp.pprint(dic)
    #print('\n 비국회의원 이름 목록\n')
    #print(df92)
    #pp.pprint(sorted(df92['name']))


    if return_type == 'all': return df
    else: return df1, df2


class Collector:

    def __init__(self):
        
