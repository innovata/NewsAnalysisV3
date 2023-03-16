import unittest
import inspect
import re


from inews.base import mongo
from inews.lib import dbg


class ModuleTestCase(unittest.TestCase):

    def setUp(self):
        pass

    @dbg.utestfunc
    def test01__db(self):
        self.assertTrue(hasattr(mongo, 'client'))
        self.assertTrue(hasattr(mongo, 'db'))
        self.assertEqual(mongo.dbname, 'inews')


# @unittest.skip("test")
class ModelTestCase(unittest.TestCase):

    companyname = '삼성전자'
    companycode = '123456'

    def setUp(self):
        class SampleModel(mongo.Model):
            def __init__(self):
                pass
        self.cls = SampleModel()

    @dbg.utestfunc
    def test00__setUp(self):
        pass

    @dbg.utestfunc
    # @unittest.skip("test")
    def test01__modeling(self):
        self.cls.modeling(cls=self.cls.__class__)
        dbg.clsdict(cls=self.cls)
        self.assertEqual(self.cls.modelname, 'SampleModel')
        self.assertTrue(hasattr(self.cls, 'tbl'))

    @dbg.utestfunc
    # @unittest.skip("test")
    def test02__submodeling(self):
        self.cls.submodeling(cls=self.cls.__class__, modelsuffix=f"{self.companyname}_{self.companycode}")
        dbg.clsdict(cls=self.cls)
        self.assertEqual(self.cls.modelname, 'SampleModel_삼성전자_123456')
        self.assertTrue(hasattr(self.cls, 'tbl'))

    @dbg.utestfunc
    # @unittest.skip("test")
    def test03__attributize(self):
        self.cls.attributize(dic={'a':1,'b':2})
        dbg.clsdict(cls=self.cls)
        self.assertTrue(hasattr(self.cls, 'a'))
        self.assertTrue(hasattr(self.cls, 'b'))

    @dbg.utestfunc
    # @unittest.skip("test")
    def test04__attributize_flocals(self, p1=10, p2=20):
        self.cls.attributize_flocals(frame=inspect.currentframe())
        self.assertTrue(hasattr(self.cls, 'p1'))
        self.assertTrue(hasattr(self.cls, 'p2'))
        print(f"param1 : {self.cls.p1}\nparam2 : {self.cls.p2}")


# @unittest.skip("test")
class DatabaseHandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.cls = mongo.DatabaseHandler(dbname='inews')

    @dbg.utestfunc
    def test00__setUp(self):
        dbg.clsdict(cls=self.cls)

    @dbg.utestfunc
    def test01__list_collection_names(self):
        tbls = self.cls.list_collection_names()
        dbg.printiter(iterable=tbls, slen=50)

    @dbg.utestfunc
    @unittest.skip("critical")
    def test02__change_collection_names(self):
        self.cls.change_collection_names()


if __name__ == "__main__":
    unittest.main()
