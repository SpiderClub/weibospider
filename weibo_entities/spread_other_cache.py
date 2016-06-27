# -*-coding:utf-8 -*-
# 该类用于过滤获取spreadother的upperuserid
class SpreadOtherCache(object):
    def __init__(self):
        self.user_id = ''
        self.user_name = ''

    def set_id(self, uid):
        self.user_id = uid

    def set_name(self, name):
        self.user_name = name

    def get_id(self):
        return self.user_id

    def get_name(self):
        return self.user_name

    def __str__(self):
        return 'id={id},name={name}'.format(id=self.user_id, name=self.user_name)