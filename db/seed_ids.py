# coding:utf-8
from sqlalchemy import text
from db.basic_db import db_session
from db.models import SeedIds
from decorators.decorator import db_commit_decorator


def get_seed_ids():
    """
    获取所有个人信息需要被抓取的用户id
    :return: 
    """
    return db_session.query(SeedIds.uid).filter(text('is_crawled=0')).all()


def get_home_ids():
    """
    获取所有主页需要被抓取的用户id
    :return: 
    """
    return db_session.query(SeedIds.uid).filter(text('home_crawled=0')).all()


@db_commit_decorator
def set_seed_crawled(uid, result):
    """
    该表适用于用户抓取相关逻辑
    :param uid: 被抓取用户id
    :param result: 抓取结果
    :return: None
    """
    seed = db_session.query(SeedIds).filter(SeedIds.uid == uid).first()
    if seed:
        if seed.is_crawled == 0:
            seed.is_crawled = result
    else:
        seed = SeedIds(uid=uid, is_crawled=result)
        db_session.add(seed)
    db_session.commit()


def get_seed_by_id(uid):
    return db_session.query(SeedIds).filter(SeedIds.uid == uid).first()


@db_commit_decorator
def insert_seeds(ids):
    # 批量插入，遇到重复则跳过
    db_session.execute(SeedIds.__table__.insert().prefix_with('IGNORE'), [{'uid': i} for i in ids])
    db_session.commit()


@db_commit_decorator
def set_seed_other_crawled(uid):
    """
    存在则更新，不存在则插入
    :param uid: 用户id
    :return: None
    """
    seed = get_seed_by_id(uid)
    if seed is None:
        seed = SeedIds(uid=uid, is_crawled=1, other_crawled=1)
        db_session.add(seed)
    else:
        seed.other_crawled = 1
    db_session.commit()


@db_commit_decorator
def set_seed_home_crawled(uid):
    """
    将该用户的home_crawled字段设置为已经抓取,它和set_seed_other_crawled(uid)不同，因为后者的uid是通过用户关注
    或者粉丝列表获取的,它们的信息有可能是没有的，所以需要判断是否存在，而这里是基于已经存在的信息
    :param uid: 用户id
    :return: None
    """
    seed = get_seed_by_id(uid)
    seed.home_crawled = 1
    db_session.commit()
