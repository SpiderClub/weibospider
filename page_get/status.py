import json

from utils import text_filter
from .basic import get_page


BASE_URL = 'http://s.weibo.com/ajax/direct/morethan140?mid={}'


def get_cont_of_weibo(mid):
    """
    :param mid: weibo's mid
    :return: all cont of the weibo
    """
    url = BASE_URL.format(mid)
    html = get_page(url, auth_level=0, is_ajax=True)

    if html:
        try:
            html = json.loads(html, encoding='utf-8').get('data').get('html')
            cont = text_filter(html)
        except AttributeError:
            cont = ''
        return cont
    else:
        return ''

