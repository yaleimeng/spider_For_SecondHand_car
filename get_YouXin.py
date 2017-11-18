# -*- coding: utf-8 -*-
'''
@author: yaleimeng@sina.com
@license: (C) Copyright 2017, HUST Corporation Limited.
@desc:
@DateTime: Created on 2017/11/18，at 11:31            '''

import requests as rq
from bs4 import BeautifulSoup as bs

def requestPage(page):   #不加Cookie也可以访问。但访问频繁会被反爬虫机制拦截。请控制访问速度，不要太快。
    head = {
        'Cookie':'RELEASE_KEY=; uid=rBAKDFnUmyQbcj/dEzTfAg==; XIN_UID_CK=7896203a-cf64-fa25-6e12-b000bc142859; '
                 'XIN_anti_uid=60B2CBE2-6F5B-A01F-8003-C18F8115BA4C; '
                 'SEO_REF=https://www.baidu.com/link?url=CqVOkK6sluyY7q6z7BllYRpew65KAeSCia9CJDLwOcm&wd=&eqid=e99216140001d3c4000000035a0fa912;'
                 ' XIN_bhv_expires=1511062846544; XIN_CARBROWSE_IDS=%5B78694508%2C72044260%5D; XIN_bhv_pc=2; '
                 'XIN_LOCATION_CITY=%7B%22cityid%22%3A%221502%22%2C%22areaid%22%3A%226%22%2C%22big_areaid%22%3A%221%22%'
                 '2C%22provinceid%22%3A%2215%22%2C%22cityname%22%3A%22%5Cu82cf%5Cu5dde%22%2C%22ename%22%3A%22suzhou%22%'
                 '2C%22shortname%22%3A%22SZ%22%2C%22service%22%3A%221%22%2C%22near%22%3A%221406%2C910%2C201%2C1505%'
                 '2C3001%2C2101%2C1509%2C1501%2C2401%22%2C%22tianrun_code%22%3A%220512%22%2C%22zhigou%22%3A%222%22%2C'
                 '%22longitude%22%3A%22120.5853150%22%2C%22latitude%22%3A%2231.2988860%22%2C%22city_rank%22%3A%2210%22%7D;'
                 ' NSC_20.eqppmxfc.yjo.dpn=ffffffffaf18141e45525d5f4f58455e445a4a423660; Hm_lvt_ae57612a280420ca44598b857'
                 'c8a9712=1510975787; Hm_lpvt_ae57612a280420ca44598b857c8a9712=1510976479; XIN_bhv_oc=5',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
               'Maxthon/5.0.4.3000 Chrome/47.0.2526.73 Safari/537.36'    }
    r = rq.get(page, headers=head, timeout=3)
    return bs(r.text, 'lxml')

def get_cars_in_Page(page):
    soup = requestPage(page)
    cars = soup.select('li div.across a.aimg')
    for car in cars:
        print('http:'+car.get('href'))
        #如果想保存到数据库或文件，在这里增加相应代码。
    print('\n本页获取车辆数：', len(cars))

#从单个页码进去，获得40条URL。
# pageList = ['https://www.xin.com/suzhou/sn_t1000/i{}'.format(str(n))  for n in range(1, 50)]
# get_cars_in_Page(pageList[5])    #单个网页测试url提取效果

# for page in pageList:           #如果想批量获取车辆详情页的url，用页码列表循环即可。
#     get_cars_in_Page(page)

def  get_info_from(car_page):
    soup = requestPage(car_page)
    title = soup.select('div.cd_m_h span')[0]
    info = soup.select('ul.cd_m_info_desc li')
    pris = soup.select('p.cd_m_info_price span')
    dict = {
        '名称':title.text.strip(),
        '现价' :pris[0].text.strip()[1:],  #去掉了￥符号。
        '全新价':pris[2].text.replace('\r\n','').replace(' ',''),
        '上牌年月':info[0].text.split('\n')[2][:-2],
        '已开里程':info[1].text.strip().split('\n')[0],
        '排放等级':info[2].text.split('\n')[1],
        '排量'  :info[3].text.split('\n')[1],
        }
    print (dict,'\n\n')          #调试时可以打印字典出来观察。需要保存数据的话可以稍微更改，加入代码
    extra = soup.select('div.cd_m_i_pz > dl > dd')
    for ele in extra:
        print(ele.text.strip().replace('\n','').replace(' ',''))     #这是附加信息。

one_car = 'https://www.xin.com/suzhou/che21064622.html'      #这是具体车辆页面网址，用来对单页信息抽取函数进行测试。
get_info_from(one_car)


# info_got = '''获得信息如下：
# {'名称': '大众 途安 2015款 1.4T 自动 舒适版5座', '现价': '12.88万', '全新价': '新车含税18.65万', '上牌年月': '2015年01月', '已开里程': '5.5万公里', '排放等级': '国5', '排量': '1.4L'}
#
# 排放标准国5
# 所在城市苏州
# 使用性质非营运
# 年检到期2019-01-01
# 保险到期2018-01-24
# 保养情况4S店非定期
# 车辆厂商上汽大众
# 车辆级别MPV
# 颜色咖啡色
# 车身结构5门5座MPV
# 整备质量1550kg
# 轴距2678mm
# 发动机EA111
# 变速器DCT双离合
# 排量1390mL
# 燃料类型汽油
# 驱动方式前驱
# 综合油耗--      '''