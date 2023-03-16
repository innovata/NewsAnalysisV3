
from inews.base.press import naver
from inews.base import dbg
import unittest
import pandas as pd
import copy



@unittest.skip("test")
class MobileHomeSnapshotParserTestCase(unittest.TestCase):

    def setUp(self):
        self.cls = naver.mhome.SnapshotParser()

    @dbg.utestfunc
    def test00__setUp(self):
        dbg.clsdict(cls=self.cls)
        # cursor = self.cls.tbl.find()
        # dbg.printdf(df=pd.DataFrame(list(cursor)))

    @unittest.skip("test")
    @dbg.utestfunc
    def test01__parsing_docs(self):
        docs = self.cls.parsing_docs()
        dbg.printdf(df=pd.DataFrame(docs))

    # @unittest.skip("test")
    @dbg.utestfunc
    def test02__parse(self):
        docs = self.cls.parsing_docs()
        self.cls.parse(docs=docs)


# @unittest.skip("test")
class MobileNewsHomeSnapshotParserTestCase(unittest.TestCase):

    def setUp(self):
        self.cls = naver.mnewshome.SnapshotParser()

    @dbg.utestfunc
    def test00__setUp(self):
        dbg.clsdict(cls=self.cls)
        cursor = self.cls.tbl.find()
        dbg.printdf(df=pd.DataFrame(list(cursor)))
        
