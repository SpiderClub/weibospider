from sqlalchemy import text
from sqlalchemy.exc import IntegrityError as SqlalchemyIntegrityError
from pymysql.err import IntegrityError as PymysqlIntegrityError
from sqlalchemy.exc import InvalidRequestError

from logger import db_logger
from .basic import get_db_session
from .models import (
    LoginInfo, KeywordsWbdata, KeyWords, SeedIds,
    WeiboComment, WeiboRepost, User, WeiboData, WeiboPraise
)


class CommonOper:
    @classmethod
    def add_one(cls, data):
        rs = 1
        with get_db_session() as db:
            try:
                db.add(data)
                db.commit()
            except SqlalchemyIntegrityError:
                rs = 0
            except Exception as e:
                db_logger.error('exception {} is raied'.format(e))
                rs = 0
        return rs

    @classmethod
    def add_all(cls, datas):
        count = len(datas)
        with get_db_session() as db:
            try:
                db.add_all(datas)
                db.commit()
            except (SqlalchemyIntegrityError, PymysqlIntegrityError,
                    InvalidRequestError):
                count = 0
                for data in datas:
                    count += cls.add_one(data)
        return count


class LoginInfoOper:
    @classmethod
    def get_login_info(cls):
        with get_db_session() as db:
            return db.query(LoginInfo.name, LoginInfo.password,
                            LoginInfo.enable).filter(text('enable=1')).all()

    @classmethod
    def freeze_account(cls, name, rs):
        """
        :param name: login account
        :param rs: 0 stands for banned，1 stands for normal，
        2 stands for name or password is invalid
        :return:
        """
        with get_db_session() as db:
            account = db.query(LoginInfo).filter(LoginInfo.name == name).first()
            account.enable = rs
            db.commit()


class KeywordsDataOper:
    @classmethod
    def insert_keyword_wbid(cls, keyword_id, wbid):
        with get_db_session() as db:
            keyword_wbdata = KeywordsWbdata()
            keyword_wbdata.wb_id = wbid
            keyword_wbdata.keyword_id = keyword_id
            db.add(keyword_wbdata)
            db.commit()


class KeywordsOper:
    @classmethod
    def get_search_keywords(cls):
        with get_db_session() as db:
            return db.query(KeyWords.keyword, KeyWords.id). \
                filter(text('enable=1')).all()

    @classmethod
    def set_useless_keyword(cls, keyword):
        with get_db_session() as db:
            search_word = db.query(KeyWords).filter \
                (KeyWords.keyword == keyword).first()
            search_word.enable = 0
            db.commit()


class SeedidsOper:
    @classmethod
    def get_seed_ids(cls):
        """
        Get all user id to be crawled
        :return: user ids
        """
        with get_db_session() as db:
            return db.query(SeedIds.uid).filter(text('is_crawled=0')).all()

    @classmethod
    def get_home_ids(cls):
        """
        Get all user id who's home pages need to be crawled
        :return: user ids
        """
        with get_db_session() as db:
            return db.query(SeedIds.uid).filter(text('home_crawled=0')).all()

    @classmethod
    def set_seed_crawled(cls, uid, result):
        """
        :param uid: user id that is crawled
        :param result: crawling result, 1 stands for succeed, 2 stands for fail
        :return: None
        """
        # todo make sure whether the seed variable should be inside or outside
        with get_db_session() as db:
            seed = db.query(SeedIds).filter(SeedIds.uid == uid).first()

            if seed and seed.is_crawled == 0:
                seed.is_crawled = result
            else:
                seed = SeedIds(uid=uid, is_crawled=result)
                db.add(seed)
            db.commit()

    @classmethod
    def get_seed_by_id(cls, uid):
        with get_db_session() as db:
            return db.query(SeedIds).filter(SeedIds.uid == uid).first()

    @classmethod
    def insert_seeds(cls, ids):
        with get_db_session() as db:
            db.execute(SeedIds.__table__.insert().
                       prefix_with('IGNORE'), [{'uid': i} for i in ids])
            db.commit()

    @classmethod
    def set_seed_other_crawled(cls, uid):
        """
        update it if user id already exists, else insert
        :param uid: user id
        :return: None
        """
        with get_db_session() as db:
            seed = cls.get_seed_by_id(uid)
            if seed is None:
                seed = SeedIds(uid=uid, is_crawled=1, other_crawled=1, home_crawled=1)
                db.add(seed)
            else:
                seed.other_crawled = 1
            db.commit()

    @classmethod
    def set_seed_home_crawled(cls, uid):
        """
        :param uid: user id
        :return: None
        """
        with get_db_session() as db:
            seed = cls.get_seed_by_id(uid)
            if seed is None:
                seed = SeedIds(uid=uid, is_crawled=0, other_crawled=0, home_crawled=1)
                db.add(seed)
            else:
                seed.home_crawled = 1
            db.commit()


