import os
import time
import signal
import random

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from config import headers
from logger import crawler
from login import get_cookies
from db.dao import LoginInfoOper
from utils import send_email
from db.redis_db import (
    Urls, Cookies)
from page_parse import (
    is_403, is_404, is_complete)
from decorators import (
    timeout_decorator, timeout)
from config import crawl_args


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

TIME_OUT = crawl_args.get('time_out')
MIN_CRAWL_INTERAL = crawl_args.get('min_crawl_interal')
MAX_CRAWL_INTERAL = crawl_args.get('max_crawl_interal')
MAX_RETRIES = crawl_args.get('max_retries')
EXCP_INTERAL = crawl_args.get('excp_interal')
COOKIES = get_cookies()


def is_banned(url):
    def _contains(str1, str2):
        return str1 in str2

    judge_condition = [
        'unfreeze', 'accessdeny', 'userblock', 'verifybmobile'
    ]

    return any(_contains(x, url) for x in judge_condition)


def temp_banned(url):
    return True if 'userblock&is_viewer&code=20003' in url else False


@timeout(200)
@timeout_decorator
def get_page(url, auth_level=2, is_ajax=False, need_proxy=False):
    """
    :param url: url to crawl
    :param auth_level: 0 stands for need nothing,1 stands for no
    login but need cookies,2 stands for need login.
    :param is_ajax: whether the request is ajax
    :param need_proxy: whether the request need a http/https proxy
    :return: response text, when a exception is raised, return ''
    """
    crawler.info('the crawling url is {}'.format(url))
    count = 0

    while count < MAX_RETRIES:
        if auth_level == 2:
            name_cookies = Cookies.fetch_cookies()

            if name_cookies is None:
                crawler.warning('No cookie in cookies pool. Maybe all accounts are '
                                'banned, or all cookies are expired')
                send_email()
                os.kill(os.getppid(), signal.SIGTERM)
        try:
            if auth_level == 2:
                resp = requests.get(url, headers=headers, cookies=name_cookies[1],
                                    timeout=TIME_OUT, verify=False)
            # todo no login cookies stores in redis
            elif auth_level == 1:
                resp = requests.get(url, headers=headers, cookies=COOKIES,
                                    timeout=TIME_OUT, verify=False)
            else:
                resp = requests.get(url, headers=headers, timeout=TIME_OUT, verify=False)
        except (requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectionError, AttributeError) as e:
            crawler.warning('Excepitons are raised when crawling {}.'
                            'Here are details:{}'.format(url, e))
            count += 1
            time.sleep(EXCP_INTERAL)
            continue

        if resp.status_code == 414:
            crawler.warning('This ip has been blocked by weibo system')
            if not need_proxy:
                send_email()
                os.kill(os.getppid(), signal.SIGTERM)

        if resp.text:
            page = resp.text.encode('utf-8', 'ignore').decode('utf-8')
        else:
            count += 1
            continue

        if auth_level == 2:
            # slow down to aviod being banned
            interal = random.randint(MIN_CRAWL_INTERAL, MAX_CRAWL_INTERAL)
            time.sleep(interal)

            if temp_banned(resp.url):
                crawler.warning('Account {} is temporarily blocked'.format
                                (name_cookies[0]))
                count += 1
                time.sleep(EXCP_INTERAL)
                continue

            if is_banned(resp.url) or is_403(page):
                crawler.warning('Account {} has been banned'.format(name_cookies[0]))
                LoginInfoOper.freeze_account(name_cookies[0], 0)
                Cookies.delete_cookies(name_cookies[0])
                count += 1
                continue

            if not is_ajax and not is_complete(page):
                count += 1
                continue

        if is_404(page):
            crawler.warning('{} seems to be 404'.format(url))
            return ''
        Urls.store_crawl_url(url, 1)
        return page

    Urls.store_crawl_url(url, 0)
    return ''
