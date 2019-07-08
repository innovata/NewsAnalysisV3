
from inews import *
from inews.tests.new_layout import *

import unittest
import copy



@unittest.skip("showing class skipping")
class YouTubeTestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test__download_audio(self):
        print(f"\n{'='*60}\n test_funcname : {inspect.stack()[0][3]}\n")
        y = YouTube()
        url = 'https://www.youtube.com/watch?v=tQYxANatre0&frags=pl%2Cwn'
        path = '/Users/sambong/Downloads'
        filename = '정__영턱스클럽.mp3'
        y.download_audio(url, path, filename)

@unittest.skip("showing class skipping")
class WebStreamingTestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test__download_audio(self):
        print(f"\n{'='*60}\n test_funcname : {inspect.stack()[0][3]}\n")
        url = 'http://vod3.kocw.net/media/v2/lec/2015/first_term/hanyang_erica/hanheechang/1-1.mp4'
        filepath = '/Users/sambong/Downloads/hanheechang.mp4'
        ws = WebStreaming()
        ws.download_video(url, filepath)


def main():
    unittest.main()
