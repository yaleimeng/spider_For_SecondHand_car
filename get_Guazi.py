# -*- coding: utf-8 -*-
'''
@author: Yalei Meng    E-mail: yaleimeng@sina.com
@license: (C) Copyright 2017, HUST Corporation Limited.
@desc:
@DateTime: Created on 2017/9/15，at 13:02            '''

import pymongo as mg
import time
import random
import requests as rq
from bs4 import BeautifulSoup as bs

def requestPage(page):
    head = {    #Cookie信息要从自己浏览器的请求头里面复制。代码中的Cookie只在当时有用。过期作废。
        'Cookie': 'antipas=79082rf81t548E692Z6k1Eq7q1I6; uuid=724da661-71ad-4f77-a3ad-a03c2732c100; ganji_uuid=9341781085735653512305; -_views=1; cityDomain=nj; preTime=%7B%22last%22%3A1505466209%2C%22this%22%3A1505437495%2C%22pre%22%3A1505437495%7D; clueSourceCode=10103192012%2300; cainfo=%7B%22ca_s%22%3A%22sem_baiduss%22%2C%22ca_n%22%3A%22ss3%22%2C%22ca_i%22%3A%22-%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22%25E7%2593%259C%25E5%25AD%2590%25E4%25BA%258C%25E6%2589%258B%25E8%25BD%25A6%25E7%259B%25B4%25E5%258D%2596%22%2C%22ca_kw%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%2253362186047%22%2C%22scode%22%3A%2210103192012%22%2C%22version%22%3A1%2C%22platform%22%3A%221%22%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%22724da661-71ad-4f77-a3ad-a03c2732c100%22%2C%22sessionid%22%3A%2256578dfa-839b-43cf-9199-1e31204b3e78%22%7D; lg=1; Hm_lvt_e6e64ec34653ff98b12aab73ad895002=1505437578; Hm_lpvt_e6e64ec34653ff98b12aab73ad895002=1505466317; _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A32872103251%7D; sessionid=56578dfa-839b-43cf-9199-1e31204b3e78; 724da661-71ad-4f77-a3ad-a03c2732c100_views=21; 56578dfa-839b-43cf-9199-1e31204b3e78_views=20',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/5.0.4.3000 Chrome/47.0.2526.73 Safari/537.36'    }
    r = rq.get(page, headers=head, timeout=3)
    return bs(r.text, 'lxml')

def get_cars_in_Page(page):
    host = 'https://www.guazi.com'
    soup = requestPage(page)
    cars = soup.select('ul.carlist a')
    for car in cars:
        print(host + car.get('href'))
        #如果想保存到数据库或文件，在这里增加相应代码。
    print('\n本页获取车辆数：', len(cars))

#从单个页码进去，获得40条URL。URL中#后面的部分其实也可以去掉。能正常访问
# pageList = ['https://www.guazi.com/nj/buy/o{}'.format(str(n))  for n in range(1, 66)]
# get_cars_in_Page(pageList[6])

# for page in pageList:           #如果想批量获取车辆详情页的url，用页码列表循环即可。
#     get_cars_in_Page(page)

def  get_info_from(car_page):
    soup = requestPage(car_page)
    title = soup.find('div', class_='titlebox').find('p')
    info = soup.select('ul.assort span')
    pris = soup.select('div.pricebox span')
    dict = {
        '名称':title.text,
        '现价' :pris[0].text.replace(' ',''),
        '全新价':pris[2].text.replace('\r\n','').replace(' ',''),
        '上牌年月':info[0].text,
        '已开里程':info[1].text,
        '排放等级':info[3].text[:2],
        '变速箱'  :info[5].text,
        }
    print (dict,'\n\n')          #调试时可以打印字典出来观察。需要保存数据的话可以稍微更改，加入代码
    extra = soup.select('ul.basic-eleven li div')[6:-1]
    for ele in extra:
        print(ele.text)     #这是附加信息。

one_car = 'https://www.guazi.com/nj/e0f2ef61d37fa8a3x.htm'
get_info_from(one_car)