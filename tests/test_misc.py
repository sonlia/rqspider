#coding:utf-8
#!usr/bin/python
from utils.misc import  dump_tmp_list,load_tmp_list
from utils.misc_spider import  listspider
from utils.misc_spider import  spider_single_request,spider_single_reponse
from utils.misc_spider import  singlespider

from utils.misc_spider import  _import_file,walk_modules
def test_import_file():
    print _import_file("a")
def test_walk_modules():
    print walk_modules("spider.tests.a")
def test_dump_tmp():
    class e :
        pass
    a = e()
    a.url='eee'
    c = e()
    c.url='e3ee'

    dump_tmp_list([a,c],a.url)
def test_load_tmp():
    class e :
        pass
    a = e()
    a.url='eee'
    print 'ee'
    
    print load_tmp_list(a.url)
def test_listspider():
    listspider('/home/spider/group')
def test_singlespider():
    singlespider('/home/spider/group/bt/bt.py')
    

#替换 spider 继承的父类
def  process_task(self,iteration_request):
            print 'eeee'
            #循环处理任务回调
            if isinstance(iteration_request,Iterator):
                # count = sum(1 for _ in iteration_request)
                for request in iteration_request  :
                    yield request
from tests.tmp.zhizhu import e
from itertools import tee
import copy
def  test_spider_single_request():
    iteration_request = spider_single_request(e)
    # print cop(iteration_request)
    # first,second =tee(iteration_request)
    # count = sum(1 for _ in second)
    # print count
    for i in iteration_request:
        #把request 存到
        dump_tmp_list(i,i.url)
        
        # print load_tmp_list(i.url)
def  test_spider_single_response():
    request =  load_tmp_list("https://www.dygod.net/html/gndy/jddy/20181128/111503.html")
    print request.url,'a'
    response = spider_single_reponse(e,request)
    print response ,'ee'