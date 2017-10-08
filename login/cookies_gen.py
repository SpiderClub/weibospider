import re
import json
import time
import random
from urllib import parse

import requests

from config import FakeChromeUA
from decorators import retry
from exceptions import CookieGenException

PASSPORT_URL = 'https://passport.weibo.com/visitor/visitor?entry=miniblog&a=enter&url={}&domain=.wei' \
               'bo.com&ua=php-sso_sdk_client-0.6.23&_rand={}'.format(parse.quote_plus('http://weibo.com/'),
                                                                     format(time.time(), '0.4f'))
POST_URL = 'https://passport.weibo.com/visitor/genvisitor'
INRARNATE_URL = 'https://passport.weibo.com/visitor/visitor?a=incarnate&t={}&w={}&c={}&gc=&cb=cross_domain&from=' \
                'weibo&_rand={}'
CHECK_URL = 'http://weibo.com/1319066361/Flttyxak8'

user_agent = FakeChromeUA.get_ua()
brower_type, brower_version = user_agent.split(' ')[-2].split('/')
brower_info = ''.join((brower_type, ','.join(brower_version.split('.'))))
headers = {
    'User-Agent': user_agent,
    'Referer': INRARNATE_URL,
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Host': 'passport.weibo.com',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
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
         '(version: 1.4.8.1008)::widevinecdmadapter.dll::Widevine Content Decryption Module"'.format(
             browser=brower_info) \
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
        if c != 100:
            c = '0' + str(c)
        new_tid = gen_visitor.get('data').get('new_tid')
    except AttributeError:
        raise CookieGenException('failed to gen cookies without login')
    else:
        if str(new_tid).lower() == 'false':
            w = 2
        else:
            w = 3

        return tid, c, w


@retry(10, 1, exceptions=CookieGenException)
def get_cookies():
    """
    :return: cookies: sub and subp
    """

    tid, c, w = get_tid_and_c(POST_URL)
    r_tid = parse.quote_plus(tid)
    inrarnate_url = INRARNATE_URL.format(r_tid, w, c, format(random.random(), '.17f'))
    cookies = {'tid': tid + '__' + c}
    resp = requests.get(inrarnate_url, headers=headers, cookies=cookies)
    try:
        m = re.search(extract_pattern, resp.text)
        resp_str = m.group()
        if 'errline' in resp_str:
            raise CookieGenException('Invalid cookie without login')
        s = json.loads(resp_str)
        sub = s.get('data').get('sub', '')
        subp = s.get('data').get('subp', '')
    except AttributeError:
        raise CookieGenException('Failed to gen cookies without login')
    if not sub and not subp:
        raise CookieGenException('Invalid cookie without login')
    return dict(SUB=sub, SUBP=subp)