"""
============================== 핵심일 ==============================
from thenews.news.handler import *
"""
# 프로젝트 라이브러리
from thenews.__lib__ import *
print('\n' + '# '*5 + sys.modules[__name__].__file__ + ' #'*5)

# 전역변수

# 프로젝트 모듈
from thenews import news
"""
==============================  ==============================
"""
def load(dbg_on=True):
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbg_on)
    inputs = dbg.inputs(inspect.currentframe(), dbg_on)
    """
    """
    tbl = db[news.TBL]
    cursor = tbl.find().limit(1)
    dicli = list(cursor)
    print('\n dicli :\n')
    #pp.pprint(dicli)
    print('\n dicli_keys :\n\n {}'.format(dicli[0].keys()))


def update():
    whoami = dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3], dbg_on=True)
    start_t = datetime.now()

    tbl = db[news.TBL]
    query = {}
    #update = {'$rename':{'화면배치id':'layoutid'}}
    update = {'$unset':{'res':''}}
    tbl.update_many(filter=query, update=update, upsert=False)

    dbg.runtimelog(start_t=start_t, title=whoami)


def extract_r_txt_from_rescol():
    import json
    def f(id, res):
        if 'text' in list(res.keys()):
            query = {'_id':id}
            update = {'$set':{'r_txt':res['text']}}
            tbl.update_one(filter=query, update=update, upsert=False)
    """
    """
    start_t = datetime.now()

    tbl = db[news.TBL]
    query = {'res':{'$ne':None}, 'r_txt':None}
    projection = {'_id':1, 'res':1}
    cursor = tbl.find(filter=query, projection=projection)
    dbg.runtimelog(start_t=start_t, title='cursor')

    dicli = list(cursor)
    dbg.runtimelog(start_t=start_t, title='list(cursor)')

    dicli_len = len(dicli)
    i=1
    for d in dicli:
        print('\n' + '-'*60 + '{}/{}'.format(i, dicli_len))

        res = d['res']
        if isinstance(res, dict): f(id=d['_id'], res=res)
        elif isinstance(res, list): f(id=d['_id'], res=res[0])
        else: pass

        i+=1
