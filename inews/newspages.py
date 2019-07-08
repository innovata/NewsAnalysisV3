
from inews import models
import igoogle
import pandas as pd


class NewsPageCollector(models.NewsPage):

    def __init__(self, url=None):
        super().__init__()
        url = url if url is not None else 'https://docs.google.com/spreadsheets/d/1kxlAuepdMnZndw59zjluvkkx6zY92_xuisjtII8xO1s/edit#gid=0'
        self.gs = igoogle.drive.Gsheets(url)

    def collect(self, sheet='Sheet1'):
        df = self.gs.get_sheet(sheet)
        df = df.rename(columns={'URL':'url','페이지명':'name','언론사':'pressname'})
        for d in df.to_dict('records'):
            self.attributize(d).update_doc({'url':self.url}, True)
