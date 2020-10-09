#-*- coding:utf-8 -*-
#!/usr/bin/python
from __future__ import absolute_import
import logging ,sys
from rq.utils import make_colorizer
'''  dark_colors = ["black", "darkred", "darkgreen", "brown", "darkblue",
                       "purple", "teal", "lightgray"]
        light_colors = ["darkgray", "red", "green", "yellow", "blue",
                        "fuchsia", "turquoise", "white"]
                        
CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
'''
red = make_colorizer('red')
def log(name):
    """
    The main entry point of the application
    """
    logger = logging.getLogger(name)
    
    fh = logging.FileHandler("spider_log.log")
    console_handler = logging.StreamHandler(sys.stdout)
    
    
    formatter = logging.Formatter(red('%(asctime)s - %(name)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s'))
    
    fh.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)
    fh.setLevel(logging.INFO)
    console_handler.setLevel(logging.DEBUG)
    

    logger.addHandler(fh)
    logger.addHandler(console_handler)
    
    return logger
