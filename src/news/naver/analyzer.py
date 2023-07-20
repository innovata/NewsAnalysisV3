
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
# ArticleParser.
#============================================================


class ArticleParser(models.Article):

    def __init__(self):
        super().__init__('네이버')

    def remove_non_articles(self):
        """아래 놈들을 위한 별도의 파서클래스를 만들어라."""
        df = self.get_df()

        TF = df.url.str.contains(pat='https://m\.news\.naver\.com/newspaper/')
        newspaper_df = df[TF]
        df = df[~TF]

        TF = df.url.str.contains(pat='https://m\.news\.naver\.com/hotissue/')
        hotissue_df = df[TF]
        df = df[~TF]

        TF = df.url.str.contains(pat='https://m\.news\.naver\.com/viewer/news\?listUrl=https://m\.naver\.com')
        viewer_df = df[TF]
        df = df[~TF]

        self.docs = df.to_dict('records')
        return self

    def get_targets(self):
        self.load({'html':{'$ne':None}, 'headline':None})
        self.remove_non_articles()
        return self

    def parse(self):
        self.get_targets()
        loop = dbg.Loop(f"{self.__class__} | {inspect.stack()[0][3]}", len(self.docs))
        for d in self.docs:
            self.attributize(d)
            soup = BeautifulSoup(self.html, 'html.parser')
            s = soup.find('div',class_='responsive_col1')
            if s is None:
                errmsg = f"soup.find('div',class_='responsive_col1') is None.\n 기사페이지의 핵심내용태그(responsive_col1)가 없는 껍데기 페이지."
                print(f"\n{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n {errmsg}")
            else:
                self.parse_uppertier(s)
                self.parse_middletier(s)
                self.parse_lowertier(s)
                if len(list(self.schematize().doc)) > 3:
                    self.update_doc({'_id':self._id})
            loop.report(addi_info=self.url)

    def parse_uppertier(self, soup):
        """기사제목, 언론사명|언론사로고, 발행일시, 좋아요수, 댓글수."""
        s = soup.find('div',class_='media_end_head')
        if s is None:
            print(f"\n{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]} | soup.find('div',class_='media_end_head') is None.\n")
        else:
            self.headline = s.find('h2',class_='media_end_head_headline').get_text()
            self.issuetitle = None

            npp = NaverPressInfoParser().parse(s)
            self.pressname = npp.name

            datetimes = s.find_all(class_='media_end_head_info_datestamp_time')
            self.published_dt = None if len(datetimes) < 1 else idatetime.datetime_strptime_for_AMPM(datetimes[0].string)
            if self.published_dt is not None:
                self.published_dt = self.published_dt.astimezone(timezone(timedelta(hours=+9)))
            self.revised_dt = None if len(datetimes) < 2 else idatetime.datetime_strptime_for_AMPM(datetimes[1].string)
            if self.revised_dt is not None:
                self.revised_dt = self.revised_dt.astimezone(timezone(timedelta(hours=+9)))

            etcinfo = s.find(id='commentFontGroup')
            like = etcinfo.find(class_='media_end_head_info_variety_likeit')
            if like is not None:
                like_cnt = like.find('span',class_="u_likeit_text _count num")
                if like_cnt is not None:
                    self.like_cnt = like_cnt.get_text()
            comment_cnt = etcinfo.find('a', id="comment_count")
            if comment_cnt is not None:
                comment_cnt = comment_cnt.get_text()
                if comment_cnt.isnumeric():
                    self.comment_cnt = comment_cnt
        return self

    def parse_middletier(self, soup):
        """기사본문, 사용된 사진, 언론인명, 언론인-이메일, 좋아요상세."""
        s = soup.find(id='contents')
        if s is None:
            print(f"\n{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]} | soup.find(id='contents') is None.\n")
        else:
            s1 = s.find(id='dic_area')
            if s1.find('span') is None:
                print(f"\n{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]} | s.find(id='dic_area').find('span') is None. 기사 본문내용(bodytext)가 없다. 씨발!\n")
            else:
                s1.span.decompose()
                text = s1.get_text('\n')
                jnlist = journalists.NaverJournalistInfoParser()
                p_jname = re.compile(pattern='([가-힣·]+|[가-힣]+\s+)기자')
                p_jemail = re.compile(pattern='[a-zA-Z0-9]+@[a-z0-9]+\.[a-z]+')
                p_trash = re.compile("^\[|^▶\[*|^\[ⓒ*|네이버[가-힝\s]+받아보기|무단\s*전재 및 재배포\s*금지|네이버[가-힝\s]+구독(하기|하세요)|네이버[가-힝a-zA-Z0-9.'\s]+보세요|네이버 구독 \d+위 신문|페이스북'\s*친구추가|구독$")
                p_letter = re.compile("[가-힝]")
                self.bodytext = ''
                for line in text.splitlines():

                    m1 = p_jname.search(string=line)
                    if m1 is not None:
                        jnlist.name = line[m1.start():m1.end()]
                        self.journalistname = jnlist.name
                    m2 = p_jemail.search(string=line)
                    if m2 is not None:
                        jnlist.email = line[m2.start():m2.end()]
                    if (m1 is None) and (m2 is None):
                        if len(line) is not 0:
                            if p_trash.search(string=line) is None:
                                if p_letter.search(string=line) is not None:
                                    self.bodytext += (line + '\n')
                # bodytext 청소.
                # 언론인정보를 별도 테이블에 저장.
                jnlist.pressname = self.pressname
                # 기자_뉴스모음페이지
                s2 = s1.find('a', class_='media_journalistcard_summary')
                jnlist.naver_jcard_url = None if s2 is None else s2.attrs['href']
                jnlist.save()
        return self

    def parse_lowertier(self, soup):
        """전체 댓글."""
        s = soup.find(class_='u_cbox')
        if s is None:
            print(f"\n{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]} | soup.find(class_='u_cbox') is None.\n")
        else:
            print(f"\n{'#'*60}\n{self.__class__} | {inspect.stack()[0][3]} | How is it possible?\n")
        return self


def parse_articles():
    arp = ArticleParser()
    arp.parse()


class NaverPressInfoParser(models.Press):

    def parse(self, soup):
        atag = soup.find('a', class_='media_end_head_top_logo')
        if atag is not None:
            self.url = atag.attrs['href']
            img = atag.find('img')
            if img is not None:
                self.logo_url = img.attrs['src']
                self.name = img.attrs['alt']
        self.update_doc({'url':self.url}, True)
        return self


class ArticleCommentCollector:

    def __init__(self):
        self.uri = "https://apis.naver.com"
        self.url = f"{self.uri}/commentBox/cbox/web_neo_list_jsonp.json"
        self.qs = "?ticket=news&templateId=view_politics_m2&pool=cbox5&_callback=jQuery21403750129072197055_1551720193625&lang=ko&country=KR&objectId=news011%2C0003513679&categoryId=&pageSize=5&indexSize=10&groupId=&listType=OBJECT&pageType=more&page=1&initialize=true&userType=&useAltSort=true&replyPageSize=20&moveTo=&sort=favorite&includeAllStatus=true&_=1551720193626"

    def parse_querystring(self):
        qs = irequest.convert_QSstr_to_QSdic(f"{self.url}{self.qs}")
        dbg.dic(qs, 'final qs.')
