from inews import *
from inews.etri import *

import unittest
import copy
from ilib import ifile
import json

def main():
    unittest.main()

#@unittest.skip("showing class skipping")
class LangAnalysisTestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test__init(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        la = LangAnalysis()
        self.assertEqual(la.url, "http://aiopen.etri.re.kr:8000/WiseNLU")
        self.assertEqual(la.access_key, "8393a2fc-eb89-4bf3-993f-a35f9df007a0")

    #@unittest.skip("demonstrating skipping")
    def test__api__invalid_text(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        la = LangAnalysis().api('')
        self.assertEqual(la, None)

    @unittest.skip("demonstrating skipping")
    def test__api__saving_jsonfile(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        filepath = "/Users/sambong/pjts/inews/data/sample_article.txt"
        text = ifile.open_file(filepath)
        rjson = LangAnalysis().api(text)
        # rjson 데이터타입 검증?
        # save in jsonfile.
        text = json.dumps(rjson)
        filepath = "/Users/sambong/pjts/inews/data/sample_article.json"
        ifile.write_file(filepath, text)
