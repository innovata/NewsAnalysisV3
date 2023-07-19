
from inews.base import *
from inews.base import models, press, journalists

from bs4 import BeautifulSoup
import copy
import re
from datetime import timezone, timedelta

from ilib import idatetime, irequest
#import collective_intelligence as pci



class ArticleParser(models.Article):

    NEWS_DS = {
        '뉴스제목':'',
        '뉴스본문':'',
        '언론사명':'',
        '언론인명':'',

        '입력일시':'',
        '최종수정일시':'',
        '네이버기준_쟁점명':'',
        '좋아요':'',
    }

    def __init__(self):
        super().__init__(url='',html='',
            headline='',bodytext='',
            pressname='',journalistname='',
            published_dt='',revised_dt='',issuetitle='')
        layout = models.NewsPageLayout()
        filter = {
            'article_html':{'$ne':None},
            'article_url':{'$regex':'news.naver.com/','$options':'i'}}
        self.articles = layout.load(filter).docs

    def parse_save(self):
        loop = dbg.Loop(f"{__class__.__name__}.{inspect.stack()[0][3]}", len(self.articles))
        for article in self.articles:
            dbg.dic(article, 'article of layout.', ['article_html'])
            loop.report(addi_info=article['article_url'])
            soup = BeautifulSoup(article['article_html'], 'html.parser')
            soup = soup.find('div',class_='responsive_col1')

            # 기사제목, 언론사명|언론사로고, 발행일시, 좋아요수, 댓글수.
            uppertier = soup.find('div',class_='media_end_head')
            self.parse_uppertier(uppertier)
            # 기사본문, 사용된 사진, 언론인명, 언론인-이메일, 좋아요상세.
            middletier = soup.find(id='contents').find(id='dic_area')
            self.parse_middletier(middletier)
            # 전체 댓글.
            #lowertier = soup.find(id='cbox_module')
            lowertier = soup.find(class_='u_cbox')
            if lowertier is None: print(f"\n lowertier soup is None.\n Build a class to collect json data.")
            else: print("\n How is it possible?\n")

            self.schematize()
            dbg.dic(self.doc, 'NaverArticle.doc')
            #self.update_doc()
            return self

    def parse_uppertier(self, soup):
        self.headline = soup.find('h2',class_='media_end_head_headline').get_text()
        self.issuetitle = None

        npp = press.NaverPressInfoParser()
        self.pressname = npp.parse_save(soup).name

        datetimes = soup.find_all(class_='media_end_head_info_datestamp_time')
        self.published_dt = None if len(datetimes) < 1 else idatetime.datetime_strptime_for_AMPM(datetimes[0].string)
        if self.published_dt is not None:
            self.published_dt = self.published_dt.astimezone(timezone(timedelta(hours=+9)))
        self.revised_dt = None if len(datetimes) < 2 else idatetime.datetime_strptime_for_AMPM(datetimes[1].string)
        if self.revised_dt is not None:
            self.revised_dt = self.revised_dt.astimezone(timezone(timedelta(hours=+9)))

        etcinfo = soup.find(id='commentFontGroup')
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
        s = copy.copy(soup)
        s.span.decompose()
        text = s.get_text('\n')
        #print(f"\n body text : \n\n{text.lstrip().rstrip()}\n")
        p_jinfo = re.compile(pattern='[가-힣]+기자\s+[a-zA-Z0-9]+@[a-z]')
        p_jname = re.compile(pattern='[가-힣]+기자')
        p_jemail = re.compile(pattern='[a-zA-Z0-9]+@[a-z0-9]+\.[a-z]+')
        self.bodytext = ''
        jnlist = journalists.NaverJournalistInfoParser()
        for line in text.splitlines():
            if p_jinfo.search(string=line) is None:
                if len(line) is not 0:
                    self.bodytext += (line + '\n')
            else:
                m = p_jname.search(string=line)
                jnlist.name = line[m.start():m.end()]
                m = p_jemail.search(string=line)
                jnlist.email = line[m.start():m.end()]
                break
        # 언론인정보를 별도 테이블에 저장.
        self.journalistname = jnlist.name
        jnlist.pressname = self.pressname
        # 기자_뉴스모음페이지
        s = soup.find('a', class_='media_journalistcard_summary')
        jnlist.naver_jcard_url = None if s is None else s.attrs['href']
        jnlist.save()
        return self

class ArticleCommentCollector:

    def __init__(self):
        self.uri = "https://apis.naver.com"
        self.url = f"{self.uri}/commentBox/cbox/web_neo_list_jsonp.json"
        self.qs = "?ticket=news&templateId=view_politics_m2&pool=cbox5&_callback=jQuery21403750129072197055_1551720193625&lang=ko&country=KR&objectId=news011%2C0003513679&categoryId=&pageSize=5&indexSize=10&groupId=&listType=OBJECT&pageType=more&page=1&initialize=true&userType=&useAltSort=true&replyPageSize=20&moveTo=&sort=favorite&includeAllStatus=true&_=1551720193626"

    def parse_querystring(self):
        qs = irequest.convert_QSstr_to_QSdic(f"{self.url}{self.qs}")
        dbg.dic(qs, 'final qs.')
