# -*- coding:utf-8 -*-
# -*- coding:gbk -*-
# __@author__Keen
import multiprocessing
from TextHandle import seg_sentence
from gensim.models import Word2Vec

import logging

class MySentence(object):
    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        for line in open(self.filename, 'r'):
            yield line.split(' ')



logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)

sentence = MySentence('all_corpus.txt')
# sentence = word2vec.Text8Corpus('all_corpus.txt')
# sentence2 = word2vec.Text8Corpus('total_doc.txt')
#
My_model = Word2Vec(sentence, min_count=0, iter=5, size=100, window=10,workers=multiprocessing.cpu_count())

#My_model.train(sentence2, total_examples=65, epochs = 5)
My_model.save('myModel4test')


