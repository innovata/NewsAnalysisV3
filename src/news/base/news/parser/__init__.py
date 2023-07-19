

def load_parsingtarget(url, dbg_on=False, unitest=False):
    """
    파싱완료True가_아닌_타겟을_dicli로딩
    - 여러가지 기준으로 파싱대상여부를 결정한다.
    """
    start_t = datetime.now()

    tbl = db[news.TBL]
    #query = {'url':{'$regex':url}, '파싱완료':{'$ne':True}, 'r_txt':{'$ne':None}}
    query = {'url':{'$regex':url}}
    projection = {'_id':1, 'r_txt':1}
    if unitest is True: cursor = tbl.find(filter=query, projection=projection).limit(1)
    else: cursor = tbl.find(filter=query, projection=projection)
    dbg.runtimelog(start_t=start_t, title='cursor')

    dicli = list(cursor)
    dbg.runtimelog(start_t=start_t, title=whoami)
    if len(dicli) == 0: print('len(dicli) == 0')
    else: return dicli

def make_parsed_true(id, dbg_on=False):
    """
    news TBL 에 파싱된_타겟을_파싱완료 True로_업뎃
    - None : 파싱대상여부의 가치판단 이전
    - True : 파싱대상여부의 가치판단 후 YES
    - False : 파싱대상여부의 가치판단 후 No 또는 파싱완료
    """
    tbl = db[layout.TBL]
    query = {'_id':id}
    update = {'$set':{'파싱완료':True}}
    tbl.update_one(filter=query, update=update, upsert=False)
