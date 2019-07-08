
import os
os.getcwd()
import sys
sys.path.append("/Users/sambong/pjts/inews/env/lib/python3.7/site-packages")
sys.path.append("/Users/sambong/pjts/libs/i-nlp")
sys.path.append("/Users/sambong/pjts/libs/idebug")
sys.path
other_pjts = ['stock']
for other in other_pjts:
    path = f"/Users/sambong/pjts/{other}/env/lib/python3.7/site-packages"
    sys.path.remove(path)
sorted(sys.path)
%env GOOGLE_AUTH_PATH=/Users/sambong/pjts/libs/igoogle/igoogle-auth.json
%env ETRI_ACCESS_KEY=8393a2fc-eb89-4bf3-993f-a35f9df007a0
import pprint
pp = pprint.PrettyPrinter(indent=2)


from inews import models, etri
import idebug as dbg
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
from pandas.io.json import json_normalize
import copy

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn import metrics



#============================================================
"""Loading the 20 newsgroups dataset."""
"""sklearn의 기본 vectorizer의 토큰화의 약점을 보완하기 위해 ETRIAI 를 사용해서 vectorizer한다."""
#============================================================

def get_dataset():
    targetmodel = 'Article__네이버'
    targetcol = 'headline'
    techname = 'LangAnalysis'
    apicode = 'srl'
    method = 'morp'
    """NNG(일반명사), NNP(고유명사), NNB(의존명사) 중 NNB는 제외."""
    type_regex = '^NN[GP]'
    df = etri.load_results(targetmodel, targetcol, techname, apicode, method, type_regex)

    """traindf와 testdf를 분리한다."""
    train_idxes = np.random.choice(a=list(df.index), size=1000, replace=False)
    TF = df.index.isin(train_idxes)
    traindf = df[TF]
    testdf = df[~TF]
    traindf = traindf.drop_duplicates(keep='first',subset=['noun_txt'])
    return traindf, testdf

traindf, testdf = get_dataset()

class UnsupervisedLearning:
    """
    Clustering train_data.
    Training a classifier.
    Predict test_data.
    """
    def __init__(self, traindf, testdf, n_clusters=100):
        self.traindf = traindf
        self.testdf = testdf
        self.vectorizer = CountVectorizer()
        self.tfidf_transformer = TfidfTransformer()
        self.cluster = KMeans(n_clusters=n_clusters, random_state=0)

    def clustering(self):
        """이미 분류된 traindf가 없기 때문에 별도로 클러스터링 해야 한다."""
        fr = dbg.Function(inspect.currentframe()).report_init()
        self.X_train_counts = self.vectorizer.fit_transform(list(self.traindf.noun_txt))
        self.X_train_tfidf = self.tfidf_transformer.fit_transform(self.X_train_counts)
        cluster = self.cluster.fit(self.X_train_tfidf.toarray())
        self.traindf['label'] = cluster.labels_
        fr.report_fin()
        return self

    def classify(self, algorithm):
        fr = dbg.Function(inspect.currentframe()).report_init()
        traindf = self.traindf.copy()
        if algorithm == 'MultinomialNB':
            self.clf = Pipeline([
                ('vect', self.vectorizer),
                ('tfidf', self.tfidf_transformer),
                ('clf', MultinomialNB()),
            ])
            self.clf.fit(list(traindf.noun_txt), list(traindf.label))
        elif algorithm == 'SGDClassifier':
            self.clf = Pipeline([
                ('vect', self.vectorizer),
                ('tfidf', self.tfidf_transformer),
                ('clf', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, random_state=42,max_iter=5, tol=None)),
            ])
            self.clf.fit(list(traindf.noun_txt), list(traindf.label))
        else:
            self.clf = None
        if self.clf is not None:
            self.predicted = self.clf.predict(list(self.testdf.noun_txt))
            self.testdf['predicted'] = self.predicted
        fr.report_fin()
        return self

usp = UnsupervisedLearning(traindf, testdf, 100)
usp.clustering()
usp1 = copy.deepcopy(usp)
usp1.classify('MultinomialNB')
usp2 = copy.deepcopy(usp)
usp2.classify('SGDClassifier')

#============================================================
"""Evaluation of the performance on the test set."""
#============================================================

"""분리된 벡터화-단어빈도수-분류화 Predict 절차."""
"""Pipeline으로 한번에 Predict."""

usp1.traindf.reindex(columns=['label','docid']).groupby('label').count().T
usp2.traindf.reindex(columns=['label','docid']).groupby('label').count().T

usp1.testdf.reindex(columns=['predicted','docid']).groupby('predicted').count().T
usp2.testdf.reindex(columns=['predicted','docid']).groupby('predicted').count().T

usp1.traindf.query('label == "0"').sort_values('noun_txt')
usp1.testdf.query('predicted == "0"').sort_values('noun_txt')
usp2.traindf.query('label == "0"').sort_values('noun_txt')
usp2.testdf.query('predicted == "0"').sort_values('noun_txt')

#============================================================
"""Parameter tuning using grid search."""
#============================================================
