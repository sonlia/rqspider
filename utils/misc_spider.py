#coding:utf-8
#!usr/bin/python
from __future__ import absolute_import
from importlib import import_module
from pkgutil import iter_modules
# from src.spider.base import spiders
import inspect
from six.moves.configparser import SafeConfigParser
import six 
from core.base import spider
import os
ENVVAR = 'SCRAPY_SETTINGS_MODULE'
def walk_modules(path):
    mods = []

    mod = import_module(path)
    mods.append(mod)
    if hasattr(mod, '__path__'):

        for _, subpath, ispkg in iter_modules(mod.__path__):
            fullpath = path + '.' + subpath
            if ispkg:
                mods += walk_modules(fullpath)
            else:
                submod = import_module(fullpath)
                mods.append(submod)
    return mods



def iter_spider_classes(module):

#   判断类是否是spider 子类，通过：是否是  类，是否继承的spider 还有name
    for obj in six.itervalues(vars(module)):
        if inspect.isclass(obj) and \
           obj.__module__ == module.__name__ and \
           getattr(obj, 'name', None)  and issubclass(obj,spider):
            yield obj

import importlib 
import os

# 通过路径导入模块
def import_source(module_name):
    module_file_path = module_name.__file__
    module_name = module_name.__name__
    module_spec = importlib.util.spec_from_file_location(
        module_name, module_file_pat)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    print(dir((module)))
    msg = 'The {module_name} module has the following methods {methods}'
    print(msg.format(module_name=module_name, methods=dir(module)))

# 通过路径导入模块 生成列表
#explame :  filepath: '/home/a.py'
def _import_file(filepath):
    import sys
    abspath = os.path.abspath(filepath)
    dirname, file = os.path.split(abspath)
    fname, fext = os.path.splitext(file)
    # print fname,fext,abspath,dirname,file
    if fext != '.py':
        raise ValueError("Not a Python source file: %s" % abspath)
    if dirname:
        sys.path = [dirname] + sys.path
    try:
        module = import_module(fname)
    
    finally:
        if dirname:
            sys.path.pop(0)
    return module
def listspider(path):
    # print 'hello'
    # 检索出目录下是所有
    #  通过路径检索有 name  and  继承spider 的类
    # parm:str   '/home/spider/group' 是个目录
    # return:list     [{<module 'test' from '/home/spider/group/test.pyc'>: ['test']}, {<module 'bt' from '/home/spider/group/bt/bt.pyc'>: ['bt']}, {<module 'douban_imdb' from '/home/spider/group/douban_imdb/douban_imdb.pyc'>: ['douban_imdb']}, {<module 'yify_torrent' from '/home/spider/group/yify_torrent/yify_torrent.pyc'>: ['a', 'yify_torrent']}] 
    filelist = []
    modulelist=[]
    for  root,dirs,files in os.walk(path):
        for i in files:
            if  i.split(".")[-1]=='py' and i!='__init__.py' :
                filelist.append(os.path.join(root,i))
    for i in filelist:

            modulelist.append(_import_file(i))



    spiderall={}
    for i in modulelist:
        # print i
        # print dir(i)
        # print i.__path__
        path = filelist[modulelist.index(i)]
        spider ={}
        spidercount={}
        for a in  iter_spider_classes(i):
            spidercount[a.name]='debug'
        # spider[path]= spidercount
        if spidercount:
            spiderall[path]= spidercount
            # spiderallspider)
    # print spiderall
    return  spiderall
def singlespider(filepath):
    # parm : filepath 是一个文件路径 ~ ‘/home/spider.py’
    # return : 一个模块的下面有几个爬虫
    
    module =_import_file(filepath)
    modulelist = []
    for i in   iter_spider_classes(module):
        modulelist.append([filepath ,  i.__name__ ] )
    return  modulelist

# 处理 spider request 然后返回到spidert tree,做了个装饰器 直接替换掉  父类的 函数，
#来打断正常的 程序流程
from collections import Iterable ,Iterator
def rebuild_spider(spider):
    class  spider_single_request:
           def  process_task(self,iteration_request):
            print 'eeee'
            #循环处理任务回调
            if isinstance(iteration_request,Iterator):
                # count = sum(1 for _ in iteration_request)
                for request in iteration_request  :
                    yield request
    return  spider_single_request
from settings import Settings
from collections import Iterable ,Iterator
import types 
from utils.misc import  dump_tmp,load_tmp 
def  spider_single_request(spider):
    def  process_task(self,iteration_request):
            #循环处理任务回调
            if isinstance(iteration_request,Iterator):
                # for request in iteration_request  :
                    # yield request
                    return iteration_request
    newclass = spider(Settings)
    newclass.process_task = types.MethodType(process_task,newclass)
    iter = newclass.start()
    return  newclass.process_task(iter)
def  spider_single_reponse(spider):
    def  process_task(self,iteration_request):
            #request 落地
            if isinstance(iteration_request,Iterator):
                for request in iteration_request  :
                    # print 'hello ....................'
                    dump_tmp(request,request.url)
                    yield request
    # def get_request(self,url):
    #     return load_tmp(url)
    def run(self,url):
        request =load_tmp(url)
        # 如果之前请求国 就直接本地读取
        response = self.get_response(request)
        return  self.perform_callback(request,response)
        
    newclass = spider(Settings)
    
    # newclass.get_request = types.MethodType(get_request,newclass)
    newclass.run = types.MethodType(run,newclass)
    newclass.process_task = types.MethodType(process_task,newclass)
    return newclass
    # newclass.run(url)
    # return  newclass.get_response(request)
import sys, cStringIO, contextlib
@contextlib.contextmanager
def redirect_stdout(status=False):
    original = sys.stdout
    sys.stdout = cStringIO.StringIO()
    c =sys.stdout
    yield
    if status:
	    sys.stdout =original
	    print c.getvalue()
import os
# 用于传送公共的 spider 输出信息
pipe_name='/tmp/log.fd'
# w,r = os.pipe()
from multiprocessing import  Pipe
r,w =Pipe()
import select
def send(data):
    # global  w,r
    # os.close(r)
    # a = os.fdopen(w, 'w')
    # a.write(data)
    # a.close()
    # yield 'a'
    w.send(data)
    w.close()
    print 'kaishi ...........',data
    # if not os.path.exists(pipe_name):
        # os.mkfifo(pipe_name)  
    # pipeout = os.open(pipe_name, os.O_CREAT | os.O_WRONLY | os.O_NONBLOCK)
    print '圣通平'
    # w,r = select.select([],[pipeout],[])
    # # os.write(pipeout, data)
    # os.close(pipeout)
def rec(r):
    # os.close(w)
    # r = os.fdopen(r)
    # return  r.read()
    print '我第一。。。。。。。。'
    # try:
    #     _,a,_=select.select([r],[],[])
    #     return a.recv()
    # except:
    #     print 'ee'

    


