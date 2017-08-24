# -*- coding:utf-8 -*-
# -*- coding:gbk -*-
# __@author__Keen

from urllib import urlopen
from bs4 import BeautifulSoup
import numpy as np
from urllib import quote
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def get_price(keyword):
    if  keyword >= u'\u4e00' and keyword<=u'\u9fa5':
        url = 'https://search.jd.com/Search?keyword='+quote(keyword)+'&enc=utf-8&wq='\
           + quote(keyword)
    else:
        url = 'https://search.jd.com/Search?keyword='+keyword
    # print(url)

    response = urlopen(url)

    html = response.read()
    soup = BeautifulSoup(html, 'lxml')
    # print(soup
    prices = []
    for i in soup.find_all('div', class_='gl-i-wrap', limit=5):
        pri = i.find_all('strong')[0].get_text().replace('¥', '')
        # pri2 = i.find('strong').get('data-price')
        # print(pri, type(pri), pri2)
        if pri == '':
            continue
        else:
            price = float(pri)
            prices.append(price)

    avg_price = np.mean(prices)
    return avg_price

