
import schedule
import time
from inews import snapshots, articles, press
import idebug as dbg
import inspect
import sys



def minutes_job():
    """뉴스페이지 스냅샷 수집, 파싱"""
    print(f"\n {inspect.stack()[0][3]} :\n{inspect.getdoc(minutes_job)}\n")
    fr = dbg.Function(inspect.currentframe()).report_init()
    snapshots.collect()
    snapshots.parse()
    fr.report_fin()

def hours_job():
    """뉴스_수집, 뉴스_파싱"""
    print(f"\n {inspect.stack()[0][3]} :\n{inspect.getdoc(hours_job)}\n")
    fr = dbg.Function(inspect.currentframe()).report_init()
    articles.collect()
    articles.parse()
    fr.report_fin()

def days_job():
    """ETRI언어분석_수집"""
    print(f"\n {inspect.stack()[0][3]} :\n{inspect.getdoc(days_job)}\n")
    fr = dbg.Function(inspect.currentframe()).report_init()
    articles.collect_etri_analysis(pressname='네이버', targetcol='headline', techname='LangAnalysis', apicode='srl')
    articles.collect_etri_analysis(pressname='네이버', targetcol='bodytext', techname='LangAnalysis', apicode='srl')
    fr.report_fin()


def jobs():
    """
    schedule.every(1).hours.do(hours_job).run()
    schedule.every(1).days.do(days_job).run()
    """
    print(f"\n {inspect.stack()[0][3]} :\n{inspect.getdoc(jobs)}\n")
    schedule.every(5).minutes.do(minutes_job).run()
    schedule.every(1).hours.do(hours_job).run()
    schedule.every(1).days.do(days_job).run()
    #schedule.every().days.at("23:59").do(days_job).run()
    while True:
        schedule.run_pending()
        time.sleep(0.01)


if __name__ == '__main__':
    print(f"{'='*60}\n sys.modules[__name__].__file__ : {sys.modules[__name__].__file__}")
    jobs()
