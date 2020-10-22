#-*- coding:utf-8 -*-
#!/usr/bin/python
from __future__ import absolute_import

import sys
from scheduler import job_scheduler
from utils.bloomfilter import  BloomFilter  as _bf
from utils.log import log as _log
from utils.database import  data ,mongo
from utils.database import db
from utils.misc import forhash

from request import request
from grab.base import Grab
from redis import Redis
from rq_scheduler import Scheduler
from datetime import datetime
from collections import Iterable ,Iterator
from rq import  get_current_job ,get_current_connection
from rq.job import  Job
from user_agent import generate_user_agent

log = _log('rq.'+__name__)
bf = _bf()
from utils.misc import load_tmp_list,dump_tmp_list
def  job_expire(request,job=None):
        if not job:
            job = get_current_job(get_current_connection())
        job.ttl=request.ttl
        job.result_ttl=request.result_ttl
        job.timeout=request.timeout
        job.save()

class spider_base(object):
    name = ''
    factory = True
    def __init__(self,settings):
        self.settings = settings()
        self.g =self.create_grab_instance()
    def prepare(self,g):
        g.config['user_agent'] = generate_user_agent()
        # g.setup(proxy='127.0.0.1:3128')
        g.setup(timeout=300)
        g.setup(connect_timeout=300)
        return g
    def start(self):
        pass
    def save(self):
        pass
    def login(self):
        pass
    def tmp_data(self,spidername=None):
        if  spidername:
            prex = spidername
        else:
            pre = self.name
        d = data(prex)
        return d
    def  process_task(self,iteration_request):
        #循环处理任务回调
        if isinstance(iteration_request,Iterator):
            for request in iteration_request  :
                if  self.factory:
                    log.debug("start working")
                    url = request.url
                    if  request.dupefilter :
                        if  bf.check(url):
                            log.info("process  exist url %s " % url)
                            break
                    if  request.status=='sched':
                        self._job(self.settings).sched( func=self.push_task,\
                                                                args= request,\
                                                                interval=request.interval,\
                                                                repeat=-1 ,\
                                                                timeout=-1,\
                                                                result_ttl =-1,\
                                                                ttl = -1 ,\

                                                                )
                    elif request.status=='cron':
                        self._job(self.settings).cron( func=self.push_task,\
                                                                args= request,\
                                                                cron_string=request.cron_string,\

                                                                )
                    else:
                        self._job(self.settings).enqueue( func=self.push_task,\
                                                                args= request,\
                                                                timeout=-1,\
                                                                result_ttl =-1,\
                                                                ttl = -1 ,\

                                                                )
                else:
                    log.debug("test model")
                    data=  load_tmp(request)
                    if not data:
                        response = self.get_response(request)
                        dump_tmp(request,response)
                    else:
                        request,response = data
                    self.perform_callback(request,response)
                    break
        else:
            log.debug("spidert ending .....")
    def push_task(self,request):
        log.debug("star process url : %s " % request.url)
        b = self._job(self.settings).queue
        _data = b.enqueue(self.get_response,request,timeout=-1,ttl=-1,result_ttl=-1)
        b.enqueue(self.get_rq_data,request,depends_on=_data,timeout=request.timeout,ttl=request.ttl,result_ttl=request.result_ttl)
        job_expire(request)
    def _job(self,settings):
        _url = settings.get("DB_URL")
        a = job_scheduler.from_settings(_url["run"])
        return a
    @classmethod
    def from_settings(cls,settings):
        return cls(settings)
    def get_rq_data(self,request):
        q = self._job(self.settings).queue
        current_job = get_current_job(get_current_connection())
        first_job_id = current_job._dependency_id
        depends_job = q.fetch_job(first_job_id)
        response = depends_job.result
        self.perform_callback(request,response)
        # job_expire(request,depends_job)
        #depend_on (依赖get_response)任务完成后 设置过期时间
        # tl=10
        depends_job.cleanup(ttl=220)
        # depends_job.ttl=tl
        # depends_job.result_ttl=tl
        # depends_job.save()
        # depends_job.refresh()

    def perform_callback(self,request,response):
        e = request.grab
        callback = self.get_callback(request)
        hander  =  self.find_task_hander(callback)
        log.info("callback is %s"% callback)

        if hander:
            return self.process_task(hander(response) )
    def get_response(self,request):
        register_task = self.add_task(request)
        g = register_task.grab
        g.meta=request.meta
        times = 0
        while True :
            try :
                        log.debug("start request")
                        log.debug(g.config["url"])
                        data = g.request()
                        log.debug("times %s " % times)
                        return data
            except :
                if times <5:
                        times +=1
                        log.debug("try %s times" % times)
                        continue
                else:
                    log.error('out try times,request erro')
                    raise "request erro"

    def add_task(self,request):
        #添加任务
        if not  request.grab:
            g=self.prepare(self.g)
        else:
            g=self.prepare(request.grab)
        if request.url:
            g.config["url"]= request.url
        if request.setup:
            g.setup(**request.setup)
        request.grab = g
        return request
    def  create_grab_instance(self):
        #构建实例
        return Grab()
    def get_callback(self,request):
        #取得回调值
        callback =  request.callback
        return callback
    def find_task_hander(self,callback):
        #处理回调控制器
        hander = getattr(self,callback)
        return hander

class spider(spider_base):
    ## 添加 cookies 维护 ，动态调用cookies， 调度前一段时间 判断是否有效，任务中出现cookie失效的时候
    ## 更新 cookies
    ##添加 验证码 验证队列
    ## 添加 js 服务
    ## 添加 前端 http 代理
    #看板。。以后做。
    ## 修复 ：loging存 redis
    ##agent  要分 手机 pc  苹果 linux 等
    ##fix  queue name
    pass
__all__ = ("spider","request","_log")