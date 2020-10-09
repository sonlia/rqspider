#-*- coding:utf-8 -*-
#!/usr/bin/python
from __future__ import absolute_import
# from group.bt.bt import bt
from group.yify_torrent.yify_torrent import yify_torrent
from settings import Settings
class engine(object):

    def start(self):

        g = bt(Settings)
        g1 = yify_torrent(Settings)

        iteration_request  = g.debug()
        iteration_request1  = g1.debug()
        g.process_task(iteration_request)
        g1.process_task(iteration_request1)


if  __name__ == "__main__":
    en = engine()
    en.start()