# -*- coding: utf-8 -*-
from __future__ import absolute_import
import sys  
# sys.path.append("/home/spider")
# print(sys.path)
# print sys.modules

from collections import defaultdict
from utils.misc_spider import walk_modules ,iter_spider_classes

class spider_loader_1(object):

    def __init__(self):

        self.spider_modules = "bttiantangs"

        self._spiders = {}
        self._found = defaultdict(list)
        self._load_all_spiders()

    def _load_spiders(self, module):
        for spcls in iter_spider_classes(module):
            self._found[spcls.name].append((module.__name__, spcls.__name__))
            self._spiders[spcls.name] = spcls
    def _load_all_spiders(self):
        for name in self.spider_modules:
            try:

                for module in walk_modules(name):

                    self._load_spiders(module)
            except:
                print "no spider in the project"

    def load(self, spider_name):
        try:
            return self._spiders[spider_name]
        except KeyError:
            raise KeyError("Spider not found: {}".format(spider_name))
from settings import Settings
from utils.misc_spider import spider_single_reponse
from  utils.misc_spider import _import_file
class spider_loader(object): 
    def __init__(self,path,name):
        self.path=path
        self.name=name

    def  import_module(self,path,name):
            instan = _import_file(path)
            return getattr(instan, name)
    def load(self,url,callback):
        spider = self.import_module(self.path,self.name)
        newspider =spider_single_reponse(spider)
        if callback=='start':
            iteration_request=newspider.start()
            return newspider.process_task(iteration_request)
        else:
            return newspider.run(url)
    def requestlist(self,url,callback):
            index = 0
            for  i in  self.load(url,callback):
                        index+=1
                        _url = i.url
                        _callback = i.callback
                        isParent=True
                        tmp.append({'path':self.path,'name':str(index)+str(':')+_callback,'url':_url,'callback':_callback,'isParent': isParent,'spiderclass':self.spiderclass})
                        print  tmp,'4444'
            return tmp
if __name__ == "__main__":
    import sys
    spider_loader(sys.argv[1],sys.argv[2]).requestlist(sys.argv[3],sys.argv[4])
