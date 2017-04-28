import time

import requests

from config.get_config import get_timeout, get_crawl_interal, get_excp_interal
from db.login_info import set_account_freeze
from db.cookies_db import fetch_cookies
from decorator.decorators import timeout_decorator, timeout
from headers import headers
from logger.log import crawler
from page_parse.basic import is_403, is_404, is_complete

time_out = get_timeout()
interal = get_crawl_interal()
excp_interal = get_excp_interal()
name_cookies = fetch_cookies()


# 每次抓取都从redis中随机取一个cookie以降低被封号的危险，但是还没验证不同ip对账号的影响
# todo 验证代理ip使用cookie访问用户信息会不会出现验证码
@timeout(200)
@timeout_decorator
def get_page(url, user_verify=True):
    """
    :param url: 待出现
    :param user_verify: 是否为可能出现验证码的页面(ajax连接不会出现验证码，如果是请求微博或者用户信息可能出现验证码)，否为抓取转发的ajax连接
    :return: 返回请求的数据，如果出现404或者403,或者是别的异常，都返回空字符串
    """
    crawler.info('本次抓取的url为{url}'.format(url=url))

    try:
        resp = requests.get(url, headers=headers, cookies=name_cookies[1], timeout=time_out, verify=False)
        page = resp.text.encode('utf-8', 'ignore').decode('utf-8')

        # 每次抓取过后程序sleep的时间，降低封号危险
        time.sleep(interal)

        if user_verify:
            if 'unfreeze' in resp.url or is_403(page):
                crawler.warning('账号{}已经被冻结'.format(name_cookies[0]))
                set_account_freeze(name_cookies[0])
                # todo 将抓取失败的任务加入重试队列（但是微博扩散的失败重试逻辑和用户抓取的失败重试逻辑不同）
                return ''
            if is_404(page):
                crawler.warning('url为{url}的连接不存在'.format(url=url))
                return ''
            if not is_complete(page):
                time.sleep(excp_interal)
                try:
                    page = requests.get(url, headers=headers, timeout=time_out, verify=False).text. \
                        encode('utf-8', 'ignore').decode('utf-8')
                except Exception as why:
                    crawler.error(why)
                    return ''

    except requests.exceptions.ReadTimeout:
        crawler.warning('抓取{url}时连接目标服务器超时'.format(url=url))
        time.sleep(excp_interal)
        return ''
    except requests.exceptions.ConnectionError as e:
        crawler.warning('目标服务器拒绝连接，程序休眠{}分钟,具体异常信息为:{}'.format(excp_interal, e))
        time.sleep(excp_interal)
        return ''
    else:
        return page
