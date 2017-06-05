# -*-coding:utf-8 -*-
import re
import json
from bs4 import BeautifulSoup
from logger.log import parser
from db.models import WeiboData
from decorators.decorator import parse_decorator


@parse_decorator(1)
def get_weibo_infos_right(html):
    """
    通过网页获取用户主页右边部分（即微博部分）字符串
    :param html: 
    :return: 
    """
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all('script')
    pattern = re.compile(r'FM.view\((.*)\)')

    # 如果字符串'fl_menu'(举报或者帮上头条)这样的关键字出现在script中，则是微博数据区域
    cont = ''
    for script in scripts:
        m = pattern.search(script.string)
        if m and 'fl_menu' in script.string:
            all_info = m.group(1)
            cont += json.loads(all_info).get('html', '')
    return cont


@parse_decorator(5)
def get_weibo_info_detail(each, html):
    wb_data = WeiboData()

    user_cont = each.find(attrs={'class': 'face'})
    user_info = str(user_cont.find('a'))
    user_pattern = 'id=(\\d+)&amp'
    m = re.search(user_pattern, user_info)
    if m:
        wb_data.uid = m.group(1)
    else:
        parser.warning('未提取到用户id,页面源码是{}'.format(html))
        return None

    weibo_pattern = 'mid=(\\d+)'
    m = re.search(weibo_pattern, str(each))
    if m:
        wb_data.weibo_id = m.group(1)
    else:
        parser.warning('未提取到页面的微博id,页面源码是{}'.format(html))
        return None

    time_url = each.find(attrs={'node-type': 'feed_list_item_date'})
    wb_data.create_time = time_url.get('title', '')
    wb_data.weibo_url = time_url.get('href', '')
    if 'weibo.com' not in wb_data.weibo_url:
        wb_data.weibo_url = 'http://weibo.com{}'.format(wb_data.weibo_url)

    wb_data.weibo_cont = each.find(attrs={'node-type': 'feed_content'}).find\
        (attrs={'node-type': 'feed_list_content'}).text.strip()
    try:
        wb_data.device = each.find(attrs={'class': 'WB_from'}).find(attrs={'action-type': 'app_source'}).text
    except Exception as e:
        parser.error('本次解析设备出错，具体是{}'.format(e))
        wb_data.device = ''

    try:
        wb_data.repost_num = int(each.find(attrs={'action-type': 'fl_forward'}).find_all('em')[1].text)
    except Exception:
        wb_data.repost_num = 0
    try:
        wb_data.comment_num = int(each.find(attrs={'action-type': 'fl_comment'}).find_all('em')[1].text)
    except Exception:
        wb_data.comment_num = 0
    try:
        wb_data.praise_num = int(each.find(attrs={'action-type': 'fl_like'}).find_all('em')[1].text)
    except Exception:
        wb_data.praise_num = 0
    return wb_data


def get_weibo_list(html):
    """
    获取所有微博信息列表
    :param html: 
    :return: 
    """
    if not html:
        return list()
    soup = BeautifulSoup(html, "html.parser")
    feed_list = soup.find_all(attrs={'action-type': 'feed_list_item'})
    weibo_datas = []
    for data in feed_list:
        wb_data = get_weibo_info_detail(data, html)
        if wb_data is not None:
            weibo_datas.append(wb_data)
    return weibo_datas


def get_max_num(html):
    """
    获取总页数
    :param html: 
    :return: 
    """
    soup = BeautifulSoup(html, "html.parser")
    href_list = soup.find(attrs={'action-type': 'feed_list_page_morelist'}).find_all('a')
    return len(href_list)


def get_wbdata_fromweb(html):
    """
    从主页获取具体的微博数据
    :param html: 
    :return: 
    """
    cont = get_weibo_infos_right(html)
    return get_weibo_list(cont)


def get_home_wbdata_byajax(html):
    """
    通过返回的ajax内容获取用户微博信息
    :param html: 
    :return: 
    """
    cont = json.loads(html, encoding='utf-8').get('data', '')
    return get_weibo_list(cont)


def get_total_page(html):
    """
    从ajax返回的内容获取用户主页的所有能看到的页数
    :param html: 
    :return: 
    """
    cont = json.loads(html, encoding='utf-8').get('data', '')
    if not cont:
        # todo 返回1或者0还需要验证只有一页的情况
        return 1
    return get_max_num(cont)
