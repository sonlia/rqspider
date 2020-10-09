#-*- coding:utf-8 -*-
#!/usr/bin/python
from __future__ import absolute_import
from utils.database import  mongo as db
from  grab import Grab

d = db()
data = d.get("trade").find({},{'_id':1,'email':1})
def seo(email):
    url = "http://seo.hkisit.com/index.php/checkemail?mail={0}".format(email)
    g = Grab(url=url )
    seo_headers={
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7",
    "Connection":"keep-alive",
    "Host":"seo.hkisit.com",
    "Referer":url,
    "Upgrade-Insecure-Requests":1
    }

    g.setup(headers=seo_headers)
    d = g.request()
    if    ''.join(d.tree.xpath('//p[@class="text-muted"]/following-sibling::*/text()')[0]).encode("utf-8").find("可到达对方服务器")==1 :
        return email,0.3
    else: return email,0
def hscript(email):
    url="https://www.hscripts.com/cn/tools/mailid%E9%AA%8C%E8%AF%81/%E6%8C%87%E6%95%B0.html"
    headers = {

        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7",
        "Cache-Control":"max-age=0",
        "Connection":"keep-alive",

        "Content-Type":"application/x-www-form-urlencoded",
        "Host":"www.hscripts.com",
        "Origin":"https://www.hscripts.com",
        "Referer":url,
        "Upgrade-Insecure-Requests":1,
        }

    g = Grab(url=url)
    g.setup(headers=headers,post={"email":"meer@dtusb.com" ,"start":"go"})
    d = g.request()
    print d.tree.xpath("//form[@name='email-ver']//span/text()")[0].encode("utf-8").find("电子邮件地址无效")
    if   d.tree.xpath("//form[@name='email-ver']//span/text()")[0].encode("utf-8").find("电子邮件地址无效")==-1:
        return 0
    else:
        return 1
