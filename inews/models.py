
from inews import mongo
import pandas as pd
import inspect
from pandas.io.json import json_normalize
import idebug as dbg


#============================================================
"""뉴스페이지 & 기사."""
#============================================================

def submodeling(obj, *args):
    submodel = "_".join(args)
    obj.submodel = f"{obj.modelname}__{submodel}"
    obj.tblname = obj.submodel
    return obj

class NewsPage(mongo.Model):

    def __init__(self, **kwargs):
        super().__init__(__class__)
        self.attributize(kwargs)
        self.schema = ['_id','url','name','pressname']

class NewsPageSnapshot(mongo.Model):
    """html-text를 layout-json으로 파싱."""
    def __init__(self, pressname, pagename):
        super().__init__(__class__)
        self = submodeling(self, pressname, pagename)
        self.handle_flocals(inspect.currentframe())
        self.schema = ['_id','snapshot_dt','html','layout']
        self.set_newspage_info()

    def set_newspage_info(self):
        page = NewsPage().load({'name':self.pagename, 'pressname':self.pressname})
        if len(page.docs) is 1:
            page.attributize(page.docs[0])
            self.pageurl = page.url
            self.pageid = page._id
        return self

    def jnload(self, filter={}):
        fr = dbg.Function(inspect.currentframe()).report_init()
        filter.update({'layout':{'$ne':None}})
        self.load(filter, {'html':0})
        fr.report_fin()
        if len(self.docs) is 0:
            print("\n len(self.docs) is 0.\n")
        else:
            return json_normalize(self.docs, 'layout', ['_id','snapshot_dt']).rename(columns={'_id':'snapshotID'})

class PageLayout(mongo.ModelHandler):

    def __init__(self, html):
        super().__init__()
        self.html = html
        self.schema = ['screen_order','section_name','section_order','article_name','article_order','article_url']

    def change_dtype(self, df):
        df.section_order = df.section_order.astype(dtype='int64', copy=True, errors='raise')
        df.article_order = df.article_order.astype(dtype='int64', copy=True, errors='raise')
        return df

class Article(mongo.Model):

    def __init__(self, pressname):
        super().__init__(__class__)
        self = submodeling(self, pressname)
        self.handle_flocals(inspect.currentframe())
        self.schema = ['url','html','snapshot_dt','pagename',
            'headline','bodytext','pressname','journalistname','published_dt','revised_dt','issuetitle']

#============================================================
# ETRI AI API.
#============================================================

class ETRIAI(mongo.Model):

    def __init__(self, targetmodel, targetcol, techname, apicode):
        super().__init__(__class__)
        self = submodeling(self, targetmodel, targetcol)
        self.handle_flocals(inspect.currentframe())
        self.schema = ['techname','apicode','docid','results']

#============================================================
# 언론사/인.
#============================================================

class Press(mongo.Model):

    def __init__(self, **kwargs):
        super().__init__(__class__)
        self.attributize(kwargs)
        self.schema = ['name','url','logo_url']

class Journalist(mongo.Model):

    def __init__(self, **kwargs):
        super().__init__(__class__)
        self.attributize(kwargs)
        self.schema = ['pressname','name','email','naver_jcard_url']

class NaverArticleComment(mongo.Model):

    def __init__(self, **kwargs):
        super().__init__(__class__)
        self.attributize(kwargs)

#============================================================
# 정치인 소셜네트워크.
#============================================================

class Assemblymen(mongo.Model):

    def __init__(self):
        super().__init__(__class__)
        self.schema = ['chinese_name','english_name','korean_name','photo_url','elected_cnt','region','partyname']

#============================================================
# Libs.
#============================================================
