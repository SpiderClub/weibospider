# -*-coding:utf-8 -*-
from db.basic_db import Base
from db.tables import *


class LoginInfo(Base):
    __table__ = login_info


class User(Base):
    __table__ = wbuser


class SeedIds(Base):
    __table__ = seed_ids


class KeyWords(Base):
    __table__ = keywords


class WeiboData(Base):
    __table__ = weibo_data


class KeywordsWbdata(Base):
    __table__ = keywords_wbdata


class WeiboComment(Base):
    __table__ = weibo_comment

    def __repr__(self):
        return 'weibo_id:{},comment_id:{},comment_cont:{}'.format(self.weibo_id, self.comment_id, self.comment_cont)


class WeiboRepost(Base):
    __table__ = weibo_repost

    def __repr__(self):
        return 'id:{},user_id:{},user_name:{},parent_user_id:{},parent_user_name:{}, weibo_url:{},weibo_id:{},' \
               'repost_time:{},repost_cont:{}'.format(self.id, self.user_id, self.user_name, self.parent_user_id,
                                                      self.parent_user_name, self.weibo_url, self.weibo_id,
                                                      self.repost_time, self.repost_cont)


class UserRelation(Base):
    __table__ = user_relation

    def __init__(self, uid, other_id, type):
        self.user_id = uid
        self.follow_or_fans_id = other_id
        self.type = type



