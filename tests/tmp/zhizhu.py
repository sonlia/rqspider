#coding:utf-8
#!usr/bin/python
from core.base import  spider
from request import request
from utils.log import log as _log

log = _log(__name__)
class e(spider):
    name = "dygod"
    def start(self):
        print 'start'
        import time
        print 'next'
        yield   request(url="https://www.dygod.net/html/gndy/jddy/20181123/111507.html",callback='link') 
        # time.sleep(1)
        yield   request(url="https://www.dygod.net/html/gndy/jddy/20181124/111507.html",callback='link') 
    def link(self,a):
        yield   request(url="https://www.dygod.net/html/gndy/jddy/20181125/111504.html",callback='link1') 
        yield   request(url="https://www.dygod.net/html/gndy/jddy/20181126/111504.html",callback='link1') 
        yield   request(url="https://www.dygod.net/html/gndy/jddy/20181127/111504.html",callback='link1') 
        print  '成功进入第二层'
        # print a.select('#content > div > fieldset > h2').text()
    def lin1k(self,a):
        print  '这事第三层'
        # print a.select('//*[@id="Zoom"]/p[10]').text()
        yield   request(url="https://www.dygod.net/html/gndy/jddy/20181128/111503.html",callback='li2k')
    def li2k(self,a):
        print '第四层'