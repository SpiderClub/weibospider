# coding:utf-8
from sqlalchemy import text
from db.basic_db import db_session
from db.models import WeiboData
from pymysql.err import IntegrityError
from decorators.decorator import db_commit_decorator


@db_commit_decorator
def insert_weibo_data(weibo_data):
    # 存入数据的时候从更高一层判断是否会重复，不在该层做判断
    db_session.add(weibo_data)
    db_session.commit()


def get_wb_by_mid(mid):
    """
    :param mid: 微博id
    :return: 
    """
    return db_session.query(WeiboData).filter(WeiboData.weibo_id == mid).first()


@db_commit_decorator
def insert_weibo_datas(weibo_datas):
    # 批量插入，如果重复那么就单个插入
    try:
        db_session.add_all(weibo_datas)
    except IntegrityError:
        for data in weibo_datas:
            r = get_wb_by_mid(data.weibo_id)
            if r:
                continue
            insert_weibo_data(data)
    finally:
        db_session.commit()


@db_commit_decorator
def set_weibo_comment_crawled(mid):
    """
    如果存在该微博，那么就将comment_crawled字段设置为1
    :param mid: 
    :return: 
    """
    weibo_data = get_wb_by_mid(mid)
    if weibo_data:
        weibo_data.comment_crawled = 1
        db_session.commit()


@db_commit_decorator
def get_weibo_comment_not_crawled():
    return db_session.query(WeiboData.weibo_id).filter(text('comment_crawled=0')).all()
