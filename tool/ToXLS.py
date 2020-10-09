#-*- coding:utf-8 -*-
#!/usr/bin/python
from __future__ import absolute_import
import pymongo
import  xlwt

class mongo:
    def __init__(self,dbname="spiders_data"):
        self.client = pymongo.MongoClient("192.168.2.243", 27017)
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
xls = xlwt.Workbook()  
sheet = xls.add_sheet("Sheet1") 
d = mongo()
data = d.get("dt").find({})

for i,dd in 	enumerate(data) :

    sheet.write(i,0, dd["CompanyName"])
    sheet.write(i,1, dd["area"])
    sheet.write(i,2, dd["address"])
    sheet.write(i,3, dd["contact"])
    sheet.write(i,4, dd["telephone"])
    sheet.write(i,5, dd["fax"])
    sheet.write(i,6, dd["email"])
    sheet.write(i,7, dd["web"])
    sheet.write(i,8, dd["description"])
    sheet.write(i,9, ",".join(dd["Category"]))


xls.save("c.xls")