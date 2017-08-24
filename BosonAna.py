# -*- coding:utf-8 -*-
# -*- coding:gbk -*-
# __@author__Keen
from bosonnlp import BosonNLP
import pickle
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

nlp = BosonNLP('Li03uKMm.16233.EVw-C1d8M1Qv')

class BosonAnalysis(object):

    @staticmethod
    def Bosonanalysis(corpus):
        print('进行语义分析中...')
        sense = []
        entity = []
        #topic = []
        text = []
        mid = []
        n = len(corpus)
        for i in range(n):
            if (i+1) % 10 == 0:
                text.append(' '.join(mid))
                mid = []
            if corpus[i][1].strip() != '':
                mid.append(corpus[i][1].strip())
        for line in text:
            result1 = nlp.ner(line[0:4000], sensitivity=4)[0]
            result2 = nlp.sentiment(line)
            sense.append(result2[0])
            words = result1['word']
            entities = result1['entity']
            entity_mid = []
            for item in entities:
                word = ''.join(words[item[0]:item[1]])
                if (word, item[2].strip()) not in entity_mid:
                    entity_mid.append((word, item[2].strip()))
            entity.extend(entity_mid)
        # entity_line = []
        # result1 = nlp.sentiment(text) 情绪识别暂不做
        # result2 = nlp.ner(text)[0]
        # words = result2['word']
        # entities = result2['entity']
        # # topic.append(nlp.classify(line)) 暂不做分类
        # #if result1[0][0] > result1[0][1]:
        # #    sense.append(1)
        # #else:
        # #    sense.append(-1)
        # for item in entities:
        #     word = ''.join(words[item[0]:item[1]])
        #     if (word,item[2].strip()) not in entity_line:
        #         entity.append((word,item[2].strip()))
        #     entity.extend(entity)
        # print('语义分析完成')
        return (sense, entity)

    @staticmethod
    def topic_infer(corpus):
        topics = []
        for title in corpus:
            topic = nlp.classify(title)
            topics.append(topic)

        return topics

