from request import request
from group.bt.bt import bt
from group.test import test
from settings import Settings
from spider.base import spider_base
from collections import Iterable ,Iterator
#添加任务
def test_spider_add_task():
        a = request(url = "www.bttiantangs.com")
        b = bt(Settings)
        c = b.add_task(a)
        c.grab.request()
        #获取返回的数据
def test_spider_get_response():
        a = request(url = "www.bttiantangs.com")
        b = bt(Settings)
        c = b.get_response(a)
#得到request  的callback 的 实例
def test_spider_base_find_task_hander():
        a = spider_base(Settings)
        hander = a.find_task_hander("save")
        assert  isinstance(hander,Iterator)==False