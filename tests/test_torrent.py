#coding:utf-8
#!usr/bin/python
from utils.torrent import magnet_info
def test_magnet_info():
    print magnet_info('/home/spider/a.torrent')[2]