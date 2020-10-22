#-*- coding:utf-8 -*-
#!/usr/bin/python
from __future__ import absolute_import
from core.base import spider
from core.base import request
from utils.misc import  push_tmp
from utils.database import  mongo as db

from utils.log import log as _log
from lxml import html
import time
import datetime
import re
log = _log('rq.'+__name__)
class abt(spider):
    name ='een '
class bt(spider):
    name = "bttiantangs"
    factory = False
    page =1
    try_times = 1
    url = "http://bttiantangs.com"
    key_words= "CAM|枪版|TS|TC"
    def debug(self):
        for i in range(1,50000):
            yield request(url = "http://www.bttiantangs.com/movie/{0}.html".format(str(i)),callback="content1")
    def start(self,url=None):
         yield request(url = "http://bttiantangs.com/",callback="cc").cron("20 0 * * *")
         yield request(url = "http://bttiantangs.com/list/dianying/index.html",callback="cc").cron("40 0 * * *")
         yield request(url = "http://bttiantangs.com/list/dianying/index_2.html",callback="cc").cron("20 0 * * *")
         yield request(url ="http://bttiantangs.com/list/dianying/index_3.html",callback="cc").cron("50 0 * * *")
         yield request(url ="http://bttiantangs.com/top/update.html",callback="cc").cron("10 1 * * *")


    def cc(self,response):
        if  response.body:
            dd=response.body
        else :
            dd='erro'
        d = html.fromstring(dd)
        hre = d.xpath("//div[@class='article']//a/@href")
        for i in  map(lambda x :self.url+x , hre):
            log.info("push url. {0}".format(i))
            yield  request(url =i,callback="content1")

    def content1(self,response):

        if  response.body:
            dd=response.body
        else :
            dd='erro'
        d = html.fromstring(dd)
        #递归页面

        content = d.xpath("//div[@class='article_container row  box']//div[@class='context']")
        erro = d.xpath("//div[@class='article_container row  box']//div[@class='omg404']")
        log.info(response.url)
        if  content and not len(erro):

            data = {}
            imdb_id = re.search(r"http://www.imdb.com/title/(.\w+.\d+)", response.body, re.I | re.M)
            douban_id = re.search(r"http://movie.douban.com/subject/(.\d+)",response.body, re.I | re.M)

            if  imdb_id:
                data.update({"imdb":imdb_id.group(1)})

            if douban_id:
                data.update({"douban":douban_id.group(1)})
            data.update({"update_time":datetime.datetime.now()})

            if imdb_id or douban_id:
                #获得 磁力hash
                manget_hash= []
                hash_info=[]
                manget_list =  d.xpath("//ul[@class='dlist']//li")

                for i in manget_list:
                    _name = ''.join(i.xpath(".//em/text()"))
                    name = re.search(r"CAM|枪版|TS|TC", _name, re.I | re.M)
                    if not name:
                        try:
                            tag = "".join(i.xpath(".//@href"))
                            manget_data = re.search('magnet\:\?xt=(\w+)\:(\w+)\:(\w+\d+)',tag,re.I | re.M)
                            hash =  manget_data.group(3)
                            manget_hash.append(hash)
                            _name =i.xpath(".//a[2]/text()")[0]

                            size = re.search('\d*.\d*\s*GB',_name,re.I | re.M).group(0)
                            name = _name.rstrip(size)
                            hash_info.append({hash:{"name":name,"size":size}})
                        except:
                            continue
                #插入数据
                f_data={}
                #过滤条件
                for i in data.keys():
                    if i  in ["imdb","douban"]:
                        f_data.update({i:data.get(i)})

                        push_tmp(i,data.get(i))
                f_data.update({"hash_info":hash_info})
                db().put("bt",{"$or":[f_data]},data)
                db().put_list("bt",f_data,"hash_list",manget_hash)

