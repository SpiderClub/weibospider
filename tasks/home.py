import time

from logger import crawler
from .workers import app
from page_parse.user import public
from page_get import get_page
from config import (get_max_home_page, get_time_after)
from db.dao import (
    WbDataOper, SeedidsOper)
from page_parse.home import (
    get_data, get_ajax_data, get_total_page)


# only crawls origin weibo
HOME_URL = 'http://weibo.com/u/{}?is_ori=1&is_tag=0&profile_ftype=1&page={}'
AJAX_URL = 'http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain={}&pagebar={}&is_ori=1&id={}{}&page={}' \
           '&pre_page={}&__rnd={}'


def determine(weibo_datum, timeafter):
    weibo_time = time.mktime(
        time.strptime(weibo_datum.create_time, '%Y-%m-%d %H:%M'))
    if weibo_time < timeafter:
        return False
    if WbDataOper.get_wb_by_mid(weibo_datum.weibo_id):
        return False
    return True


@app.task(ignore_result=True)
def crawl_ajax_page(url, auth_level):
    """
    :param url: user home ajax url
    :param auth_level: 1 stands for no login but need fake cookies, 2 stands for login
    :return: resp.text
    """
    ajax_html = get_page(url, auth_level, is_ajax=True)
    ajax_wbdata = get_ajax_data(ajax_html)
    if not ajax_wbdata:
        return ''

    timeafter = time.mktime(
        time.strptime(get_time_after(), '%Y-%m-%d %H:%M:%S'))
    ajax_wbdata = [
        ajax_wbdatum for ajax_wbdatum in ajax_wbdata
        if determine(ajax_wbdatum, timeafter)
    ]

    WbDataOper.add_all(ajax_wbdata)
    return ajax_html


@app.task(ignore_result=True)
def crawl_weibo_datas(uid):
    limit = get_max_home_page()
    cur_page = 1
    while cur_page <= limit:
        url = HOME_URL.format(uid, cur_page)
        if cur_page == 1:
            html = get_page(url, auth_level=1)
        else:
            html = get_page(url, auth_level=2)
        weibo_datas = get_data(html)

        if not weibo_datas:
            crawler.warning("user {} has no weibo".format(uid))
            return

        # Check whether weibo created after time in spider.yaml
        length_weibo_datas = len(weibo_datas)
        timeafter = time.mktime(
            time.strptime(get_time_after(), '%Y-%m-%d %H:%M:%S'))
        weibo_datas = [
            weibo_datum for weibo_datum in weibo_datas
            if determine(weibo_datum, timeafter)
        ]

        WbDataOper.add_all(weibo_datas)

        # If the weibo isn't created after the given time, jump out the loop
        if len(weibo_datas) != length_weibo_datas:
            break

        domain = public.get_userdomain(html)
        cur_time = int(time.time()*1000)
        ajax_url_0 = AJAX_URL.format(domain, 0, domain, uid, cur_page, cur_page, cur_time)
        ajax_url_1 = AJAX_URL.format(domain, 1, domain, uid, cur_page, cur_page, cur_time+100)

        if cur_page == 1:
            # here we use local call to get total page number
            total_page = get_total_page(crawl_ajax_page(ajax_url_1, 2))
            auth_level = 1

            if total_page < limit:
                limit = total_page

            # Since the second ajax of page 1 has already been crawled
            # in the code above and has been stored in databse,
            # we only have to crawl the first ajax of page 1
            crawl_ajax_page(ajax_url_0, auth_level)

        else:
            auth_level = 2

            # Still the same as before
        # if total_page != limit:
        #     limit = total_page
        #     crawler.warning("total pagenum is {}".format(total_page))
        crawl_ajax_page(ajax_url_0, auth_level)
        crawl_ajax_page(ajax_url_1, auth_level)

        cur_page += 1

    SeedidsOper.set_seed_home_crawled(uid)


@app.task(ignore_result=True)
def execute_home_task():
    # you can have many strategies to crawl user's home page, here we choose table seed_ids's uid
    # whose home_crawl is 0
    id_objs = SeedidsOper.get_home_ids()
    for id_obj in id_objs:
        app.send_task('tasks.home.crawl_weibo_datas', args=(id_obj.uid,), queue='home_crawler',
                      routing_key='home_info')
