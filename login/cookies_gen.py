import re
import json
import time
import random
import string

import requests

from config import FakeChromeUA
from exceptions import CookieGenException


PASSPORT_URL = 'https://passport.weibo.com/visitor/visitor?entry=miniblog&a=enter&url=http://weibo.com/&domain=.wei' \
               'bo.com&ua=php-sso_sdk_client-0.6.23&_rand={}'.format(format(time.time(), '0.4f'))
POST_URL = 'https://passport.weibo.com/visitor/genvisitor'
INRARNATE_URL = 'https://passport.weibo.com/visitor/visitor?a=incarnate&t={}&w={}&c={}&gc=&cb=cross_domain&from=' \
                'weibo&_rand={}'
CHECK_URL = 'http://weibo.com/1319066361/Flttyxak8'

user_agent = FakeChromeUA.get_ua()
brower_type, brower_version = user_agent.split(' ')[-2].split('/')
brower_info = ''.join((brower_type, ','.join(brower_version.split('.'))))


headers = {
    'User-Agent': user_agent,
    'Referer': PASSPORT_URL
}


extract_pattern = r'({.*})'


def get_tid_and_c(post_url):
    """
    get all args including tid、c and w
    :return: tuple(tid, c, w)
    """
    fp = '{' + \
         '"os":"1","browser":"{browser}","fonts":"undefined","screenInfo":"1436*752*24","plugins":"Portable ' \
         'Document Format::internal-pdf-viewer::Chrome PDF Plugin|::mhjfbmdgcfjbbpaeojofohoefgiehjai::Chrome PDF Viewer' \
         '|::internal-nacl-plugin::Native Client|Enables Widevine licenses for playback of HTML audio/video content. ' \
         '(version: 1.4.8.1008)::widevinecdmadapter.dll::Widevine Content Decryption Module"'.format(browser=brower_info) \
         + '}'

    post_data = {
        'cb': 'gen_callback',
        'fp': fp
    }

    resp = requests.post(post_url, data=post_data, headers=headers)
    m = re.search(extract_pattern, resp.text)
    try:
        s = m.group()
        gen_visitor = json.loads(s)
        tid = gen_visitor.get('data').get('tid')
        c = gen_visitor.get('data').get('confidence', 100)
        new_tid = gen_visitor.get('data').get('new_tid')
    except AttributeError:
        raise CookieGenException('failed to gen cookies without login')
    else:
        if new_tid == 'False':
            w = 3
        else:
            w = 2

        return tid, c, w


def get_cookies(mode):
    """
    :param mode: if mode is 'strict', get subp and sub from weibo system;
    if mode is default, just gen sub and subp by random
    :return:
    """
    if mode == 'strict':
        tid, c, w = get_tid_and_c(POST_URL)
        inrarnate_url = INRARNATE_URL.format(tid, w, c, format(random.random(), '.17f'))
        resp = requests.get(inrarnate_url, headers=headers)
        try:
            m = re.search(extract_pattern, resp.text)
            s = json.loads(m.group())
            sub = s.get('data').get('sub')
            subp = s.get('data').get('subp')
        except AttributeError:
            raise CookieGenException('failed to gen cookies without login')

        cookie_str = 'SUB={};SUBP={};'.format(sub, subp)
        headers.update(Cookie=cookie_str)
        resp = requests.get(CHECK_URL, headers=headers)
        if '$CONFIG' not in resp.text:
            raise CookieGenException('failed to gen cookies without login')
        return cookie_str
    else:
        sub = '_' + ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)
                            for _ in range(83)) + '..'
        subp = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)
                       for _ in range(88))

    cookies = dict(SUB=sub, SUBP=subp)
    resp = requests.get(CHECK_URL, cookies=cookies)
    if '$CONFIG' not in resp.text:
        raise CookieGenException('failed to gen cookies without login')
    return dict(SUB=sub, SUBP=subp)



