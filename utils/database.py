#-*- coding:utf-8 -*-
#!/usr/bin/python
from __future__ import absolute_import
import redis
import pymongo
from utils.bloomfilter import  BloomFilter
from utils.log import log as _log
log = _log('rq.'+__name__)
def db (url):
    pool = redis.ConnectionPool.from_url(url)
    redis_conn = redis.Redis(connection_pool=pool)
    return redis_conn
class db_base(object):
    def __init__(self, host='localhost', port=6379, db=1):
        self.host=host
        self.port=port
        self.db=db
        self.redis = redis.StrictRedis(host=host, port=port, db=db)
    def put(self,key,value):
        pass
    def get(self,key):
        pass
    def _pack(self,val):
        pass
    def _unpack(self,val):
        pass
class data(db_base):
    '''
    临时内容 存储用

    '''
    def __init__(self,prex='tmp_data',host='localhost', port=6379, db=1):
        super(data, self).__init__(host, port, db)
        self.prex = prex
    def push(self,key  ,value):
        return self.redis.lpush(self.key(key),value)
    def getall(self,key):
        return self.redis.lrange(self.key(key),0,-1)
    def count(self,key):
        return self.redis.llen(self.key(key))
    def pop(self,key):
        return self.redis.lpop(self.key(key))
    def push_tmp(self,key,value):
        # print 'eee'
        bf =BloomFilter(host=self.host,port=self.port,db=self.db)
        print bf
        if not bf.check(value):
            log.info("not exist  %s " % value)
            self.push(key,value)
    def key(self,x):
        return ':'.join([self.prex,x])
class mongo:
    def __init__(self,dbname="spiders_data"):
        self.client = pymongo.MongoClient("localhost", 27017)
        self.db=self.client[dbname]
    def put(self,table,filter,data):
        ''' 去重插入数据，不是数组数据
        @table：type(str)  要插入的表
        @filter: type（dict）过滤条件
        @data：type（）  要插入的数据

        return ：
        '''
        return self.db[table].update(filter,{"$set":data},upsert=True)

    def get(self,table):
        '''根据修改器 获得数据
        @table：type（str） 修改的表
        # @mongo_modifier:type（修改器）
        @return ：mongod  instance
        '''
        d = self.db[table]
        return d
        # if isinstance(mongo_modifier,dict):
        #     return d.find(*mongo_modifier)

    def count(self,data):
        pass
    def insert(self,table,data):
        d= self.db[table]
        return d.insert(data)
    def put_list(self,table,filter_condition,key,data):
        '''去重插入数组数据
        @table: type（str） 要插入的数据表
        @filter_condition:type(mongo  修改器) 过滤条件
        @key:type(str) 要插入数组的 键（key）
        @data：type（list） 要插入的数据

        @reutrn  ： type（list） 迭代器
        '''
        d= self.db[table]
        return d.update_one(filter_condition,{"$addToSet":{key:{"$each":data} } })
