from urllib import parse as url_parse

from celery import group

from logger import crawler_logger
from page_get import get_page
from config import max_search_page
from page_parse import search as search_parse
from db.models import (
    KeywordsWbdata, SeedIds)
from db.dao import (
    KeywordsOper, KeywordsDataOper,
    WbDataOper, UserOper)
from .workers import app

# This url is just for original weibos.
# If you want other kind of search, you can change the url below
# But if you change this url, maybe you have to rewrite some
# part of the parse code
URL = 'http://s.weibo.com/weibo/{}&scope=ori&suball=1&page={}'


@app.task
def search_keyword(keyword, keyword_id):
    crawler_logger.info('We are searching keyword "{}"'.format(keyword))
    cur_page = 1
    encode_keyword = url_parse.quote(keyword)
    while cur_page < max_search_page:
        cur_url = URL.format(encode_keyword, cur_page)
        # current only for login, maybe later crawling page one
        #  without login
        search_page = get_page(cur_url, auth_level=2)
        if not search_page:
            crawler_logger.warning('No search result for keyword {}, '
                                   'the source page is {}'.
                                   format(keyword, search_page))
            return

        search_list = search_parse.get_search_info(search_page)

        # Because the search results are sorted by time, if
        # any result has been stored in mysql,
        # We need not crawl the same keyword in this turn
        for wb_data in search_list:
            rs = WbDataOper.get_weibo_by_mid(wb_data.weibo_id)
            kd = KeywordsWbdata(wb_id=wb_data.weibo_id, keyword_id=keyword_id)
            KeywordsDataOper.add_one(kd)
            # todo incremental crawling using time
            if rs:
                crawler_logger.info('Weibo {} has been crawled, skip it.'.
                                    format(wb_data.weibo_id))
                continue
            else:
                WbDataOper.add_one(wb_data)
                seed = SeedIds(uid=wb_data.uid)
                UserOper.add_one(seed)
        if cur_page == 1:
            cur_page += 1
        elif 'noresult_tit' not in search_page:
            cur_page += 1
        else:
            crawler_logger.info('Keyword {} has been crawled in this turn'.
                                format(keyword))
            return


@app.task
def execute_search_task():
    keywords = KeywordsOper.get_search_keywords()
    caller = group(search_keyword.s(each[0], each[1]) for each in keywords)
    caller.delay()