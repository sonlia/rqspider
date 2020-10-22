#-*- coding:utf-8 -*-
#!/usr/bin/python
from __future__ import absolute_import
from utils.log import log as _log
log = _log(__name__)
class request(object):
    def __init__(self,  url=None, dupefilter=False ,callback=None, \
                        meta=None,setup=None,grab=None,timeout=1000,\
                        result_ttl=1000,ttl=3000,queue_name='default'):

        self.url = url
        self.setup=setup
        self.dupefilter = dupefilter
        self.callback = callback
        self.meta=meta
        self.grab = None
        self.interval =None
        self.repeat = None
        self.timeout = timeout
        self.result_ttl =result_ttl
        self.ttl = ttl
        self.cron_string=None
        self.status=None
        self.connection=None

        # for item, value  in  kwargs.items():
        #     # if item=='meta':
        #         setattr(self,item,value)
    def get(self,key,default=None):

            return getattr(self,key,default)
    def cron(self,cron_string,repeat=None):
        self.cron_string=cron_string
        self.repeat=None

        self.status='cron'
        return self

    def sched(self,interval=None,repeat=None):
        if  interval  :
            self.interval = interval
            self.repeat = repeat

        else :
            raise "pls set a correct value"
        self.status="sched"
        return self

        