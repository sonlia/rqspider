#-*- coding:utf-8 -*-
#!/usr/bin/python
from __future__ import absolute_import
from spider.base import spider
from spider.base import request
from utils.database import  mongo as db
from utils.log import log as _log
from lxml import html
import time,random
import datetime
import re
log = _log('rq.'+__name__)
class email(spider):
    name = "email"
    factory = True
    def start(self,url=None):
        # url ='https://purchaser.mingluji.com/Gift'
        url ='https://purchaser.mingluji.com/Electronic_and_Information_Products'
        yield   request(url=url,callback='link')
        for i in map( lambda x: url+'/'+str(x),range(0,23)):
            i.rstrip("%0A").strip()
            yield request(url=i,callback='link')
            # break
        # with open("erro.txt","r") as f:
        #     for i in f.readlines():
        #         i.rstrip("%0A").strip()
        #         if  i is not None:
        #             yield request(url="https://purchaser.mingluji.com/BASIS_%26_BASIS_S.A.",callback='content')
                # break
    def link(self,response):

        if  response.body:
            dd=response.body
        else :
            dd='erro'
        d = html.fromstring(dd)
        hre = d.xpath("//div[@id='mw-content-text']/table//tr/td[1]/ol/li/a/@href")
        # print hre
        for i in  map(lambda x: "https://purchaser.mingluji.com"+x, hre ):
            i.rstrip("%0A").strip()
            yield request(url=i,callback='content')
            # break
    def content(self,response):

        if  response.body:
            dd=response.body
        else :
            dd='erro'
        d = html.fromstring(dd)
        try :
            description = d.xpath('//*[@id="mw-content-text"]//span[@itemprop="description"]//text()')
            content = d.xpath('//*[@id="mw-content-text"]//div//dl')
            _d=[]

            for i in content:
                _d.append (i.xpath(".//dd//text()") )

            def listTostr(list1):
                a=''
                for i in list1:
                    if i!=' N.A.':
                        a+=i
                return a
            def remove_space(list1):
                for i  in list1:
                    i.encode('utf-8')
                    if ' ' in list1:
                            list1.remove(' ')
                return list1
            def  remove_chinse(list1):
                a = remove_space(list1)
                c=[]
                for i in a:
                    if  "(" and ")" in i:
                        c.append(i.split( "(" )[0])
                return c
            data = {}
            data["CompanyName"]=listTostr(_d[0])
            data["area"]=remove_chinse(_d[1])[0]
            data["address"]=listTostr(_d[2])
            data["contact"]=listTostr(_d[3])
            data["telephone"]=listTostr(_d[4])
            data["fax"]=listTostr(_d[5])
            data["email"]=listTostr(_d[6])
            data["web"]=listTostr(_d[7])
            data["Category"]=remove_chinse(  _d[8])
            data["description"]=description[0]
            print data,"......"
            db().insert("dt",data)
        except:
            with open ("erro2.txt","a") as f :
                f.write(response.url+"\n")

