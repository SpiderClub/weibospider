from sqlalchemy import text
from sqlalchemy.exc import IntegrityError as SI
from pymysql.err import IntegrityError as PI
from sqlalchemy.exc import InvalidRequestError

from .basic_db import db_session
from .models import WeiboData
from decorators import db_commit_decorator


def get_wb_by_mid(mid):
    return db_session.query(WeiboData).filter(WeiboData.weibo_id == mid).first()


def get_weibo_comment_not_crawled():
    return db_session.query(WeiboData.weibo_id).filter(text('comment_crawled=0')).all()


def get_weibo_repost_not_crawled():
    return db_session.query(WeiboData.weibo_id, WeiboData.uid).filter(text('repost_crawled=0')).all()


@db_commit_decorator
def insert_weibo_data(data):
    db_session.add(data)
    db_session.commit()


@db_commit_decorator
def insert_weibo_datas(datas):
    try:
        db_session.add_all(datas)
        db_session.commit()
    except (SI, PI, InvalidRequestError):
        for data in datas:
            insert_weibo_data(data)


@db_commit_decorator
def set_weibo_comment_crawled(mid):
    weibo_data = get_wb_by_mid(mid)
    if weibo_data:
        weibo_data.comment_crawled = 1
        db_session.commit()


@db_commit_decorator
def set_weibo_repost_crawled(mid):
    weibo_data = get_wb_by_mid(mid)
    if weibo_data:
        weibo_data.repost_crawled = 1
        db_session.commit()