# -*-coding:utf-8 -*-
# 各类用户公有的模块
import re
import json
from bs4 import BeautifulSoup
from do_dataprocess.do_statusprocess import status_parse
from weibo_decorator.decorators import parse_decorator


def get_userid(html):
    return status_parse.get_userid(html)


def get_username(html):
    return status_parse.get_username(html)


def get_userdomain(html):
    return status_parse.get_userdomain(html)


@parse_decorator(1)
def _get_header(html):
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all('script')
    pattern = re.compile(r'FM.view\((.*)\)')
    cont = ''
    for script in scripts:
        m = pattern.search(script.string)
        if m and 'pl.header.head.index' in script.string:
            all_info = m.group(1)
            cont = json.loads(all_info)['html']
    return cont


def get_verifytype(html):
    """
    :param html:
    :return: 0表示未认证，1表示个人认证，2表示企业认证
    """
    if 'icon_pf_approve_co' in html:
        return 2
    elif 'icon_pf_approve' in html:
        return 1
    else:
        return 0


@parse_decorator(1)
def get_verifyreason(html, verify_type):
    if verify_type == 1 or verify_type == 2:
        soup = BeautifulSoup(_get_header(html), 'html.parser')
        return soup.find(attrs={'class': 'pf_intro'})['title']
    else:
        return ''


@parse_decorator(1)
def get_headimg(html):
    soup = BeautifulSoup(_get_header(html), 'html.parser')
    try:
        headimg = soup.find(attrs={'class': 'photo_wrap'}).find(attrs={'class': 'photo'})['src']
    except AttributeError:
        headimg = ''
    return headimg


@parse_decorator(1)
def get_left(html):
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all('script')
    pattern = re.compile(r'FM.view\((.*)\)')
    cont = ''
    l_id = ''
    # 这里先确定左边的标识
    for script in scripts:
        m = pattern.search(script.string)
        if m and 'WB_frame_b' in script.string:
            all_info = m.group(1)
            cont = json.loads(all_info)['html']
            lsoup = BeautifulSoup(cont, 'html.parser')
            l_id = lsoup.find(attrs={'class': 'WB_frame_b'}).div['id']
    for script in scripts:
        m = pattern.search(script.string)
        if m and l_id in script.string:
            all_info = m.group(1)
            try:
                cont = json.loads(all_info)['html']
            except KeyError:
                return ''
    return cont


@parse_decorator(1)
def get_right(html):
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all('script')
    pattern = re.compile(r'FM.view\((.*)\)')
    cont = ''
    # 这里先确定右边的标识,企业用户可能会有两个r_id
    rids = []
    for script in scripts:
        m = pattern.search(script.string)
        if m and 'WB_frame_c' in script.string:
            all_info = m.group(1)
            cont = json.loads(all_info)['html']
            rsoup = BeautifulSoup(cont, 'html.parser')
            r_ids = rsoup.find(attrs={'class': 'WB_frame_c'}).find_all('div')
            for r in r_ids:
                rids.append(r['id'])
    for script in scripts:
        for r_id in rids:
            m = pattern.search(script.string)
            if m and r_id in script.string:
                all_info = m.group(1)
                try:
                    cont += json.loads(all_info)['html']
                except KeyError:
                    return ''
    return cont

if __name__ == '__main__':
    with open('F:/360data/重要数据/桌面/luce.html', 'rb') as f:
        source = f.read().decode('utf-8')
    print(get_username(source))

