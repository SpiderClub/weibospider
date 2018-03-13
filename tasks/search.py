from urllib import parse as url_parse

from celery import group

from logger import crawler
from .workers import app
from page_get import get_page
from config import crawl_args
from page_parse import search as parse_search
from db.dao import (
    KeywordsOper, KeywordsDataOper, WbDataOper)


# This url is just for original weibos.
# If you want other kind of search, you can change the url below
# But if you change this url, maybe you have to rewrite some part of the parse code
URL = 'https://s.weibo.com/weibo/{}&scope=ori&suball=1&page={}'
LIMIT = crawl_args.get('max_search_page')


# todo 找到total page
@app.task(ignore_result=True)
def search_keyword(keyword, keyword_id):
    crawler.info('We are searching keyword "{}"'.format(keyword))
    cur_page = 1
    duplicate = 1
    encode_keyword = url_parse.quote(keyword)
    while cur_page < LIMIT:
        cur_url = URL.format(encode_keyword, cur_page)
        # current only for login, maybe later crawling page one without login
        search_page = get_page(cur_url, auth_level=2)
        if not search_page:
            crawler.warning('No search result for keyword {}, the source page is {}'.
                            format(keyword, search_page))
            return
        # it has reached the last page
        if 'noresult_tit' in search_page and 'noresult_support' in search_page and 'pl_noresult' in search_page:
            crawler.info('Keyword {} has been crawled in this turn, not find result.'.format(keyword))
            return

        search_list = parse_search.get_search_info(search_page)

        # Because the search results are sorted by time, if any result has been stored in keywordsWbdata,
        # We need not crawl the same keyword in this turn
        for wb_data in search_list:
            # judge if the weibo has been insert into keywordsWbdata before
            # if there contains 3 duplicate, this turn is finish.
            for keywordsWbdata in KeywordsDataOper.get_weibo_ids(keyword_id):
                if (wb_data.weibo_id == keywordsWbdata.wb_id):
                    duplicate += 1
                    if (duplicate == 3):
                        crawler.info('Keyword {} has been crawled in this turn, find identity keyword'.format(keyword))
                        return
                    else:
                        continue
            KeywordsDataOper.insert_keyword_wbid(keyword_id, wb_data.weibo_id)
            # if wb_data.uid == '-1', it's has be crawler so we skip it.
            if wb_data.uid == '-1':
                crawler.info('Weibo {} has been crawled, skip it.'.format(wb_data.weibo_id))
                continue
            else:
                WbDataOper.add_one(wb_data)
                # todo: only add seed ids and remove this task
                app.send_task('tasks.user.crawl_person_infos', args=(wb_data.uid,), queue='user_crawler',
                              routing_key='for_user_info')
        cur_page += 1


@app.task(ignore_result=True)
def execute_search_task():
    keywords = KeywordsOper.get_search_keywords()
    caller = group(search_keyword.s(each[0], each[1]) for each in keywords)
    caller.delay()