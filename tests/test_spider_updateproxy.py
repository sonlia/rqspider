#--coding:utf-8--
#! /usr/bin/python
from rq import Queue
from utils.database import db
from updatesquid import squid
class Test_spider_updateproxy:
    def test_updateproxy(self):
        s = squid()
        a = Queue(connection=db)
        a.enqueue(s)


