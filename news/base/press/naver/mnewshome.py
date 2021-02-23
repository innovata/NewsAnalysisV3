"""
Mobile News Home
"""
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
    pagename = '모바일뉴스홈'

    def __init__(self):
        super().__init__(self.pressname, self.pagename)
        u = urlparse(self.pageurl)
        self.pageuri = f"{u.scheme}://{u.netloc}"

    def parsing_docs(self):
        cursor = self.tbl.find(filter={
                    'rawdata':{'$ne':None}, 'data':None
                }).sort('snapshot_dt', DESCENDING)
        return list(cursor)

    def parse(self, docs):
        for d in docs:
            lay = SnapshotPageLayoutParser(self.html, self.pageuri)
            self.update_doc({'_id':self._id}, True)
        return self


class SnapshotPageLayoutParser:

    def __init__(self, html, uri):
        super().__init__(html)
        self.uri = uri
        # 네이버-모바일-뉴스홈 만의 특수한 컬럼들 추가. : 많이 본 조회수, 네이버가 조회수 집계한 시간.
        self.addi_schema = ['article_category','viewed_cnt','totalized_time']
        self.schema += self.addi_schema

    def parse(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        """HTML 클래스-트리구조 : r_home_wrp _moreViewLinkArea / __persist_content / r_group _reset"""
        s = soup.find(class_='__persist_content')
        if s is not None:
            self.thumnail_text_section(s)
            self.mostviewed_section(s)
        return self

    def thumnail_text_section(self, soup):
        self.section_name = '썸네일-문자열타입 뉴스리스트'
        s1 = soup.find(class_='r_group_lft')
        if s1 is not None:
            self.screen_order = 1
            self.section_order = 1
            self.thumnail_text_newslists(s1)
        s2 = soup.find(class_='r_group_rgt')
        if s2 is not None:
            self.screen_order = 2
            self.section_order = 2
            self.thumnail_text_newslists(s2)
        return self

    def thumnail_text_newslists(self, soup):
        """개별 뉴스 파싱"""
        a_tags = soup.find_all('a', class_='r_news_drw')
        for i, a in enumerate(a_tags):
            self.article_order = i+1
            news_text = a.find('div', class_='r_news_tx')
            news_title = news_text.find('span', class_='r_news_tit')
            for string in news_title.stripped_strings:
                self.article_name = string
            self.article_url = f"{self.uri}/{a.attrs['href']}"
            self.docs.append(self.schematize().doc.copy())
        return self

    def mostviewed_section(self, soup):
        self.section_name = '많이 본 뉴스'
        self.screen_order = 3
        self.section_order = 3
        s = soup.find(class_='r_group_comp _popular')
        if s is not None:
            self.mostviewed_metadata(s)
            self.mostviewed_newslists(s)
        return self

    def mostviewed_metadata(self, soup):
        metadata = soup.find(class_="h2_area")
        meta_time = metadata.find('span',class_='h2_area_time').find('em')
        for string in meta_time.stripped_strings:
            self.totalized_time = None if len(string) is 0 else string
        return self.schematize()

    def mostviewed_newslists(self, soup):
        newslists = soup.find(class_="commonlist")
        if newslists is not None:
            a_tags = newslists.find_all('a')
            for i, a in enumerate(a_tags):
                self.article_order = i+1
                self.article_url = f"{self.uri}/{a.attrs['href']}"
                self.article_category = a.find(class_='commonlist_cate').string
                self.article_name = a.find(class_='commonlist_tx_headline').string
                viewed = a.find(class_='commonlist_tx_visit')
                for string in viewed.stripped_strings:
                    if string.isalpha() is False:
                        self.viewed_cnt = int(string.replace(',',''))
                self.docs.append(self.schematize().doc.copy())
        return self


def parse_mnewshome(all=False):
    newshome = Parser()
    if all:
        newshome.load()
    else:
        newshome.load({'html':{'$ne':None}, 'layout':None})
    newshome.parse()


def df_cols_sorter(df, firstfactor):
    cols = list(df.columns)
    #print(f"\n original cols : {cols}\n")
    for fac in firstfactor:
        cols.remove(fac)
    for addi in naver_addi_cols:
        cols.remove(addi)
    cols = firstfactor + cols + naver_addi_cols
    #print(f"\n reordered cols : {cols}\n")
    return df.reindex(columns=cols)
