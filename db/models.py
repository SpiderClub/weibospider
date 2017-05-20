# -*-coding:utf-8 -*-
from sqlalchemy import Column, INTEGER, String
from db.basic_db import Base
from db.tables import *


class LoginInfo(Base):
    # 登录账号表 login_info
    __table__ = login_info


class User(Base):
    # 用户表 wbuser
    __table__ = wbuser
    # 这里需要设置默认值，否则空的话可能会存储None，可能会引发未catch的异常


class SeedIds(Base):
    # 种子用户表 seed_ids
    __table__ = seed_ids


class KeyWords(Base):
    # 关键词搜索表 keywords
    __table__ = keywords


class WeiboData(Base):
    # 微博信息表 weibo_data
    __table__ = weibo_data


class KeywordsWbdata(Base):
    # 微博信息关键词联系表 keywords_wbdata
    __table__ = keywords_wbdata


class WeiboComment(Base):
    # 微博评论表
    __table__ = weibo_comment

    def __repr__(self):
        return 'weibo_id:{},comment_id:{},comment_cont:{}'.format(self.weibo_id, self.comment_id, self.comment_cont)
