from .workers import app
from page_parse import comment
from config import conf
from page_get import get_page
from db.dao import (
    WbDataOper, CommentOper)


BASE_URL = 'http://weibo.com/aj/v6/comment/big?ajwvr=6&id={}&page={}'


@app.task(ignore_result=True)
def crawl_comment_by_page(mid, page_num):
    cur_url = BASE_URL.format(mid, page_num)
    html = get_page(cur_url, auth_level=1, is_ajax=True)
    comment_datas = comment.get_comment_list(html, mid)
    CommentOper.add_all(comment_datas)
    if page_num == 1:
        WbDataOper.set_weibo_comment_crawled(mid)
    return html, comment_datas


@app.task(ignore_result=True)
def crawl_comment_page(mid):
    limit = conf.get_max_comment_page() + 1
    # 这里为了马上拿到返回结果，采用本地调用的方式
    first_page = crawl_comment_by_page(mid, 1)[0]
    total_page = comment.get_total_page(first_page)

    if total_page < limit:
        limit = total_page + 1

    for page_num in range(2, limit):
        app.send_task('tasks.comment.crawl_comment_by_page', args=(mid, page_num), queue='comment_page_crawler',
                      routing_key='comment_page_info')


@app.task(ignore_result=True)
def execute_comment_task():
    # 只解析了根评论，而未对根评论下的评论进行抓取，如果有需要的同学，可以适当做修改
    weibo_datas = WbDataOper.get_weibo_comment_not_crawled()
    for weibo_data in weibo_datas:
        app.send_task('tasks.comment.crawl_comment_page', args=(weibo_data.weibo_id,), queue='comment_crawler',
                      routing_key='comment_info')
