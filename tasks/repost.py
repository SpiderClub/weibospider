# -*-coding:utf-8 -*-
from db import wb_data
from db import weibo_repost
from tasks.workers import app
from page_parse import repost
from logger.log import crawler
from db.redis_db import IdNames
from page_get.basic import get_page
from page_get import user as user_get
from config.conf import get_max_repost_page
from page_get.user import get_profile

base_url = 'http://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id={}&page={}'


@app.task(ignore_result=True)
def crawl_repost_by_page(mid, page_num, uid):
    cur_url = base_url.format(mid, page_num)
    html = get_page(cur_url, user_verify=False)
    repost_datas = repost.get_repost_list(html, mid)

    root_user = user_get.get_profile(uid)

    for repost_obj in repost_datas:
        # get_profile(repost_obj.user_id)
        user_id = IdNames.fetch_uid_by_name(repost_obj.parent_user_name)
        if not user_id:
            # 设置成根用户的uid和用户名
            repost_obj.parent_user_id = root_user.uid
            repost_obj.parent_user_name = root_user.name
        else:
            repost_obj.parent_user_id = user_id

    weibo_repost.save_reposts(repost_datas)

    return html, repost_datas


@app.task(ignore_result=True)
def crawl_repost_page(mid, uid):
    if wb_data.check_weibo_repost_crawled(mid):
        return
    wb_data.set_weibo_repost_crawled(mid)

    limit = get_max_repost_page() + 1
    first_repost_data = crawl_repost_by_page(mid, 1, uid)

    total_page = repost.get_total_page(first_repost_data[0])
    repost_datas = first_repost_data[1]

    if not repost_datas:
        return

    if total_page < limit:
        limit = total_page + 1
    for page_num in range(2, limit):
        app.send_task('tasks.repost.crawl_repost_by_page', args=(mid, page_num, uid),
                      queue='repost_page_crawler',
                      routing_key='repost_page_info')
        # 补上user_id，方便可视化


@app.task(ignore_result=True)
def excute_repost_task():
    # 以当前微博为源微博进行分析，不向上溯源，如果有同学需要向上溯源，需要自己判断一下该微博是否是根微博
    weibo_datas = wb_data.get_weibo_repost_not_crawled()
    count = 0
    for weibo_data in weibo_datas:
        weibo_data = weibo_data
        app.send_task('tasks.repost.crawl_repost_page', args=(weibo_data.weibo_id, weibo_data.uid),
                      queue='repost_crawler', routing_key='repost_info')
        count += 1
    crawler.info('本次一共有{}条微博需要抓取转发信息'.format(count))
