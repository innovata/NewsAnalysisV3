
from inews import *
from Layout_Analyzer import URL_파싱_v1

import re


언론사 = ['언론사명','언론사_url','언론사_로고_url']
언론인 = ['언론인명','소속_언론사명','이메일','기자의_뉴스모음페이지_url','기자의_기사모음페이지_url']
TBL = '언론사'
#정치인 = []
#인물 =
#개개인
#누가 = 언론사 + 언론인

class NaverPressInfoParser:

    def __init__(self):
        """."""

    def insert_pressinfo_into(self):
        """화면배치_URL_TBL에_언론사정보_삽입
        mg.insert_many(db명=DB명, tbl명='화면배치_URL', dicli=dicli, dbg_on=True, 사전검증=False)
        언론사정보_삽입후_화면배치URL_TBL의_중복제거()
        """
        df0 = mg.find(db명=DB명, tbl명=TBL, query=None, projection=None, dbg_on=True, 컬럼순서li=[], df보고형태='df')
        pp.pprint({'원본 길이':len(df)})
        df = df0.drop_duplicates(subset=['언론사_url'])
        pp.pprint({'중복제거 후 길이':len(df)})

        dic = {
            '언론사':list(df['언론사명']),
            'URL':list(df['언론사_url'])
        }
        df1 = pd.DataFrame(dic)
        df1 = df1.assign(서비스명= '뉴스')
        df1 = df1.assign(페이지명= '홈')
        self.docs = df1.to_dict('records')

    def 언론사정보_삽입후_화면배치URL_TBL의_중복제거():
        #화면배치_URL
        pc_df = mg.find(db명=DB명, tbl명='언론사', query=None, projection=None, dbg_on=False, 컬럼순서li=[], df보고형태='df')

        len(pc_df)
        pc_df.dtypes
        print(len(pc_df))
        pc_df = pc_df.drop_duplicates(subset=['언론사_url','언론사명'])
        print(len(pc_df))

        dicli = pc_df.to_dict('records')
        mg.insert_many(db명=DB명, tbl명='언론사', dicli=dicli)


        pc_df_, g = URL_파싱_v1(df=pc_df, URL명='언론사_url', dbg_on=True)
        print(len(pc_df_))
        pc_df_ = pc_df_.drop_duplicates(subset=['URI'])
        print(len(pc_df_))
        pc_df_ = pc_df_.assign(PresComName= lambda x: x.URI)


        def 특수도메인기호_삭제(x):
            dlt_e_li = ['www.','.com','.co','.kr','/','']
            for e in dlt_e_li:
                rs = re.search(e, x)
                print(rs)
                if rs is not None:
                    print(x[rs.start():rs.end()])
                    x = x.replace(x[rs.start():rs.end()], '')
            print({'x':x})
            return x

        pc_df_['PresComName'] = pc_df_['PresComName'].apply(특수도메인기호_삭제)
        pc_dicli = pc_df_.to_dict('records')
        for d in pc_dicli:
            print('\n' + '-'*60)
            query = {'언론사_url':{'$regex':d['URI']}}
            update = {'$set':{'언론사영문명':d['PresComName']}}
            mg.update_one(db명=DB명, tbl명='언론사', query=query, update=update, upsert=False)
