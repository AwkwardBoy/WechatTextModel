# -*- coding:utf-8 -*-
# -*- coding:gbk -*-
# __@author__Keen
import pickle
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from collections import Counter
from sklearn.externals import joblib
from gensim.models import word2vec
# 获取所有的用户ID以获取语料库
# IDs = []
# fid1 = open('all_wechat_id.txt', 'r')
# fid2 = open('gender.txt','r')
# lines1 = fid1.readlines()
# lines2 = fid2.readlines()
# labels = []
# for line1 in lines1:
#     IDs.append(line1.strip())
#
# for line2 in lines2:
#     labels.append(int(line2.strip()))
#
# with open('labels.pkl', 'w+') as f:
#     pickle.dump(labels, f)
# doc_total = open('total_doc.txt', 'w+')
# total_seg_words = []
# for id in IDs:
#     SD = SourceData(id)
#     wechat_id, nickname,time, life_concern, work_concern, title, source_name = SD.get_source()
#     life_words = seg_words(life_concern)
#     work_words = seg_words(work_concern)
#     life_words.extend(work_words)
#     life_words.extend(source_name)
#     life_words.insert(0, nickname)
#     if life_concern != []:
#         doc_total.write(' '.join(life_words).strip())
#         doc_total.write('\n')
#
# doc_total.close()
with open('labels.pkl', 'r') as f:
    labels = pickle.load(f)
fid = open('total_doc.txt','r')
corpus = []

My_model = word2vec.Word2Vec.load('myModel')
X = []
for line in fid.readlines():
    if line.strip() != '':
        words = line.strip().split(' ')
        word_mat = []
        for word in words:
            try:
                word_vec = My_model[word.decode('utf-8')]
                word_mat.append(word_vec)
            except(KeyError):
                pass
        word_vec = np.mean(word_mat, axis=0)
        X.append(word_vec)




# vectorizer = CountVectorizer()
# transformer = TfidfTransformer()

# X1 = vectorizer.fit_transform(corpus)
# X2 = transformer.fit_transform(X1.toarray())


pca = PCA(n_components=30)
reduce_X = pca.fit_transform(X)

labels = np.array(labels)
labels[labels==-1] = 0

print labels
print np.bincount(labels)
clf = SVC(C=1.0,kernel='linear',class_weight={1:2.3})
rf = clf.fit(np.array(X), labels)
n_row, n_col = reduce_X.shape
result = []
for i in range(n_row):
    gender = rf.predict(np.array(X[i]).reshape(1,100))
    result.append(gender[0])

print result
print Counter(result)
joblib.dump(rf, 'clf.model')
# XY = np.hstack((reduce_X,labels))
# XY11 = XY[XY[:,-1]==1][:,8]
# XY12 = XY[XY[:,-1]==1][:,13]
# XY21 = XY[XY[:,-1]==-1][:,8]
# XY22 = XY[XY[:,-1]==-1][:,13]
# print len(XY11)
# print len(XY21)
# ax = plt.subplot(111)
# ax.plot(XY11,XY12,'.',color='r')
# ax.plot(XY21,XY22,'.',color='b')
# plt.show()