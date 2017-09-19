# -*- coding: utf-8 -*-
'''
@author: Yalei Meng    E-mail: yaleimeng@sina.com
@license: (C) Copyright 2017, HUST Corporation Limited.
@DateTime: Created on 2017/9/13，at 9:40            '''

import requests as rq
from  bs4 import BeautifulSoup as bs
import time
import random
import csv

def  requestPage(page ,want_Text = True ):
    ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/5.0.4.3000 Chrome/47.0.2526.73 Safari/537.36'
    head = {'User-Agent': ua}
    try:
        r = rq.get(page , headers = head)
    except Exception as e:
        print(e.args)
        return None
    return bs(r.text, 'lxml')

def getProxys():     #固定访问前面4页，从中获取代理。
    url_list = ['http://www.xicidaili.com/nn/{}'.format(str(n)) for n in range(1,5) ] #透明代理是nt，高匿名代理是nn
    httpList = [];      httpsList= []
    for url in url_list:
        soup = requestPage(url)
        if soup is None:
            time.sleep(1.5);            continue
        infos = soup.select('tr.odd')
        if len(infos)>0:
            for info in infos:
                item = info.select('td')
                if len(item)>5 :
                    address = 'http://' + item[1].text + ':' + item[2].text
                    if item[5].text == 'HTTP':
                        httpList.append(address)
                    elif item[5].text == 'HTTPS':
                        httpsList.append(address)
        else:
            print('没有得到内容，可能服务器限制访问。')
        time.sleep(1.5)
    print (httpList,'\n\n')
    return httpList,httpsList

def verifyProxys(nlist,slist):
    if len(nlist)<1 or  len(slist)<1:      #如果列表为空，什么都不做
        print('列表为空，无法验证！');        return []
    goodlist = []
    ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/5.0.4.3000 Chrome/47.0.2526.73 Safari/537.36'
    head = {'User-Agent': ua}
    for npro in nlist:
        num = random.randint(0,5)
        pro = {'http':npro,'https':slist[num]}
        try:
            res = rq.get('http://www.rsdown.cn/', headers=head, proxies= pro,timeout=3)
            if res.status_code != 200:
                time.sleep(1.3);                continue
            soup = bs(res.content,'lxml')
            print( soup.select('ul.morebh a')[num].text)
            goodlist.append(pro)     #把构造出来的代理加入到list中去。
        except Exception as ex:
            print('='*15,'获取服务器响应失败…………')
            #print(ex.args)
        finally:
            time.sleep(1.3)
    print('优质HTTP代理数量：%d\n'%len(goodlist),goodlist)
    return  goodlist

def  write_file( gList):
    if len(gList)>0:
        Headers = ['http','https']
        with open('E:/Good_Proxies.csv', 'w', encoding='utf-8')as fp:
           fw = csv.DictWriter(fp,Headers)
           fw.writeheader()
           fw.writerows(gList)

if __name__ == '__main__':
    norm, safe = getProxys()
    good = verifyProxys(norm,safe)
    write_file(good)                #把运行良好的代理写入到csv文件了。
