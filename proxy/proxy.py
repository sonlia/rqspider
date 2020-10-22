#-*- coding:utf-8 -*-
#!/usr/bin/python
from __future__ import absolute_import
import sys
from getproxy import GetProxy
import datetime ,requests
import time
import uuid
import hashlib
import random ,numpy
import random
from tinydb import TinyDB, Query
from utils.log import log as _log
log = _log(__name__)
class grab_proxy(GetProxy):
    def _validate_proxy(self, proxy, scheme='http'):
        country = proxy.get('country')
        host = proxy.get('host')
        port = proxy.get('port')

        _proxy_hash = '%s://%s:%s' % (scheme, host, port)
        proxy_hash = hashlib.sha1(_proxy_hash).hexdigest()
        if proxy_hash in self.proxies_hash:
            return

        self.proxies_hash[proxy_hash] = True
        request_proxies = {
            scheme: "%s:%s" % (host, port)
        }
        time_list = []
        num =1
        for i in range(num):
            request_begin = time.time()
            try:
                response_json = requests.get(
                    "%s://httpbin.org/get?show_env=1&cur=%s" % (scheme, request_begin),
                    proxies=request_proxies,
                    timeout=5
                ).json()
            except:
                break
    
            if str(request_begin) != response_json.get('args', {}).get('cur', ''):
                break
            request_end = time.time()
            _time  = round(request_end - request_begin, 4)
            time_list.append(_time)

            time.sleep(random.uniform(1, 5))
        if  len(time_list):
            na = numpy.array(time_list)
            var = na.var()
            mean = na.mean()
            succes_ratio = float(num)/len(time_list)
            anonymity = self._check_proxy_anonymity(response_json)
            country = country or self.geoip_reader.country(host).country.iso_code
            export_address = self._check_export_address(response_json)
            return {
                "id": str(uuid.uuid1()),
                "host": host,
                "port": port,
                "anonymity": anonymity,
                "country": country,
                "response_time": round(mean,4),
                "var" : var,
                "succes_ratio":succes_ratio,
                "hash":proxy_hash,
                "update_time": str(datetime.datetime.now()),
                "flag":0,
                "type":scheme,
            }
    
    def save_proxies(self):
            d = db()
            d.insert_many(data =self.valid_proxies,table="proxy_ip")
            # for i in  self.valid_proxies:
    def data(self):
        return  self.valid_proxies
            #      d.insert(i)
    def start(self):
        self.init()
        self.load_input_proxies()
        self.validate_input_proxies()
        self.load_plugins()
        self.grab_web_proxies()
        self.validate_web_proxies()
        # self.save_proxies()

class db:
    #ip 数量 低于50 启动爬虫
    #ip 数量大于20 的时候 每次使用 flag 增加1  超过2就删除ip
    #ip 数量低于 20 的时候 则更新所有 flag  非 0 的 ip
    def __init__(self,path="/home/ubuntu/workspace/spider/proxy/db.json"):
        self.db = TinyDB(path)

    def table(self,table,cache_size=None):
        return self.db.table(table,cache_size=None)
    def insert(self,table,data):

        self.table(table).insert(data)
        
    def get_all(self,table="proxy_ip"):
        return self.table(table).all()
    def insert_many(self,data,table="proxy_ip"):
        self.table(table).insert_multiple(data)
        
    def get_ip(self,table="proxy_ip"):
        Qu = Query()
        da = self.table(table).search(Qu.flag==0)

        all_count = self.get_all()
        log.debug("total ip count : %s " % len(all_count))

        if len(all_count)<50:
            log.debug("ip count is not engough")
            g =grab_proxy()  #此处应该更新ip池 
            g.start()
            time.sleep(10)
            print "sleep 10s restart crawl"
            self.get_ip(table)
                
        if len(da)>20:
            log.debug("left useful ip : %s " % len(da))
            i =   random.choice(da)
            proxy_hash = i["hash"]
            self.add_flag(proxy_hash)
            log.debug("get ip: %s " % i["host"])
            return i
        else :
            log.debug("left %s " % len(da))
            self.update_flag()
    def get_random_list(self,table="proxy_ip",num=10):
        #从 未爬取的page 列表里面随机选取num 
        Qu = Query()
        da = self.table(table).search(Qu.flag!=0)
        a = random.sample(da,num)
        return a   
    def grab_list(self,num):
        pass
    def remove_ip(self,ip,table="proxy_ip"):
        pass
    def add_flag(self,proxy_hash,table = "proxy_ip"):
        Qu = Query()
        da = self.table(table).search(Qu.hash==proxy_hash)[0]
        num = da.get("flag")
        if num==2:
            a = self.table(table).get(Qu.hash==proxy_hash)
            # print dir(a)
            e = a.eid
            log.debug("removing ip")
            self.table(table).remove(eids=[e])
        else :
            self.table(table).update({"flag":num+1},Qu.hash==proxy_hash)
    def update_flag(self,table="proxy_ip"):
        Qu = Query()
        log.debug("update flag")
        da = self.table(table).update({"flag":0},Qu.flag!=0)
        
    
def start():
    grab  = grab_proxy()
    grab.start()
if __name__ == "__main__":
    start()