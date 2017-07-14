# -*-coding:utf-8 -*-
import json
from utils import filters
from page_get.basic import get_page


base_url = 'http://weibo.com/p/aj/mblog/getlongtext?ajwvr=6&mid={}'


def get_cont_of_weibo(mid):
    """
    :param mid: weibo's mid
    :return: all cont of the weibo
    """
    url = base_url.format(mid)
    html = get_page(url, user_verify=False)

    if html:
        try:
            html = json.loads(html, encoding='utf-8').get('data').get('html')
            cont = filters.text_filter(html)
        except AttributeError:
            cont = ''
        return cont

__all__ = ['get_cont_of_weibo']
