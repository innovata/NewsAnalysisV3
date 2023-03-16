from inews.base import newspage, dbg
import unittest
import inspect
import pprint
pp = pprint.PrettyPrinter(indent=2)



#@unittest.skip("test")
class NewsPageCollectorTestCase(unittest.TestCase):

    def setUp(self):
        self.cls = newspage.NewsPageCollector()

    @dbg.utestfunc
    def test00__setUp(self):
        dbg.clsdict(cls=self.cls)

    # @unittest.skip("test")
    @dbg.utestfunc
    def test01__dedup(self):
        df = self.cls.dedup()
        dbg.printdf(df=df, slen=5)
        print(df)

    @unittest.skip("test")
    @dbg.utestfunc
    def test__collect(self):
        pageshot = Collector()
        pageshot.collect()


if __name__ == "__main__":
    unittest.main()
