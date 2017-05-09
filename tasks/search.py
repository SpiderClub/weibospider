# coding:utf-8
from urllib import parse as url_parse
from logger.log import crawler
from page_parse import search
from tasks.workers import app
from config.conf import get_max_search_page
from page_get.basic import get_page
from db.search_words import get_search_keywords
from db.weibosearch_dao import add_search_cont


# 只抓取原创微博，默认是按照时间进行排序
url = 'http://s.weibo.com/weibo/{}&scope=ori&suball=1&page={}'
limit = get_max_search_page() + 1


@app.task
def search_one(keyword):
    cur_page = 1
    # todo 如果到了以前解析的地方，那就说明没有新的微博了，就退出循环
    while cur_page < limit:
        cur_url = url_parse.quote(url.format(keyword, cur_page))

        search_page = get_page(cur_url)

        if search_page:
            search_list = search.get_search_info(search_page)

            if search_list:
                # todo 该函数插入之前，先判断数据库里是否存在相关的微博，如果有，那就说明是已经抓取的微博，就退出循环
                add_search_cont(search_list)

            # 判断是否包含下一页
            if 'page next S_txt1 S_line1' in search_page:
                cur_page += 1
            else:
                crawler.info('关键词{}搜索完成'.format(keyword))
                return
        else:
            crawler.warning('本次并没获取到关键词{}的相关微博,该页面源码是{}'.format(keyword, search_page))
            return


@app.task
def search_all():
    # keyword应该从数据库中读取出来
    keywords = get_search_keywords()
    for each in keywords:
        search_one(each.keyword)