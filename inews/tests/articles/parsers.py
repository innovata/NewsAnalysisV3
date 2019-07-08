from inews import *
from inews.articles import *

import unittest
import copy


def main():
    unittest.main()


#@unittest.skip("showing class skipping")
class ArticleParserTestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test__init(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        n = naver.ArticleParser()
        #dbg.obj(n)
        self.assertEqual(n.tblname, 'Article')

    @unittest.skip("demonstrating skipping")
    def test__load_targets(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        n = naver.ArticleParser()
        n.load_targets()
        df = n.get_df()
        if len(df) is not 0:
            dbg.li(list(df.url), "articles' url", 100)
            df = df.reindex(columns=['parsed','url','html'])
            dbg.dframe(df, 'NaverArticleParser.df')

    #@unittest.skip("demonstrating skipping")
    def test__parse_save(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        n = naver.ArticleParser()
        n.parse_save()

@unittest.skip("showing class skipping")
class ArticleCommentCollectorTestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test__parse_querystring(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        acc = naver.ArticleCommentCollector()
        acc.parse_querystring()
