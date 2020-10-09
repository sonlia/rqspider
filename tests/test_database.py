#-*- coding:utf-8 -*-
#!/usr/bin/python
# from src.spider.base import  spider_base
# import Queue
# import pickle
# from src.core.core import core
from scheduler import a ,sched


class Test_database(object):

    def test_get(self,db):
        e = {"$or":[{"hash":"12cb1159c1f72383abf5935909bc64f42092482"},{"imdb" : "tt0044476"}]}
        a =  db.get('bt',e)
        # print dir(a)
        # for i in a:
        #     print(i)
    def test_put(self,db):
        db.put('bt',{"douban" : "1294618"},{'hash1':'eds'})
        # print(a)
    def test_get2(self,db):
        assert db.count('test')==9
        # assert db.count('test')==3
        
        # assert "3" in x
    def test_insert_list(self,db):
        # a = db.db['bt']
        #db.bt.find({"$or":[{"hash":"12cb1159c1f72383abf5935909bc64f42092482"},{"imdb" : "tt0044476"}]})
        # a.update({"douban" : "1294618"},{"$push":{"hash1":"s" } })
        c = {"douban" : "1294618"}
        d= ["ddds","se"]
        # a.update(c,{"$addToSet":{"hash1":{"$each":d} } })
        print db.insert_list("bt",c,"hash1",d)

def proxy(y):
    
    return y.response
class Test_core(object):
    def test_core(self,curl):
    
       print curl.headers

       assert curl.status_code ==200
    def test_response_pickle(self,curl):
        a = core('GET',url='http://www.bttiantangs.com/')
        g = a.send()
        # print "....",g.headers,"0000"
        q = Queue.Queue()
        # c =proxy(curl)
        # print dir(curl)
        
        _pickle = pickle.dumps(g)
        q.put(_pickle)
        _data = q.get()
        data = pickle.loads(_data)
        print dir(data),data.status_code
        
    def test_xpath(self,curl):
        e = '//*[@id="post_container"]/li/div[3]/h2/a/text()'
        print(curl.xpath(e)[0])
        assert curl.xpath(e)[0]==u'生化危机：复仇.2017'
class Test_spider_base(object):
    def test_get_response(self,request_able,base):
        
        b =base.get_response(request_able)
        # print dir(b)
        assert b.response.status_code==200
    def _da(self,d):
        yield d
    def test_process_task(self,base,request_able):
        e = self._da(request_able)
        a = base.process_task(e)
        print a
class Test_scheduler(object):
    def test_sched(self):
        # sched(a,3,3,3)
        sched(a,3)