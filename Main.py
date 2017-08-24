# -*- coding:utf-8 -*-
# -*- coding:gbk -*-
# __@author__Keen
import numpy as np
from TextHandle import TextProcess
from BosonAna import BosonAnalysis
from VisualView import VisualView
from FreqInfer import FreqInfer
# from timeshaft import timeshaft
from JdValue import get_price
from MongoData import SourceData
from GenHtml import GenHtml
from collections import defaultdict

from Dict_Infer import DictInfer
from WaitFor import wait_for
from collections import Counter
import requests
import pickle
from sys import argv
import math
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def Main():
    wechatId = 'ququhk123'
    info = defaultdict()
    info['wechat'] = wechatId
    SD = SourceData(wechatId)
    GH = GenHtml(wechatId)
    #SD.df_handle()
    with open('Dict_Info.pkl', 'r') as f:
        Dict_Info = pickle.load(f)

    with open('sense.pkl', 'r') as f:
        sense = pickle.load(f)
    with open('entity.pkl', 'r') as f:
        entity = pickle.load(f)

    DI = DictInfer(Dict_Info)

    if not os.path.exists('/share/disk0/nlpdata/'+wechatId):
        os.mkdir('/share/disk0/nlpdata/'+wechatId)


    wechatId, nickname, time, life_concern, work_concern, title, source_name, loc = SD.get_source()
    sleep_time, wake_up_time = DI.time_infer(time)
    hour_sleep = int(sleep_time)
    min_sleep = int((sleep_time-hour_sleep) * 60)
    if hour_sleep >=24:
        hour_sleep = hour_sleep-24
    hour_wake = int(wake_up_time)
    min_wake = int((wake_up_time-hour_wake)*60)

    wake = '起床时间: %d 时 %d 分' % (hour_wake, min_wake)
    sleep = '睡觉时间: %d 时 %d 分' % (hour_sleep, min_sleep)

    pos = {'pos_noun' : ['n', 'nr', 'nr1', 'nr2', 'nrj', 'nrf', 'ns', 'nsf', 'nt', 'nz', 'nl', 'ng', 'eng'],
           'pos_adj' : ['a', 'ad', 'an', 'ag', 'al'],
           'pos_verb' : ['vd', 'vn', 'vf', 'vx', 'vi', 'vl', 'vg']}

    #time_info = timeshaft(life_concern, createtime)

    TP = TextProcess(pos)
    noun_life, adj_life, verb_life = TP.get_pos(life_concern, pos = pos)
    noun_work, adj_work, verb_work = TP.get_pos(work_concern, pos = pos)
    #noun_title, adj_title, verb_title = TP.get_pos(title, pos=pos)

    num1, words_life = TP.seg_words(life_concern)
    num2, words_work = TP.seg_words(work_concern)
    # num3, words_title = TP.seg_words(title)
    # num4, words_source = TP.seg_words(source_name)
    location_final = DI.location_infer(life_concern, work_concern, source_name)
    sex = DI.sex_infer(num1, words_life, source_name)
    kid = DI.kid_infer(num1, words_life, words_work, source_name)
    university = DI.university_infer(words_life, source_name)
    marriage = DI.marriage_infer(num1, words_life, kid)
    kid, marriage, age = DI.age_infer(num1, words_life,source_name, kid, marriage)
    graduation = DI.graduation_infer(num1, words_life, source_name)

    res1, res2 = DI.important_time(life_concern)
    house = DI.house_infer(num1, words_life,source_name)
    income = DI.income_infer(num1, words_life, house, location_final)
    car = DI.car_infer(num1, words_life,source_name,income)
    if age == '相关信息不足':
        age = res1
    if university == '相关信息不足':
        university = res2
    print (sex)
    print (kid)
    print (marriage)
    print (age)
    print (graduation)
    print (university)
    print (car)
    print (house)
    print (income)
    print (location_final)
 
    dic_noun_life= TextProcess.get_freq2plot(noun_life)
    dic_adj_life = TextProcess.get_freq2plot(adj_life)
    dic_verb_life = TextProcess.get_freq2plot(verb_life)
