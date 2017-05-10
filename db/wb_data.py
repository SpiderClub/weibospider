# coding:utf-8
from db.basic_db import db_session
from db.models import WeiboData
from decorator.decorators import db_commit_decorator


@db_commit_decorator
def insert_weibo_datas(weibo_datas):
    # 批量插入，遇到重复则跳过
    db_session.execute(WeiboData.__table__.insert().prefix_with('IGNORE'), [data for data in weibo_datas])
    db_session.commit()


@db_commit_decorator
def insert_weibo_data(weibo_data):
    db_session.add(weibo_data)
    db_session.commit()


def get_wb_by_mid(mid):
    """
    :param mid: 微博id
    :return: 
    """
    return db_session.query(WeiboData).filter(WeiboData.weibo_id == mid).first()