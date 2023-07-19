
from inews.base import models
import re
import inspect


def pageurls(f, initurl=None):
    def sliceli(urls):
        for i, e in enumerate(urls):
            if re.search(pattern=initurl, string=e) is not None:
                break
        return urls[i:]

    whoiam = f"{__name__}.{inspect.stack()[0][3]}"
    newspage = models.NewsPage()
    urls = newspage.tbl.distinct(key='url', filter={'url':{'$ne':None}})
    urls = sorted(urls)
    if initurl is not None:
        urls = sliceli(urls)
    urls_len = len(urls)
    for i, url in enumerate(urls, start=1):
        print(f"{'-'*50} {whoiam} | ({i}/{urls_len}) url : {url}")
        try:
            f(pageurl=url)
        except Exception as e:
            print(f"{'#'*50} {whoiam}\nException : {e}")
