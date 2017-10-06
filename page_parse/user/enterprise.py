import re
import json

from bs4 import BeautifulSoup

from page_parse.user import public
from decorators import parse_decorator


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


@parse_decorator('')
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


