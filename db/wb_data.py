# coding:utf-8
from sqlalchemy import text
from db.basic_db import db_session
from db.models import WeiboData
from decorators.decorator import db_commit_decorator


@db_commit_decorator
def insert_weibo_data(weibo_data):
    db_session.add(weibo_data)
    db_session.commit()


def get_wb_by_mid(mid):
    return db_session.query(WeiboData).filter(WeiboData.weibo_id == mid).first()


@db_commit_decorator
def insert_weibo_datas(weibo_datas):
    for data in weibo_datas:
        r = get_wb_by_mid(data.weibo_id)
        if not r:
            db_session.add(data)
    db_session.commit()


@db_commit_decorator
def set_weibo_comment_crawled(mid):
    weibo_data = get_wb_by_mid(mid)
    if weibo_data:
        weibo_data.comment_crawled = 1
        db_session.commit()


def get_weibo_comment_not_crawled():
    return db_session.query(WeiboData.weibo_id).filter(text('comment_crawled=0')).all()


def get_weibo_repost_not_crawled():
    return db_session.query(WeiboData.weibo_id, WeiboData.uid).filter(text('repost_crawled=0')).all()


@db_commit_decorator
def set_weibo_repost_crawled(mid):
    weibo_data = get_wb_by_mid(mid)
    if weibo_data:
        weibo_data.repost_crawled = 1
        db_session.commit()