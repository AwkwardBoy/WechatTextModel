# -*- coding:utf-8 -*-
# -*- coding:gbk -*-
# __@author__Keen
from collections import Counter
from collections import defaultdict
from TextHandle import TextProcess
import numpy as np
class FreqInfer(object):

    @staticmethod
    def separate_entity(entity):
        location = []
        relationship = []
        organization =[]
        product = []
        company = []
        for item in entity:
            word, name = item
            if name == 'location':
                location.append(word)
            elif name == 'person_name':
                relationship.append(word)
            elif name == 'org_name':
                organization.append(word)
            elif name == 'product_name':
                product.append(word)
            elif name == 'company_name':
                company.append(word)
        return (location, relationship, organization, product, company)


    @staticmethod
    def direct_infer(entity):
        freq = Counter(entity)
        result1 = freq.most_common(3)
        result = []
        for item in result1:
            name, value = item
            result.append(name)
        result = ' '.join(result)
        return result

    @staticmethod
    def work_infer(dic):
        freq = sorted(dic.items(), key=lambda d: d[1], reverse=True)
        domain = freq[0:5]
        d = []
        for item in domain:
            name, num = item
            d.append(name)
        return d

'''
    @staticmethod
    def person_info(noun, group):
        label = []
        group1 = []
        group2 = []
        group3 = []
        group4 = []
        for line in noun:
            line = line.strip().split(' ')
            for word in line:
                if word in group['普通上班族']:
                    group1.append(word)
                elif word in group['学生党']:
                    group2.append(word)
                elif word in group['技术人员']:
                    group3.append(word)
                elif word in group['公司高层']
                # --------------------
                # 可以增加其他类别
                # -------------------
        label.append(Counter(group1).most_common(1)[0][1])
        label.append(Counter(group2).most_common(1)[0][1])
        label.append(Counter(group3).most_common(1)[0][1])
        label.append(Counter(group4).most_common(1)[0][1])
        cate = np.argmax(label) + 1
        if cate == 1:
            cate = '普通上班族'
        elif cate == 2:
            cate = '学生党'
        elif cate == 3:
            cate = '技术人员'
        return cate

    @staticmethod
    def concern_domain(work_noun):
        dic = TextProcess.get_freq2plot(work_noun)
        freq = sorted(dic.items(), key=lambda d: d[1], reverse=True)
        n = 5
        concern = []
        for i in range(n):
            item, t = freq[i]
            concern.append(item)
        return concern
'''
