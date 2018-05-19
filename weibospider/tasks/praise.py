import time

from celery import group
from celery.exceptions import SoftTimeLimitExceeded

from page_parse import praise
from page_get import get_page
from logger import crawler_logger

from .workers import app

from db.dao import (WbDataOper, PraiseOper)


BASE_URL = 'http://weibo.com/aj/v6/like/big?ajwvr=6&mid={}&' \
           'page={}&__rnd={}'


@app.task
def crawl_praise_by_page(mid, page_num):
    cur_time = int(time.time() * 1000)
    cur_url = BASE_URL.format(mid, page_num, cur_time)
    try:
        html = get_page(cur_url, auth_level=2, is_ajax=True)
        datas = praise.get_praise_list(html, mid)
    except SoftTimeLimitExceeded:
        crawler_logger.error(
            "Timeout for celery to crawl praise {}".format(cur_url))
    else:
        PraiseOper.add_all(datas)
        if page_num == 1:
            WbDataOper.set_praise_crawled(mid)
        return html, datas


@app.task
def crawl_praise_page(mid):
    first_page = crawl_praise_by_page(mid, 1)[0]
    total_page = praise.get_total_page(first_page)
    caller = group(crawl_praise_by_page.s(mid, page) for page
                   in range(2, total_page+1))
    caller.delay()


@app.task
def execute_praise_task():
    datas = WbDataOper.get_praise_not_crawled()
    caller = group(crawl_praise_page.s(data.weibo_id) for data in datas)
    caller.delay()

