from .workers import app
from page_parse import comment, dialogue
from config import conf
from page_get import get_page
from db.dao import (WbDataOper, CommonOper)
import time

AJAX_URL = 'https://weibo.com/aj/v6/comment/conversation?ajwvr=6&cid={}&type=small&ouid=&cuid=&is_more=1&__rnd={}'
COMMENT_URL = 'http://weibo.com/aj/v6/comment/big?ajwvr=6&id={}&page={}'


@app.task(ignore_result=True)
def crawl_dialogue_by_comment_id(cid, mid):
    cur_time = int(time.time() * 1000)

    dialogue_url = AJAX_URL.format(cid, cur_time)

    html = get_page(dialogue_url, auth_level=2, is_ajax=True)
    dialogue_data, uids = dialogue.get_dialogue(html, mid, cid)
    if dialogue_data:
        CommonOper.add_one(dialogue_data)

    if uids:
        for uid in uids:
            # crawl_person_infos_not_in_seed_ids(uid)
            app.send_task('tasks.user.crawl_person_infos_not_in_seed_ids',
                          args=(uid,),
                          queue='user_crawler',
                          routing_key='for_user_info')


@app.task(ignore_result=True)
def crawl_dialogue_by_comment_page(mid, page_num):
    comment_url = COMMENT_URL.format(mid, page_num)
    html = get_page(comment_url, auth_level=1, is_ajax=True)
    comment_ids = dialogue.get_comment_id(html, mid)
    for cid in comment_ids:
        crawl_dialogue_by_comment_id(cid, mid)

    if page_num == 1:
        WbDataOper.set_weibo_dialogue_crawled(mid)
    return html


@app.task(ignore_result=True)
def crawl_dialogue(mid):
    limit = conf.get_max_dialogue_page() + 1

    first_page = crawl_dialogue_by_comment_page(mid, 1)
    total_page = comment.get_total_page(first_page)

    if total_page < limit:
        limit = total_page + 1

    for page_num in range(2, limit):
        # crawl_dialogue_by_comment_page(mid, page_num)
        app.send_task('tasks.comment.crawl_dialogue_by_comment_page',
                      args=(mid, page_num),
                      queue='comment_page_crawler',
                      routing_key='comment_page_info')


@app.task(ignore_result=True)
def execute_dialogue_task():
    weibo_datas = WbDataOper.get_weibo_dialogue_not_crawled()
    for weibo_data in weibo_datas:
        # crawl_dialogue(weibo_data.weibo_id)
        app.send_task('tasks.dialogue.crawl_dialogue',
                      args=(weibo_data.weibo_id,),
                      queue='dialogue_crawler',
                      routing_key='dialogue_info')
