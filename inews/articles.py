
import os
os.getcwd()
import sys
sys.path.append("/Users/sambong/pjts/inews/env/lib/python3.7/site-packages")
sys.path.append("/Users/sambong/pjts/libs/i-nlp")
sys.path.append("/Users/sambong/pjts/libs/idebug")
sys.path
#%env GOOGLE_AUTH_PATH=/Users/sambong/pjts/libs/igoogle/igoogle-auth.json
#%env ETRI_ACCESS_KEY=8393a2fc-eb89-4bf3-993f-a35f9df007a0
import pprint
pp = pprint.PrettyPrinter(indent=2)


from inews import mongo, models, snapshots, etri, press
import pandas as pd
import requests
from datetime import datetime, timezone, timedelta
import re
from pandas.io.json import json_normalize
import inspect
import idebug as dbg
import sys
import copy
import inlp
from nltk import word_tokenize
from nltk.tokenize import TweetTokenizer

#============================================================
"""Collector."""
#============================================================

class Collector(models.Article):

    def __init__(self, pressname, pagename):
        super().__init__(pressname)
        self.pagename = pagename

    def get_targets(self):
        """스냅샷에서 유일한 url을 가진 df로딩."""
        df = snapshots.get_df_with_unique_article_urls(self.pressname, self.pagename)
        if df is not None:
            """기 수집된 article_url을 로딩한 후 수집타겟에서 제외."""
            collected_urls = self.distinct(key='url')
            TF = df.article_url.isin(collected_urls)
            article_urls = list(df[~TF].article_url)
            target_urls = self.filter_urls(article_urls)
            return target_urls

    def filter_urls(self, article_urls):
        """예외처리 : 기사가 아닌 URL은 제거."""
        p1 = re.compile(pattern='^http[s]*://m\.search\.naver\.com/search\.naver\?')
        """ '임시'예외처리 : aritlce_url 중 이상하게 파싱된 애들 제거."""
        p2 = re.compile(pattern='^http:/r')
        """ 'http(s)//'가 미포함이면 강제로 추가."""
        p3 = re.compile(pattern='^http[s]*://')

        target_urls = article_urls.copy()
        for url in article_urls:
            if p1.search(string=url) is not None:
                target_urls.remove(url)
            if p2.search(string=url) is not None:
                target_urls.remove(url)
            if p3.search(string=url) is None:
                print(f"\n 'http(s)//'가 미포함이면 강제로 추가 :\n url : {url}")
                target_urls.remove(url)
                target_urls.append(f"https://{url}")
        return target_urls

    def collect(self):
        target_urls = self.get_targets()
        if target_urls is not None:
            loop = dbg.Loop(f"{self.__class__} | {inspect.stack()[0][3]}", len(target_urls))
            for url in target_urls:
                self.url = url
                try:
                    r = requests.get(self.url)
                except Exception as e:
                    print(f"\n Exception :\n{e}\n")
                else:
                    if (r.status_code is 200) and (len(r.text) is not 0):
                        self.html = r.text
                        self.update_doc({'url':self.url}, True)
                    else:
                        print(f"\n{'#'*60}\n 네이버에서 이상감지를 한 듯.")
                        dbg.obj(r, f"{self.__class__} | {inspect.stack()[0][3]}")
                loop.report(addi_info=f" url : {self.url}")

def collect(pressname=None, pagename=None):
    fr = dbg.Function(inspect.currentframe()).report_init()
    filter = {}
    if isinstance(pressname,str) and isinstance(pagename,str):
        filter.update({'pressname':pressname, 'name':pagename})
    page = models.NewsPage().load(filter)
    loop = dbg.Loop(f"{sys.modules[__name__].__file__} | {inspect.stack()[0][3]}", len(page.docs))
    for d in page.docs:
        page.attributize(d)
        c = Collector(page.pressname, page.name)
        c.collect()
        loop.report(addi_info=f" pressname : {page.pressname}, pagename : {page.name}")
    fr.report_fin()

def parse():
    fr = dbg.Function(inspect.currentframe()).report_init()
    press.naver.parse_articles()

#============================================================
"""Analyzer."""
#============================================================

