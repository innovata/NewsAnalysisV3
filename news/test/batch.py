from inews.base import *
from inews.batch import *

import unittest
import copy

def main():
    unittest.main()

#@unittest.skip("showing class skipping")
class BatchTestCase(unittest.TestCase):

    @unittest.skip("demonstrating skipping")
    def test__minutes_job(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        minutes_job()

    #@unittest.skip("demonstrating skipping")
    def test__jobs(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        jobs()
