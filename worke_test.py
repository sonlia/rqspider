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
    worke("test")
    

