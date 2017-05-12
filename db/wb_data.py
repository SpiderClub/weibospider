# coding:utf-8
from db.basic_db import db_session
from db.models import WeiboData
from decorators.decorator import db_commit_decorator


@db_commit_decorator
def insert_weibo_datas(weibo_datas):
    # 批量插入，遇到重复则跳过
    dict_weibo_datas = [weibo_data.__dict__ for weibo_data in weibo_datas]
    db_session.execute(WeiboData.__table__.insert().prefix_with('IGNORE'), dict_weibo_datas)
    db_session.commit()


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