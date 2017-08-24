# -*- coding:utf-8 -*-
# -*- coding:gbk -*-
# __@author__Keen

import pickle
import numpy as np
from MongoData import SourceData
from TextHandle import seg_words
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from collections import Counter
from gensim.models import word2vec
from sklearn.externals import joblib

My_model = word2vec.Word2Vec.load('myModel')
clf = joblib.load('clf.model')
with open('vectorizer.pkl', 'r') as f1:
    vectorizer = pickle.load(f1)
with open('transformer.pkl', 'r') as f2:
    transformer = pickle.load(f2)
with open('pca.pkl', 'r') as f3:
    pca = pickle.load(f3)

SD = SourceData('euphoria0612')
wechat_id, nickname, time, life_concern, work_concern, title, source_name = SD.get_source()
life_words = seg_words(life_concern)
word_mat = []
for word in life_words:
    try:
        word_vec = My_model[word.decode('utf-8')]
        word_mat.append(word_vec)
    except(KeyError):
        pass

X_new = np.mean(word_mat, axis=0)

print clf.predict(X_new.reshape(1,100))[0]