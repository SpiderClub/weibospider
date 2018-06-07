from .basic import Base
from .tables import *


class LoginInfo(Base):
    __table__ = login_info


class User(Base):
    __table__ = wbuser

    def __init__(self, uid):
        self.uid = uid


class SeedId(Base):
    __table__ = seed_id


class KeyWord(Base):
    __table__ = keyword


class WeiboData(Base):
    __table__ = wbdata

    def __repr__(self):
        return 'weibo url:{};weibo content:{}'.format(self.weibo_url,
                                                      self.weibo_cont)


class TaskLabel(Base):
    __table__ = task_label

    def __init__(self, mid):
        self.weibo_id = mid


class KeywordWbdata(Base):
    __table__ = keyword_wbdata


class WeiboComment(Base):
    __table__ = comment

    def __repr__(self):
        return 'weibo_id:{},comment_id:{},comment_cont:{}'.format(
            self.weibo_id, self.comment_id, self.comment_cont)


class WeiboPraise(Base):
    __table__ = praise

    def __repr__(self):
        return 'user_id:{},weibo_id:{}'.format(self.user_id, self.weibo_id)


class WeiboRepost(Base):
    __table__ = repost

    def __repr__(self):
        return 'id:{},user_id:{},user_name:{},parent_user_id:{},parent_user_name:{},' \
               ' weibo_url:{},weibo_id:{}, repost_time:{},repost_cont:{}'.format(
            self.id, self.user_id, self.user_name, self.parent_user_id,
            self.parent_user_name, self.weibo_url, self.weibo_id, self.repost_time,
            self.repost_cont)


class UserRelation(Base):
    __table__ = relation

    def __init__(self, uid, other_id, type):
        self.user_id = uid
        self.follow_or_fans_id = other_id
        self.type = type

    def __repr__(self):
        return 'user_id:{},follow_or_fans_id:{},type:{}'.format(self.user_id, self.follow_or_fans_id, self.type)


class WeiboDialogue(Base):
    __table__ = dialogue

    def __repr__(self):
        return 'weibo_id:{},dialogue_id:{},dialogue_cont:{}'.format(
            self.weibo_id, self.dialogue_id, self.dialogue_cont)
