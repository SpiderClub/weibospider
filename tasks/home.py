import time

from celery import group

from logger import crawler
from .workers import app
from page_parse.user import public
from page_get import get_page
from config import crawl_args
from db.dao import (
    WbDataOper, SeedidsOper)
from page_parse.home import (
    get_data, get_ajax_data, get_total_page)


# only crawls origin weibo
HOME_URL = 'https://weibo.com/u/{}?is_ori=1&is_tag=0&profile_ftype=1&page={}'
AJAX_URL = 'https://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain={}&pagebar={}&is_ori=1&id={}{}&page={}' \
           '&pre_page={}&__rnd={}'
LIMIT = crawl_args.get('max_home_page')


@app.task(ignore_result=True)
def crawl_ajax_page(url, auth_level):
    """
    :param url: user home ajax url
    :param auth_level: 1 stands for no login but need fake cookies, 2 stands for login
    :return: resp.text
    """
    ajax_html = get_page(url, auth_level, is_ajax=True)
    ajax_wbdatas = get_ajax_data(ajax_html)
    if not ajax_wbdatas:
        return ''

    WbDataOper.add_all(ajax_wbdatas)
    return ajax_html


@app.task(ignore_result=True)
def crawl_weibo_datas(uid):
    cur_page = 1
    to_crawl_page = LIMIT
    while cur_page <= to_crawl_page:
        url = HOME_URL.format(uid, cur_page)
        if cur_page == 1:
            html = get_page(url, auth_level=1)
        else:
            html = get_page(url, auth_level=2)
        weibo_datas = get_data(html)

        if not weibo_datas:
            crawler.warning("user {} has no weibo".format(uid))
            return

        WbDataOper.add_all(weibo_datas)

        domain = public.get_userdomain(html)
        cur_time = int(time.time()*1000)
        ajax_url_0 = AJAX_URL.format(domain, 0, domain, uid, cur_page, cur_page, cur_time)
        ajax_url_1 = AJAX_URL.format(domain, 1, domain, uid, cur_page, cur_page, cur_time+100)

        if cur_page == 1:
            # here we use local call to get total page number
            total_page = get_total_page(crawl_ajax_page(ajax_url_1, 2))
            to_crawl_page = total_page if total_page < LIMIT else LIMIT
            auth_level = 1
        else:
            auth_level = 2

        # crawl all the pages if you want
        #if total_page != limit:
            #limit = total_page
            #crawler.warning("total pagenum is {}".format(total_page))
        crawl_ajax_page(ajax_url_0, auth_level)
	crawl_ajax_page(ajax_url_1, auth_level)
        cur_page += 1

    SeedidsOper.set_seed_home_crawled(uid)


@app.task(ignore_result=True)
def execute_home_task():
    # you can have many strategies to crawl user's home page, here we choose table seed_ids's uid
    # whose home_crawl is 0
    id_objs = SeedidsOper.get_home_ids()
    caller = group(crawl_weibo_datas.s(obj.uid for obj in id_objs))
    caller.delay()
