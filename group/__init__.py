#-*- coding:utf-8 -*-
#!/usr/bin/python
# from spider.base import spider
# from spider.base import request
# from spider.base import _log
# import re
# from spider.utils.misc import parse
    
    
# __all__=["re","parse","_log","request","spider"]
from utils.log import log as _log
from core.base import spider
from core.base import request
from utils.log import log as _log
from utils.database import  mongo as db
from utils.database import  data as tmp
from utils.misc import extract_douban_id,extract_imdb_id,extract_magnet