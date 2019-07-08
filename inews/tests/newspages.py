from inews import *
from inews.newspages import *

import unittest
import copy

def main():
    unittest.main()

#@unittest.skip("showing class skipping")
class CollectorTestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test__init(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        pageshot = Collector()
        pageshot.pageid = 'idid'
        pageshot.collect_dt = 'today'
        pageshot.html = 'HTML'
        pageshot.schematize()
        dbg.obj(pageshot)

    #@unittest.skip("demonstrating skipping")
    def test__collect(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        pageshot = Collector()
        pageshot.collect()
