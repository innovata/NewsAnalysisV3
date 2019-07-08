
# coding: utf-8


# 프로젝트 라이브러리
from thenews.__lib__ import *

# 나의 패키지
import __Twitter as twitter
import __pymongo as mg
import __matplotlib as mpl

# 오픈 패키지
import pandas as pd
import json
from datetime import datetime

# 프로젝트 라이브러리
import News as news
import Layout as lay
import Twitter as twt


# In[3]:


LA = news.LangAnalysis
#.report


# In[4]:


dir(LA)


# In[5]:


LA.TBL명


# In[6]:


mg.TBL_자료구조_보고(db명=DB명, tbl명=LA.TBL명, col_uq=False, 보고제외할col_li=[])


# In[7]:


#la_col = '뉴스제목srl_WSDNNGli'
la_col = '뉴스본문srl_WSDNNGli'


# In[8]:


query = {la_col:{'$ne':None}}
projection = {'뉴스id':1, la_col:1}
df = mg.find(db명=DB명, tbl명=LA.TBL명, query=query, projection=projection, dbg_on=False, 컬럼순서li=[], df보고형태='df')


# In[9]:


# 원본 기초 청소
df[la_col] = df[la_col].apply(lambda x: sorted(x))



# # 명사SEQ 사전 정의
"""
============================== 명사SEQ 사전 정의 ==============================
"""

# In[11]:


dbl_arr = list(df[la_col])


# In[199]:


import re
word_li = []
for arr in dbl_arr:
    for e in arr:
        rs = re.search(r'[가-힝]', e, re.IGNORECASE)
        if rs is None:
            print(e)
        else:
            rs = re.search(r'[\˝\~\!\@\#\$\%\^\&\*\(\)\_\+\{\}\|\[\]\:\"\;\'\<\>\?\,\.\/]', e, re.IGNORECASE)
            if rs is None:
                word_li.append(e)
            else:
                print(rs)
                e = re.sub(pattern=r'[˝]', repl='', string=e, count=0, flags=0)
                print(e)
len(word_li)


# In[ ]:


[]


# In[200]:


df1 = pd.DataFrame({'명사':word_li})
len(df1)


# In[201]:


df1


# In[108]:


df1 = df1.drop_duplicates(subset=None, keep='first', inplace=False)
len(df1)


# In[111]:


df1 = df1.sort_values(by='명사', ascending=True)


# In[112]:


df1['seq'] = range(len(df1))


# In[113]:


df1


# In[118]:


#mg.insert_many(db명=DB명, tbl명='명사SEQ', dicli=df1.to_dict('records'), dbg_on=False, 사전검증=False)


# In[125]:


df1[ df1['명사']=='보수' ].to_dict('records')[0]['seq']


# In[128]:


def 명사양자화(x_li):
    """x는 리스트"""
    y_li = []
    for x in x_li:
        df2 = df1[ df1['명사']==x ]
        if len(df2) is not 0:
            seq = df2.to_dict('records')[0]['seq']
            y_li.append(seq)
    return y_li

df[la_col] = df[la_col].apply(명사양자화)


"""
============================== 원본 df 와 양자화 df0 를 fix ==============================
"""
# # 원본 df 와 양자화 df0 를 fix

# In[297]:


# 양자화
df0


# In[296]:


df


# In[22]:


df[la_col] = df[la_col].apply(lambda x: sorted(x))


# In[131]:


df0


# In[12]:

"""
============================== 클러스터 ==============================
"""

import sys
sys.path.append('/Users/sambong/p/news')
sys.path.append('/Users/sambong/p/lib')
import News as news
import __pymongo as mg
import pandas as pd
import __sklearn as skl


# In[13]:


# df : 원본의 청소
# df0 : 원본의 청소의 양자화


# In[154]:


def 숫자리스트를_문자타입문자열로_변환(x_li):
    x_li = [str(e) for e in x_li]
    s = ' '.join(x_li)
    return s

df01 = df0.copy()
df01[la_col] = df01[la_col].apply(숫자리스트를_문자타입문자열로_변환)


# In[145]:


#df[la_col] = df[la_col].apply(lambda x: x.remove)


# In[172]:


df01


# In[298]:


df1 = df.iloc[:1000,]
#df1 = df.copy()


# In[236]:


df1[la_col] = df1[la_col].apply(lambda x: ' '.join(x))


# In[299]:


df1.head(1)


# In[238]:


X = df1[la_col]#list()


# In[239]:


Tfidf_vect, X_train_counts = skl.lang_train_model.벡터화(X)


# In[240]:


X = X_train_counts.toarray()


# In[225]:


X1 = list(X)[0]
X1 = list(X1)


# In[226]:


sorted(X1, reverse=True)


# In[356]:


print(__doc__)

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


# In[176]:


