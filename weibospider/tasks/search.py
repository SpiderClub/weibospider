from urllib import parse as url_parse

from celery import group

from ..logger import crawler_logger
from ..page_get import get_page
from ..config import max_search_page
from ..page_parse import search as search_parse
from ..db.models import (
    KeywordWbdata, SeedId)
from ..db.dao import (
    KeywordsOper, KeywordsDataOper,
    WbDataOper, UserOper)
from .workers import app

# This url is just for original weibos.
# If you want other kind of search, you can change the url below

# But if you change this url, maybe you have to rewrite some
# part of the parse code
URL = 'https://s.weibo.com/weibo/{}&scope=ori&suball=1&page={}'


@app.task
def search_keyword(keyword, keyword_id):
    crawler_logger.info('We are searching keyword "{}"'.format(keyword))
    cur_page = 1
    encode_keyword = url_parse.quote(keyword)
    while cur_page < max_search_page:
        cur_url = URL.format(encode_keyword, cur_page)
        # current only for login, maybe later crawling page one without login
        search_page = get_page(cur_url, auth_level=2)
        if not search_page:
            crawler_logger.warning('No search result for keyword {}, '
                                   'the source page is {}'.
                                   format(keyword, search_page))
            return
        # it has reached the last page
        if 'noresult_tit' in search_page and 'noresult_support' in search_page \
                and 'pl_noresult' in search_page:
            crawler_logger.info('Keyword {} has been crawled in this turn, '
                                'not find result.'.format(keyword))
            return

        search_list = search_parse.get_search_info(search_page)

        # The search results are sorted by time,
        # if any result has been stored in KeywordsWbdata,
        # We need not crawl the same keyword in this turn
        for wb_data in search_list:
            # judge if the weibo has been insert into keywordsWbdata before
            # if there contains 3 duplicate, this turn is finish.
            datas = KeywordsDataOper.get_weibo_ids(keyword_id, wb_data.weibo_id)
            if datas:
                crawler_logger.info('Keyword {} has been crawled in this turn'.
                                    format(keyword))
                return

            KeywordsDataOper.add_one(
                KeywordWbdata(keyword_id=keyword_id, wb_id=wb_data.weibo_id))
            # if wb_data.uid == '-1', it's has be crawler so we skip it.
            if wb_data.uid == '-1':
                crawler_logger.info('Weibo {} has been crawled, skip it.'.
                                    format(wb_data.weibo_id))
            else:
                seed = SeedId(uid=wb_data.uid)
                UserOper.add_one(seed)
                WbDataOper.add_one(wb_data)

        cur_page += 1


@app.task
def execute_search_task():
    keywords = KeywordsOper.get_search_keywords()
    caller = group(search_keyword.s(each[0], each[1]) for each in keywords)
    caller.delay()
