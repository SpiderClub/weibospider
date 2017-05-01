# coding:utf-8
# 搜索页面获取
from headers import headers
from page_get.basic import get_page
from page_parse import search
from db.weibosearch_dao import add_search_cont


# 根据某个关键字搜索,只抓取最热门(第一页)的内容
def search_one(keyword, session):
    url = 'http://s.weibo.com/weibo/' + keyword + '&Refer=STopic_box'
    search_page = get_page(url, session, headers)
    if search_page:
        search_list = search.get_search_info(search_page)
        for s in search_list:
            s.keyword = keyword
            s.mk_primary = '_'.join([str(s.mid), keyword])
        add_search_cont(search_list)
    else:
        print('并未解析到搜索结果:{page}'.format(page=search_page))


def search_all(d):
    cur_session = d['session']
    keywords = ['火影忍者', '川大', '舒淇', 'iphone 7']
    for keyword in keywords:
        search_one(keyword, cur_session)