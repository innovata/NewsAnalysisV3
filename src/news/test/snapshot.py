
from inews.base import snapshot, dbg, models
import unittest
import pandas as pd
from pymongo import ASCENDING, DESCENDING
import inspect
import pprint
pp = pprint.PrettyPrinter(indent=2)


pressname = '네이버'
pagename = '모바일뉴스홈'
pageurl = 'http://m.news.naver.com/home.nhn'


@unittest.skip("test")
class SnapshotCollectorTestCase(unittest.TestCase):

    def setUp(self):
        self.pressname = pressname
        self.pagename = pagename
        self.cls = snapshot.SnapshotCollector(self.pressname, self.pagename)

    @dbg.utestfunc
    def test00__setUp(self):
        dbg.clsdict(cls=self.cls)
        cursor = self.cls.tbl.find()
        dbg.printdf(df=pd.DataFrame(list(cursor)))

    @unittest.skip("critical")
    @dbg.utestfunc
    def test01__change_colnm(self):
        self.cls.change_colnm()
        print("\n검증 :\n")
        cursor = self.cls.tbl.find()
        dbg.printdf(df=pd.DataFrame(list(cursor)))

    # @unittest.skip("test")
    @dbg.utestfunc
    def test02__fetch(self):
        self.cls.fetch(timeout=20)
        print("\n검증 :\n")
        cursor = self.cls.tbl.find().sort(
                'snapshot_dt', DESCENDING).limit(1)
        dbg.printdf(df=pd.DataFrame(list(cursor)))

    @unittest.skip("test")
    @dbg.utestfunc
    def test__parse_save(self):
        home = MobileHomeParser()
        home.parse_save()
        dbg.dic(home.doc, 'MobileHomeParser.doc')


@unittest.skip("test")
class APIsTestCase(unittest.TestCase):

    def setUp(self):
        self.pressname = pressname
        self.pagename = pagename
        self.pageurl = pageurl

    @unittest.skip("test")
    @dbg.utestfunc
    def test01__change_colnm(self):
        snapshot.change_colnm(pageurl=self.pageurl)

    @unittest.skip("heavy_test")
    @dbg.utestfunc
    def test02__change_colnm_iterurls(self):
        snapshot.change_colnm_iterurls(initurl=None)

    # @unittest.skip("heavy_test")
    @dbg.utestfunc
    def test03__fetch_iterurls(self):
        snapshot.fetch_iterurls(initurl=None)


@unittest.skip("test")
class MobileNewsHomeParserTestCase(unittest.TestCase):

    #@unittest.skip("test")
    @dbg.utestfunc
    def test__get_targets(self):
        newshome = naver.MobileNewsHomeParser()
        pageshot = newshome.get_targets()
        df = pageshot.get_df()
        dbg.dframe(df, 'pageshot.df')

    #@unittest.skip("test")
    @dbg.utestfunc
    def test__parse_save(self):
        newshome = naver.MobileNewsHomeParser()
        newshome.parse_save()
        dbg.dframe(newshome.get_df(), 'MobileNewsHomeParser.df')


if __name__ == "__main__":
    unittest.main()
