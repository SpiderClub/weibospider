# 搜索页面获取

import json, logging, os
from gl import headers, count, page_max
from do_dataget.basic import get_page
from do_dataprocess import basic
from db_operation import spread_original_dao
from do_dataprocess.do_statusprocess import status_parse
from weibo_entities.spread_other_cache import SpreadOtherCache
from do_dataget import get_statusinfo
from do_dataget import get_userinfo
from db_operation import spread_other_dao, weibosearch_dao


# 根据某个关键字搜索
def search_one(keyword):
    url = 'http://s.weibo.com/weibo/' + keyword + '&Refer=STopic_box'