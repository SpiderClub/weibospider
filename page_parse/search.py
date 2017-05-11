# -*-coding:utf-8 -*-
import re
from bs4 import BeautifulSoup
from logger.log import parser
from db.models import WeiboData
from decorator.decorators import parse_decorator


user_pattern = r'id=(\d+)&u'


@parse_decorator(1)
def _search_page_parse(html):
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all('script')
    pattern = re.compile(r'view\((.*)\)')
    for script in scripts:
        m = pattern.search(str(script))
        # 这个判断不全面，对于json编码的可以成功，对于直接返回的不会成功
        if m and 'pl_weibo_direct' in script.string and 'S_txt1' in script.string:
            search_cont = m.group(1)
            pattern2 = re.compile(r'"html":"(.*)"}$')
            m2 = pattern2.search(search_cont)
            if m2:
                return m2.group(1).encode('utf-8', 'ignore').decode('unicode-escape', 'ignore').replace('\\', '')
    print('未匹配到相关内容')
    return ''


@parse_decorator(5)
def get_weibo_info(each, html):
    wb_data = WeiboData()
    try:
        try:
            user_cont = each.find(attrs={'class': 'face'})
            user_info = user_cont.find('a')
            m = re.match(user_pattern, user_info.img.get('usercard'))

            if m:
                wb_data.uid = m.group(1)
            else:
                parser.warning('未提取到用户id,页面源码是{}'.format(html))
                return None

        except Exception as why:
            parser.error('解析用户信息出错，出错原因:{},页面源码是{}'.format(why, html))
            return None

        wb_data.weibo_id = each.find(attrs={'class': 'WB_screen'}).find('a').get('action-data')[4:]
        try:
            wb_data.weibo_url = each.find(attrs={'node-type': 'feed_list_item_date'})['href']
        except Exception as e:
            parser.error('解析微博url出错，出错原因是{},页面源码是{}'.format(e, html))

        try:
            feed_action = each.find(attrs={'class': 'feed_action'})
            wb_data.create_time = each.find(attrs={'node-type': 'feed_list_item_date'})['title']

        except Exception as why:
            parser.error('解析feed_action出错,出错原因:{},页面源码是{}'.format(why, html))
            wb_data.device = ''

        else:
            try:
                wb_data.repost_num = int(feed_action.find(attrs={'action-type': 'feed_list_forward'}).find('em').text)
            except (AttributeError, ValueError):
                wb_data.repost_num = 0
            try:
                wb_data.comment_num = int(feed_action.find(attrs={'action-type': 'feed_list_comment'}).find('em').text)
            except (AttributeError, ValueError):
                wb_data.comment_num = 0
            try:
                wb_data.praise_num = int(feed_action.find(attrs={'action-type': 'feed_list_like'}).find('em').text)
            except (AttributeError, ValueError):
                wb_data.praise_num = 0

        try:
            wb_data.weibo_cont = each.find(attrs={'class': 'comment_txt'}).text.strip()
        except Exception as why:
            parser.error('解析微博内容出错:{}, 页面源码是{}'.format(why, html))
            return None

    except Exception as why:
        parser.error('整条解析出错,原因为:{}, 页面源码是{}'.format(why, html))
        return None
    else:
        return wb_data


@parse_decorator(5)
def get_search_info(html):
    """
    通过搜索页的内容获取搜索结果
    :param html: 
    :return: 
    """
    # 搜索结果可能有两种方式，一种是直接返回的，一种是编码过后的
    content = _search_page_parse(html) if '举报' not in html else html

    if content == '':
        return list()

    soup = BeautifulSoup(content.encode('utf-8', 'ignore').decode('utf-8'), "html.parser")
    feed_list = soup.find_all(attrs={'action-type': 'feed_list_item'})
    search_list = []
    for each in feed_list:
        wb_data = get_weibo_info(each, html)
        if wb_data is not None:
            search_list.append(wb_data)
    return search_list




