# coding:utf-8
import time
from db import wb_data
from logger.log import crawler
from tasks.workers import app
from page_parse import comment
from page_get.basic import get_page
from db.weibo_comment import save_comments
from config.conf import get_max_comment_page

base_url = 'http://weibo.com/aj/v6/comment/big?ajwvr=6&{}&from=singleWeiBo&__rnd={}'
# 起始请求地址
start_url = 'http://weibo.com/aj/v6/comment/big?ajwvr=6&id={}&from=singleWeiBo&__rnd={}'


@app.task(ignore_result=True)
def crawl_comment_page(mid):
    limit = get_max_comment_page()
    cur_page = 1
    next_url = ''
    while cur_page <= limit:
        cur_time = int(time.time()*1000)
        if cur_page == 1:
            url = start_url.format(mid, cur_time)
        else:
            url = base_url.format(next_url, cur_time)
        html = get_page(url, user_verify=False)
        comment_datas = comment.get_comment_list(html, mid)

        if not comment_datas and cur_page == 1:
            crawler.warning('微博id为{}的微博评论未采集成功，请检查原因'.format(mid))
            return

        save_comments(comment_datas)
        # 由于这里每一步都要根据上一步来迭代，所以不适合采用网络调用（主要是比较麻烦）
        next_url = comment.get_next_url(html)

        if not next_url:
            crawler.info('微博{}的评论采集已经完成'.format(mid))
            return
        cur_page += 1


@app.task
def excute_comment_task():
    #weibo_datas = wb_data.get_weibo_comment_not_crawled()
    weibo_data = '4079144788308403'
    # for weibo_data in weibo_datas:
    #     app.send_task('tasks.comment.crawl_comment_page', args=(weibo_data.weibo_id,), queue='comment_crawler',
    #                   routing_key='comment_info')
    app.send_task('tasks.comment.crawl_comment_page', args=(weibo_data,), queue='comment_crawler',
                  routing_key='comment_info')