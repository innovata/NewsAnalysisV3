

import __sklearn as skl
import pandas as pd
from datetime import datetime
import News_ as news_
import News as news
LA = news.LangAnalysis

TBL명 = '뉴스_클러스터'



def my_cluster(벡터화tbl명=LA.TBL명, 벡터화col명='뉴스본문srl_WSDNNGli', 표본샘플링수=10, n_clusters=3, crt_pnt=0.4, clst_algthm='MiniBatchKMeans', dbg_on=False):
    """
    뉴스본문srl_WSDNNGli 중첩 명사에 대해 클러스터 -> "뉴스본문srl_WSDNNGli" 컬럼 사용
    뉴스본문srl_WSDNNGli 에 대한 중복제거 후 클러스터 -> "뉴스본문srl_WSDNNGli_중복제거" 컬럼 사용
    """

    """
    ============================== 로딩 ==============================
    """
    print('\n'+'='*60+'로딩')
    query = {벡터화col명:{'$ne':None}}
    projection = {'뉴스id':1, 벡터화col명:1}
    df = mg.find(db명=DB명, tbl명=벡터화tbl명, query=query, projection=projection, dbg_on=False, 컬럼순서li=[], df보고형태='df')

    # 원본 기초 청소
    print('\n'+'='*60+'원본 기초 청소')
    df[벡터화col명] = df[벡터화col명].apply(lambda x: sorted(x))
    """
    ============================== 벡터화-트랜스폼-클러스터 ==============================
    {'표본샘플링수': 5000}
    벡터화 루프 실행시간 sec : 446.4348
    """
    from difflib import SequenceMatcher
    # 샘플링
    print('\n'+'='*60+'샘플링')
    df = df.iloc[:표본샘플링수,]
    pp.pprint({'표본샘플링수':표본샘플링수})


    print('\n'+'='*60+'벡터화')
    # 복제
    df61 = df.copy()
    df62 = df.copy()

    dicli61 = df61.to_dict('records')
    dicli62 = df62.to_dict('records')

    # 벡터화 : 1단계. 핵심 부분 -> 근데 죤나 느려
    시작시간 = datetime.now()
    corr_dicli = []
    i=1
    for d61 in dicli61:
        for d62 in dicli62:
            #print('\n'+'-'*60+'{}'.format(i))
            s = SequenceMatcher(isjunk=None, a=d61[벡터화col명], b=d62[벡터화col명], autojunk=True)
            match_ratio = round(s.ratio(), 3)
            #print( match_ratio )
            dic = {
                'src뉴스id':d61['뉴스id'],
                'dst뉴스id':d62['뉴스id'],
                'ratio':match_ratio,
            }
            corr_dicli.append(dic)
            i+=1

    실행시간sec = (datetime.now() - 시작시간).total_seconds()
    print('\n 벡터화 루프 실행시간 sec : {}\n'.format(실행시간sec))
    df7 = pd.DataFrame(corr_dicli)
    """
    ============================== 트랜스폼 ==============================
    """
    print('\n'+'='*60+'트랜스폼')
    print('\n 임계값 : {}\n'.format(crt_pnt))
    pvt = pd.pivot_table(data=df7, values='ratio', index='src뉴스id', columns='dst뉴스id', aggfunc='mean', fill_value=None, margins=False, dropna=True, margins_name='All')
    pvt1 = pvt.applymap(lambda x: 0 if x < crt_pnt else x )
    if dbg_on == True: print('\n pvt1 :\n', pvt1)
    print('\n 임계값 적용후 pvt1 :\n', pvt1)
    X = list(pvt1.values)
    if dbg_on == True: print('\n X :\n', X)
    """
    ============================== 클러스터 ==============================
    """
    print('\n'+'='*60+'클러스터')
    opts, args = skl.doc_cluster.사용자_입력()
    if clst_algthm == 'MiniBatchKMeans': pass
    elif clst_algthm == 'KMeans': opts.minibatch = False


    km = skl.doc_cluster.클러스터링(opts=opts, true_k=n_clusters, X=X, dbg_on=False)
    label_li = km.labels_
    df61['label'] = label_li
    print('\n 유일한 label 개수 : {}\n'.format( len(df61['label'].unique()) ))

    print('\n label 분포현황보고 \n')
    g = df61.groupby('label').count()
    print(g)

    print('\n'+'='*60+'클러스터 결과보고')
    df61 = df61.sort_values('label')
    print(df61)

    print('\n'+'='*60+'클러스터 결과저장')
    """
    """
    저장할_dic = {
        '벡터화tbl명':벡터화tbl명,
        '벡터화col명':벡터화col명,
        '표본샘플링수':표본샘플링수,
        '클러스터결과_dicli':df61.to_dict('records'),
        '벡터화_실행시간sec':실행시간sec,
    }
    query = {'벡터화tbl명':저장할_dic['벡터화tbl명'], '벡터화col명':저장할_dic['벡터화col명'], '표본샘플링수':저장할_dic['표본샘플링수']}
    update = {'$set':저장할_dic}
    mg.update_one(db명=DB명, tbl명='매칭율기반_클러스터결과', query=query, update=update, upsert=True, dbg_on=dbg_on, 사전검증=False)

    return df61
    """
    ============================== 시각화 ==============================
    """
    #Compute_clusterinxg_with_MeanShift(X)

def Compute_clustering_with_MeanShift(X):
    import numpy as np
    from sklearn.cluster import MeanShift, estimate_bandwidth
    from sklearn.datasets.samples_generator import make_blobs

    # #############################################################################
    # Generate sample data
    centers = [[1, 1], [-1, -1], [1, -1]]
    #X, _ = make_blobs(n_samples=10000, centers=centers, cluster_std=0.6)

    # #############################################################################
    # Compute clustering with MeanShift

    # The following bandwidth can be automatically detected using
    bandwidth = estimate_bandwidth(X, quantile=0.2, n_samples=500)

    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(X)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_

    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)

    print("number of estimated clusters : %d" % n_clusters_)

    # #############################################################################
    # Plot result
    import matplotlib.pyplot as plt
    from itertools import cycle

    plt.figure(1)
    plt.clf()

    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    for k, col in zip(range(n_clusters_), colors):
        my_members = labels == k
        cluster_center = cluster_centers[k]
        plt.plot(X[my_members, 0], X[my_members, 1], col + '.')
        plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=14)
    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.show()

"""
sampling = 500 # 10 보다 큰수를 넣는게 당연하지...
n_clusters = int(round(sampling / 10, 0)) if sampling >= 20 else 2
my_cluster(벡터화tbl명=LA.TBL명, 벡터화col명='뉴스제목srl_WSDNNGli', 표본샘플링수=sampling, n_clusters=n_clusters, crt_pnt=0.5, clst_algthm='KMeans', dbg_on=False)
"""
