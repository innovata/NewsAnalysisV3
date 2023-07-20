
from inews.base import models, mongo
import requests
from bs4 import BeautifulSoup
import pandas as pd
import idebug as dbg
import inspect


URL = 'http://www.assembly.go.kr/assm/memact/congressman/memCond/memCond.do'
URL1 = 'http://www.assembly.go.kr/assm/memact/congressman/memCond/memCondListAjax.do'
ASS_TBL명 = '국회의원현황'
PRT_TBL명 = '정당명코드'


class Party(mongo.ModelHandler):

    def __init__(self):
        """대한민국국회 웹사이트에서 정의된 정당명/코드."""
        self.parties = {
            '더불어민주당':101182,
            '자유한국당':101186,
            '바른미래당':101192,
            '민주평화당':101191,
            '정의당':101180,
            '대한애국당':101188,
            '민중당':101190,
            '무소속':101030
        }
        super().__init__()

    def get(self):
        for key, value in self.parties.items():
            self.docs.append({'name':key, 'code':value})
        return self.get_df()

class Assemblymen(models.Assemblymen):

    def __init__(self):
        super().__init__()
        self.url = 'http://www.assembly.go.kr/assm/memact/congressman/memCond/memCondListAjax.do'

    def set_form_of_korea_assembly_website(self):
        self.form = {
            's_poly_cd': self.partycode,
            's_dept_cd': '',
            's_dtl_no': '',
            's_elected_method':'',
            's_up_orig_cd': '',
            's_dw_orig_cd': '',
            's_mem_nm': '',
            'currentPage': '',
            'movePageNum': '',
            'rowPerPage': 300,
        }

    def collect(self, partyname, partycode):
        self.partyname = partyname
        self.partycode = partycode
        self.set_form_of_korea_assembly_website()
        try:
            r = requests.post(self.url, data=self.form)
        except Exception as e:
            print(f"\n Exception : {e}\n")
        else:
            if (r.status_code is 200) and (len(r.text) is not 0):
                self.r = r
        return self

    def parse(self):
        if 'r' in self.__dict__:
            soup = BeautifulSoup(self.r.text, 'html.parser')
            s = soup.find(class_='memberna_list')
            docs = []
            for dl in s.find_all('dl'):
                name = dl.find('dt')
                self.korean_name = name.find('a').get_text().lstrip().rstrip()
                self.chinese_name = name.find('span', class_='chi').get_text().lstrip().rstrip()
                names = []
                for string in name.stripped_strings:
                    if string.lstrip().rstrip() not in [self.korean_name, self.chinese_name]:
                        names.append(string.lstrip().rstrip())
                self.english_name = names[0]
                self.photo_url = dl.find('dd', class_='img').find('a').find('img').attrs['src']
                self.elected_cnt = dl.find('dd', class_='mt').get_text().lstrip().rstrip()
                self.region = dl.find('dd', class_='ht').get_text().lstrip().rstrip()
                self.update_doc({'korean_name':self.korean_name, 'chinese_name':self.chinese_name, 'partyname':self.partyname}, True)

def collect():
    self = Assemblymen()
    party = Party().get()
    loop = dbg.Loop(f"{self.__class__} | {inspect.stack()[0][3]}", len(party))
    for d in party.to_dict('records'):
        party.attributize(d)
        self.collect(party.name, party.code).parse()
        loop.report(addi_info=f" partyname : {party.name}")
