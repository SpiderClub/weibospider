# -*-coding:utf-8 -*-
class SpreadOtherAndCache(object):
    def __init__(self, so, soc):
        self.__so = so
        self.__soc = soc

    def get_so(self):
        return self.__so

    def get_soc(self):
        return self.__soc

    def set_so(self, so):
        self.__so = so

    def set_soc(self, soc):
        self.__soc = soc
