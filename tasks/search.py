# coding:utf-8
from urllib import parse as url_parse
from logger.log import crawler
from tasks.workers import app
from page_get.basic import get_page
from config.conf import get_max_search_page
from page_parse import search as parse_search
from db.search_words import get_search_keywords
from db.keywords_wbdata import insert_keyword_wbid
from db.wb_data import insert_weibo_data, get_wb_by_mid

# 只抓取原创微博，默认是按照时间进行排序，如果只抓首页，那么就不需要登录
url = 'http://s.weibo.com/weibo/{}&scope=ori&suball=1&page={}'
limit = get_max_search_page() + 1


@app.task(ignore_result=True)
def search_keyword(keyword, keyword_id):
    cur_page = 1
    encode_keyword = url_parse.quote(keyword)
    while cur_page < limit:
        cur_url = url.format(encode_keyword, cur_page)

        search_page = get_page(cur_url)
        if not search_page:
            crawler.warning('本次并没获取到关键词{}的相关微博,该页面源码是{}'.format(keyword, search_page))
            return

        search_list = parse_search.get_search_info(search_page)
        # 先判断数据库里是否存在相关的微博，如果是已有的，那就说明是已经抓取的微博(因为结果默认按时间排序)，就退出循环
        for wb_data in search_list:
            rs = get_wb_by_mid(wb_data.weibo_id)
            if rs:
                crawler.info('关键词{}本次搜索更新的微博已经获取完成'.format(keyword))
                return
            else:
                insert_weibo_data(wb_data)
                insert_keyword_wbid(keyword_id, wb_data.weibo_id)
                # 这里暂时使用网络调用而非本地调用，权衡两种方法的好处
                app.send_task('tasks.user.crawl_person_infos', args=(wb_data.uid,), queue='user_crawler',
                              routing_key='for_user_info')

        # 判断是否包含下一页
        if 'page next S_txt1 S_line1' in search_page:
            cur_page += 1
        else:
            crawler.info('关键词{}搜索完成'.format(keyword))
            return


@app.task(ignore_result=True)
def excute_search_task():
    keywords = get_search_keywords()
    for each in keywords:
        app.send_task('tasks.search.search_keyword', args=(each[0], each[1]), queue='search_crawler',
                      routing_key='for_search_info')