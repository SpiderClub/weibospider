# coding:utf-8
from db.basic_db import db_session
from db.models import WeiboRepost
from pymysql.err import IntegrityError
from decorators.decorator import db_commit_decorator


@db_commit_decorator
def save_reposts(repost_list):
    print('正在存储数据')
    try:
        db_session.add_all(repost_list)
    except IntegrityError:
        for data in repost_list:
            r = get_repost_by_rid(data.weibo_id)
            if r:
                continue
            save_repost(data)
    finally:
        db_session.commit()


@db_commit_decorator
def save_repost(repost):
    db_session.add(repost)
    db_session.commit()


def get_repost_by_rid(rid):
    """
    根据转发微博id获取该转发微博信息
    :param rid: 转发微博id
    :return: 
    """
    return db_session.query(WeiboRepost).filter(WeiboRepost.weibo_id == rid).first()
