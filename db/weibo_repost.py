# coding:utf-8
from db.basic_db import db_session
from db.models import WeiboRepost
from decorators.decorator import db_commit_decorator


# TODO 弄清楚"pymysql.err.IntegrityError"捕捉不了的原因
@db_commit_decorator
def save_reposts(repost_list):
    for repost in repost_list:
        r = get_repost_by_rid(repost.weibo_id)
        if not r:
            save_repost(repost)
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
