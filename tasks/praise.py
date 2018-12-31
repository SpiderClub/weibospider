import time

from .workers import app
from page_parse import praise
from logger import crawler
from config import conf
from page_get import get_page
from db.dao import (WbDataOper, PraiseOper)


# Please note that m.weibo.cn can return more data than PC side
BASE_URL = 'https://weibo.com/aj/v6/like/likelist?ajwvr=6&mid={}&issingle=1&type=0&_t=0&__rnd={}'
PAGE_URL = 'https://weibo.com/aj/v6/like/likelist?ajwvr=6&{}&_t=0&__rnd={}'


@app.task(ignore_result=True)
def crawl_praise_by_page(mid, ext_param):
    cur_time = int(time.time() * 1000)
    cur_url = PAGE_URL.format(ext_param, cur_time)
    html = get_page(cur_url, auth_level=2, is_ajax=True)
    praise_data, ext_param = praise.get_praise_list(html, mid)
    PraiseOper.add_all(praise_data)
    return html, praise_data, ext_param


@app.task(ignore_result=True)
def crawl_praise_page(mid):
    # 这里为了马上拿到返回结果，采用本地调用的方式
    cur_time = int(time.time() * 1000)
    cur_url = BASE_URL.format(mid, cur_time)
    html = get_page(cur_url, auth_level=2, is_ajax=True)
    praise_data, ext_param = praise.get_praise_list(html, mid)
    PraiseOper.add_all(praise_data)
    
    WbDataOper.set_weibo_praise_crawled(mid)

    if not ext_param:
        crawler.error('fail to get praise page 2 ext_param, mid is {mid}'.format(mid=mid))
        return

    # why no app.send_task and fall back to sequential execution
    # because weibo praise now require a parameter called max_id
    # and request without it will return something different from normal browser

    # should work after 5
    # TODO: retry or return depending on ext_param
    for __ in range(2,5):
        # ext_param mainly max_id will be updated each time and be used next time
        html, praise_data, ext_param = crawl_praise_by_page(mid, ext_param)
    return


@app.task(ignore_result=True)
def execute_praise_task():
    weibo_datas = WbDataOper.get_weibo_praise_not_crawled()
    for weibo_data in weibo_datas:
        app.send_task('tasks.praise.crawl_praise_page', args=(weibo_data.weibo_id,), queue='praise_crawler',
                      routing_key='praise_info')
