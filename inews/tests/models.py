
from inews import *
from inews.models import *

import unittest
import copy
from ilib import ifile

def main():
    unittest.main()


#============================================================
# 뉴스페이지 & 기사.
#============================================================

@unittest.skip("test class skipping")
class NewsPageTestCase(unittest.TestCase):

    #pressname = '네이버'
    #name = 'MobileHome'
    #url = 'www.naver.com'
    #name = 'MobileNewsHome'
    #url = 'm.news.naver.com'
    pressname = '조선일보'
    name = 'Mobile home'
    url = 'http://m.chosun.com/'

    @unittest.skip("demonstrating skipping")
    def test__handler(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        newspage = NewsPage()
        filter = {}
        update = {'$rename':{'medianame':'pressname'}}
        newspage.update_many(filter, update)
        dbg.UpdateResult(newspage.UpdateResult)

    #@unittest.skip("demonstrating skipping")
    def test__init(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        newspage = NewsPage(pressname=self.pressname, name=self.name, url=self.url)
        self.assertEqual(newspage.tblname, 'NewsPage')
        self.assertEqual(newspage.schema, ['pressname','name','url'])
        self.assertEqual(set(list(newspage.doc)), {'pressname','name','url'})

    #@unittest.skip("demonstrating skipping")
    def test__save(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        newspage = NewsPage(pressname=self.pressname, name=self.name, url=self.url)
        filter = {'url':newspage.url}
        update = {'$set':newspage.doc}
        newspage.update_one(filter, update, True)
        newspage.load(filter)
        self.assertEqual(len(newspage.docs), 1)
        dbg.dframe(newspage.get_df(), self.name)

    #@unittest.skip("demonstrating skipping")
    def test__loadall(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        newspage = NewsPage().load()
        df = newspage.get_df().sort_values('pressname')
        dbg.dframe(df, 'All news pages.')

@unittest.skip("test class skipping")
class NewsPageTimeshotTestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test__init(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        pageshot = NewsPageTimeshot()
        self.assertEqual(pageshot.tblname, 'NewsPageTimeshot')

    @unittest.skip("demonstrating skipping")
    def test__generate(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        url = 'm.naver.com'
        page = NewsPage().load({'url':url}).docs[0]
        pageid = page['_id']
        collect_dt = datetime.now().astimezone()
        html = 'html'
        pageshot = NewsPageTimeshot(pageid=pageid, collect_dt=collect_dt, html=html)
        self.assertEqual(pageshot.tblname, 'NewsPageTimeshot')
        self.assertEqual(set(list(pageshot.doc)), {'pageid','collect_dt','html'})
        dbg.dics(pageshot.doc)

    @unittest.skip("demonstrating skipping")
    def test__load(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        pageshot = NewsPageTimeshot()
        pageshot.load()
        #dbg.docs(pageshot)

    #@unittest.skip("demonstrating skipping")
    def test__joinload__parsingTargets(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        pageshot = NewsPageTimeshot()
        pagefilter = {'url':'m.news.naver.com/home.nhn'}
        filter = {'parsed':None}
        pageshot.joinload(pagefilter=pagefilter, filter=filter)
        df = pageshot.get_df()
        dbg.dframe(df, 'join_df')

    #@unittest.skip("demonstrating skipping")
    def test__joinload__parsedTrue(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        pageshot = NewsPageTimeshot()
        pagefilter = {'url':'m.news.naver.com/home.nhn'}
        filter = {'parsed':True}
        pageshot.joinload(pagefilter=pagefilter, filter=filter)
        df = pageshot.get_df()
        dbg.dframe(df, 'join_df')

    #@unittest.skip("demonstrating skipping")
    def test__handler(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        pageshot = NewsPageTimeshot()
        filter = {}
        update = {'$unset':{'parsed':''}}
        pageshot.update_many(filter, update)

@unittest.skip("test class skipping")
class TimeshotArticlesLayoutTestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test__init(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        layout = TimeshotArticlesLayout()
        self.assertEqual(layout.tblname, 'TimeshotArticlesLayout')

    #@unittest.skip("demonstrating skipping")
    def test__load(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        layout = TimeshotArticlesLayout().load()
        dbg.dframe(layout.get_df(), 'layout')

@unittest.skip("test class skipping")
class ArticleTestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test__init(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        a = Article()
        self.assertEqual(a.tblname, 'Article')

    @unittest.skip("demonstrating skipping")
    def test__save_one_bodytext_in_file(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        a = Article().load({},{'_id':0,'bodytext':1})
        #dbg.docs(a)
        doc = a.docs[3]
        text = doc['bodytext']
        filepath = "/Users/sambong/pjts/inews/data/sample_article.txt"
        ifile.write_file(filepath, text)

#============================================================
# 기사 제목/본문.
#============================================================

@unittest.skip("test class skipping")
class ArticleBodytextTestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test__init__adddoc(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        ab = ArticleBodytext(articleid=None, apiname='LangAnalysis',method=None,analysis_result=None)
        self.assertEqual(ab.tblname, 'ArticleBodytext')
        #dbg.obj(ab)

    #@unittest.skip("demonstrating skipping")
    def test__init__load(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        ab = ArticleBodytext().load()
        self.assertEqual(ab.tblname, 'ArticleBodytext')
        df = ab.get_df()
        dbg.dframe(df, 'ArticleBodytext.df')

@unittest.skip("test class skipping")
class ArticleHeadlinetTestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test__schematize(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        h = ArticleHeadline()
        h.schema = ['articleid','headline','url']
        h.articleid = 'idid'
        h.headline = 'sample head'
        h.url = 'www.google.com'
        dbg.dic(h.schematize().doc)

    #@unittest.skip("demonstrating skipping")
    def test__reverse_schematize(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        h = ArticleHeadline()
        h.schema = ['articleid','headline','url']
        doc = {'articleid': 'idid', 'headline': 'sample head', 'url': 'www.google.com'}
        h.attributize(doc)
        dbg.obj(h)

#============================================================
# 언론사/인.
#============================================================

@unittest.skip("test class skipping")
class PressTestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test__init(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        #m = Press(name='naver', url='www.naver.com')
        m = Press()
        #dbg.obj(m)
        self.assertEqual(m.tblname, 'Press')
        m.name = 'daum'
        m.set_schema('new',['name','url']).schematize()
        m.set_schema('add',['logo']).schematize()
        m.set_schema('del',['name']).schematize()
        #dbg.obj(m)

    @unittest.skip("demonstrating skipping")
    def test__save(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        url = 'http://www.segye.com'
        m = Press(name='세계일보', url=url, logo_url='https://ssl.pstatic.net/mimgnews//image/upload/office_logo/022/2017/01/11/logo_022_6_20170111151211.jpg?20180823_143150')
        #dbg.dics(m.doc)
        filter = {'url':url}
        m.update_one(filter, {'$set':m.doc}, True)
        m.load(filter)
        self.assertEqual(len(m.docs), 1)
        dbg.docs(m)

    #@unittest.skip("demonstrating skipping")
    def test__load(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        m = Press().load()
        df = m.get_df().sort_values('name')
        df = df.reindex(columns=['name','englishname','url','logo_url'])
        #dbg.dframe(df)
        m.docs = df.to_dict('records')
        dbg.docs(m)
