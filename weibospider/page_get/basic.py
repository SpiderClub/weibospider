import os
import time
import signal
import random

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from config import headers
from logger import crawler_logger
from login import get_cookies
from db.dao import LoginInfoOper
from utils import send_email
from db.redis_db import (
    Urls, Cookies)
from page_parse import (
    is_403, is_404, is_complete)
from decorators import (
    timeout_decorator, timeout)
from config import (request_time_out, min_crawl_interval,
                    max_crawl_interval, max_retries,
                    excp_interval)


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
COOKIES = get_cookies()


def _is_banned(url):
    if 'unfreeze' in url or 'accessdeny' in url or 'userblock' in url \
            or 'verifybmobile' in url:
        return True
    return False


@timeout(200)
@timeout_decorator
def get_page(url, auth_level=2, is_ajax=False, need_proxy=False):
    """
    :param url: url to crawl
    :param auth_level: 0 stands for need nothing,1 stands for no login but need cookies,2 stands for need login.
    :param is_ajax: whether the request is ajax
    :param need_proxy: whether the request need a http/https proxy
    :return: response text, when a exception is raised, return ''
    """
    crawler_logger.info('the crawling url is {}'.format(url))
    count = 0
    kwargs = {
        'headers': headers,
        'timeout': request_time_out,
        'verify': False
    }

    while count < max_retries:
        if auth_level == 2:
            name_cookies = Cookies.fetch_cookies()

            if name_cookies is None:
                crawler_logger.warning('No cookie in cookies pool. Maybe all accounts are banned, '
                                       'or all cookies are expired')
                send_email()
                os.kill(os.getppid(), signal.SIGTERM)

        try:
            if auth_level == 2:
                resp = requests.get(url, cookies=name_cookies[1], **kwargs)
            elif auth_level == 1:
                resp = requests.get(url, cookies=COOKIES, **kwargs)
            else:
                resp = requests.get(url, **kwargs)
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError, AttributeError) as e:
            crawler_logger.warning('Excepitons are raised when crawling {}.Here are details:{}'.format(url, e))
            count += 1
            time.sleep(excp_interval)
            continue

        if resp.status_code == 414:
            crawler_logger.warning('This ip has been blocked by weibo system')
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
            interval = random.randint(min_crawl_interval, max_crawl_interval)
            time.sleep(interval)
            if _is_banned(resp.url) or is_403(page):
                crawler_logger.warning('Account {} has been banned'.format(name_cookies[0]))
                LoginInfoOper.freeze_account(name_cookies[0], 0)
                Cookies.delete_cookies(name_cookies[0])
                count += 1
                continue

            if not is_ajax and not is_complete(page):
                count += 1
                continue

        if is_404(page):
            crawler_logger.warning('{} seems to be 404'.format(url))
            return ''
        Urls.store_crawl_url(url, 1)
        return page

    Urls.store_crawl_url(url, 0)
    return ''