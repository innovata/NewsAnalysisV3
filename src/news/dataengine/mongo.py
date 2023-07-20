# 2019.08.13


import os
import copy
import re
import inspect
import pprint
pp = pprint.PrettyPrinter(indent=2)


from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure
import pandas as pd


from inews.lib import dbg


#============================================================
print(f"{'*'*50} {__name__} | Start.\n\nMongoDB Server Checking...\n\n")
#============================================================

client = MongoClient(host='localhost', port=27017, document_class=dict, tz_aware=False, connect=True, maxPoolSize=100)
try:
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
except ConnectionFailure as cf:
    print(f"{'#'*50} {__name__}\nServer not available.\nConnectionFailure : {cf}")

try:
    dbname = os.environ['MONGO_DBNAME']
except Exception as e:
    print(f"{'#'*50} {__name__}\nException : {e}\n\nSetup below :\nexport MONGO_DBNAME=prefered_name")
    raise
else:
    db = client[dbname]
    print(f"\ndb : {db}")
finally:
    print(f"\n{'*'*50} {__name__} | End.")

#============================================================
"""Base Code."""
#============================================================

class Model:

    def modeling(self, cls):
        self.modelname = f"{cls.__name__}"
        self.tbl = db[self.modelname]
        return self

    def submodeling(self, cls, modelsuffix):
        self.modelname = f"{cls.__name__}_{modelsuffix.capitalize()}"
        self.tbl = db[self.modelname]
        return self

    def attributize(self, dic):
        for key, value in dic.items():
            setattr(self, key, value)
        return self

    def schematize(self):
        try:
            self.doc = {}
            for attr in list(self.__dict__):
                if attr in self.schema:
                    self.doc[attr] = getattr(self, attr)
        except Exception as e:
            print(f"{'#'*50} {self.modelname}.{inspect.stack()[0][3]}\nException : {e}")
            raise
    """handle_flocals --> attributize_flocals"""
    def attributize_flocals(self, frame):
        dic = {k:v for k,v in frame.f_locals.items() if k not in ['self','__class__']}
        return self.attributize(dic)

    def get_df(self):
        return pd.DataFrame(self.docs)

    def insert_doc(self):
        self.schematize()
        InsertOneResult = self.tbl.insert_one(self.doc)
        pp.pprint(InsertOneResult.raw_result)
        del(self.doc['_id'])
        return self

    def update_doc(self, filter, upsert=False):
        self.schematize()
        update = {'$set':self.doc}
        UpdateResult = self.tbl.update_one(filter, update, upsert)
        pp.pprint(UpdateResult.raw_result)
        return self

    def explain(self, cursor):
        explain = cursor.explain()
        if explain['executionStats']['nReturned'] == 0:
            pp.pprint(explain)


class DatabaseHandler:

    def __init__(self, dbname=None):
        if dbname is None:
            self.db = client[os.environ['MONGO_DBNAME']]
        else:
            self.db = client[dbname]

    def list_collection_names(self):
        tbls = self.db.list_collection_names()
        return sorted(tbls)

    def list_collections(self):
        cursor = self.db.list_collections()
        dbg.clsdict(cls=cursor)
        return cursor

    def command_collstats(self, tblname):
        response = self.db.command('collstats', tblname)
        print(f"{'='*50} {__name__} | {self.command_collstats.__qualname__}")
        dbg.clsdict(cls=response)
        return response

    def command_connpoolstats(self):
        pp.pprint(self.db.command({'connPoolStats':1}))

    def get_collections(self, regex):
        tbls = self.list_collection_names()
        p = re.compile(regex)
        tables = []
        for tbl in tbls:
            if p.search(string=tbl) is not None:
                tables.append(tbl)
        return tables

    def drop_all_collections(self):
        tblnames = self.db.list_collection_names()
        for tblname in tblnames:
            print(f"\n tblname : {tblname}")
            db[tblname].drop()

    def change_collection_names(self):
        tbls = self.list_collection_names()
        p_target = re.compile('__')
        for tblnm in tbls:
            print(f"{'-'*50} {tblnm}")
            new_tblnm = p_target.sub(string=tblnm, repl='_')
            print(new_tblnm)
            if tblnm != new_tblnm:
                self.db[tblnm].rename(new_tblnm)
        print("\n검증 :\n")
        tbls = self.list_collection_names()
        dbg.printiter(iterable=tbls, slen=50)
