#-*- coding:utf-8 -*-
#!/usr/bin/python
import six
import json
import copy
import warnings
from collections import MutableMapping
from importlib import import_module
from pprint import pformat



from . import default_settings



class BaseSettings(MutableMapping):



    def __init__(self, values=None):
        self.attributes = {}
        self.update(values)
    def set(self, name, value):
        self.attributes[name] = value
    def setmodule(self, module):
        if isinstance(module, six.string_types):
            module = import_module(module)
        for key in dir(module):
            if key.isupper():
                self.set(key, getattr(module, key))
    def update(self, values):
        if isinstance(values, six.string_types):
            values = json.loads(values)
        if values is not None:
                    self.set(name, value)
    def delete(self, name):
        del self.attributes[name]
    def getlist(self, name):

        value = self.get(name)
        if isinstance(value, six.string_types):
            value = value.split(',')
        return list(value)
    def get(self, name):

        return self[name] 
    def __delitem__(self, name):

        del self.attributes[name]
    def __setitem__(self, name, value):
        self.set(name, value)
    def __iter__(self):
        return iter(self.attributes)

    def __len__(self):
        return len(self.attributes)
    def __iter__(self):
        return iter(self.attributes)
    def __getitem__(self, name):
           return self.attributes[name]
    def copy(self):
        return copy.deepcopy(self)

class Settings(BaseSettings):
    def __init__(self, values=None):

        super(Settings, self).__init__()
        self.setmodule(default_settings)
