# -*- coding: utf-8 -*-
'''
@author: Yalei Meng    E-mail: yaleimeng@sina.com
@license: (C) Copyright 2017, HUST Corporation Limited.
@DateTime: Created on 2017/9/15，at 12:09            '''
from bs4 import BeautifulSoup as bs
import requests as  rq
import pymongo as mg
import time
import random

def get_cars_in_Page(page):
    host = 'https://www.renrenche.com'
    ug = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)  Safari/537.36' #Chrome/62.0.3192.0
    head = {'User-Agent': ug,'Accept-Language':'zh-CN','Cache-Control':'no-cache'}
    r = rq.get(page, headers = head,timeout=3)
    #r.encoding = 'utf-8'
    soup = bs(r.text,'lxml')
    cars = soup.select('div.container.search-list-wrapper a')
    for car in cars:
        print(host + car.get('href'))
        #如果想保存到数据库或文件，在这里增加相应代码。
    print('\n本页获取车辆数：', len(cars))

#用单个页码进行测试
pageList = ['https://www.renrenche.com/suz/ershouche/p{}//'.format(str(n))  for n in range(1, 26)]
get_cars_in_Page(pageList[9])

# for page in pageList:           #如果想批量获取，用列表循环即可。
#     get_cars_in_Page(page)

def  get_info_from(page):
    ua = 'Mozilla/5.0 (Windows NT 6.1;) AppleWebKit/532.5 (KHTML, like Gecko) Safari/532.5'
    head = {'User-Agent': ua}
    r = rq.get(page,headers = head, timeout=3)
    #time.sleep(random.uniform(1.2,2.5))         #访问间隔时间。
    soup = bs(r.text, 'lxml')                #因为文字编码问题，不能使用text，而必须是content
    title = soup.find('h1',class_ ='title-name').text
    new_price = soup.find('div',class_='list').find_all('p')[1].text
    old_price =  soup.find('div',class_='list').find_all('span')[1].text
    inf = soup.select('div.row-fluid-wrapper  strong')
    print(inf)
    dict = {
        '名称':title,
        '现价' :new_price,
        '全新价':old_price,
        '上牌年月':inf[0].text,
        '已开里程':inf[1].text,
        '排放等级':inf[2].text,
        '排量'    :inf[3].text,
        '其他信息': soup.find('div',class_='info-about-car').text.replace('\xa0','')
    }
    print (dict)          #调试时可以打印字典出来观察。


web = 'https://www.renrenche.com/suz/car/5e3d2f58b560eef7'
get_info_from(web)
