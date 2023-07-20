"""
============================== news_TBL_자료구조 ==============================

뉴스_원본id                       object
뉴스본문_ETRI언어분석_수집완료              bool
뉴스제목_ETRI언어분석_수집완료              bool
"""

KEY = ['_id','url','수집일시']

WHO = ['언론사명','언론인명']

WHEN = ['입력일시','최종수정일시']

포털 = ['네이버','다음']
SNS = ['twitter','facebook','kakaotalk']
WHERE = 포털 + SNS

WHAT = ['네이버기준_쟁점명','사건_id']#네이버의_쟁점명 --> 네이버_정의_쟁점명
HOW = ['뉴스본문','뉴스제목']
ETC = ['좋아요']

COL_ORDER = WHO + WHEN + WHAT + HOW + ETC + KEY

def get_ds():
    ds = {}
    ds.update( {e:'' for e in WHO} )
    ds.update( {e:'' for e in WHEN} )
    ds.update( {e:'' for e in WHAT} )
    ds.update( {e:'' for e in HOW} )
    ds.update( {e:'' for e in ETC} )
    ds.update( {e:'' for e in KEY} )
