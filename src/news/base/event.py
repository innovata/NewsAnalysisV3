"""
뉴스와 트윗의 사건번호를 기준으로 둘을 묶어서 사건 객체라고 볼 수 있다.
"""
import __matplotlib as mpl




"""
============================================================
특정사건에_대한_뉴스와_트윗의_상관관계계수_계산저장
============================================================
"""
def 특정사건에_대한_뉴스와_트윗의_상관관계계수_계산저장():
    print('\n' + '='*60 + inspect.stack()[0][3])

    news_df = News.analyzer.보고용_뉴스df_기초검사_및_청소후_로딩()
    tw_df = Twitter.analyzer.보고용_트위터_유저타임라인df_기초검사_및_청소후_로딩()

    news_df, tw_df = 시간_상관관계를_주축으로_할_것이므로_시간_범위가_동일해야_한다(news_df, tw_df)
    news_df, tw_df, intc_li = predicted_값_범위가_동일해야_한다(news_df, tw_df)

    corr_dicli = 특정사건들에_대한_상관관계_계산(news_df, tw_df, intc_li)
    corr_df = pd.DataFrame(corr_dicli)

    corr_err = CorrCeffErr_cross_inspection(corr_df)
    mg.insert_many(db명=DB명, tbl명='뉴스트윗_사건번호별_상관관계계수', dicli=corr_dicli, dbg_on=False, 사전검증=False)
    return corr_df, corr_err

def 시간_상관관계를_주축으로_할_것이므로_시간_범위가_동일해야_한다(news_df, tw_df):
    print('\n' + '='*60 + inspect.stack()[0][3])

    공통시간축 = ['2018-08-09','2018-09-05']
    shared_date_li = list(pd.date_range(start=공통시간축[0], end=공통시간축[1], freq='D'))
    len(shared_date_li)

    print(len(news_df))
    news_df = news_df[ news_df['입력일시'].ge(공통시간축[0]) ]
    print(len(news_df))
    news_df = news_df[ news_df['입력일시'].le(공통시간축[1]) ]
    print(len(news_df))

    print(len(tw_df))
    tw_df = tw_df[ tw_df['created_at'].ge(공통시간축[0]) ]
    print(len(tw_df))
    tw_df = tw_df[ tw_df['created_at'].le(공통시간축[1]) ]
    print(len(tw_df))

    return news_df, tw_df

def predicted_값_범위가_동일해야_한다(news_df, tw_df):
    import __list as lh
    print('\n' + '='*60 + inspect.stack()[0][3])

    news_g = news_df.groupby('predicted').count().loc[:, ['news_id']]
    tw_g = tw_df.groupby('predicted').count().loc[:,['tw_id']]

    news_prd_li = list(news_g.index)
    tw_prd_li = list(tw_g.index)
    intc_li = lh.리스트1과_리스트2의_교집합을_찾기(li1=news_prd_li, li2=tw_prd_li)
    print({'len(intc_li)':len(intc_li)})

    print(len(news_df))
    news_df = news_df[ news_df['predicted'].isin(intc_li) ]
    print(len(news_df))

    news_g = news_df.groupby('predicted').count().loc[:, ['news_id']]
    print(len(news_g))

    return news_df, tw_df, intc_li

def XX_g_검사():
    print('\n' + '='*60 + inspect.stack()[0][3])

    news_g = news_df.groupby('predicted').count().loc[:, ['news_id']]
    print(len(news_g))
    news_g = news_g.sort_values('news_id', ascending=False).head()

    tw_g = tw_df.groupby('predicted').count().loc[:, ['tw_id']]
    print(len(tw_g))
    tw_g = tw_g.sort_values('tw_id', ascending=False).head()

    return news_g, tw_g

def 특정사건들에_대한_상관관계_계산(news_df, tw_df, intc_li):
    import Report
    print('\n' + '='*60 + inspect.stack()[0][3])

    intc_li = sorted(intc_li)
    intc_li_len = len(intc_li)
    i=1
    corr_dicli = []
    for event_num in intc_li:
        print('\n' + '-'*60 + '{}/{}, event_num:{}'.format(i, intc_li_len, event_num))

        news_g = news_df[ news_df['predicted']==event_num ].groupby('입력일시').count().loc[:, ['news_id']]
        tw_g = tw_df[ tw_df['predicted']==event_num ].groupby('created_at').count().loc[:,['tw_id']]
        print({'news_g_len':len(news_g)})
        print({'tw_g_len':len(tw_g)})
        #print(news_g)
        #print(tw_g)

        """= = = = = = = = = = = = = = = 합치기 = = = = = = = = = = = = = = =
        -> 시간인덱스를 변경해가며 합치기
        """
        print('\n' + '= '*30 + '합치기')
        news_data = Report.TimeResampled_data(df=news_g, rsp_period='24H', agg='sum')
        tw_data = Report.TimeResampled_data(df=tw_g, rsp_period='24H', agg='sum')

        corr_dic = pd_corr(news_data, tw_data)
        corr_dic['event_num'] = event_num
        corr_dicli.append(corr_dic)

        i+=1
        #break
    return corr_dicli

def pd_corrwith(news_data, tw_data):
    print('\n' + '='*60 + inspect.stack()[0][3])

    news_data = news_data.rename(columns={'news_id':'event_cnt'})
    tw_data = tw_data.rename(columns={'tw_id':'event_cnt'})
    corr = news_data.corrwith(tw_data, axis=1, drop=True)
    print(corr)
    print(corr.describe())

def pd_corr(news_data, tw_data):
    print('\n' + '='*60 + inspect.stack()[0][3])

    tw_len = len(tw_data)
    news_len = len(news_data)
    if news_len >= tw_len:
        cmb_data = news_data.join(tw_data)
    else:
        cmb_data = tw_data.join(news_data)
    print(cmb_data)

    corr = cmb_data.corr()
    corr = corr.fillna(0)
    print(corr)
    print(corr.values[0][1])
    print(corr.values[1][0])
    print(corr.describe())
    corr_val = {'01':corr.values[0][1], '10':corr.values[1][0]}
    return corr_val

def CorrCeffErr_cross_inspection(corr_df):
    print('\n' + '='*60 + inspect.stack()[0][3])

    corr_df['err'] = corr_df['01'] - corr_df['10']
    corr_err = corr_df[ corr_df['err'] != 0 ]
    return corr_err

"""
============================================================
논문 삽입용 코드
============================================================
def CorrCoeff_Calculation_by_event(news_df, tw_df, intersections):
    import Report

    corr_dicli = []
    for event_num in intersections:
        news_g = news_df[ news_df['predicted']==event_num ].groupby('입력일시').count().loc[:, ['news_id']]
        tw_g = tw_df[ tw_df['predicted']==event_num ].groupby('created_at').count().loc[:,['tw_id']]

        news_data = Report.TimeResampled_data(df=news_g, rsp_period='24H', agg='sum')
        tw_data = Report.TimeResampled_data(df=tw_g, rsp_period='24H', agg='sum')

        if len(news_data) >= len(tw_data):
            cmb_data = news_data.join(tw_data)
        else:
            cmb_data = tw_data.join(news_data)
        print(cmb_data)

        corr = cmb_data.corr()
        corr = corr.fillna(0)
        corr_val = {'01':corr.values[0][1], '10':corr.values[1][0]}
        corr_dic['event_num'] = event_num
        corr_dicli.append(corr_dic)

    return corr_dicli
"""
