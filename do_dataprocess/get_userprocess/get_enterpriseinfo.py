# -*-coding:utf-8 -*-
# 认证企业资料页面
import re
import json
from bs4 import BeautifulSoup
from do_dataprocess.get_userprocess import get_publicinfo


def get_detail(html):
    """
    这个是从认证企业的个人资料页面解析数据,一般不用这个
    :param html:
    :return:
    """
    details = {}
    cont = get_publicinfo.get_right(html)
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
def get_friends(html):
    cont = get_publicinfo.get_left(html)
    soup = BeautifulSoup(cont, 'html.parser')
    return soup.find_all('strong')[0].get_text()
#    return soup.find_all(attrs={'class': 'W_f14'})[0].get_text()


def get_fans(html):
    cont = get_publicinfo.get_left(html)
    soup = BeautifulSoup(cont, 'html.parser')
    return soup.find_all('strong')[1].get_text()


def get_status(html):
    cont = get_publicinfo.get_left(html)
    soup = BeautifulSoup(cont, 'html.parser')
    return soup.find_all('strong')[2].get_text()


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


if __name__ == '__main__':
    with open('F:/360data/重要数据/桌面/luce.html', 'rb') as f:
        source = f.read().decode('utf-8')
    print(get_fans(source))