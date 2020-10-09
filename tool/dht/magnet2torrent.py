import libtorrent
import time
import tempfile
import binascii
import sys


def magnet2torrent(link,torrent_file):
  sess = libtorrent.session()
  sess.add_dht_router('router.bittorrent.com', 6881)
  sess.add_dht_router('router.utorrent.com', 6881)
  sess.add_dht_router('router.bitcomet.com', 6881)
  sess.add_dht_router('dht.transmissionbt.com', 6881)
  sess.start_dht();
  params = {
            "save_path": tempfile.gettempdir(),
            "storage_mode":libtorrent.storage_mode_t.storage_mode_sparse,
            "paused": True,
            "auto_managed": True,
            "duplicate_is_error": True
           }
  handle = libtorrent.add_magnet_uri(sess, link, params)
  while True:
    s = handle.status()
    print "waiting..."
    if s.state != 2:
      t = handle.get_torrent_info()
      print "Saving torrent -=%s=-" % t.name()
      fs = libtorrent.file_storage()
      for i in t.files():
        fs.add_file(i)
        print "\tFile: %s" % i.path
      ct = libtorrent.create_torrent(fs) 
      for i in t.trackers():
        print "\tTracker: %s, %s " % (i.url, i.tier)
        ct.add_tracker(i.url, i.tier)
      ct.set_creator(t.creator())
      ct.set_comment(t.comment())
      ct.set_priv(t.priv())
      f = open(torrent_file, "wb")
      g = ct.generate()
      g["info"]["pieces"] = "".join([binascii.unhexlify("%s" % t.hash_for_piece(i)) for i in range(t.num_pieces())])
      g["info"]["piece length"] = t.piece_length()
      g["info"]["length"] = t.total_size()
      f.write(libtorrent.bencode(g))
      f.close()
      return
    time.sleep(1) # sleep for a second
magnet2torrent('magnet:?xt=urn:btih:510601eb05e96723d9f2a7a18fcfb16f784b44aa',"a.torrent")