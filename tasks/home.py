# coding:utf-8
from logger.log import crawler
from tasks.workers import app
from page_parse.user import public
from page_get.basic import get_page
from db.wb_data import insert_weibo_datas
from db.seed_ids import get_home_ids
from config.conf import get_max_home_page
from page_parse.home import get_wbdata_fromweb, get_home_wbdata_byajax, get_total_page


# 只抓取原创微博
home_url = 'http://weibo.com/u/{}?is_ori=1&is_tag=0&profile_ftype=1&page={}'
ajax_url = 'http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain={}&pagebar={}&is_ori=1&id={}{}&page={}&pre_page={}'


@app.task(ignore_result=True)
def crawl_ajax_page(url):
    ajax_html = get_page(url, user_verify=False)
    ajax_wbdatas = get_home_wbdata_byajax(ajax_html)
    if not ajax_wbdatas:
        return

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
            crawler.warning('用户id为{}的用户主页微博数据未采集成功，请检查原因'.format(uid))
            return

        insert_weibo_datas(weibo_datas)

        domain = public.get_userdomain(html)
        ajax_url_0 = ajax_url.format(domain, 0, domain, uid, cur_page, cur_page)
        ajax_url_1 = ajax_url.format(domain, 1, domain, uid, cur_page, cur_page)

        if cur_page == 1:
            total_page = get_total_page(crawl_ajax_page(ajax_url_1))

        if total_page < limit:
            limit = total_page

        cur_page += 1
        app.send_task('tasks.home.crawl_ajax_page', args=(ajax_url_0,), queue='ajax_home_crawler',
                      routing_key='ajax_home_info')

        app.send_task('tasks.home.crawl_ajax_page', args=(ajax_url_1,), queue='ajax_home_crawler',
                      routing_key='ajax_home_info')


@app.task
def excute_home_task():
    # 这里的策略由自己指定，可以基于已有用户做主页抓取，也可以指定一些用户,我这里直接选的种子数据库中的uid
    #id_objs = get_home_ids()
    uids = ['2703907413', '5938331617', '6138171929', '2315766414', '5336708875', '5575751581', '2993049293']
    for uid in uids:
        app.send_task('tasks.home.crawl_weibo_datas', args=(uid,), queue='home_crawler',
                      routing_key='home_info')
