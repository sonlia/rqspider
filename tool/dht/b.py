import libtorrent as lt
import time

'''
    transfer a torrent file to a magnet link
'''
def torrent2magnet(torrent_file):
    
    info = lt.torrent_info(torrent_file)
    link = "magnet:?xt=urn:btih:%s&dn=%s" % (info.info_hash(), info.name())
    return link

'''
    transfer a magnet link to a torrent file
'''
def magnet2torrent(link, torrent_file):
    
    sess = lt.session()
    sess = lt.session()
    sess.listen_on(6881, 6891)
    sess.add_extension('ut_pex')
    sess.add_extension('ut_metadata')
    sess.add_extension('smart_ban')
    sess.add_extension('metadata_transfer') 
    
    sess.add_dht_router("router.utorrent.com", 6881)
    sess.add_dht_router("router.bittorrent.com", 6881)
    sess.add_dht_router("dht.transmissionbt.com", 6881)
    sess.add_dht_router("router.bitcomet.com", 6881)
    sess.add_dht_router("dht.aelitis.com", 6881)
    sess.start_dht()
    sess.start_dht()
    sess.start_lsd()
    sess.start_upnp()
    sess.start_natpmp()

    params = {
        "save_path": 'D:\\Desktop',
        "storage_mode":lt.storage_mode_t.storage_mode_sparse,
        "paused": True,
        "auto_managed": True,
        "duplicate_is_error": True
    }
    handle = lt.add_magnet_uri(sess, link, params)
    
    # waiting for metadata
    while (not handle.has_metadata()):
        time.sleep(5)
    
    # create a torrent
    torinfo = handle.get_torrent_info()
    torfile = lt.create_torrent(torinfo)
    torcontent = lt.bencode(torfile.generate())

    # save to file
    t = open(torrent_file, "wb")
    t.write(torcontent)
    t.close()
    
    return True
from datetime import datetime
c = datetime.now()
magnet2torrent( "magnet:?xt=urn:btih:BFEFB51F4670D682E98382ADF81014638A25105A&dn=openSUSE+13.2+DVD+x86_64.iso&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80&tr=udp%3A%2F%2Ftracker.ccc.de%3A80","b.torrent")
print datetime.now()-c,"ok"