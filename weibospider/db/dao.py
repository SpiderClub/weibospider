from pymysql.err import IntegrityError as PymysqlIntegrityError
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError as SqlalchemyIntegrityError
from sqlalchemy.exc import InvalidRequestError

from ..logger import db_logger
from .basic import get_db_session
from .models import (
    LoginInfo, KeyWord, SeedId,
    User, WeiboData, KeywordWbdata,
    TaskLabel
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

    @classmethod
    def get_attrs_by_key(cls, model, attrs, conditions='1=1'):
        """
        get entities' assigned atters according to conditons
        :param model: sqlalchemy model
        :param attrs: attrs that will be return, it's a list
        :param conditions: filter conditions
        """
        model_attrs = list()
        for attr in attrs:
            model_attr = getattr(model, attr)
            if model_attr:
                model_attrs.append(model_attr)

        with get_db_session() as db:
            return db.query(*model_attrs).filter(text(conditions)).all()

    @classmethod
    def get_entity_by_key(cls, model, conditions):
        """get one entity according to the conditions"""
        with get_db_session() as db:
            return db.query(model).filter(text(conditions)).first()

    @classmethod
    def set_entity_attrs(cls, model, conditions, attr_maps):
        """set attrs for the entity"""
        entity = cls.get_entity_by_key(model, conditions)
        if not entity:
            return

        with get_db_session() as db:
            for attr, value in attr_maps.items():
                setattr(entity, attr, value)
            db.merge(entity)
            db.commit()

    @classmethod
    def update_or_insert_entity(cls, model, conditions, attr_maps):
        entity = cls.get_entity_by_key(model, conditions)
        with get_db_session() as db:
            if not entity:
                entity = model()
                for attr, value in attr_maps.items():
                    setattr(entity, attr, value)
                cls.add_one(entity)
            else:
                for attr, value in attr_maps.items():
                    setattr(entity, attr, value)
                db.merge(entity)
            db.commit()


class LoginInfoOper(CommonOper):
    @classmethod
    def get_login_info(cls):
        attrs = ['name', 'password', 'enable']
        return cls.get_attrs_by_key(attrs, 'enable=1')

    @classmethod
    def freeze_account(cls, name, rs):
        """
        :param name: login account
        :param rs: 0 stands for banned，1 stands for normal，
        2 stands for name or password is invalid
        :return:
        """
        # notice that if it's a str in conditions, use double quote like "str"
        conditions = 'name="{}"'.format(name)
        maps = {'enable': rs}
        cls.set_entity_attrs(LoginInfo, conditions, maps)


class KeywordsOper(CommonOper):
    @classmethod
    def get_search_keywords(cls):
        attrs = ['keyword', 'id']
        return cls.get_attrs_by_key(KeyWord, attrs, 'enable=1')


class SeedidsOper(CommonOper):
    @classmethod
    def get_seed_ids(cls):
        return cls.get_attrs_by_key(SeedId, ['uid'], 'is_crawled=0')

    @classmethod
    def get_home_ids(cls):
        return cls.get_attrs_by_key(SeedId, ['uid'], 'home_crawled=0')

    @classmethod
    def get_relation_ids(cls):
        return cls.get_attrs_by_key(SeedId, ['uid'], 'relation_crawled=0')

    @classmethod
    def get_seed_by_id(cls, uid):
        return cls.get_entity_by_key(SeedId, 'uid={}'.format(uid))

    @classmethod
    def insert_seeds(cls, ids):
        with get_db_session() as db:
            db.execute(SeedId.__table__.insert().
                       prefix_with('IGNORE'), [{'uid': i} for i in ids])
            db.commit()

    @classmethod
    def set_seed_crawled(cls, uid, result):
        """
        :param uid: user id that is crawled
        :param result: crawling result, 1 stands for success,
        2 stands for failure
        """
        maps = {
            'uid': uid,
            'is_crawled': result,
        }
        cls.update_or_insert_entity(SeedId, 'uid={}'.format(uid), maps)

    @classmethod
    def set_relation_crawled(cls, uid):
        maps = {
            'uid': uid,
            'relation_crawled': 1,
        }
        cls.update_or_insert_entity(SeedId, 'uid={}'.format(uid), maps)

    @classmethod
    def set_home_crawled(cls, uid):
        maps = {
            'uid': uid,
            'home_crawled': 1
        }
        cls.update_or_insert_entity(SeedId, 'uid={}'.format(uid), maps)


class UserOper(CommonOper):
    @classmethod
    def get_user_by_uid(cls, uid):
        return cls.get_entity_by_key(User, 'uid={}'.format(uid))

    @classmethod
    def get_user_by_name(cls, user_name):
        return cls.get_entity_by_key(User, 'name="{}"'.format(user_name))


class WbDataOper(CommonOper):
    @classmethod
    def get_weibo_by_mid(cls, mid):
        return cls.get_entity_by_key(WeiboData, 'weibo_id={}'.format(mid))

    @classmethod
    def get_comment_not_crawled(cls):
        return cls.get_attrs_by_key(TaskLabel, ['weibo_id'], 'comment_crawled=0')

    @classmethod
    def get_praise_not_crawled(cls):
        return cls.get_attrs_by_key(TaskLabel, ['weibo_id'], 'praise_crawled=0')

    @classmethod
    def get_repost_not_crawled(cls):
        return cls.get_attrs_by_key(TaskLabel, ['weibo_id'], 'repost_crawled=0')

    @classmethod
    def get_dialogue_not_crawled(cls):
        return cls.get_attrs_by_key(TaskLabel, ['weibo_id'], 'dialogue_crawled=0')

    @classmethod
    def get_img_not_download(cls):
        with get_db_session() as db:
            rs = db.query(TaskLabel.weibo_id).join(
                WeiboData, WeiboData.weibo_id == TaskLabel.weibo_id).filter(
                WeiboData.weibo_img != "")
            return rs

    @classmethod
    def set_comment_crawled(cls, mid):
        maps = {'comment_crawled': 1}
        cls.set_entity_attrs(TaskLabel, 'weibo_id={}'.format(mid), maps)

    @classmethod
    def set_praise_crawled(cls, mid):
        maps = {'praise_crawled': 1}
        cls.set_entity_attrs(TaskLabel, 'weibo_id={}'.format(mid), maps)

    @classmethod
    def set_repost_crawled(cls, mid):
        maps = {'repost_crawled': 1}
        cls.set_entity_attrs(TaskLabel, 'weibo_id={}'.format(mid), maps)

    @classmethod
    def set_dialogue_crawled(cls, mid):
        maps = {'dialogue_crawled': 1}
        cls.set_entity_attrs(TaskLabel, 'weibo_id={}'.format(mid), maps)

    @classmethod
    def set_img_downloaded(cls, mid):
        maps = {'image_download': 1}
        cls.set_entity_attrs(TaskLabel, 'weibo_id={}'.format(mid), maps)


class KeywordsDataOper(CommonOper):
    @classmethod
    def get_weibo_ids(cls, keyword_id, wb_id):
        conditions = 'keyword_id={} and wb_id={}'.format(keyword_id, wb_id)
        return cls.get_attrs_by_key(KeywordWbdata, ['keyword_id', 'wb_id'], conditions)


class RelationOper(CommonOper):
    pass


class RepostOper(CommonOper):
    pass


class CommentOper(CommonOper):
    pass


class PraiseOper(CommonOper):
    pass


class Dialogue(CommonOper):
    pass

