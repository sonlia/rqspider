#-*- coding:utf-8 -*-
#!/usr/bin/python
from __future__ import absolute_import

from rq_scheduler import Scheduler
from datetime import datetime
from rq import Queue
# from  fakeredis  import  FakeStrictRedis
from utils.database import db
from utils.log import log as _log
log = _log(__name__)
class job_scheduler:
    def __init__(self,db):

        self.queue = Queue(connection=db)
        self.scheduler = Scheduler(connection=db)
    @classmethod
    def from_settings(cls,url):
        # log.debug("add to job to scheduler :%s " % url)
        _db=db(url)
        return cls(_db)
    def cron(self,cron_string,func,args,repeat=None):
        return self.scheduler.cron(cron_string=cron_string,func=func,args=[args], repeat=repeat)

    def  sched(self,func,args,interval=None,repeat=None,timeout=None,result_ttl=None,ttl=None):
        ##TODO  添加过滤 防止 重复定时同一个的地址 造成死循环，
        ## 添加 执行过的任务重新定时 执行
        if interval:
            log.debug("crawl url %s " % args )
            return self.scheduler.schedule(
                scheduled_time=datetime.utcnow(), # Time for first execution, in UTC timezone
                func=func,                     # Function to be queued
                args=[args],             # Arguments passed into function when executed
                interval=interval,                   # Time before the function is called again, in seconds
                repeat=repeat,
                timeout=timeout,
                result_ttl =result_ttl,
                ttl = ttl ,  # Repeat this number of times (None means repeat forever)
                queue_name=queue_name
                    )
    def enqueue(self,func,args,timeout=None,result_ttl=None,ttl = None):
            return self.queue.enqueue(func,args,timeout=timeout,result_ttl =result_ttl,ttl = ttl)

