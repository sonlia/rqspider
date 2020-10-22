#-*- coding:utf-8 -*-
#!/usr/bin/python
from __future__ import absolute_import
from core.base import spider
from core.base import request
from utils.log import log as _log
log = _log('rq.'+__name__)
class douban_imdb(spider):
    name = "douban_imdb"
    factory = False
    def debug(self):
          pass


    def start(self,url=None):
         pass