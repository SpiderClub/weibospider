# coding:utf-8
import time

from logger.log import crawler
from tasks.workers import app
from page_parse.user import public
from page_get.basic import get_page
from db.wb_data import insert_weibo_datas
from config.conf import get_max_home_page
from db.seed_ids import (get_home_ids,
                         set_seed_home_crawled
                         )
from page_parse.home import (get_wbdata_fromweb,
                             get_home_wbdata_byajax,
                             get_total_page
                             )


# only crawls origin weibo
home_url = 'http://weibo.com/u/{}?is_ori=1&is_tag=0&profile_ftype=1&page={}'
ajax_url = 'http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain={}&pagebar={}&is_ori=1&id={}{}&page={}' \
           '&pre_page={}&__rnd={}'


@app.task(ignore_result=True)
def crawl_ajax_page(url):
    """
    :param url: user home ajax url
    :return: resp.text
    """
    ajax_html = get_page(url, user_verify=False)
    ajax_wbdatas = get_home_wbdata_byajax(ajax_html)
    if not ajax_wbdatas:
        return ''

    insert_weibo_datas(ajax_wbdatas)
    return ajax_html


@app.task(ignore_result=True)
def crawl_weibo_datas(uid):
    limit = get_max_home_page()
    cur_page = 1
    while cur_page <= limit:
        url = home_url.format(uid, cur_page)
        html = get_page(url)
        weibo_datas = get_wbdata_fromweb(html)

        if not weibo_datas:
            crawler.warning("user {} has no weibo".format(uid))
            return

        insert_weibo_datas(weibo_datas)

        domain = public.get_userdomain(html)
        cur_time = int(time.time()*1000)
        ajax_url_0 = ajax_url.format(domain, 0, domain, uid, cur_page, cur_page, cur_time)
        ajax_url_1 = ajax_url.format(domain, 1, domain, uid, cur_page, cur_page, cur_time+100)

        if cur_page == 1:
            # here we use local call to get total page number
            total_page = get_total_page(crawl_ajax_page(ajax_url_1))

        if total_page < limit:
            limit = total_page

        cur_page += 1
        app.send_task('tasks.home.crawl_ajax_page', args=(ajax_url_0,), queue='ajax_home_crawler',
                      routing_key='ajax_home_info')

        app.send_task('tasks.home.crawl_ajax_page', args=(ajax_url_1,), queue='ajax_home_crawler',
                      routing_key='ajax_home_info')
    set_seed_home_crawled(uid)


@app.task
def excute_home_task():
    # you can have many strategies to crawl user's home page, here we choose table seed_ids's uid
    # whose home_crawl is 0
    id_objs = get_home_ids()
    for id_obj in id_objs:
        app.send_task('tasks.home.crawl_weibo_datas', args=(id_obj.uid,), queue='home_crawler',
                      routing_key='home_info')