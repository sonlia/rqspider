#coding:utf-8
#!usr/bin/python
from utils.bloomfilter import BloomFilter as _bf
def test_bloomfilter():
    bf = _bf()
    assert bf.check("www.bawidu.com")==False