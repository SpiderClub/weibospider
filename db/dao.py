from sqlalchemy import text
from sqlalchemy.exc import IntegrityError as SqlalchemyIntegrityError
from pymysql.err import IntegrityError as PymysqlIntegrityError
from sqlalchemy.exc import InvalidRequestError

from .basic import db_session
from .models import (
    LoginInfo, KeywordsWbdata, KeyWords, SeedIds,
    WeiboComment, WeiboRepost, User, WeiboData
)
from decorators import db_commit_decorator


class CommonOper:
    @classmethod
    @db_commit_decorator
    def add_one(cls, data):
        db_session.add(data)
        db_session.commit()

    @classmethod
    @db_commit_decorator
    def add_all(cls, datas):
        try:
            db_session.add_all(datas)
            db_session.commit()
        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            for data in datas:
                cls.add_one(data)


class LoginInfoOper:
    @classmethod
    def get_login_info(cls):
        return db_session.query(LoginInfo.name, LoginInfo.password, LoginInfo.enable). \
            filter(text('enable=1')).all()

    @classmethod
    @db_commit_decorator
    def freeze_account(cls, name, rs):
        """
        :param name: login account
        :param rs: 0 stands for banned，1 stands for normal，2 stands for name or password is invalid
        :return:
        """
        account = db_session.query(LoginInfo).filter(LoginInfo.name == name).first()
        account.enable = rs
        db_session.commit()


class KeywordsDataOper:
    @classmethod
    @db_commit_decorator
    def insert_keyword_wbid(cls, keyword_id, wbid):
        keyword_wbdata = KeywordsWbdata()
        keyword_wbdata.wb_id = wbid
        keyword_wbdata.keyword_id = keyword_id
        db_session.add(keyword_wbdata)
        db_session.commit()


class KeywordsOper:
    @classmethod
    def get_search_keywords(cls):
        return db_session.query(KeyWords.keyword, KeyWords.id).filter(text('enable=1')).all()

    @classmethod
    @db_commit_decorator
    def set_useless_keyword(cls, keyword):
        search_word = db_session.query(KeyWords).filter(KeyWords.keyword == keyword).first()
        search_word.enable = 0
        db_session.commit()


class SeedidsOper:
    @classmethod
    def get_seed_ids(cls):
        """
        Get all user id to be crawled
        :return: user ids
        """
        return db_session.query(SeedIds.uid).filter(text('is_crawled=0')).all()

    @classmethod
    def get_home_ids(cls):
        """
        Get all user id who's home pages need to be crawled
        :return: user ids
        """
        return db_session.query(SeedIds.uid).filter(text('home_crawled=0')).all()

    @classmethod
    @db_commit_decorator
    def set_seed_crawled(cls, uid, result):
        """
        :param uid: user id that is crawled
        :param result: crawling result, 1 stands for succeed, 2 stands for fail
        :return: None
        """
        seed = db_session.query(SeedIds).filter(SeedIds.uid == uid).first()

        if seed and seed.is_crawled == 0:
            seed.is_crawled = result
        else:
            seed = SeedIds(uid=uid, is_crawled=result)
            db_session.add(seed)
        db_session.commit()

    @classmethod
    def get_seed_by_id(cls, uid):
        return db_session.query(SeedIds).filter(SeedIds.uid == uid).first()

    @classmethod
    @db_commit_decorator
    def insert_seeds(cls, ids):
        db_session.execute(SeedIds.__table__.insert().prefix_with('IGNORE'), [{'uid': i} for i in ids])
        db_session.commit()

    @classmethod
    @db_commit_decorator
    def set_seed_other_crawled(cls, uid):
        """
        update it if user id already exists, else insert
        :param uid: user id
        :return: None
        """
        seed = cls.get_seed_by_id(uid)
        if seed is None:
            seed = SeedIds(uid=uid, is_crawled=1, other_crawled=1, home_crawled=1)
            db_session.add(seed)
        else:
            seed.other_crawled = 1
        db_session.commit()

    @classmethod
    @db_commit_decorator
    def set_seed_home_crawled(cls, uid):
        """
        :param uid: user id
        :return: None
        """
        seed = cls.get_seed_by_id(uid)
        if seed is None:
            seed = SeedIds(uid=uid, is_crawled=0, other_crawled=0, home_crawled=1)
            db_session.add(seed)
        else:
            seed.home_crawled = 1
        db_session.commit()


class UserOper(CommonOper):
    @classmethod
    def get_user_by_uid(cls, uid):
        return db_session.query(User).filter(User.uid == uid).first()


class UserRelationOper(CommonOper):
    pass


class WbDataOper(CommonOper):
    @classmethod
    def get_wb_by_mid(cls, mid):
        return db_session.query(WeiboData).filter(WeiboData.weibo_id == mid).first()

    @classmethod
    def get_weibo_comment_not_crawled(cls):
        return db_session.query(WeiboData.weibo_id).filter(text('comment_crawled=0')).all()

    @classmethod
    def get_weibo_repost_not_crawled(cls):
        return db_session.query(WeiboData.weibo_id, WeiboData.uid).filter(text('repost_crawled=0')).all()

    @classmethod
    def get_weibo_dialogue_not_crawled(cls):
        return db_session.query(WeiboData.weibo_id).filter(text('dialogue_crawled=0')).all()

    @classmethod
    @db_commit_decorator
    def set_weibo_comment_crawled(cls, mid):
        data = cls.get_wb_by_mid(mid)
        if data:
            data.comment_crawled = 1
            db_session.commit()

    @classmethod
    @db_commit_decorator
    def set_weibo_repost_crawled(cls, mid):
        data = cls.get_wb_by_mid(mid)
        if data:
            data.repost_crawled = 1
            db_session.commit()

    @classmethod
    @db_commit_decorator
    def set_weibo_dialogue_crawled(cls, mid):
        data = cls.get_wb_by_mid(mid)
        if data:
            data.dialogue_crawled = 1
            db_session.commit()


class CommentOper(CommonOper):
    @classmethod
    def get_comment_by_id(cls, cid):
        return db_session.query(WeiboComment).filter(WeiboComment.comment_id == cid).first()


class RepostOper(CommonOper):
    @classmethod
    def get_repost_by_rid(cls, rid):
        return db_session.query(WeiboRepost).filter(WeiboRepost.weibo_id == rid).first()