from pandas.io.json import json_normalize
dicli = df.to_dict('records')
df5 = json_normalize(data=dicli, record_path=la_col, meta='뉴스id', meta_prefix=None, record_prefix=None, errors='raise', sep='.')


# In[178]:


df5 = df5.rename(columns={0:'seq'})


# In[179]:


df5.head(1)


# In[181]:


df5['seq'].corr(df5['뉴스id'], method='spearman')


# # df6 : 수동 벡터화

# In[14]:


df.head(1)


# In[15]:


#df6 = df.iloc[:100,]
df6 = df.copy()


# In[16]:


len(df6)


# In[17]:


df61 = df6.copy()
df62 = df6.copy()


# In[245]:


#df61.corrwith(df62, axis=1)


# In[18]:


#df61.head(1)


# In[289]:


len(df62)


# In[19]:


dicli61 = df61.to_dict('records')
dicli62 = df62.to_dict('records')


# ### 벡터화 : 1단계. 핵심 부분 -> 근데 죤나 느려

# In[20]:


from difflib import SequenceMatcher
corr_dicli = []
i=1
for d61 in dicli61:
    for d62 in dicli62:
        print('\n' + '-'*60 + '{}'.format(i))
        s = SequenceMatcher(isjunk=None, a=d61[la_col], b=d62[la_col], autojunk=True)
#        print(d61, d62)
#        pp.pprint(d61)
#        pp.pprint(d62)
        print( round(s.ratio(), 3) )
        ratio = round(s.ratio(), 3)
        dic = {
            'src뉴스id':d61['뉴스id'],
            'dst뉴스id':d62['뉴스id'],
            'ratio':ratio,
        }
        corr_dicli.append(dic)
        i+=1


# In[306]:


df7 = pd.DataFrame(corr_dicli)
len(df7)


# In[307]:


df7.head(1)


# In[344]:


# 트랜스폼
pvt = pd.pivot_table(data=df7, values='ratio', index='src뉴스id', columns='dst뉴스id', aggfunc='mean', fill_value=None, margins=False, dropna=True, margins_name='All')


# In[345]:


pvt


# In[346]:


crt_pnt = 0.4
pvt1 = pvt.applymap(lambda x: 0 if x < crt_pnt else x )


# In[348]:


pvt1


# In[351]:


pvt1.values


# In[355]:


X = list(pvt1.values)


# In[357]:


sys.path.append('/Users/sambong/p/lib/scikit_learn')
from document_clustering_v3 import *


# In[358]:


opts, args = 사용자_입력()


# In[366]:


km = 클러스터링(opts=opts, true_k=10, X=X, dbg_on=False)


# In[367]:


label_li = km.labels_
label_li


# In[368]:


len(label_li)


# In[362]:


df61.head(1)


# In[369]:


df61['label'] = label_li


# In[370]:


df61


# In[371]:


len(df61['label'].unique())


# In[374]:


df61.sort_values(['label'])


# In[327]:


crt_pnt = 0.4 # critical point
df71 = df7[ df7['ratio'] == 1 ] #-> 제거대상
df72 = df7[ (df7['ratio'] < 1) & (df7['ratio'] > crt_pnt) ] #-> 핵심대상
df73 = df7[ df7['ratio'] == crt_pnt ] #-> 핵심대상
df74 = df7[ (df7['ratio'] < crt_pnt) & (df7['ratio'] > 0) ]
df75 = df7[ df7['ratio'] == 0 ]

print(len(df71))
print(len(df72))
print(len(df73))
print(len(df74))
print(len(df75))


# In[317]:


# 넷 중에 어떤 범위가 의미가 있는가?

df70 = df7[ (df7['ratio'] < 1) & (df7['ratio'] >= crt_pnt) ]


# In[319]:


df70 = df70.sort_values('ratio', ascending=False)
print(len(df70))
df70


# In[320]:


# 의미있는 매칭율을 보유한 df의 src/dst뉴스id의 유일한 리스트를 추출한 후, 그 뉴스제목/본문을 눈으로 검사
li1 = list(df70['src뉴스id'])
li2 = list(df70['dst뉴스id'])


# In[321]:


li = li1 + li2


# In[333]:


query = {'_id':{'$in':li}}
projection = {'뉴스제목':1}
df8 = mg.find(db명=DB명, tbl명=news.TBL명, query=query, projection=projection, dbg_on=False, 컬럼순서li=[], df보고형태='df')


# In[334]:


len(df8)


# In[335]:


df8.sort_values('뉴스제목')


# In[336]:


df81 = df8.join(df70.set_index('src뉴스id'), on='_id')
df81.sort_values('ratio', ascending=False)


# In[337]:


len(df81)


# In[330]:


sorted(df8['뉴스제목'])


# In[ ]:


df
