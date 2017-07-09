# coding:utf-8
import os
import time
import signal
import requests
from headers import headers
from db.redis_db import Urls
from db.redis_db import Cookies
from logger.log import crawler, other
from db.login_info import freeze_account
from utils.email_warning import send_email
from page_parse.basic import is_403, is_404, is_complete
from decorators.decorator import timeout_decorator, timeout
from config.conf import get_timeout, get_crawl_interal, get_excp_interal, get_max_retries


time_out = get_timeout()
interal = get_crawl_interal()
max_retries = get_max_retries()
excp_interal = get_excp_interal()


def is_banned(url):
    if 'unfreeze' in url or 'accessdeny' in url or 'userblock' in url:
        return True
    return False


@timeout(200)
@timeout_decorator
def get_page(url, user_verify=True, need_login=True):
    """
    :param url: url to be crawled
    :param user_verify: if it's ajax url, the value is False, else True
    :param need_login: if the url is need to login, the value is True, else False
    :return: return '' if exception happens or status_code != 200
    """
    crawler.info('the crawling url is {url}'.format(url=url))
    count = 0

    while count < max_retries:
        if need_login:
            name_cookies = Cookies.fetch_cookies()

            if name_cookies is None:
                crawler.warning('no cookies in cookies pool, please find out the reason')
                send_email()
                os.kill(os.getppid(), signal.SIGTERM)
        try:
            if need_login:
                resp = requests.get(url, headers=headers, cookies=name_cookies[1], timeout=time_out, verify=False)

                if "$CONFIG['islogin'] = '0'" in resp.text:
                    crawler.warning('account {} has been banned'.format(name_cookies[0]))
                    freeze_account(name_cookies[0], 0)
                    Cookies.delete_cookies(name_cookies[0])
                    continue
            else:
                resp = requests.get(url, headers=headers, timeout=time_out, verify=False)

            page = resp.text

            if page:
                page = page.encode('utf-8', 'ignore').decode('utf-8')
            else:
                continue

            # slow down to aviod being banned
            time.sleep(interal)

            if user_verify:
                if is_banned(resp.url) or is_403(page):
                    crawler.warning('account {} has been banned'.format(name_cookies[0]))
                    freeze_account(name_cookies[0], 0)
                    Cookies.delete_cookies(name_cookies[0])
                    count += 1
                    continue

                if 'verifybmobile' in resp.url:
                    crawler.warning('account {} has been locked，you should use your phone to unlock it'.
                                    format(name_cookies[0]))
        
                    freeze_account(name_cookies[0], -1)
                    Cookies.delete_cookies(name_cookies[0])
                    continue

                if not is_complete(page):
                    count += 1
                    continue

                if is_404(page):
                    crawler.warning('{url} seems to be 404'.format(url=url))
                    return ''

        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError, AttributeError) as e:
            crawler.warning('excepitons happens when crawling {}，specific infos are {}'.format(url, e))
            count += 1
            time.sleep(excp_interal)

        else:
            Urls.store_crawl_url(url, 1)
            return page

    crawler.warning('max tries for {}，check the url in redis db2'.format(url))
    Urls.store_crawl_url(url, 0)
    return ''

__all__ = ['get_page']