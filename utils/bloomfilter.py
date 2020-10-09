#-*- coding:utf-8 -*-
#!/usr/bin/python
from __future__ import absolute_import
import redis
from hashlib import md5
from utils.log import log as _log
import config
_test = config.MODEL.get("baidu")
log = _log(__name__)

class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret


class BloomFilter(object):
    def __init__(self, host='localhost', port=6379, db=0, blockNum=1, key='bloomfilter'):
        """
        默认blockNum=1。Bloomfilter算法是有漏失概率的（即不存在的会误判为存在），
        在保证漏失率小于万分之一的情况下，一个blockNum可满足7千万条数据的去重，
        一个blockNum占用256M内存（注意Linux如果开了自动持久化，redis占用内存会加倍）。
        :param host: the host of Redis
        :param port: the port of Redis
        :param db: witch db in Redis
        :param blockNum: one blockNum for about 90,000,000; if you have more strings for filtering, increase it.
        :param key: the key's name in Redis
        """
        self.server = redis.Redis(host=host, port=port, db=db)
        self.bit_size = 1 << 31  # Redis的String类型最大容量为512M，现使用256M
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.key = key
        self.blockNum = blockNum
        self.hashfunc = []
        for seed in self.seeds:
            self.hashfunc.append(SimpleHash(self.bit_size, seed))

    def isContains(self, str_input):
        if not str_input:
            return False
        m5 = md5()
        m5.update(str_input)
        str_input = m5.hexdigest()
        ret = True
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            ret = ret & self.server.getbit(name, loc)
        return ret

    def insert(self, str_input):
        m5 = md5()
        m5.update(str_input)
        str_input = m5.hexdigest()
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            self.server.setbit(name, loc, 1)
    def check(self,str_input):

            if self.isContains(str_input):
                log.info(str_input+'is exists')
                return True
            else:
                self.insert(str_input)
                return False

