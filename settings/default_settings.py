#-*- coding:utf-8 -*-
#!/usr/bin/python
# debug  runnig ,test, prodcue

QUEUES = ['high', 'normal', 'low','default']
DB_URL = {  #在debug 所用数据库，与 生产 环境分开
           "run":"redis://localhost:6379/0",    # 生产环境队列
        #   "temp":"redis://localhost:6379/2" ,  #爬虫临时数据
          "save":"mongodb://192.168.2.243:6379/1"  , #数据保存 的数据库
        #   "test":"redis://localhost:6379/1",    # 临时测试队列
        }


