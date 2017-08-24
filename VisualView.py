# -*- coding:utf-8 -*-
# -*- coding:gbk -*-
# __@author__Keen
from scipy.misc import imread
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import collections
from collections import Counter
from wordcloud import WordCloud, ImageColorGenerator
from scipy.interpolate import spline
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class VisualView(object):


    @staticmethod
    def get_wordcloud(freq, wechatId):

        back_color = imread('credoo.jpeg')
        wc = WordCloud(background_color='white',
                       max_words=1500,
                       mask = back_color,
                       font_path = 'Songti.ttc',
                       max_font_size=100,
                       random_state=30)

        wc.generate_from_frequencies(freq)
        image_colors = ImageColorGenerator(back_color)
        plt.figure(figsize=(12,10))
        plt.imshow(wc)
        plt.axis('off')
        plt.savefig('/share/disk0/nlpdata/'+wechatId+'/word_cloud.png')
        return True

    @staticmethod
    def get_word_plot1(item2plot1,item2plot2,item2plot3,wechatId,num):
        noun, num1 = item2plot1
        plt.figure(figsize=(12,10))
        ax1 = plt.subplot(1,3,1)
        if len(noun)>=10:
            noun = noun[:10]
            num1 = num1[:10]
        y_pos1 = np.arange(len(noun))
        ax1.barh(y_pos1, num1, align='center', color='lightblue')
        ax1.set_yticks(y_pos1)
        ax1.set_yticklabels(noun)
        ax1.invert_yaxis()
        ax1.set_xlabel('Frequency')
        ax1.set_title('名词')

        adj, num2 = item2plot2
        if len(adj) >= 10:
            adj = adj[:10]
            num2 = num2[:10]
        ax2 = plt.subplot(1, 3, 2)
        y_pos2 = np.arange(len(adj))
        ax2.barh(y_pos2, num2, align='center', color='pink')
        ax2.set_yticks(y_pos2)
        ax2.set_yticklabels(adj)
        ax2.invert_yaxis()
        ax2.set_xlabel('Frequency')
        ax2.set_title('形容词')

        verb, num3 = item2plot3
        if len(verb) >= 10:
            verb = verb[:10]
            num3 = num3[:10]
        ax3 = plt.subplot(1, 3, 3)
        y_pos3 = np.arange(len(verb))
        ax3.barh(y_pos3, num3, align='center', color='orange')
        ax3.set_yticks(y_pos3)
        ax3.set_yticklabels(verb)
        ax3.invert_yaxis()
        ax3.set_xlabel('Frequency')
        ax3.set_title('动词')
        plt.savefig('/share/disk0/nlpdata/'+wechatId+'/word_freq'+str(num)+'.png')
        return True

    # @staticmethod
    # def get_word_plot2(item2plot1,item2plot2,item2plot3,wechatId,num):
    #     noun, num1 = item2plot1
    #     plt.figure(figsize=(12,10))
    #     ax4 = plt.subplot(1,3,1)
    #     y_pos = np.arange(len(noun))
    #     ax4.barh(y_pos, num1, align='center', color='lightblue')
    #     ax4.set_yticks(y_pos)
    #     ax4.set_yticklabels(tuple(noun))
    #     ax4.invert_yaxis()
    #     ax4.set_xlabel('Frequency')
    #     ax4.set_title('名词')
    #
    #     adj, num2 = item2plot2
    #     ax5 = plt.subplot(1, 3, 2)
    #     ax5.barh(y_pos, num2, align='center', color='pink')
    #     ax5.set_yticks(y_pos)
    #     ax5.set_yticklabels(tuple(adj))
    #     ax5.invert_yaxis()
    #     ax5.set_xlabel('Frequency')
    #     ax5.set_title('形容词')
    #
    #     verb, num3 = item2plot3
    #     ax6 = plt.subplot(1, 3, 3)
    #     ax6.barh(y_pos, num3, align='center', color='orange')
    #     ax6.set_yticks(y_pos)
    #     ax6.set_yticklabels(tuple(verb))
    #     ax6.invert_yaxis()
    #     ax6.set_xlabel('Frequency')
    #     ax6.set_title('动词')
    #     plt.savefig('/share/disk0/nlpdata/'+wechatId+'/word_freq'+str(num)+'.png')
    #     return True

    @staticmethod
    def social_network(entity, wechatId, num):
        new_entity = []
        for item in entity:
            if item not in new_entity:
                new_entity.append(item)
        plt.figure(figsize=(12, 10))
        G = nx.Graph()
        G.add_node('客户主体')
        edges = []
        for entities in new_entity:
            edges.append((entities,'客户主体'))
        G.add_edges_from(edges)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, node_color='b', node_size=800, with_labels=True, alpha=0.3, font_size=15)
        plt.savefig('/share/disk0/nlpdata/' + wechatId + '/social'+str(num)+'.png')
        return True

    @staticmethod
    def get_ER(entity,wechatId):
        dic = collections.defaultdict()
        for item in entity:
            word, ent = item
            if ent not in dic.keys():
                dic[ent] = []
                dic[ent].append(word)
            else:
                if word not in dic.values():
                    dic[ent].append(word)
        plt.figure(figsize=(12,10))
        G = nx.Graph()
        G.add_node('客户主体')
        edges = []
        for item in dic['person_name']:
            edges.append((item,'客户主体'))
        G.add_edges_from(edges)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, node_color='b', node_size=800, with_labels=True, alpha=0.3, font_size=15)
        plt.savefig('/share/disk0/nlpdata/'+wechatId+'/E_R.png')

        plt.figure(figsize=(12,10))
        G1 = nx.Graph()
        G1.add_node('客户主体')
        edges1 = []
        for item in dic['company_name']:
            edges1.append((item,'客户主体'))
        G1.add_edges_from(edges1)
        pos1 = nx.spring_layout(G1)
        nx.draw(G1,pos1, node_code='b', node_size=800, with_labels=True, alpha=0.3, font_size=15)
        plt.savefig('/share/disk0/nlpdata/'+wechatId+'/company.png')

        return True

    @staticmethod
    def get_emotion_plot(sense, wechatId):
        positive = 0
        negative = 0
        for emotion in sense:
            positive = positive + emotion[0]
            negative = negative + emotion[1]
        plt.figure(figsize=(12,10))
        ax = plt.subplot(111)
        labels = ['positive', 'negative']
        sizes = [positive, negative]
        explode = (0, 0.1)
        ax.pie(sizes, explode=explode, labels = labels, autopct='%1.1f%%', shadow=False, startangle=90)
        ax.pie([1], radius=0.5, colors='w')
        ax.axis('equal')
        ax.set_title('情绪分析')
        plt.savefig('/share/disk0/nlpdata/'+wechatId+'/emotion.png')
        return True

    @staticmethod
    def get_topic_pie(topics,wechatId):
        concern = []
        for topic in topics:
            if topic[0] == 0:
                concern.append('体育')
            elif topic[0] == 1:
                concern.append('教育')
            elif topic[0] == 2:
                concern.append('财经')
            elif topic[0] == 3:
                concern.append('社会')
            elif topic[0] == 4:
                concern.append('休闲')
            elif topic[0] == 5:
                concern.append('军事')
            elif topic[0] == 6:
                concern.append('国内')
            elif topic[0] == 7:
                concern.append('科技')
            elif topic[0] == 8:
                concern.append('互联网')
            elif topic[0] == 9:
                concern.append('房产')
            elif topic[0] == 10:
                concern.append('国际')
            elif topic[0] == 11:
                concern.append('生活')
            elif topic[0] == 12:
                concern.append('汽车')
            elif topic[0] == 13:
                concern.append('游戏')
        item2plot = Counter(concern)
        labels = item2plot.keys()
        sizes = item2plot.values()
        plt.figure(figsize=(12,10))
        ax = plt.subplot(111)
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
        ax.axis('equal')
        plt.savefig('/share/disk0/nlpdata/'+wechatId+'/topic.png')
        return True

    @staticmethod
    def get_time_plot(time, wechatId):
        hour = []
        weekdays = []
        for item in time:
            T = item.hour
            hour.append(T)
            weekdays.append(item.weekday())

        hour_new = Counter(hour)
        weekdays = Counter(weekdays)
        weekdays_new = []
        t = []
        freq = []
        for item in hour_new.items():
            a, b =item
            t.append(a)
            freq.append(b)

        t_new = np.linspace(0,24,300)
        freq_smooth = spline(t,freq,t_new)
        plt.figure(figsize=(24,10))
        ax1 = plt.subplot(121)
        ax1.hist(hour,47)
        week = ('星期一','星期二','星期三','星期四','星期五','星期六','星期天')
        ax1.plot(t_new,freq_smooth)
        ax1.set_xlabel('发表时间')
        ax1.set_ylabel('发朋友圈频次')
        ax1.set_title('时间分布')
        ax1.set_xlim((0,24))
        ax1.set_ylim((0,np.max(freq)+10))
        for i in range(7):
            weekdays_new.append(weekdays[i])
        width = 0.5

        ax2 = plt.subplot(122)
        ax2.bar(np.arange(len(week)),weekdays_new,width,color='pink', align = 'center')
        ax2.set_xlabel('星期')
        ax2.set_ylabel('发表朋友圈频次')
        ax2.set_xticks(np.arange(len(week)))
        ax2.set_xticklabels(week)
        ax2.set_title('星期分布')
        plt.savefig('/share/disk0/nlpdata/'+wechatId+'/week_plot.png')
        return True
