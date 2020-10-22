#coding:utf-8
#!usr/bin/python
def decorator(aClass):
    class newClass:
        def __init__(self, age):
            self.total_display   = 0
            # self.wrapped         = aClass(age)
        def display(self):
            self.total_display += 1
            print("total display: ", self.total_display)
            # self.wrapped.display()
    return newClass
#对类使用装饰器
@decorator
class Blog:
    def __init__(self, age):
        self.age = age
    def display(self):
        print("http://blog.csdn.net/caimouse age is", self.age)
 
 
# #创建类对象
# myBlog = Blog(15)
# for i in range(3):
#     myBlog.display()
import  pickledb
db=pickledb.load('example.db',False) # 加载数据库，如果没有会自动创建


dict_=db.dcreate('erew') # 创建dict


db.dadd('erew',(1,2)) # 将一个键值对添加到字典中，“pair”是一个元组
# dict_=db.dcreate('erew') # 创建dict
db.dadd('erew',(2,3))
print db.dgetall('erew') # 从字典中返回所有键值对 {1: 2, 2: 3}
print db.getall()

ist_=db.lcreate('database') # 创建list

data={1:1,2:2,3:3}

db.ladd('database',data) # 将data 添加到list
db.ladd('database',data) # 将data 添加到list

print db.lgetall('database') # 获取list中的所有内容 [{1: 1, 2: 2, 3: 3}]
print db.getall()

