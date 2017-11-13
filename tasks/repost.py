from celery import group

from .workers import app
from page_parse import repost
from logger import crawler
from db.redis_db import IdNames
from config import crawl_args
from db.dao import (
    WbDataOper, RepostOper)
from page_get import (
    get_page, get_profile)


BASE_URL = 'http://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id={}&&page={}'
LIMIT = crawl_args.get('max_repost_page')


@app.task
def crawl_repost_by_page(mid, page_num):
    total_page = 1
    cur_url = BASE_URL.format(mid, page_num)
    html = get_page(cur_url, auth_level=1, is_ajax=True)
    repost_datas = repost.stroe_and_get_reposts(html, mid)
    if page_num == 1:
        total_page = repost.get_total_page(html)
        WbDataOper.set_weibo_repost_crawled(mid)
    return total_page, repost_datas


@app.task
def crawl_repost_page(mid, uid):
    total_page, repost_datas = crawl_repost_by_page(mid, 1)

    if not repost_datas:
        return

    root_user, _ = get_profile(uid)

    to_crawl_page = total_page if total_page < LIMIT else LIMIT

    for page_num in range(2, to_crawl_page+1):
        _, cur_repost_datas = crawl_repost_by_page(mid, page_num)
        if cur_repost_datas:
            repost_datas.extend(cur_repost_datas)

    for index, repost_obj in enumerate(repost_datas):
        user_id = IdNames.fetch_uid_by_name(repost_obj.parent_user_name)
        if not user_id:
            # when it comes to errors, set the args to default(root)
            repost_obj.parent_user_id = root_user.uid
            repost_obj.parent_user_name = root_user.name
        else:
            repost_obj.parent_user_id = user_id
        repost_datas[index] = repost_obj

    RepostOper.add_all(repost_datas)


@app.task
def execute_repost_task():
    # regard current weibo url as the original url, you can also analyse from the root url
    weibo_datas = WbDataOper.get_weibo_repost_not_crawled()
    crawler.info('There are {} repost urls have to be crawled'.format(len(weibo_datas)))
    caller = group(crawl_repost_page.s(data.weibo_id, data.uid) for data in weibo_datas)
    caller.delay()
