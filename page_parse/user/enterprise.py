# -*-coding:utf-8 -*-
# 认证企业资料页面
import re
import json
from bs4 import BeautifulSoup
from page_parse.user import public
from decorators.decorator import parse_decorator


@parse_decorator(4)
def get_detail(html):
    """
    这个是从认证企业的个人资料页面解析数据,一般不用这个
    :param html:
    :return:
    """
    details = {}
    cont = public.get_right(html)
    soup = BeautifulSoup(cont, 'html.parser')
    basic_modules = soup.find_all(attrs={'class': 'WB_cardwrap S_bg2'})
    basic_info = soup.find_all(attrs={'class': 'li_1 clearfix'})
    for each_module in basic_modules:
        if '简介' in each_module.get_text():
            description = each_module.find(attrs={'node-type': 'text'}).get_text().replace('\n', '')
            details['description'] = description
        if '基本讯息' in each_module.get_text():
            for each in basic_info:
                if '友情链接' in each.get_text():
                    friend_links = each.find(attrs={'class': 'pt_detail'}).get_text()
                    details['friend_links'] = friend_links
    return details


# 以下是通过认证企业主页进行解析
@parse_decorator(0)
def get_friends(html):
    cont = public.get_left(html)
    soup = BeautifulSoup(cont, 'html.parser')
    return int(soup.find_all('strong')[0].get_text())


@parse_decorator(0)
def get_fans(html):
    cont = public.get_left(html)
    soup = BeautifulSoup(cont, 'html.parser')
    return int(soup.find_all('strong')[1].get_text())


@parse_decorator(0)
def get_status(html):
    cont = public.get_left(html)
    soup = BeautifulSoup(cont, 'html.parser')
    return int(soup.find_all('strong')[2].get_text())


@parse_decorator(1)
def get_description(html):
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all('script')
    pattern = re.compile(r'FM.view\((.*)\)')
    cont = ''
    description = ''
    for script in scripts:
        m = pattern.search(script.string)
        if m and 'pl.content.homeFeed.index' in script.string and '简介' in script.string:
            all_info = m.group(1)
            cont = json.loads(all_info)['html']
    if cont != '':
        soup = BeautifulSoup(cont, 'html.parser')
        detail = soup.find(attrs={'class': 'ul_detail'}).find_all(attrs={'class': 'item S_line2 clearfix'})
        for li in detail:
            if '简介' in li.get_text():
                description = li.find_all('span')[1].get_text().replace('\r\n', '').strip()[3:].strip()
    return description


