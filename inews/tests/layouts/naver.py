from inews import *
from inews.layouts.naver import *

import unittest
import copy

def main():
    unittest.main()



@unittest.skip("showing class skipping")
class MobileHomeParserTestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test__get_targets(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        home = MobileHomeParser()
        pageshot = home.get_targets()
        df = pageshot.get_df()
        dbg.dframe(df, 'pageshot.df')

    #@unittest.skip("demonstrating skipping")
    def test__parse_save(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        home = MobileHomeParser()
        home.parse_save()
        dbg.dic(home.doc, 'MobileHomeParser.doc')

#@unittest.skip("showing class skipping")
class MobileNewsHomeParserTestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test__get_targets(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        newshome = MobileNewsHomeParser()
        pageshot = newshome.get_targets()
        df = pageshot.get_df()
        dbg.dframe(df, 'pageshot.df')

    #@unittest.skip("demonstrating skipping")
    def test__parse_save(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        newshome = MobileNewsHomeParser()
        newshome.parse_save()
        dbg.dframe(newshome.get_df(), 'MobileNewsHomeParser.df')
