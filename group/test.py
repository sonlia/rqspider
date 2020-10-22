#-*- coding:utf-8 -*-
#!/usr/bin/python
import os,sys
# from __future__ import absolute_import
# print os.path.split( os.path.realpath( sys.argv[0] ) )[0]
#获取脚本运行目录
# print os.getcwd()
from core.base import spider
from core.base import request
from utils.database import  mongo as db
from utils.log import log as _log
from lxml import html
import time,random
import datetime
import re

log = _log('rq.'+__name__)
class test(spider):
    name = "dygod"
    def start(self):
        yield   request(url="https://www.dygod.net/html/gndy/jddy/20181126/111519.html",callback='link') 
    def link(self,a):
        yield   request(url="https://www.dygod.net/html/gndy/jddy/20181126/111502.html",callback='link2') 
    def link2(self,a):
      print  'eee'
      print 'nima 年末的。'

class test1(spider):
    name = "dygod222"
    def start(self):

        yield   request(url="https://www.dygod.net/html/gndy/jddy/20181126/111507.html",callback='link') 
        yield   request(url="https://www.dygod.net/html/gndy/jddy/20181126/111507.html",callback='link') 
        yield   request(url="https://www.dygod.net/html/gndy/jddy/20181126/111507.html",callback='link') 
    def link(self,a):
        print "。。。。。。 。。。。 。。 "

        yield   request(url="https://www.dygod.net/html/gndy/jddy/20181126/111507.html",callback='link') 
    def link(self,a):
        print "。。。。。。 。。。。 。。 "
