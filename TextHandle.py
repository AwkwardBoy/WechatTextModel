# -*- coding:utf-8 -*-
# -*- coding:gbk -*-
# __@author__Keen

import jieba.posseg as pseg
import jieba
import collections
import numpy as np
import sys
from sklearn.feature_extraction.text import CountVectorizer
import pickle
reload(sys)
sys.setdefaultencoding('utf-8')

class TextProcess(object):
    def __init__(self, pos):
        self.pos_noun = pos

    @staticmethod
    def get_binary(filename, key):
        fid = open(filename)
        lines = fid.readlines()
        mid = []
        with open('Dict_Info.pkl', 'r') as f:
            Dict_Info = pickle.load(f)
        for line in lines:
            if line.strip() != '':
                mid.append(line.strip())
        Dict_Info[str(key)] = mid
        with open('Dict_Info.pkl', 'w+') as f:
            pickle.dump(Dict_Info,f)

    @staticmethod
    def get_stopwords():
        stop_id1 = open('stopwords.txt', 'r')
        stop_id2 = open('emoji_words.txt', 'r')
        lines1 = stop_id1.readlines()
        lines2 = stop_id2.readlines()
        stopwords = []
        for line in lines1:
            line = line.strip()
            stopwords.append(line)
        for line in lines2:
            line = line.strip()
            stopwords.append(line)
        return stopwords

    def seg_words(self, corpus):
        jieba.load_userdict('user_dict.txt')
        seg_words = []
        stopwords = self.get_stopwords()
        num = 0
        for line in corpus:
            if len(line) == 1:
                if line.strip() != '':
                    num = num + 1
                    words = jieba.cut(line.strip())
                    for word in words:
                        if word != '':
                            if word not in stopwords:
                                if word not in seg_words:
                                    seg_words.append(word)
            else:
                if line[1].strip() != '':
                    num = num + 1
                    words = jieba.cut(line[1].strip())
                    for word in words:
                        if word != '':
                            if word not in stopwords:
                                if word not in seg_words:
                                    seg_words.append(word)

        return (num,seg_words)

    def get_pos(self, corpus, pos):
        print('词性标注中...')
        jieba.load_userdict('user_dict.txt')
        pos_noun = []
        pos_adj = []
        pos_verb = []
        stopwords = self.get_stopwords()
        for line in corpus:
            if line[1] != '':
                noun_line = []
                adj_line = []
                verb_line = []
                words = pseg.cut(line[1].strip())
                for item in words:
                    word, flag = item
                    if word != '':
                        if word not in stopwords:
                            if flag in pos['pos_noun']:
                                if word not in noun_line:
                                    noun_line.append(word)
                            elif flag in pos['pos_adj']:
                                if word not in adj_line:
                                    adj_line.append(word)
                            elif flag in pos['pos_verb']:
                                if word not in verb_line:
                                    verb_line.append(word)
                noun_line = ' '.join(noun_line)
                adj_line = ' '.join(adj_line)
                verb_line = ' '.join(verb_line)
                pos_noun.append(noun_line)
                pos_adj.append(adj_line)
                pos_verb.append(verb_line)
        print('词性标注完成')
        return (pos_noun, pos_adj, pos_verb)

    @staticmethod
    def get_freq2plot(corpus):
        dic = collections.defaultdict()
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(corpus)
        word = vectorizer.get_feature_names()
        X = X.toarray()
        count = np.sum(X, 0)
        m, n = X.shape
        for i in range(n):
            dic[word[i]] = count[i]
        return dic

    @staticmethod
    def item2plot(dic):
        freq = sorted(dic.items(), key=lambda d: d[1], reverse=True)
        pos = []
        num = []
        for item in freq:
            a, b = item
            pos.append(a)
            num.append(b)
        # if len(freq) < 10:
        #     while len(freq) < 10:
        #         freq.append(('None',0))
        #     item2plot = freq
        # else:
        #     item2plot = freq[:10]
        # pos = []
        # num = []
        # for item in item2plot:
        #     a, b = item
        #     pos.append(a)
        #     num.append(b)
        return (pos, num)



'''
    @staticmethod
    def separate_text(filename):
        fid = open(filename, 'r')
        print('分离文本中...')
        lines = fid.readlines()
        length = len(lines)
        f_work = open('work_concern.txt', 'w+')
        f_life = open('life_concern.txt', 'w+')
        f_title = open('title.txt', 'w+')
        for i in range(1, length):
            line = lines[i]
            line = line.split(',')
            if line[4] == '':
                if len(line[5])>:
                    f_life.write(line[5][:100])
                    f_life.write('\n')
                else:
                    f_life.write(line[5].strip())
                    f_life.write('\n')
            else:
                f_title.write(line[4].strip())
                f_title.write('\n')
                f_work.write(line[5].strip())
                f_work.write('\n')
        f_work.close()
        f_life.close()
        return ('life_concern.txt','work_concern.txt','title.txt')
'''