class UserOper(CommonOper):
    @classmethod
    def get_user_by_uid(cls, uid):
        with get_db_session() as db:
            return db.query(User).filter(User.uid == uid).first()

    @classmethod
    def get_user_by_name(cls, user_name):
        with get_db_session() as db:
            return db.query(User).filter(User.name == user_name).first()


class UserRelationOper(CommonOper):
    pass


class WbDataOper(CommonOper):
    @classmethod
    def get_wb_by_mid(cls, mid):
        with get_db_session() as db:
            return db.query(WeiboData).filter(WeiboData.weibo_id == mid).first()

    @classmethod
    def get_weibo_comment_not_crawled(cls):
        with get_db_session() as db:
            return db.query(WeiboData.weibo_id).filter(text('comment_crawled=0')).all()

    @classmethod
    def get_weibo_praise_not_crawled(cls):
        with get_db_session() as db:
            return db.query(WeiboData.weibo_id).filter(text('praise_crawled=0')).all()

    @classmethod
    def get_weibo_repost_not_crawled(cls):
        with get_db_session() as db:
            return db.query(WeiboData.weibo_id, WeiboData.uid).filter(
                text('repost_crawled=0')).all()

    @classmethod
    def get_weibo_dialogue_not_crawled(cls):
        with get_db_session() as db:
            return db.query(WeiboData.weibo_id).filter(text('dialogue_crawled=0')).all()

    # todo find a better way to do all the below
    @classmethod
    def set_weibo_comment_crawled(cls, mid):
        with get_db_session() as db:
            data = cls.get_wb_by_mid(mid)
            if data:
                data.comment_crawled = 1
                db.commit()

    @classmethod
    def set_weibo_praise_crawled(cls, mid):
        with get_db_session() as db:
            data = cls.get_wb_by_mid(mid)
            if data:
                data.praise_crawled = 1
                db.commit()

    @classmethod
    def set_weibo_repost_crawled(cls, mid):
        with get_db_session() as db:
            data = cls.get_wb_by_mid(mid)
            if data:
                data.repost_crawled = 1
                db.commit()

    @classmethod
    def set_weibo_dialogue_crawled(cls, mid):
        with get_db_session() as db:
            data = cls.get_wb_by_mid(mid)
            if data:
                data.dialogue_crawled = 1
                db.commit()


class CommentOper(CommonOper):
    @classmethod
    def get_comment_by_id(cls, cid):
        with get_db_session() as db:
            return db.query(WeiboComment).filter(
                WeiboComment.comment_id == cid).first()


class PraiseOper(CommonOper):
    @classmethod
    def get_Praise_by_id(cls, pid):
        with get_db_session() as db:
            return db.query(WeiboPraise).filter(WeiboPraise.weibo_id == pid).first()


class RepostOper(CommonOper):
    @classmethod
    def get_repost_by_rid(cls, rid):
        with get_db_session() as db:
            return db.query(WeiboRepost).filter(WeiboRepost.weibo_id == rid).first()
