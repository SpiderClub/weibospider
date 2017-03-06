# -*-coding:utf-8 -*-
# 微博搜索页
import re
from bs4 import BeautifulSoup
from entities.weibo_search_data import WeiboSearch
from decorator.decorators import parse_decorator


@parse_decorator(1)
def _search_page_parse(html):
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all('script')
    pattern = re.compile(r'view\((.*)\)')
    for script in scripts:
        m = pattern.search(str(script))
        if m and 'pl_weibo_direct' in script.string and 'S_txt1' in script.string:
            search_cont = m.group(1)
            pattern2 = re.compile(r'"html":"(.*)"}$')
            m2 = pattern2.search(search_cont)
            if m2:
                return m2.group(1).encode('utf-8', 'ignore').decode('unicode-escape', 'ignore').replace('\\', '')
            else:
                print('未匹配到')
    return ''


@parse_decorator(5)
def get_search_info(html):
    content = _search_page_parse(html)
    soup = BeautifulSoup(content.encode('utf-8', 'ignore').decode('utf-8'), "html.parser")
    feed_list = soup.find_all(attrs={'action-type': 'feed_list_item'})
    user_pattern = r'id=(\d+)&u'
    search_list = []
    for each in feed_list:
        wb_search = WeiboSearch()
        try:
            try:
                user_cont = each.find(attrs={'class': 'face'})
                user_info = user_cont.find('a')
                wb_search.username = user_info.get('title')
                wb_search.user_home = user_info.get('href')
                wb_search.uheadimage = user_info.img.get('src')
                m = re.match(user_pattern, user_info.img.get('usercard'))

                if m:
                    wb_search.user_id = m.group(1)
                else:
                    print('未提取到用户id')
                    wb_search.user_id = ''
            except Exception as why:
                print('解析用户信息出错，出错原因:{why}'.format(why=why))

            wb_search.mid = each.find(attrs={'class': 'WB_screen'}).find('a').get('action-data')[4:]
            wb_search.murl = each.find(attrs={'node-type': 'feed_list_item_date'})['href']

            try:
                feed_action = each.find(attrs={'class': 'feed_action'})
                wb_search.create_time = each.find(attrs={'node-type': 'feed_list_item_date'})['title']
                device_info = each.find(attrs={'rel': 'nofollow'})
                wb_search.device = device_info.text if device_info else ''
            except Exception as why:
                print('解析feed_action出错,出错原因:{why}'.format(why=why))

            try:
                wb_search.repost_count = int(feed_action.find(attrs={'action-type': 'feed_list_forward'}).find('em').text)
            except (AttributeError, ValueError):
                wb_search.repost_count = 0
            try:
                wb_search.comment_count = int(feed_action.find(attrs={'action-type': 'feed_list_comment'}).find('em').text)
            except (AttributeError, ValueError):
                wb_search.comment_count = 0
            try:
                wb_search.praise_count = int(feed_action.find(attrs={'action-type': 'feed_list_like'}).find('em').text)
            except (AttributeError, ValueError):
                wb_search.praise_count = 0

            try:
                wb_search.content = each.find(attrs={'class': 'comment_txt'}).text.strip()
            except Exception as why:
                print('解析微博内容出错:{why}'.format(why=why))

        except Exception as why:
            print('整条解析出错,原因为:{why}'.format(why=why))
        else:
            search_list.append(wb_search)
    return search_list




