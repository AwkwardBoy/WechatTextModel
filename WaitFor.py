# -*- coding:utf-8 -*-
# -*- coding:gbk -*-
# __@author__Keen
import time
import requests

def wait_for(interval):
    wechatId = 'no wechat Id'
    start_job=True
    while start_job:
        message = do_work()
        if message == []:
            time.sleep(interval)
        else:
            start_job=False
            wechatId = message[0]['wechatId']
    return wechatId

def do_work():
    url = 'http://nlp.credoo.org/api/v1/notify/status'
    r = requests.post(url)
    info = eval(str(r.text))
    return info['data']

