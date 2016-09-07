# coding:utf-8
# 搜索页面获取
from gl import headers
from do_dataget.basic import get_page
from do_dataprocess.do_searchprocess import search_parse


# 根据某个关键字搜索,只抓取第一页的内容
def search_one(keyword, session):
    url = 'http://s.weibo.com/weibo/' + keyword + '&Refer=STopic_box'
    search_page = get_page(url, session, headers)
    if search_page:
        search_list = search_parse.get_search_info(search_page)
        print(len(search_list))
        print(search_list)
        for s in search_list:
            print(s)


def search_all(d):
    cur_session = d['session']
    keywords = ['火影忍者', '川大', '舒淇']
    for keyword in keywords:
        search_one(keyword, cur_session)