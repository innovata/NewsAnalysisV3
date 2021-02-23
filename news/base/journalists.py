
from inews.base import models
import re
import copy



class NaverJournalistInfoParser(models.Journalist):

    def __init__(self):
        super().__init__(pressname=None,name=None,email=None,naver_jcard_url=None)

    def save(self):
        self.schematize()
        filter = {'pressname':self.pressname, 'name':self.name, 'email':self.email}
        update = {'$set':self.doc}
        self.update_one(filter, update, True)
        return self

class NaverJournalistInfoMigrator:

    TBL = '언론인'

    def __init__(self):
        print(f" Old TBL name : {self.TBL}")
