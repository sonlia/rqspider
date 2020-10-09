#-*- coding:utf-8 -*-
#!/usr/bin/python
from  proxy.proxy import grab_proxy
import uuid ,os ,time
from datetime import datetime
#cache_peer ${IP} parent ${PORT} 0 login=${username}:${password} round-robin proxy-only no-query connect-fail-limit=2
def squid():
    pass  
    d = grab_proxy()
    d.start()
    data =d.data()
    rule=[]
    for i in  data:
        port=i['port']
        ip=i['host']
        id=i["id"]
    
        a = "cache_peer {0} parent {1} 0  round-robin proxy-only no-query connect-fail-limit=2  name={2}  \n  ".format(ip,port,id)
        
        rule.append(a)
    
    with open("/etc/squid3/peers.conf",'w') as f:
        for i in rule:
            f.write(i)
    os.system('squid3 -s reload')
    os.system('squid3 -k reconfigure')
def run():
    time.sleep(8*3600)
    squid()
if __name__ == '__main__':
    while True:
        print "waiting  for update squid"
        print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        run()