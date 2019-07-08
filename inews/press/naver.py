
from inews import models, journalists
from inews.libs import idatetime
from ilib import irequest
from bs4 import BeautifulSoup
import idebug as dbg
import inspect
import copy
import re
from datetime import timezone, timedelta
import pandas as pd
from urllib.parse import urlparse


#============================================================
# NewsPageParser.
#============================================================

class MobileHomeParser(models.NewsPageSnapshot):

    def __init__(self):
        super().__init__('네이버', '모바일홈')

    def parse(self):
        loop = dbg.Loop(f"{self.__class__} | {inspect.stack()[0][3]}", len(self.docs))
        for d in self.docs:
            self.attributize(d)
            lay = MobileHomeLayoutParser(self.html)
            self.layout = lay.parse().docs
            self.update_doc({'_id':self._id}, True)
            loop.report(addi_info=f" snapshot_dt : {self.snapshot_dt}")
        return self

class MobileHomeLayoutParser(models.PageLayout):

    def __init__(self, html):
        super().__init__(html)
        # 네이버-모바일홈 만의 특수한 컬럼들 추가.
        self.addi_schema = ['data_area', 'data_class', 'data_clk', 'data_gdid', 'data_rank']
        self.schema += self.addi_schema

    def parse(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        self.parse_chartype_newslist(soup)
        self.parse_thumnail_newslist(soup)
        return self

    def parse_chartype_newslist(self, soup):
        """문자형뉴스리스트_영역배치"""
        self.screen_order = 1
        self.section_name = '문자형 뉴스리스트'
        self.section_order = 1
        s = soup.find(class_='uio_text')
        if s is not None:
            return self.parse_atags(s)

    def parse_thumnail_newslist(self, soup):
        """썸네일뉴스_영역배치"""
        self.screen_order = 2
        self.section_name = '썸네일형 뉴스리스트'
        self.section_order = 2
        s = soup.find(class_='uio_thumbnail')
        if s is not None:
            return self.parse_atags(s)

    def parse_atags(self, soup):
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
        return self

def parse_mhome(all=False):
    home = MobileHomeParser()
    if all:
        home.load()
    else:
        home.load({'html':{'$ne':None}, 'layout':None})
    home.parse()

class MobileNewsHomeParser(models.NewsPageSnapshot):

    def __init__(self):
        super().__init__('네이버','모바일뉴스홈')
        u = urlparse(self.pageurl)
        self.pageuri = f"{u.scheme}://{u.netloc}"

    def parse(self):
        loop = dbg.Loop(f"{self.__class__} | {inspect.stack()[0][3]}", len(self.docs))
        for d in self.docs:
            self.attributize(d)
            lay = MobileNewsHomeLayoutParser(self.html, self.pageuri)
            self.layout = lay.parse().docs
            self.update_doc({'_id':self._id}, True)
            loop.report(addi_info=f" snapshot_dt : {self.snapshot_dt}")
        return self

class MobileNewsHomeLayoutParser(models.PageLayout):

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
    newshome = MobileNewsHomeParser()
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
