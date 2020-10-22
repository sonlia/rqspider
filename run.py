#-*- coding:utf-8 -*-
#!/usr/bin/python
from __future__ import absolute_import
from utils.log import log as _log
import time
from worker import worke
from worker_scheduler import main
from updatesquid import squid
from  multiprocessing import Process
# from  updatesquid import squid
log = _log(__name__)
# import threading

def sched():
    def fun_timer():
        print('Hello Timer!')
        timer = threading.Timer(5.5, fun_timer)
        timer.start()
    timer = threading.Timer(1, fun_timer)
    timer.start()

def timer():
    squid()
    time.sleep(3600*8)
 

if __name__ == '__main__':
    job=[]
    #开三个进程启动worker
    for i in xrange(3):
        log.info('start worke')
        workers = Process( target=worke,args=('run',))
        job.append(workers)
    # log.info('start worke')
    # workers = Process( target=worke,args=('run',))
    # job.append(workers)
    #开一个进程启动代理 定时刷新squid
    _squid = Process( target=timer)
    job.append(_squid)
    #开一个启动任务定时器
    # rqshceduler = Process( target=main,args=('run',))
    # job.append(rqshceduler)
    for i in job:
        i.daemon = True
        i.start()
    for i in job:
        i.join()
