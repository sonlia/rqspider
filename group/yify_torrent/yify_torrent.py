#-*- coding:utf-8 -*-
#!/usr/bin/python
from __future__ import absolute_import
from core.base import spider
from core.base import request
from utils.database import  mongo as db
from utils.log import log as _log
from lxml import html
from utils.misc import  push_tmp
import time
import datetime
import re
from utils.misc import extract_douban_id,extract_imdb_id,extract_magnet
log = _log('rq.'+__name__)
class yify_torrent(spider):
    name = "yify_torrent"
    factory = False
    page =1
    try_times = 1
    key_words= "CAM|枪版|TS|TC"
    def debug(self):
        url = "https://www.yify-torrent.org/latest-{0}.html"
        for i in range(0,257):
            yield request(url=url.format(str(i)),callback="_content")
        a = "https://www.yify-torrent.org/popular-{0}.html"
        for i in range(0,257):
            yield request(url=a.format(str(i)),callback="_content")

    def start(self,url=None):
        yield request(url="https://www.yify-torrent.org/latest.html",callback="_content").cron("30 0 * * *")
        yield request(url="https://www.yify-torrent.org/popular.html",callback="_content").cron("10 0 * * *")

    def _content(self,response):
        response.tree.make_links_absolute(response.url)
        for i in response.tree.xpath("//*[@class='mv']//a//@href"):
            yield request(url=i,callback='content')




    def content(self,response):
        imdb_id = re.search(r"http://www.imdb.com/title/(.\w+.\d+)", response.body, re.I | re.M).group(1)
        hash =   re.search('magnet\:\?xt=urn\:(\w+\:\w+\d+)',response.body,re.I | re.M).group(1)
        name = response.tree.xpath("//div[@class='name']//text()")[0]
        for  i in   response.tree.xpath("//div[@class='inattr']//li"):
            if   i.xpath(".//b/text()")[0]=="Size:":
                size =  i.xpath("./text()")[0]
        hash_info=[{hash:{"name":name,"size":size}}]
        hash_list=[]
        hash_list.append(hash)
            #         #插入数据
        data={}
        filter_data={}
        data.update({"imdb_id":imdb_id})
        data.update({"hash_info":hash_info})
        data.update({"hash_list":hash_list})
        data.update({"update_time":datetime.datetime.now()})
        filter_data.update({"imdb_id":imdb_id})

        db().put("bt",{"$or":[filter_data]},data)
        db().put_list("bt",filter_data,"hash_list",hash_list)

        push_tmp("imdb",imdb_id)

# class a(spider):
#     name='ewe'
#     ee='cc'
#     def c(self):
#         print 'sss'