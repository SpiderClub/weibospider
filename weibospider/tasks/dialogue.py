import time

from celery import group

from ..page_parse import (
    comment, dialogue)
from ..config import max_dialogue_page
from ..page_get import get_page
from ..db.dao import (
    WbDataOper, Dialogue,
    SeedidsOper)
from .workers import app


AJAX_URL = 'https://weibo.com/aj/v6/comment/conversation?ajwvr=6' \
           '&cid={}&type=small&ouid=&cuid=&is_more=1&__rnd={}'
COMMENT_URL = 'http://weibo.com/aj/v6/comment/big?ajwvr=6&id={}&page={}'


def crawl_dialogue_by_comment_id(cid, mid):
    cur_time = int(time.time() * 1000)
    dialogue_url = AJAX_URL.format(cid, cur_time)
    html = get_page(dialogue_url, auth_level=2, is_ajax=True)
    dialogue_data, uids = dialogue.get_dialogue(html, mid, cid)
    if dialogue_data:
        Dialogue.add_one(dialogue_data)

    SeedidsOper.insert_seeds(uids)


@app.task
def crawl_dialogue_by_comment_page(mid, page_num):
    comment_url = COMMENT_URL.format(mid, page_num)
    # html = get_page(comment_url, auth_level=1, is_ajax=True)
    html = get_page(comment_url, auth_level=2, is_ajax=True)
    comment_ids = dialogue.get_comment_id(html)
    for cid in comment_ids:
        crawl_dialogue_by_comment_id(cid, mid)

    if page_num == 1:
        WbDataOper.set_dialogue_crawled(mid)
    return html


@app.task
def crawl_dialogue(mid):
    first_page = crawl_dialogue_by_comment_page(mid, 1)
    total_page = comment.get_total_page(first_page)

    if max_dialogue_page == float('+inf') or total_page < max_dialogue_page:
        limit = total_page + 1
    else:
        limit = max_dialogue_page + 1

    caller = group(crawl_dialogue_by_comment_page.s(mid, page) for page
                   in range(2, limit))
    caller.delay()


@app.task
def execute_dialogue_task():
    datas = WbDataOper.get_dialogue_not_crawled()
    caller = group(crawl_dialogue.s(data.weibo_id) for data in datas)
    caller.delay()
