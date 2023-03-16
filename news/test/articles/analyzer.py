from inews.base import *
from inews.articles.analyzer import *

import unittest
import copy


def main():
    unittest.main()

#@unittest.skip("showing class skipping")
class BodytextAnalysisCollectorTestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test__init(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        b = BodytextAnalysisCollector(apiname='LangAnalysis')
        self.assertEqual(b.tblname, 'ArticleBodytext')
        self.assertTrue(isinstance(b.doc, dict))
        self.assertTrue(isinstance(b.etriapi, object))
        dbg.obj(b)

    #@unittest.skip("demonstrating skipping")
    def test__already_analyzed_articleid(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        b = BodytextAnalysisCollector()
        articles = b.already_analyzed_articleid()
        dbg.li(articles)

    #@unittest.skip("demonstrating skipping")
    def test__get_targets(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        b = BodytextAnalysisCollector()
        article = b.get_targets()
        df = article.get_df()
        self.assertEqual(set(list(df.columns)), set(['_id','bodytext']))
        dbg.dframe(article.get_df(), 'BodytextAnalysisCollector.df')
        if len(df) is not 0:
            dbg.li(list(df.bodytext), shown_cnt=105)

    #@unittest.skip("demonstrating skipping")
    def test__req_langanalysis(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        """소스코드 변경
        jsondata = {'dummy':'jsondata'}
        jsondata = True
        """
        apiname='LangAnalysis'
        method='srl'
        b = BodytextAnalysisCollector(apiname=apiname,method=method)
        b.req_langanalysis()
        #dbg.dic(b.doc, 'BodytextAnalysisCollector.doc')
        self.assertTrue(b.doc['apiname'], apiname)
        self.assertTrue(b.doc['method'], method)
        # 에러 jsondata 에 대해.
        if True:
            self.assertTrue(isinstance(b.doc['articleid'], object))
            self.assertTrue(isinstance(b.doc['analysis_result'], list))
        else:
            self.assertTrue(b.doc['analysis_result'], True)
