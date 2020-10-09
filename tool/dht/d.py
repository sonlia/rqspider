import libtorrent as lt
import time

def magnet2t(link,tfile):
    sess = lt.session()
    params = {
             "save_path": './tfile/',
             "storage_mode":lt.storage_mode_t.storage_mode_sparse,
             "paused": True,
             "auto_managed": True,
             "duplicate_is_error": True
           }

    handle = lt.add_magnet_uri(sess, link, params)

    while (not handle.has_metadata()):
        time.sleep(5)
        print handle.has_metadata()

    torinfo = handle.get_torrent_info()

    fs = lt.file_storage()
    for f in torinfo.files():
        fs.add_file(f)

    torfile = lt.create_torrent(fs)
    torfile.set_comment(torinfo.comment())
    torfile.set_creator(torinfo.creator())

    #for i in xrange(0, torinfo.num_pieces()):
    #    hashes = torinfo.hash_for_piece(i)
    #    torfile.set_hash(i, hashes)

    for url_seed in torinfo.url_seeds():
        torfile.add_url_seed(url_seed)

    for http_seed in torinfo.http_seeds():
        torfile.add_http_seed(http_seed)

    for node in torinfo.nodes():
        torfile.add_node(node)

    for tracker in torinfo.trackers():
        torfile.add_tracker(tracker)

    torfile.set_priv(torinfo.priv())

    t = open(tfile, "wb")
    t.write(lt.bencode(torfile.generate()))
    t.close()
    print '%s  generated!'% tfile

magnet2t('magnet:?xt=urn:btih:510601eb05e96723d9f2a7a18fcfb16f784b44aa',"d.torrent")