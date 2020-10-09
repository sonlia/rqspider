#-*- coding:utf-8 -*-
#!/usr/bin/python
import libtorrent as bt
def magnet_info(torrent):
    info = bt.torrent_info(torrent)
    size = info.total_size()/1000000000.0
    hash  = info.info_hash()
    name =info.name()
    return  name,hash,round(size,1)
def magnet(magnet_info):
    return  "magnet:?xt=urn:btih:%s&dn=%s" % (magnet_info[1],magnet_info[0])