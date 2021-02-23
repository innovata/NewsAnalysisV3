
import pandas as pd


TBL = '번역사전'



# 변수-영어 번역사전
"""
dictionary = {
    'predicted_li':'predicted',
    'predicted_cnt_li':'object_count_by_predicted',
    'predicted_num':'number_of_predicted',
    '실험tbl명':'test_table',
    '실험col명':'test_column',
    '분류기_알고리즘':'clf_alorithm',
    '실행시간sec':'run_time(sec)',
    'n_clusters':'number_of_clusters',
    'sampling':'number_of_sampling',
    'clst_tbl':'clustered_table',
    'clst_col':'clustered_column',
    'algorithm':'clst_algorithm',
    '뉴스':'News',
    '뉴스본문':'news body',
    '뉴스제목':'news title',
    '뉴스_ETRI언어분석':'News analyzed by ETRI lang API',
    '뉴스제목srl_WSDNNGli':'news title containing only nouns',
    '뉴스본문srl_WSDNNGli':'news body containing only nouns',
    '뉴스본문srl_WSDNNGli_중복제거':'news body containing only deduplicated nouns',
    '트위터_유저타임라인':'twitter_UserTimeline',
    '트위터_홈타임라인':'twitter_HomeTimeline',
}
"""
def 번역사전_통합로딩():
    """개발중
    """
    projection = {'_id':0}
    dicli = mg.find(db명=DB명, tbl명='번역사전', query=None, projection=projection, dbg_on=False, 컬럼순서li=[], df보고형태='dicli')
    dictionary = dicli[0]

    query = {'언론사명':{'$ne':None}, '언론사영문명':{'$ne':None}}
    projection = {'_id':0, '언론사명':1,'언론사영문명':1}
    dicli1 = mg.find(db명=DB명, tbl명='언론사', query=query, projection=projection, dbg_on=False, 컬럼순서li=[], df보고형태='dicli')
    dic_li = []
    for d in dicli1:
    #    print(d)
        dic = {d['언론사명']:d['언론사영문명']}
        dic_li.append(dic)
    dictionary1 = {}
    for e in dic_li:
        dictionary1.update(e)

    dictionary.update(dictionary1)
    return dictionary

def dictionary_updator(dictionary):
    update = {'$set':dictionary}
    mg.update_many(db명=DB명, tbl명='번역사전', query={}, update=update, upsert=True, dbg_on=False, 사전검증=False)


def dictionary_loader():
    df = mg.find(db명=DB명, tbl명='번역사전', query=None, projection=None, dbg_on=False, 컬럼순서li=[], df보고형태='df')
    dictionary = df.T[0].to_dict()
    return dictionary

# 용어 번역
def column_term_translator(df, dictionary):
    dic_keys = list(dictionary.keys())
    cols = list(df.columns)
    for col in cols:
        if col in dic_keys:
            df = df.rename(columns={col:dictionary[col]})
    return df

def index_term_translator(df, dictionary):
    dic_keys = list(dictionary.keys())
    if df.index.name in dic_keys:
        df.index.name = dictionary[df.index.name]
    return df

def value_term_translator(x, dictionary):
    dic_keys = list(dictionary.keys())
    if x in dic_keys:
        return dictionary[x]
    else:
        return x

def term_translator(df):
    dictionary = dictionary_loader()
    df = column_term_translator(df, dictionary)
    df = index_term_translator(df, dictionary)
    df = df.applymap(lambda x: value_term_translator(x, dictionary))
    return df

def 언론사명_인덱스g를_번역(g):
    g['press_company_name'] = g.index
    g = term_translator(g)
    g.index = g['press_company_name']
    del(g['press_company_name'])
    return g
