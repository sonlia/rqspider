#-*- coding:utf-8 -*-
#!/usr/bin/python
from __future__ import absolute_import
import hashlib
import pickle
import os
from lxml import html
import re

from utils.log import log as _log

from utils.database import  data as tmp
from utils.bloomfilter import  BloomFilter


import pickle, StringIO, pickledb

log = _log('rq.'+__name__)
root = os.path.join("/home/spider",'tmp')
def  forhash(content):
    return hashlib.sha1(content).hexdigest()
db = pickledb.load(os.path.join(root,"data.db"),0)


def dump_tmp_list(request,key="id"):
    print request.url,'准备存储'
    key = forhash(key)
    print key,'zheshi key'
    if  key not in  db.getall():
        db.lcreate(key) # 创建dict

    file = StringIO.StringIO()
    pickle.dump(request,file,0)
    db.ladd(key,file.getvalue())
    if  db.dump():
        return db.llen(key)


def load_tmp_list(url):
    key = forhash(url)
    if not db.llen(key):
        return 0
    tmp =db.lpop(key,0)
    # file = StringIO.StringIO()
    data =pickle.loads(tmp)
    # print data
    # unpick = pickle.Unpickler(file)
    # data = unpick.load(tmp)
    return data
    # if db.dump():
    #     return   data
def dump_tmp(request,url):
    hs = forhash(url)
    path = os.path.join(root,hs)
    if  not os.path.exists(path):
            
        with open(path,"wb") as f:
            pickle.dump(request,f,protocol=pickle.HIGHEST_PROTOCOL)


def load_tmp(url):
    hs = forhash(url)
    path = os.path.join(root,hs)
    try :
        with open(path,"rb") as f:
            request  = pickle.load(f)
            return request
    except:
        return False

def parse(data):

    return  html.fromstring(data)
def extract_imdb_id(body):
    return  re.search(r"http://www.imdb.com/title/(.\w+.\d+)", body, re.I | re.M).group(1)
def extract_douban_id(body):
    return  re.search(r"http://movie.douban.com/subject/(.\d+)",response.body, re.I | re.M).group(1)
def extract_magnet(body):
    return re.search('magnet\:\?xt=urn\:(\w+\:\w+\d+)',response.body,re.I | re.M).group(1)
def  push_tmp(key,value,db=2):
        bf =BloomFilter(db=db)
        if not bf.check(value):
            log.info("not exist  %s " % value)
            tmp(db=db).push(key,value)