#coding:utf-8
#!usr/bin/python
from src.core.engine import  CrawlerRunner ,start
import sys
import os
import shutil
import tempfile
module_dir = os.path.dirname(os.path.abspath(__file__))
class Test_engine:
    def test_crawl(self):
        orig_spiders_dir = os.path.join(module_dir, 'a')
        tmpdir = tempfile.mkdtemp()

        spiders_dir = os.path.join(tmpdir, 'a')

        shutil.copytree(orig_spiders_dir, spiders_dir)
        sys.path.append(tmpdir)
        print (sys.path)
        # print("start ...debug")
        # print(sys.path )
        # runner = CrawlerRunner()
        # runner.crawl("a")
        # print ("dd")
        start()