# #
    dic_noun_work = TextProcess.get_freq2plot(noun_work)
    dic_adj_work = TextProcess.get_freq2plot(adj_work)
    dic_verb_work = TextProcess.get_freq2plot(verb_work)
# #
    #dic_noun_title = TextProcess.get_freq2plot(noun_title)
   # freq = sorted(dic_noun_work.items(), key=lambda d: d[1], reverse=True)
#
    item2plot_noun_life = TextProcess.item2plot(dic_noun_life)
    item2plot_adj_life = TextProcess.item2plot(dic_adj_life)
    item2plot_verb_life = TextProcess.item2plot(dic_verb_life)
#
    item2plot_noun_work = TextProcess.item2plot(dic_noun_work)
    item2plot_adj_work = TextProcess.item2plot(dic_adj_work)
    item2plot_verb_work = TextProcess.item2plot(dic_verb_work)
#
    #sense, entity = BosonAnalysis.Bosonanalysis(life_concern[0:4000])
    #topics = BosonAnalysis.topic_infer(title)
    #sense, topics, entity = BosonAnalysis.Bosonanalysis(life_concern)
    #
    location, relationship, organization, product, company = FreqInfer.separate_entity(entity)
#
    company.extend(organization)
    #loc1, loc2 = FreqInfer.direct_infer(location)
    relation = FreqInfer.direct_infer(relationship)
    #co1, co2 = FreqInfer.direct_infer(company)
    #d = FreqInfer.work_infer(dic_noun_work)
#
#
    product = list(set(product))
    product_new = []
    value = 0
    for item in product:
        price = get_price(item.encode('utf-8'))
        if not math.isnan(price):
            product_new.append('('+' '.join([item, str(int(price))])+'元)')
            value = value + price
    info['nickname'] = nickname
    info['sex'] = sex
    info['kid'] = kid
    info['marriage'] = marriage
    info['graduation'] = graduation
    info['university'] = university
    info['car'] = car
    info['age'] = age
    info['house'] = house
    info['income'] = income
    info['location'] = location_final
    # info['loc1'] = loc1
    # info['loc2'] = ' '.join(loc2)
    info['relation'] = relation
    # info['sub_relation'] = ' '.join(relation2)
    # info['company'] = ' '.join(co1)

    info['product'] = '\t'.join(product_new)
    info['value'] = str(value)
    info['wake'] = wake
    info['sleep'] = sleep
    # info['domain'] = ' '.join(d)
    # info['age'] = '\n'.join(time_info)
    #
    # with open('info.pkl', 'w+') as fid:
    #     pickle.dump(info, fid)
    if len(relationship) != 0:
        VisualView.social_network(relationship, wechatId,1)
    if len(company) != 0 or len(organization)!=0:
        company.extend(organization)
        VisualView.social_network(company, wechatId, 2)
    if sense != 0:
        VisualView.get_emotion_plot(sense, wechatId)
    if len(dic_noun_life) != 0:
        VisualView.get_wordcloud(dic_noun_life, wechatId)
    if len(time) != 0:
        VisualView.get_time_plot(time, wechatId)

    if len(life_concern) != 0:
        VisualView.get_word_plot1(item2plot_noun_life, item2plot_adj_life, item2plot_verb_life, wechatId,1)
    if len(work_concern) != 0:
        VisualView.get_word_plot1(item2plot_noun_work, item2plot_adj_work, item2plot_verb_work, wechatId,2)
    # VisualView.get_word_plot2(item2plot_noun_work, item2plot_adj_work, item2plot_verb_work, wechatId,2)


 #
    GH.gen_html(info)
    requests.post('http://nlp.credoo.org/api/v1/notify/done', data={'wechatId': wechatId})
    return True

if __name__ == '__main__':
    Main()
