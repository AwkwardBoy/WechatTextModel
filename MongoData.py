# -*- coding:utf-8 -*-
# -*- coding:gbk -*-
# __@author__Keen
import pandas as pd
from pymongo import MongoClient
import urllib
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SourceData(object):

    def __init__(self, wechatId):
        self.wechatId = wechatId

    @staticmethod
    def _connect_mongo(host, port, username, password, db):

        if username and password:
            mongo_url = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
            conn = MongoClient(mongo_url)
        else:
            conn = MongoClient(host, port)
        return conn[db]

    def read_mongo(self,db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
        db = self._connect_mongo(host=host, port=port, username=username, password=password, db=db)
        fields = ['content.nickname',
                  'wechatId',
                  'content.createtime',
                  'content.sourceNickName',
                  'content.contentObj.title',
                  'content.contentDesc',
                  'content.contentObj.linkUrl',
                  'content.locationInfo.city']
        cursor = db[collection].find(query, projection=fields)
        df = pd.DataFrame(list(cursor))
        return df

    def get_source(self):

        password = urllib.quote_plus('credooP@ssw0rd')
        df = self.read_mongo(db='wechat',
                        collection='moments',
                        query={'wechatId': self.wechatId},
                        host='43.241.218.158',
                        port=27018,
                        username='credoo',
                        password=password)
        wechat_id = df['wechatId'][0]

        life_concern = []
        work_concern = []
        title = []
        source_name = []
        row, col = df.shape
        nickname = 'None'
        time = []
        loc = []
        for i in range(row):
            try:
                create_time = datetime.datetime.fromtimestamp(int(df.iloc[i]['content']['createtime']))
                time.append(create_time)
                if df.iloc[i]['content']['locationInfo']['city'].strip() != '':
                    if '·' in df.iloc[i]['content']['locationInfo']['city'].strip():
                        loc.append((create_time, df.iloc[i]['content']['locationInfo']['city'].split('·')[1].strip()))
                    else:
                        loc.append((create_time,df.iloc[i]['content']['locationInfo']['city'].strip()))
                nickname = df.iloc[1]['content']['nickname']
                if df.iloc[i]['content']['contentObj']['title'] == '':
                    life_concern.append((create_time, df.iloc[i]['content']['contentDesc']))
                else:
                    source_name.append((create_time,df.iloc[i]['content']['sourceNickName']))
                    work_concern.append((create_time,df.iloc[i]['content']['contentDesc']))
                    title.append(df.iloc[i]['content']['contentObj']['title'])
            except (KeyError):
                pass
        return (wechat_id ,nickname,time, life_concern, work_concern, title, source_name, loc)

    def df_handle(self):
        password = urllib.quote_plus('credooP@ssw0rd')
        df = self.read_mongo(db='wechat',
                             collection='moments',
                             query={'wechatId': self.wechatId},
                             host='43.241.218.158',
                             port=27018,
                             username='credoo',
                             password=password)
        wechat_id = []
        life_concern = []
        work_concern = []
        title = []
        source_name = []
        row, col = df.shape
        nickname = []
        time = []
        for i in range(row):
            try:
                create_time = datetime.datetime.fromtimestamp(int(df.iloc[i]['content']['createtime']))
                time.append(create_time)
                wechat_id.append(df['wechatId'][0])
                nickname.append(df.iloc[i]['content']['nickname'])
                if df.iloc[i]['content']['contentObj']['title'] == '':
                    life_concern.append(df.iloc[i]['content']['contentDesc'])
                    source_name.append('')
                    work_concern.append('')
                    title.append('')
                else:
                    life_concern.append('')
                    source_name.append(df.iloc[i]['content']['sourceNickName'])
                    work_concern.append(df.iloc[i]['content']['contentDesc'])
                    title.append(df.iloc[i]['content']['contentObj']['title'])
            except (KeyError):
                pass

        wechat_id = pd.Series(wechat_id)
        # nickname = pd.Series(nickname)
        time = pd.Series(time)
        life_concern = pd.Series(life_concern)
        work_concern = pd.Series(work_concern)
        title = pd.Series(title)
        source_name = pd.Series(source_name)
        df = pd.DataFrame({'id':wechat_id,
                           'time':time,
                           'life':life_concern,
                           'work':work_concern,
                           'title': title,
                           'source':source_name})
        df.to_csv('Emma.csv')
        return True

