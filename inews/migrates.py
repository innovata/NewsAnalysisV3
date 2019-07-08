
from inews import mongo, mongo1, models
import pandas as pd
import copy
import pprint
pp = pprint.PrettyPrinter(indent=2)
from urllib.parse import urlparse
import numpy as np
import idebug as dbg

def f():
    tbl = mongo1.db['뉴스_ETRI언어분석_원본']
    etri = models.ETRIAI('WiseNLU','srl')
    docids = etri.distinct(key='docid',filter={'colname':'bodytext','results':None})
    loop = dbg.Loop('뉴스_ETRI언어분석_원본',len(docids))
    for docid in docids:
        cursor = tbl.find({'뉴스id':docid},{'_id':0,'뉴스id':1,'뉴스본문srl_res':1})
        docs = list(cursor)
        if len(docs) is 1:
            d = docs[0]
            etri.modelnm = 'Article__네이버_모바일홈'
            etri.docid = d['뉴스id']
            etri.colname = 'bodytext'
            etri.results = d['뉴스본문srl_res']
            etri.update_doc({'modelnm':etri.modelnm,'docid':etri.docid,'colname':etri.colname},True)
        loop.report()

def snapshot():
    """."""

def sreen_tbl_schema():
    tbl = mongo1.db['screen']
    cursor = tbl.find({},{'_id':0}).limit(1)
    return pd.DataFrame(list(cursor))

def migrate_screen_tbl():
    """url별로 작업하기 위해 urls 리스트 로딩."""
    tbl = mongo1.db['screen']
    urls = tbl.distinct(key='url')
    loop = dbg.Loop('migrate_screen_tbl', len(urls))
    for url in urls:
        """url에 해당하는 pageid를 검색."""
        page = models.NewsPage().load({'url':url})
        if len(page.docs) is 1:
            page.attributize(page.docs[0])
            """screen-tbl에서 마이그할 대상 문서로딩."""
            cursor = tbl.find({'url':url},{'_id':0})
            scrdf = pd.DataFrame(list(cursor))
            cols_map = {'r_txt':'html','수집일시':'collect_dt'}
            scrdf = scrdf.rename(columns=cols_map).reindex(columns=['html','collect_dt'])
            """Snapshot-tbl에 마이그."""
            ss = models.NewsPageSnapshot(page.pressname, page.name)
            ss.docs = scrdf.to_dict('records')
            for d in ss.docs:
                ss.attributize(d)
                ss.update_doc({'collect_dt':ss.collect_dt},True)
        loop.report(addi_info=url)

def anlyze_newspage_urls():
    tbl = mongo1.db['screen']
    urls = tbl.distinct(key='url')
    len(urls)
    mh = mongo.ModelHandler()
    mh.schema = ['protocol','uri','path','params','query','fragment']
    for url in urls:
        u = urlparse(url)
        mh.protocol = u.scheme
        mh.uri = u.netloc
        mh.path = u.path
        mh.params = u.params
        mh.query = u.query
        mh.fragment = u.fragment
        mh.schematize()
        mh.docs.append(mh.doc.copy())

    df = pd.DataFrame(mh.docs)
    return df.groupby(['uri','path']).count().sort_values('protocol')

def divide_NewsPageSnapshot():
    tbl = mongo.db['NewsPageSnapshot']
    """url별로 작업하기 위해 urls 리스트 로딩."""
    page = models.NewsPage()
    page.load()
    loop = dbg.Loop('divide_NewsPageSnapshot', len(page.docs))
    for d in page.docs:
        """pageid에 해당하는 snapshot 데이터 로딩."""
        page.attributize(d)
        cursor = tbl.find({'pageid':page._id},{'_id':0,'collect_dt':1,'html':1})
        """newspage마다 테이블로 분할된 데이터모델에 로딩한 데이터를 저장."""
        ss = models.NewsPageSnapshot(page.pressname, page.name)
        ss.docs = list(cursor)
        for d in ss.docs:
            ss.attributize(d)
            ss.update_doc({'collect_dt':ss.collect_dt},True)
        loop.report(addi_info=page.url)

tbl = mongo.db['Article__네이버']
cursor = tbl.find().limit(1)
pd.DataFrame(list(cursor))
tbl.rename('Article__네이버__')
sorted(mongo.db.list_collection_names())



docs = list(cursor)
len(docs)
tbl = mongo.db['Article__네이버']
#tbl.insert_many(docs)
cursor = tbl.find({},{'_id':1})
docs = list(cursor)
len(docs)
