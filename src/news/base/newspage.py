
from inews.base import models
# import igoogle
import pandas as pd


class NewsPageCollector(models.NewsPage):

    def __init__(self):
        super().__init__()
        # url = url if url is not None else 'https://docs.google.com/spreadsheets/d/1kxlAuepdMnZndw59zjluvkkx6zY92_xuisjtII8xO1s/edit#gid=0'
        # self.gs = igoogle.drive.Gsheets(url)

    # def googlesheet(self, sheet='Sheet1'):
    #     df = self.gs.get_sheet(sheet)
    #     df = df.rename(columns={'URL':'url','페이지명':'name','언론사':'pressname'})
    #     for d in df.to_dict('records'):
    #         self.attributize(d).update_doc({'url':self.url}, True)

    def dedup(self):
        projection = {e:1 for e in self.schema}
        cursor = self.tbl.find(projection=projection)
        df = pd.DataFrame(list(cursor))
        df = df.sort_values(['pressname', 'name'])
        return df
        len1 = len(df)
        TF = df.duplicated(keep='first', subset=['pressname', 'name'])
        df = df[TF]
        len2 = len(df)
        print(len1, len2)
        if len(df) is not 0:
            pass
