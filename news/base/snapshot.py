import inspect
import pprint
pp = pprint.PrettyPrinter(indent=2)
from datetime import datetime, timezone, timedelta
import re
import sys
from urllib.parse import urlparse


import requests
import pandas as pd
from pandas.io.json import json_normalize


from inews.base import mongo, models, press, iter, dbg


def revise_pageurl(url):
    #p = re.compile(pattern='^http://|^https://')
    if re.search(pattern='^http[s]*://', string=url) is None:
        url = f"http://{url}"
    return url


class SnapshotCollector(models.NewsPageSnapshot):

    def __init__(self, pressname, pagename):
        super().__init__(pressname, pagename)

    @dbg.fruntime
    def fetch(self, timeout=20):
        whoiam = f"{__name__}.{self.fetch.__qualname__}"
        t = datetime.now().astimezone(timezone(timedelta(hours=+9)))
        snapshot_dt = datetime(t.year, t.month, t.day, t.hour, t.minute, t.second)
        pageurl = revise_pageurl(url=self.pageurl)
        try:
            res = requests.get(url=pageurl, timeout=timeout)
        except Exception as e:
            print(f"{'#'*50} {whoiam}\nException : {e}")
        else:
            if (res.status_code is 200) and (len(res.text) is not 0):
                self.tbl.insert_one(document={
                    'snapshot_dt':snapshot_dt,
                    'rawdata':res.text,
                })
            else:
                print(f"{'#'*50} {whoiam}\nlocals() :")
                pp.pprint(locals())

    @dbg.fruntime
    def change_colnm(self):
        update = {'$rename':{'layout':'data', 'html':'rawdata'}}
        UpdateResult = self.tbl.update_many(filter={}, update=update, upsert=False)
        pp.pprint(UpdateResult.raw_result)


@dbg.fruntime
def change_colnm(pageurl):
    newspage = models.NewsPage().identify(url=pageurl)
    ss = SnapshotCollector(newspage.pressname, newspage.name)
    ss.change_colnm()


@dbg.fruntime
def change_colnm_iterurls(initurl=None):
    iter.pageurls(f=change_colnm, initurl=initurl)


@dbg.fruntime
def fetch(pageurl):
    newspage = models.NewsPage().identify(url=pageurl)
    ss = SnapshotCollector(newspage.pressname, newspage.name)
    ss.fetch()


@dbg.fruntime
def fetch_iterurls(initurl=None):
    iter.pageurls(f=fetch, initurl=initurl)



#============================================================
"""Common Analyzer API."""
#============================================================


class Analyzer:

    def __init__(self, pressname, pagename):
        self.pressname = pressname
        self.pagename = pagename
        self.df = get_df_with_unique_aritcle_urls(pressname, pagename)
        self.navtag_cols = ['data_clk','data_area','data_gdid','data_rank','data_class']


def get_df_with_unique_article_urls(pressname, pagename):
    snapshot = models.NewsPageSnapshot(pressname, pagename)
    df = snapshot.jnload()
    if df is not None:
        return df.sort_values(['article_url','snapshot_dt']).drop_duplicates(keep='first',subset=['article_url'])


#============================================================
"""Analyzer."""
#============================================================


class ArticleUrlAnalyzer(Analyzer):
    """article_url 분포."""
    def __init__(self, pressname, pagename):
        super().__init__(pressname, pagename)
        self.unq_article_urls = list(df.article_url)
        self.structuring_urls()

    def structuring_urls(self):
        mh = mongo.ModelHandler()
        mh.schema = ['protocol','uri','path','params','query','fragment']
        for url in self.unq_article_urls:
            u = urlparse(url)
            mh.protocol = u.scheme
            mh.uri = u.netloc
            mh.path = u.path
            mh.params = u.params
            mh.query = u.query
            mh.fragment = u.fragment
            mh.docs.append(mh.schematize().doc.copy())
        self.df = pd.DataFrame(mh.docs).reindex(columns=mh.schema)
        return self

    def group_report(self, colname):
        return self.df.groupby(colname).count()


#aua = ArticleUrlAnalyzer('네이버','모바일홈')


class LayoutOccupancyAnalyzer(Analyzer):
    """
    화면배치 위치점유시간.
    첫화면에 배치된 뉴스들이 특정 위치점유시간 분석 : 분석저장
    페이지별, 화면내 위치별, 각 주제/href의 위치점유시간 분석
    언론사별_화면배치비중
    첫화면에 배치된 뉴스들의  언론사별 구성비, 성향별 구성비
    """
    def __init__(self):
        super().__init__(pressname, pagename)
        self.loc_cols = ['screen_order','section_name','section_order','article_order']
        self.cols_order1 = self.loc_cols + ['article_name','article_url'] + ['snapshotID','snapshot_dt']
        self.cols_order2 = ['snapshot_dt'] + self.loc_cols + ['article_name','article_url'] + ['snapshotID']
        self.cols_order3 = ['snapshot_dt','occupancy_sec'] + self.loc_cols + ['article_name','article_url'] + ['snapshotID']

    def counts_per_location(self):
        return self.df.groupby(self.loc_cols).count()

    def calc_occupancy_time(self):
        docs = []
        for n, g in self.df.groupby(loc_cols):
            dics = g.sort_values('snapshot_dt').to_dict('records')
            for i, d in enumerate(dics):
                d1 = dics[i]
                if i+1 < len(dics):
                    d2 = dics[i+1]
                    d1['occupancy_sec'] = (d2['snapshot_dt'] - d1['snapshot_dt']).total_seconds()
                docs.append(d1)
        return pd.DataFrame(docs).reindex(columns=self.cols_order3).sort_values('occupancy_sec',ascending=False)


#============================================================
"""."""
#============================================================


class ResErrorAnalyzer:
    """
    화면배치_원본TBL에서 r_txt에 대한 에러를 분석한다.
    에러의 종류가 무엇인지
    어떻게하면 회피할 수 있는지 다룬다.
    같은 URL, 같은 위치에 대해
    동일한 위치에서 뉴스가 변경되는 주기를 찾는다.
    화면배치 분석 시, 반드시 Layout_ParserRestorer.py를 참조.
    """
    def restriction_by_naver(self, pat='검색 서비스 이용이 제한되었습니다.'):
        return df[ df.html.str.contains(pat=pat, case=False, flags=re.IGNORECASE, na=None, regex=True) ]
