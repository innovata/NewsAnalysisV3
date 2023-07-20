
from inews.base import models, journalists, dbg
from inews.base.libs import idatetime
from bs4 import BeautifulSoup
import copy
import re
from datetime import timezone, timedelta
import pandas as pd
from urllib.parse import urlparse
from pymongo import ASCENDING, DESCENDING
import inspect
import pprint
pp = pprint.PrettyPrinter(indent=2)


#============================================================

#============================================================


class SnapshotParser(models.NewsPageSnapshot):

    pressname = '네이버'
    pagename = '모바일홈'

    def __init__(self):
        super().__init__(self.pressname, self.pagename)

    def parsing_docs(self):
        cursor = self.tbl.find(filter={
                    'rawdata':{'$ne':None}, 'data':None
                }).sort('snapshot_dt', DESCENDING)
        return list(cursor)

    def parse(self, docs):
        for d in docs:
            lay = SnapshotPageLayoutParser(self.pressname, self.pagename)
            lay.parse(rawdata=d['rawdata'])
            # update = {'$set':{'data':lay.docs}}
            # self.tbl.update_one(filter={'_id':d['_id']}, update=update, upsert=True)
        return self


class SnapshotPageLayoutParser(models.SnapshotPageLayout):

    # 네이버-모바일홈 만의 특수한 컬럼들 추가.
    addi_schema = ['data_area', 'data_class', 'data_clk', 'data_gdid', 'data_rank']

    def __init__(self, pressname, pagename):
        super().__init__(pressname, pagename)
        self.schema += self.addi_schema
        self.docs = []

    def parse(self, rawdata):
        soup = BeautifulSoup(rawdata, 'html.parser')

        self.chartype_newslist(soup)
        self.thumnail_newslist(soup)
        dbg.clsdict(cls=self)
        return self

    def chartype_newslist(self, soup):
        """문자형뉴스리스트_영역배치"""
        self.screen_order = 1
        self.section_name = '문자형 뉴스리스트'
        self.section_order = 1
        s = soup.find(class_='uio_text')
        return self.atags(s)

    def thumnail_newslist(self, soup):
        """썸네일뉴스_영역배치"""
        self.screen_order = 2
        self.section_name = '썸네일형 뉴스리스트'
        self.section_order = 2
        s = soup.find(class_='uio_thumbnail')
        return self.atags(s)

    def atags(self, soup):
        whoiam = f"{__name__}.{self.atags.__qualname__}"
        try:
            a_tags = soup.find_all('a')
            for i, a in enumerate(a_tags):
                self.article_order = i+1
                for string in a.stripped_strings:
                    self.article_name = string
                # 네이버만의 용어(href,class,etc)명 변경.
                self.article_url = a.attrs['href']
                self.data_class = list(a.attrs['class'])
                self.data_area = a.attrs['data-area']
                self.data_clk = a.attrs['data-clk']
                self.data_gdid = a.attrs['data-gdid']
                self.data_rank = a.attrs['data-rank']
                self.schematize()
                self.docs.append(self.doc.copy())
        except Exception as e:
            print(f"{'#'*50} {whoiam}\nException : {e}")
        return self
