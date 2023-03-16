
from inews.base import mongo
import pandas as pd
import inspect
import pprint
pp = pprint.PrettyPrinter(indent=2)
from pandas.io.json import json_normalize


#============================================================
"""Baseline."""
#============================================================

def category(df, cate_cols):
    for col in cate_cols:
        df[col] = df[col].astype('category')
    return df


#============================================================
"""뉴스페이지 & 기사."""
#============================================================


class NewsPage(mongo.Model):

    schema = ['url','name','pressname']
    id_cols = schema.copy()

    def __init__(self):
        self.modeling(cls=__class__)

    def identify(self, **kwargs):
        whoiam = f"{__name__}.{self.identify.__qualname__}"
        filter = {k:v for k,v in kwargs.items()}
        cursor = self.tbl.find(filter).limit(1)
        try:
            self.attributize(list(cursor)[0])
            return self
        except Exception as e:
            print(f"{'#'*50} {whoiam}\nException : {e}")
            pp.pprint(locals())
            raise


class NewsPageSnapshot(mongo.Model):
    """html-text를 layout-json으로 파싱."""
    # schema = ['snapshot_dt','html','layout']
    schema = ['snapshot_dt','rawdata','data']
    dataschema = []
    cate_cols = ['article_category']

    def __init__(self, pressname, pagename):
        page = NewsPage().identify(pressname=pressname, name=pagename)
        self.submodeling(cls=__class__, modelsuffix=f"{page.pressname}_{page.name}")
        self.pageid = page._id
        self.pageurl = page.url

    def jndf(self, filter={}):
        whoiam = f"{__name__}.{self.jndf.__qualname__}"
        filter.update({'data':{'$ne':None}})
        cursor = self.tbl.find(filter=filter, projection={'snapshot_dt':1, 'data':1})
        try:
            df = json_normalize(list(cursor), 'data', ['snapshot_dt']).sort_values('snapshot_dt')
            df.index = range(len(df))
            return category(df=df, cate_cols=self.cate_cols)
        except Exception as e:
            print(f"{'#'*50} {whoiam}\nException : {e}")


class SnapshotPageLayout(mongo.Model):

    schema = ['snapshot_dt','screen_order','section_name','section_order','article_name','article_order','article_url']

    def __init__(self, pressname, pagename):
        page = NewsPage().identify(pressname=pressname, name=pagename)
        self.submodeling(cls=__class__, modelsuffix=f"{page.pressname}_{page.name}")

    def change_dtype(self, df):
        df.section_order = df.section_order.astype(dtype='int64', copy=True, errors='raise')
        df.article_order = df.article_order.astype(dtype='int64', copy=True, errors='raise')
        return df


class Article(mongo.Model):

    def __init__(self, pressname):
        self.schema = ['url','html','snapshot_dt','pagename',
                        'headline','bodytext','pressname','journalistname','published_dt','revised_dt','issuetitle']
        self.submodeling(modelsuffix=pressname)
        self.pressname = pressname


#============================================================
# ETRI AI API.
#============================================================


class ETRIAI(mongo.Model):

    def __init__(self, targetmodel, targetcol, techname, apicode):
        self.schema = ['techname','apicode','docid','results']
        self.submodeling(modelsuffix=f"{targetmodel}_{targetcol}")
        self.attributize_flocals(inspect.currentframe())


#============================================================
# 언론사/인.
#============================================================


class Press(mongo.Model):

    def __init__(self, **kwargs):
        self.modeling()
        self.attributize(kwargs)
        self.schema = ['name','url','logo_url']


class Journalist(mongo.Model):

    def __init__(self, **kwargs):
        self.modeling()
        self.attributize(kwargs)
        self.schema = ['pressname','name','email','naver_jcard_url']


class NaverArticleComment(mongo.Model):

    def __init__(self, **kwargs):
        self.modeling()
        self.attributize(kwargs)


#============================================================
# 정치인 소셜네트워크.
#============================================================


class Assemblymen(mongo.Model):

    def __init__(self):
        self.modeling()
        self.schema = ['chinese_name','english_name','korean_name','photo_url','elected_cnt','region','partyname']


#============================================================
# Libs.
#============================================================