class ETRIAIAnalysisCollector(models.ETRIAI):
    """techname : etri module's class name."""
    def __init__(self, pressname, targetcol, techname='LangAnalysis', apicode='srl'):
        self.article = models.Article(pressname)
        super().__init__(self.article.tblname, targetcol, techname, apicode)
        self.choose_etriapi()

    def choose_etriapi(self):
        if self.techname is 'LangAnalysis':
            self.etriapi = etri.LangAnalysis(self.apicode)
        elif self.techname is 'LexicalRelationAnalysis':
            self.etriapi = etri.LexicalRelationAnalysis(self.apicode)
        else:
            print(f"\n Your techname({self.techname}) is invalid.")
        if hasattr(self, 'etriapi'):
            self.techname = self.etriapi.techname
        return self

    def get_targets(self):
        fr = dbg.Function(inspect.currentframe()).report_init()
        """기존 ETRIAIAnalysis 완료된 docids 로딩."""
        docids = self.distinct('docid')
        """Article-모델에서 분석할 타겟 로딩."""
        filter = {'_id':{'$nin':docids}, self.targetcol:{'$ne':None}}
        projection = {'_id':1, self.targetcol:1}
        self.article.load(filter,projection)
        fr.report_fin()
        return self

    def collect(self):
        self.get_targets()
        if hasattr(self, 'article'):
            article = copy.copy(self.article)
            loop = dbg.Loop(f"{self.__class__} | {inspect.stack()[0][3]}", len(article.docs))
            for d in article.docs:
                article.attributize(d)
                self.docid = article._id
                jsondata = self.etriapi.api(text=getattr(article, self.targetcol))
                if isinstance(jsondata, dict):
                    self.results = [jsondata]
                    self.update_doc({'docid':self.docid}, True)
                loop.report(addi_info=f" 기사 {self.targetcol} 일부 : {getattr(article, self.targetcol)[:30]}")

    def report_status(self):
        print(f"{'*'*60}\n{self.__class__} | {inspect.stack()[0][3]}")
        allIDs = self.article.distinct('_id',None)
        print(f" models.Article id_len : {len(allIDs)}")

        docids = self.distinct('docid')
        print(f" ETRI 분석완료된 id_len : {len(docids)}")

        filter = {'_id':{'$nin':docids}, self.targetcol:{'$ne':None}}
        _ids = self.article.distinct('_id',filter)
        print(f" ETRI 분석 안된 id_len : {len(_ids)}")

        validIDs = self.distinct('_id', {'results':{'$elemMatch':{'sentence':{'$ne':None}}}})
        print(f" results에 sentence가 있는 id_len : {len(validIDs)}")

self = ETRIAIAnalysisCollector('네이버', 'headline', techname='LangAnalysis', apicode='srl')
self.report_status()




def collect_etri_analysis(pressname='네이버', targetcol='bodytext', techname='LangAnalysis', apicode='srl'):
    fr = dbg.Function(inspect.currentframe()).report_init()
    etric = ETRIAIAnalysisCollector(pressname, targetcol, techname, apicode)
    etric.collect()
    fr.report_fin()

#collect_etri_analysis(pressname='네이버', targetcol='headline')

class Analyzer(models.Article):

    def __init__(self, pressname, targetcol, techname='LangAnalysis', apicode='srl'):
        super().__init__(pressname)
        self.handle_flocals(inspect.currentframe())

    def tokenize(self):
        fr = dbg.Function(inspect.currentframe()).report_init()
        method = 'morp'
        type_regex = '^NN[GP]'
        self.load(None,{'_id':1, self.targetcol:1})
        fr.report_fin()
        #fr.report_fin(addi_info=" self.load(None,{'_id':1, self.targetcol:1}) 에 걸린시간.")
        for d in self.docs:
            self.attributize(d)
            df = etri.load_result(self.submodel, self.targetcol, self.techname, self.apicode, self._id, method, type_regex)
            if df is None:
                print("\n df is None.")
            else:
                d['tokens'] = list(df.lemma)
        fr.report_fin()
        return self

#"""
self = Analyzer('네이버', 'headline', techname='LangAnalysis', apicode='srl')
self.tokenize()
#"""

#============================================================
"""Handler."""
#============================================================

class Deduplicator(models.Article):

    def __init__(self, pressname):
        super().__init__(pressname)

    def deduplicate(self):
        func = dbg.Function(inspect.currentframe()).report_init()
        df = self.load().get_df()
        func.report_fin(addi_info=" self.load().get_df()에 걸린시간.")
        if len(df) is 0:
            print("\n len(df) is 0.")
        else:
            TF = df.sort_values(['url','snapshot_dt']).duplicated(keep='first',subset=['url'])
            df1 = df[TF]
            if len(df1) is 0:
                print("\n len(duplicated_df) is 0.")
            else:
                self.delete_many({'_id':{'$in':list(df1)}})
            func.report_fin()

def deduplicate(pressname='네이버'):
    dup = Deduplicator(pressname)
    dup.deduplicate()
