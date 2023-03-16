
from inews import *
from inews import models

from bs4 import BeautifulSoup


location_cols = ['screen_order','section_order','section_name','article_order','article_name']
article_cols = ['article_name','article_url','article_order','article_category']
naver_addi_cols = ['data-area', 'data-class', 'data-clk', 'data-gdid', 'data-rank']

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

def save_layouts(layout_clss):
    for d in layout_clss.docs:
        filter = {'snapshotID':d['snapshotID'], 'article_url':d['article_url']}
        update = {'$set':d}
        layout_clss.update_one(filter, update, True)

class MobileHomeParser(models.PageLayout):

    def __init__(self):
        super().__init__()
        self.pressname = '네이버'
        self.pagename = '모바일홈'
        # 네이버-모바일홈 만의 특수한 컬럼들 추가.
        self.schema += ['data_class','data_area','data_clk','data_gdid','data_rank']

    def get_targets(self):
        snapshot = models.NewsPageSnapshot(self.pressname, self.pagename)
        snapshot.load({'layout':None})
        #snapshot.load({'collect_dt':{'$gt':datetime(2019,3,26)}})
        return snapshot

    def parse(self):
        snapshot = self.get_targets()
        loop = dbg.Loop(f"{self.__class__} | {inspect.stack()[0][3]}", len(snapshot.docs))
        for d in snapshot.docs:
            snapshot.attributize(d)
            soup = BeautifulSoup(snapshot.html, 'html.parser')
            self.parse_chartype_newslist(soup)
            self.parse_thumnail_newslist(soup)
            snapshot.layout = self.docs
            filter = {'_id':snapshot._id}
            snapshot.update_doc(filter, True)
            loop.report(addi_info=f" snapshot.collect_dt : {snapshot.collect_dt}")
        return self

    def parse_chartype_newslist(self, soup):
        """문자형뉴스리스트_영역배치"""
        self.screen_order = 1
        self.section_name = '문자형 뉴스리스트'
        self.section_order = 1
        s = soup.find(class_='uio_text')
        return self.parse_atags(s)

    def parse_thumnail_newslist(self, soup):
        """썸네일뉴스_영역배치"""
        self.screen_order = 2
        self.section_name = '썸네일형 뉴스리스트'
        self.section_order = 2
        s = soup.find(class_='uio_thumbnail')
        return self.parse_atags(s)

    def parse_atags(self, soup):
        if soup is not None:
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

class MobileNewsHomeParser(models.PageLayout):

    def __init__(self):
        super().__init__()
        self.pageuri = 'http://m.news.naver.com'
        self.pressname = '네이버'
        self.pagename = '모바일뉴스홈'
        # 네이버-모바일-뉴스홈 만의 특수한 컬럼들 추가. : 많이 본 조회수, 네이버가 조회수 집계한 시간.
        self.schema += ['article_category','viewed_cnt','totalized_time']

    def get_targets(self):
        snapshot = models.NewsPageSnapshot(self.pressname, self.pagename)
        snapshot.load({'layout':None})
        return snapshot

    def parse(self):
        snapshot = self.get_targets()
        loop = dbg.Loop(f"{self.__class__} | {inspect.stack()[0][3]}", len(snapshot.docs))
        for d in snapshot.docs:
            snapshot.attributize(d)
            self.collect_dt = snapshot.collect_dt
            soup = BeautifulSoup(snapshot.html, 'html.parser')
            """HTML 클래스-트리구조 : r_home_wrp _moreViewLinkArea / __persist_content / r_group _reset"""
            s = soup.find(class_='__persist_content')
            if s is not None:
                self.thumnail_text_section(s)
                self.mostviewed_section(s)
                snapshot.layout = self.docs
                pp.pprint(snapshot.schematize().doc)
                filter = {'_id':snapshot._id}
                #snapshot.update_doc(filter, True)
            loop.report(addi_info=f" snapshot.collect_dt : {snapshot.collect_dt}")
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
            self.article_url = f"{self.pageuri}{a.attrs['href']}"
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
                self.article_url = f"{self.pageuri}{a.attrs['href']}"
                self.article_category = a.find(class_='commonlist_cate').string
                self.article_name = a.find(class_='commonlist_tx_headline').string
                viewed = a.find(class_='commonlist_tx_visit')
                for string in viewed.stripped_strings:
                    if string.isalpha() is False:
                        self.viewed_cnt = int(string.replace(',',''))
                self.docs.append(self.schematize().doc.copy())
        return self


self = MobileNewsHomeParser()
dbg.obj(self)
self.parse()
snapshot = self.get_targets()
#snapshot = models.NewsPageSnapshot(self.pressname, self.pagename)

#snapshot.load()
df = snapshot.get_df()
len(df)
df
df = df.sort_values('collect_dt',ascending=False)
len(df)
df.head(1)
self.parse()
self.get_df()

snapshot.docs = df.to_dict('records')
from pandas.io.json import json_normalize
df = json_normalize(snapshot.docs, 'layout')
len(df)
df

df1 = df.drop_duplicates(subset=['article_url'])
len(df1)



snapshot = models.NewsPageSnapshot()
snapshot.schema = ['pageid','collect_dt','html','snapshotID','layout']
dbg.obj(snapshot)
df = snapshot.load({'pageid':page.pageid, 'collect_dt':{'$gt':datetime(2019,3,26)}}).get_df()
len(df)
df = df.rename(columns={'_id':'snapshotID'})
df.head(1)
snapshot.docs = df.to_dict('records')
for d in snapshot.docs:
    snapshot.attributize(d)
    break
snapshot.pageid
snapshot.snapshotID
snapshot.collect_dt

soup = BeautifulSoup(snapshot.html, 'html.parser')
print(soup.prettify())
self.parse_chartype_newslist(soup)
self.parse_thumnail_newslist(soup)
self.get_df()

snapshot.layout = self.docs
snapshot.data = None
snapshot.schematize()
snapshot.doc
