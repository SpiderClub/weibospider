from celery import group
from celery.exceptions import SoftTimeLimitExceeded

from ..logger import crawler_logger
from ..page_parse import comment
from ..config import max_comment_page
from ..page_get import get_page
from ..db.dao import (
    WbDataOper, CommentOper)
from .workers import app


BASE_URL = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id={}&&page={}'


# TODO simplify similar codes in repost.py,comment.py,praise.py...
@app.task
def crawl_comment_by_page(mid, page_num):
    cur_url = BASE_URL.format(mid, page_num)
    try:
        cur_url = BASE_URL.format(mid, page_num)
        # TODO consider crawling with haipproxy or not
        # html = get_page(cur_url, auth_level=1, is_ajax=True)
        html = get_page(cur_url, auth_level=2, is_ajax=True)
        datas = comment.get_comment_list(html, mid)
    except SoftTimeLimitExceeded:
        crawler_logger.error(
            "Timeout for celery to crawl praise {}".format(cur_url))
    else:
        CommentOper.add_all(datas)
        if page_num == 1:
            WbDataOper.set_comment_crawled(mid)
        return html, datas


@app.task
def crawl_comment_page(mid):
    # call crawl_comment_by_page locally to get total page right now
    first_page = crawl_comment_by_page(mid, 1)[0]
    total_page = comment.get_total_page(first_page)

    if max_comment_page == float('+inf') or max_comment_page > total_page:
        limit = total_page + 1
    else:
        limit = max_comment_page + 1

    caller = group(crawl_comment_by_page.s(mid, page) for page
                   in range(2, limit))
    caller.delay()


@app.task
def execute_comment_task():
    """Notice that this task only crawl root comments"""
    datas = WbDataOper.get_comment_not_crawled()
    caller = group(crawl_comment_page.s(data.weibo_id) for data in datas)
    caller.delay()
