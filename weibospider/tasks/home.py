import time

from celery import group

from logger import crawler_logger
from page_parse.user import public
from page_get import get_page
from db.dao import (
    WbDataOper, SeedidsOper)
from page_parse.home import (
    get_data, get_ajax_data, get_total_page)
from config import (
    time_after, max_home_page)
from .workers import app


# only crawls origin weibo
HOME_URL = 'https://weibo.com/u/{}?is_ori=1&is_tag=0&profile_ftype=1&page={}'
AJAX_URL = 'https://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain={}&pagebar={}&is_ori=1&id={}{}&page={}' \
           '&pre_page={}&__rnd={}'


@app.task
def crawl_ajax_page(url, auth_level):
    """
    :param url: user home ajax url
    :param auth_level: 1 stands for no login but need fake cookies,
    2 stands for login
    :return: resp.text
    """
    ajax_html = get_page(url, auth_level, is_ajax=True)
    ajax_wbdatas = get_ajax_data(ajax_html)
    if not ajax_wbdatas:
        return ''

    timeafter = time.mktime(time.strptime(time_after, '%Y-%m-%d %H:%M:%S'))
    for i in range(len(ajax_wbdatas)):
        weibo_time = time.mktime(time.strptime(
            ajax_wbdatas[i].create_time, '%Y-%m-%d %H:%M'))
        if weibo_time < timeafter:
            ajax_wbdatas = ajax_wbdatas[0:i]
            break

    WbDataOper.add_all(ajax_wbdatas)
    return ajax_html


@app.task
def crawl_weibo_datas(uid):
    cur_page = 1
    to_crawl_page = max_home_page
    while cur_page <= to_crawl_page:
        url = HOME_URL.format(uid, cur_page)
        if cur_page == 1:
            html = get_page(url, auth_level=1)
        else:
            html = get_page(url, auth_level=2)
        weibo_datas = get_data(html)

        if not weibo_datas:
            crawler_logger.warning("user {} has no weibo".format(uid))
            return

        # Check whether weibo created after time in spider.yaml
        timeafter = time.mktime(
            time.strptime(time_after, '%Y-%m-%d %H:%M:%S'))
        length = len(weibo_datas)
        flag = True
        for i in range(length):
            weibo_time = time.mktime(
                time.strptime(weibo_datas[i].create_time, '%Y-%m-%d %H:%M'))
            if weibo_time < timeafter:
                weibo_datas = weibo_datas[0:i]
                flag = False
                break

        WbDataOper.add_all(weibo_datas)
        # If the weibo isn't created after the given time, jump out the loop
        if not flag:
            break

        domain = public.get_userdomain(html)
        cur_time = int(time.time()*1000)
        ajax_url_0 = AJAX_URL.format(domain, 0, domain, uid, cur_page,
                                     cur_page, cur_time)
        ajax_url_1 = AJAX_URL.format(domain, 1, domain, uid, cur_page,
                                     cur_page, cur_time+100)

        if cur_page == 1:
            # here we use local call to get total page number
            total_page = get_total_page(crawl_ajax_page(ajax_url_1, 2))
            to_crawl_page = total_page if total_page < max_home_page else \
                max_home_page
            auth_level = 1
        else:
            auth_level = 2

        caller = group(crawl_ajax_page.s(cur_url, auth_level) for cur_url
                       in [ajax_url_0, ajax_url_1])
        caller.delay()
        cur_page += 1

    SeedidsOper.set_home_crawled(uid)


@app.task
def execute_home_task():
    # you can have many strategies to crawl user's home page, here we choose table seed_ids's uid
    # whose home_crawl is 0
    id_objs = SeedidsOper.get_home_ids()
    caller = group(crawl_weibo_datas.s(obj.uid) for obj in id_objs)
    caller.delay()