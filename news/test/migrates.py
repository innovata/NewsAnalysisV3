from inews.base import *
from inews.migrates.migrates import *

import unittest
import copy

def main():
    unittest.main()



#@unittest.skip("showing class skipping")
class TestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test__show_tables(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        if True:
            oldmongo.db['함수실행로그'].drop()
        pp.pprint(sorted(oldmongo.db.list_collection_names()))

    @unittest.skip("demonstrating skipping")
    def test__press(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        p = Press()
        #p.load_old_docs()
        drop_old_tbl(p.old_table)

    @unittest.skip("demonstrating skipping")
    def test__journalist(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        j = Journalist()
        #j.load_old_docs()
        drop_old_tbl(j.old_table)
        j.load()
        df = j.get_df()
        dbg.dframe(df, 'Journalist.df')

    @unittest.skip("demonstrating skipping")
    def test__newspage(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        p = NewsPage()
        if False:
            p.load_old_docs()
            p.save()
        else:
            drop_old_tbl(p.old_table)
        df = p.load().get_df()
        dbg.dframe(df, '저장결과 확인 : NewsPage.df')

    #@unittest.skip("demonstrating skipping")
    def test__screen(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        clss = screen()
        dbg.obj(clss)
        if False:
            clss.find().explain_cursor()
