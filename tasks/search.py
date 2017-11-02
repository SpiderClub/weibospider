from urllib import parse as url_parse

from logger import crawler
from .workers import app
from page_get import get_page
from config import get_max_search_page
from page_parse import search as parse_search
from db.dao import (
    KeywordsOper, KeywordsDataOper, WbDataOper)


# This url is just for original weibos.
# If you want other kind of search, you can change the url below
# But if you change this url, maybe you have to rewrite some part of the parse code
URL = 'http://s.weibo.com/weibo/{}&scope=ori&suball=1&page={}'
LIMIT = get_max_search_page() + 1


@app.task(ignore_result=True)
def search_keyword(keyword, keyword_id):
    crawler.info('We are searching keyword "{}"'.format(keyword))
    cur_page = 1
    encode_keyword = url_parse.quote(keyword)
    while cur_page < LIMIT:
        cur_url = URL.format(encode_keyword, cur_page)
        # current only for login, maybe later crawling page one without login
        search_page = get_page(cur_url, auth_level=2)
        if not search_page:
            crawler.warning('No search result for keyword {}, the source page is {}'.format(keyword, search_page))
            return

        search_list = parse_search.get_search_info(search_page)

        # Because the search results are sorted by time, if any result has been stored in mysql,
        # We need not crawl the same keyword in this turn
        for wb_data in search_list:
            rs = WbDataOper.get_wb_by_mid(wb_data.weibo_id)
            KeywordsDataOper.insert_keyword_wbid(keyword_id, wb_data.weibo_id)
            # todo incremental crawling using time
            if rs:
                crawler.info('Weibo {} has been crawled, skip it.'.format(wb_data.weibo_id))
                continue
            else:
                WbDataOper.add_one(wb_data)
                # todo: only add seed ids and remove this task
                app.send_task('tasks.user.crawl_person_infos', args=(wb_data.uid,), queue='user_crawler',
                              routing_key='for_user_info')
        if cur_page == 1:
            cur_page += 1
        elif 'noresult_tit' not in search_page:
            cur_page += 1
        else:
            crawler.info('Keyword {} has been crawled in this turn'.format(keyword))
            return


@app.task(ignore_result=True)
def execute_search_task():
    keywords = KeywordsOper.get_search_keywords()
    for each in keywords:
        app.send_task('tasks.search.search_keyword', args=(each[0], each[1]), queue='search_crawler',
                      routing_key='for_search_info')