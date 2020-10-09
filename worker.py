#-*- coding:utf-8 -*-
#!/usr/bin/python
from redis import Redis
from rq import Worker, Queue, Connection
from settings.default_settings import QUEUES as listen
from utils.database import db
from   settings.default_settings import DB_URL as url
import time
from utils.log import log as _log
from  multiprocessing import Process
log = _log(__name__)
# from updatesquid import run

def worke(model):
        with Connection(db(url[model])):
            worker = Worker(map(Queue, listen))
            worker.work()


if __name__ == '__main__':
    # pool = multiprocessing.Pool(processes=4)   #multiprocessing pool多进程池，processes=4 指定进程数  ，因为 跟gevent 不兼容 所有取消 进程池
    job=[]
    for i in xrange(8):

        p = Process( target=worke,args=('run',))
        job.append(p)
    # p = Process( target=timer)
    # job.append(p)
    for i in job:
        i.daemon = True
        i.start()
    for i in job:
        i.join()

        i.start()
    for i in job:
        i.join()


