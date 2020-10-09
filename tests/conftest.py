import sys, os
# myPath = os.path.dirname(os.path.abspath(__file__))
# # sys.path.insert(0, myPath + '/../')
# sys.path.insert(0, '../')
import sys, os
sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))))
import pytest
# from utils.database import mongo

# from spider.core.core import core
# from spider.requspiderest import request as reqs
# from spider.spider.base import spider


# @pytest.fixture
# def db():
#     m = mongo('spiders_data')
#     return m
# @pytest.fixture
# def curl():
#         a = core('GET',url='http://www.bttiantangs.com/')
#         g = a.send()
#         return g
# @pytest.fixture
# def request_able():
#     # print help(req)
#     yield req(url="http://www.bttiantangs.com/",callback='content',meta={"s":"d"})
# @pytest.fixture
# def base():
#     return spider()