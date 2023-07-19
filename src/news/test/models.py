import unittest
import inspect
import pprint
pp = pprint.PrettyPrinter(indent=2)


import pandas as pd
from pandas.io.json import json_normalize


from inews.base import models
from inews.lib import dbg


#============================================================
# 뉴스페이지 & 기사.
#============================================================

# pressname = '네이버'
# pagename = '모바일홈'
# pageurl = 'http://m.naver.com'
pressname = '네이버'
pagename = '모바일뉴스홈'
pageurl = 'http://m.news.naver.com/home.nhn'
# pressname = '조선일보'
# pagename = 'Mobile home'
# pageurl = 'http://m.chosun.com/'



# @unittest.skip("test")
class NewsPageTestCase(unittest.TestCase):

    def setUp(self):
        self.cls = models.NewsPage()

    @dbg.utestfunc
    def test00__setUp(self):
        dbg.clsdict(cls=self.cls)
        self.assertEqual(self.cls.modelname, 'NewsPage')

    @dbg.utestfunc
    def test01__load(self):
        cursor = self.cls.tbl.find()
        dbg.printdf(df=pd.DataFrame(list(cursor)))

    @dbg.utestfunc
    # @unittest.skip("test")
    def test02__identify(self):
        self.cls.identify(url=pageurl)
        dbg.clsdict(cls=self.cls)
        self.assertEqual(self.cls.name, pagename)
        self.assertEqual(self.cls.url, pageurl)
        self.assertEqual(self.cls.pressname, pressname)

    @unittest.expectedFailure
    @dbg.utestfunc
    def test03__identify__no_existed_press(self):
        self.cls.identify(name='삼봉')


@unittest.skip("test")
class NewsPageSnapshotTestCase(unittest.TestCase):

    def setUp(self):
        self.pressname = pressname
        self.pagename = pagename
        self.cls = models.NewsPageSnapshot(pressname=self.pressname, pagename=self.pagename)

    @dbg.utestfunc
    def test00__setUp(self):
        dbg.clsdict(cls=self.cls)
        cursor = self.cls.tbl.find()
        dbg.printdf(df=pd.DataFrame(list(cursor)))

    @dbg.utestfunc
    def test01__init(self):
        modelsuffix = f"{self.pressname}_{self.pagename}".capitalize()
        self.assertEqual(self.cls.modelname, f"NewsPageSnapshot_{modelsuffix}")
        self.assertTrue(hasattr(self.cls, 'pageid'))
        self.assertFalse(hasattr(self.cls, 'pressname'))
        self.assertFalse(hasattr(self.cls, 'pagename'))
        self.assertFalse(hasattr(self.cls, 'pageurl'))

    # @unittest.skip("test")
    @dbg.utestfunc
    def test02__jndf(self):
        cursor = self.cls.tbl.find()
        df = self.cls.jndf(filter={})
        dbg.printdf(df=df)

    @unittest.skip("critical")
    @dbg.utestfunc
    def test03__handle(self):
        update = {'$rename':{'layout':'data', 'html':'rawdata'}}
        UpdateResult = self.cls.tbl.update_many(filter={}, update=update, upsert=False)
        pp.pprint(UpdateResult.raw_result)
        cursor = self.cls.tbl.find()
        dbg.printdf(df=pd.DataFrame(list(cursor)))


@unittest.skip("test")
class ArticleTestCase(unittest.TestCase):

    def setUp(self):

        self.pressname = '조선일보'
        self.a = models.Article(pressname=self.pressname)


    def test__init(self):

        self.assertEqual(self.a.modelname, f"Article__{self.pressname}")
        self.assertTrue(hasattr(self.a, 'pressname'))


#============================================================
# 기사 제목/본문.
#============================================================


@unittest.skip("test")
class ArticleBodytextTestCase(unittest.TestCase):

    # @unittest.skip("test")
    def test__init__adddoc(self):

        ab = ArticleBodytext(articleid=None, apiname='LangAnalysis',method=None,analysis_result=None)
        self.assertEqual(ab.modelname, 'ArticleBodytext')
        #dbg.obj(ab)

    # @unittest.skip("test")
    def test__init__load(self):

        ab = ArticleBodytext().load()
        self.assertEqual(ab.modelname, 'ArticleBodytext')
        df = ab.get_df()
        dbg.dframe(df, 'ArticleBodytext.df')


@unittest.skip("test")
class ArticleHeadlinetTestCase(unittest.TestCase):

    # @unittest.skip("test")
    def test__schematize(self):

        h = ArticleHeadline()
        h.schema = ['articleid','headline','url']
        h.articleid = 'idid'
        h.headline = 'sample head'
        h.url = 'www.google.com'
        dbg.dic(h.schematize().doc)

    # @unittest.skip("test")
    def test__reverse_schematize(self):

        h = ArticleHeadline()
        h.schema = ['articleid','headline','url']
        doc = {'articleid': 'idid', 'headline': 'sample head', 'url': 'www.google.com'}
        h.attributize(doc)
        dbg.obj(h)


#============================================================
# 언론사/인.
#============================================================


@unittest.skip("test")
class PressTestCase(unittest.TestCase):

    # @unittest.skip("test")
    def test__init(self):

        #m = Press(name='naver', url='www.naver.com')
        m = Press()
        #dbg.obj(m)
        self.assertEqual(m.modelname, 'Press')
        m.name = 'daum'
        m.set_schema('new',['name','url']).schematize()
        m.set_schema('add',['logo']).schematize()
        m.set_schema('del',['name']).schematize()
        #dbg.obj(m)

    @unittest.skip("test")
    def test__save(self):

        url = 'http://www.segye.com'
        m = Press(name='세계일보', url=url, logo_url='https://ssl.pstatic.net/mimgnews//image/upload/office_logo/022/2017/01/11/logo_022_6_20170111151211.jpg?20180823_143150')
        #dbg.dics(m.doc)
        filter = {'url':url}
        m.update_one(filter, {'$set':m.doc}, True)
        m.load(filter)
        self.assertEqual(len(m.docs), 1)
        dbg.docs(m)

    # @unittest.skip("test")
    def test__load(self):

        m = Press().load()
        df = m.get_df().sort_values('name')
        df = df.reindex(columns=['name','englishname','url','logo_url'])
        #dbg.dframe(df)
        m.docs = df.to_dict('records')
        dbg.docs(m)
