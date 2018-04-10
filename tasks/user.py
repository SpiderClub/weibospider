from celery import group
from celery.exceptions import SoftTimeLimitExceeded

from db.dao import SeedidsOper
from logger import crawler_logger
from page_get import (
    get_fans_or_followers_ids,
    get_profile
)
from .workers import app


@app.task
def crawl_followers_fans(uid):
    seed = SeedidsOper.get_seed_by_id(uid)
    if seed.other_crawled == 0:
        rs = get_fans_or_followers_ids(uid, 1)
        rs.extend(get_fans_or_followers_ids(uid, 2))
        datas = set(rs)
        # If data already exits, just skip it
        if datas:
            SeedidsOper.insert_seeds(datas)
        SeedidsOper.set_relation_crawled(uid)


@app.task
def execute_relation_task():
    seeds = SeedidsOper.get_relation_ids()
    caller = group(crawl_followers_fans.s(seed.uid) for seed in seeds)
    caller.delay()


@app.task
def crawl_user_info(uid):
    """
    Crawl user info and their fans and followers
    For the limit of weibo's backend, we can only crawl 5 pages of
    the fans and followers.
    We also have no permissions to view enterprise's followers and
    fans info
    :param uid: current user id
    :return: None
    """
    if not uid:
        return

    try:
        user, is_crawled = get_profile(uid)
        # If it's enterprise user, just skip it
        if user and user.verify_type == 2:
            SeedidsOper.set_relation_crawled(uid)
            return
    except SoftTimeLimitExceeded:
        crawler_logger.error("Timeout for celery to crawl uid={}".format(uid))


@app.task
def execute_user_task():
    seeds = SeedidsOper.get_seed_ids()
    caller = group(crawl_user_info.s(seed.uid) for seed in seeds)
    caller.delay()


