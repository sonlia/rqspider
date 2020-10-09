#--coding:utf-8--
#! /usr/bin/python
from utils.spider_loader import spider_loader

class Test_spider_loader:
    def test_load(self):
        self.spider_loader = spider_loader.from_settings(settings)
        print self.spider_loader.__dict__

        