from inews import *
from inews.press import *

import unittest
import copy

def main():
    unittest.main()

#@unittest.skip("showing class skipping")
class NaverPressInfoParserTestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test__init(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        p = NaverPressInfoParser()
        #dbg.obj(p)
        self.assertEqual(p.tblname, 'Press')
