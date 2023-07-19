
import igoogle as gg
import pandas as pd


# 전역변수
TBL명 = '인물정보_이름직업수동매핑'
URL = 'https://docs.google.com/spreadsheets/d/1oBiTYaBdH_RMxlK4JcDYRMAc0cvjezPuYQcyFSuWq8Q/edit#gid=0'

class InfoCollector:

    def 인물정보_이름직업매핑_수집(self):

        s = gg.drive.구글시트_수집(url=URL, dbg_on=dbg_on)
        df = s.find('Sheet1').to_frame(index_col=None)
        print(df)

        df = df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)

        dicli = df.to_dict('records')
        mg.insert_many(db명=DB명, tbl명=TBL명, dicli=dicli, dbg_on=dbg_on, 사전검증=사전검증)
        mg.테이블의_중복제거(db명=DB명, tbl명=TBL명, subset=['이름'])
