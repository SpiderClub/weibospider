# -*-coding:utf-8 -*-
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


class WeiboRepost(Base):
    # 微博转发信息
    __table__ = weibo_repost

    def __repr__(self):
        return 'id:{},user_id:{},user_name:{},parent_user_id:{},parent_user_name:{}, weibo_url:{},weibo_id:{},' \
               'repost_time:{},repost_cont:{}'.format(self.id, self.user_id, self.user_name, self.parent_user_id,
                                                      self.parent_user_name, self.weibo_url, self.weibo_id,
                                                      self.repost_time, self.repost_cont)


