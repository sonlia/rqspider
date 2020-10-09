#coding:utf-8
#!usr/bin/python
#from src.utils.misc import  _import_file,walk_modules
from spider.proxy.proxy import db
from tinydb import TinyDB, Query
def test_db_get_all():
    d = db()
    print(d.get_all("proxy_ip"))
def test_db_get_random_list():
    d = db()
    print(d.get_random(num=2))
    assert (d.get_random(num=2))==2
def test_db_update_flag():
    d = db()
    d.update_flag()
    q = Query()
    data = d.table("proxy_ip").search(q.flag !=0)
    assert len(data)==0
def test_db_add_flag():
    d = db()
    d.add_flag(proxy_hash='04ca46d484ebe14533dd68f05c6b78c249a1cf49')
def test_db_get_ip():
    d = db()
    e = d.get_ip()
    print e
def test_db_insert_many():
    d = db()
    d.insert_many(table="proxy_ip",data =[{"a":2},{"a":2}])
    assert len(d.get_all())==2
    