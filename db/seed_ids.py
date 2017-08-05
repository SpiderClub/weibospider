# coding:utf-8
from sqlalchemy import text
from db.basic_db import db_session
from db.models import SeedIds
from decorators.decorator import db_commit_decorator


def get_seed_ids():
    """
    Get all user id to be crawled
    :return: user ids
    """
    return db_session.query(SeedIds.uid).filter(text('is_crawled=0')).all()


def get_home_ids():
    """
    Get all user id who's home pages need to be crawled
    :return: user ids
    """
    return db_session.query(SeedIds.uid).filter(text('home_crawled=0')).all()


@db_commit_decorator
def set_seed_crawled(uid, result):
    """
    :param uid: user id that is crawled
    :param result: crawling result, 1 stands for succeed, 2 stands for fail
    :return: None
    """
    seed = db_session.query(SeedIds).filter(SeedIds.uid == uid).first()

    if seed and seed.is_crawled == 0:
        seed.is_crawled = result
    else:
        seed = SeedIds(uid=uid, is_crawled=result)
        db_session.add(seed)
    db_session.commit()


def get_seed_by_id(uid):
    return db_session.query(SeedIds).filter(SeedIds.uid == uid).first()


@db_commit_decorator
def insert_seeds(ids):
    db_session.execute(SeedIds.__table__.insert().prefix_with('IGNORE'), [{'uid': i} for i in ids])
    db_session.commit()


@db_commit_decorator
def set_seed_other_crawled(uid):
    """
    update it if user id already exists, else insert
    :param uid: user id
    :return: None
    """
    seed = get_seed_by_id(uid)
    if seed is None:
        seed = SeedIds(uid=uid, is_crawled=1, other_crawled=1, home_crawled=1)
        db_session.add(seed)
    else:
        seed.other_crawled = 1
    db_session.commit()


@db_commit_decorator
def set_seed_home_crawled(uid):
    """
    :param uid: user id
    :return: None
    """
    seed = get_seed_by_id(uid)
    if seed is None:
        seed = SeedIds(uid=uid, is_crawled=0, other_crawled=0, home_crawled=1)
        db_session.add(seed)
    else:
        seed.home_crawled = 1
    db_session.commit()
