from inews.base import *
from inews.articles import *

import unittest
import copy


def main():
    unittest.main()

#@unittest.skip("showing class skipping")
class CollectorTestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test__init(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        c = Collector()
        self.assertEqual(c.tblname, 'Article')

    @unittest.skip("demonstrating skipping")
    def test__get_targets(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        c = Collector()
        layout = c.get_targets()
        #dbg.dics(layout, 'layout.docs')
        df = layout.get_df()
        #dbg.dframe(layout.get_df(), 'TimeshotArticlesLayout.df')
        if len(df) is not 0:
            dbg.li(list(df.article_url), shown_cnt=577)

    #@unittest.skip("demonstrating skipping")
    def test__collect(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        Collector().collect()
