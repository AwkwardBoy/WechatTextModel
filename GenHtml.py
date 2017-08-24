# -*- coding:utf-8 -*-
# -*- coding:gbk -*-
# __@author__Keen

from bottle import template, run
class GenHtml(object):
    
    def __init__(self, wechatId):
        self.wechatId = wechatId

    def gen_html(self, infodict):

        template_demo = '''
        <pre style=”word-wrap: break-word; white-space: pre-wrap; white-space: -moz-pre-wrap” >
        <html>
        <head><h1>用户标签分析</h1></head>
        <body>
        <p><h2>客户基本信息</h2></p>
        <p>微信号：{{wechat}}</p>
        <p>昵称：{{nickname}}</p>
        <p>性别：{{sex}}</p>   
        <p>现居地：{{location}}</p>
        <p>年龄范围：{{age}}</p>
        <p>婚姻状况：{{marriage}}</p>
        <p>是否有孩子：{{kid}}</p>
        <p>是否本科毕业：{{graduation}}</p>
        <p>毕业院校：{{university}}</p>
        <p>是否有车：{{car}}</p>
        <p>是否有住房：{{house}}</p>
        <p>收入：{{income}}</p>
        <p>关注人：{{relation}}</p>
        <p><b>生活作息</b></p>
        <p>{{wake}}</p>
        <p>{{sleep}}</p>
        <p>使用或者拥有的产品和价格：{{product}}</p>
        <p><b>情绪分析</b></p>
        <img src='./emotion.png'>
        <p><b>关注话题</b></p>
        <img src='./topic.png'>
        <p><b>相关人物网络</b></p>
        <img src='./E_R.png'>
        <p><b>有关联的公司</b></p>
        <img src='./company.png'>
        <p><b>词云</b></p>
        <img src='./word_cloud.png'>
        <p><b>词频统计</b></p>
        <img src='./word_freq1.png'>
        <img src='./word_freq2.png'>
        <p><b>朋友圈活跃时间</b></p>
        <img src='./time_plot.png'>
        </body>
        </html>
        '''
        html = template(template_demo, **infodict)
        with open('/share/disk0/nlpdata/'+self.wechatId+'/index.html', 'w+') as f:
            f.write(html)
        return True

