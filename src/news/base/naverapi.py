

import requests
from URL import NAVER_mNEWS_URI
TBL = '네이버_오픈API_뉴스검색결과'

class NaverNewsSearcher:
    """네이버 뉴스 검색 오픈 API
    https://developers.naver.com/docs/search/news/
    화면배치와는 상관없다.
    응답받은 자료를 "뉴스" 자료구조에 맞게 변환 후 "뉴스" 테이블에 저장해야 한다.
    """
    def __init__(self):
        self.auth()
        self.url = 'https://openapi.naver.com/v1/search/news.json'

    def auth(self):
        nav_key = list( mg.client['lib'].오픈API_인증정보.find({'제공자명':'네이버'}) )[0]
        self.apikey_id = nav_key['아이디']
        self.apikey_pw = nav_key['비밀번호']
        return self

    def scrape(self, keyword):
        req_header = {
            'Host': 'openapi.naver.com',
            'User-Agent': 'curl/7.49.1',
            'Accept': '*/*',
            'X-Naver-Client-Id':self.apikey_id,
            'X-Naver-Client-Secret':self.apikey_pw
        }
        req_param = {
            'query':keyword,
            'display':100, # 검색 결과 출력 건수 지정, 10(기본값), 100(최대)
            'start':'', # 검색 시작 위치로 최대 1000까지 가능, 1(기본값), 1000(최대)
            'sort':'' # 정렬 옵션: sim (유사도순), date (날짜순)
        }
        r = requests.get(self.url, headers=req_header, params=req_param)
        r_js = r.json()
        if len(r_js) == 0:
            return {}
        else:
            return r_js

    def parse(self, dic):
        lastBuildDate = dic['lastBuildDate']
        # 총개수보다 디스플레이수가 적으므로, 추가 반복 수집이 필요할까? 생각해봐라.
        총개수 = dic['total']
        start = dic['start']
        display = dic['display']
        pp.pprint({
            'lastBuildDate':lastBuildDate,
            '총개수':총개수,
            'start':start,
            'display':display
        })
        df = pd.DataFrame(dic['items'])
        if len(df) == 0:
            []
        else:
            df = df.rename(columns={
                'pubDate':'발행일시',
                'title':'제목',
                'description':'내용',
                'link':'네이버뉴스_url',
                'originallink':'원본기사_url'})
            df.발행일시 = df.발행일시.apply(lambda x: datetime.strptime(x, '%a, %d %b %Y %H:%M:%S %z'))
            df = df.assign(검색어=검색어)
            return df

    def collect(검색어):
        dic = __수집(검색어)
        if len(dic) == 0:
            pass
        else:
            df = __파싱(검색어)
