import re
import json
import time

import requests


PASSPORT_URL = 'https://passport.weibo.com/visitor/visitor?entry=miniblog&a=' \
               'enter&url=http://weibo.com/&domain=.weibo.com&ua=' \
               'php-sso_sdk_client-0.6.23&_rand={}'.format(format(time.time(),
                                                                  '0.4f'))
POST_URL = 'https://passport.weibo.com/visitor/genvisitor'

print(PASSPORT_URL)


# TODO 优化这里
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

session = requests.session()


# TODO 结合UA进行优化
post_data = {
    'cb': 'gen_callback',
    'fp': '{"os":"1","browser":"Chrome61,0,3163,100","fonts":"undefined","screenInfo":"1436*752*24","plugins":"Portable Document Format::internal-pdf-viewer::Chrome PDF Plugin|::mhjfbmdgcfjbbpaeojofohoefgiehjai::Chrome PDF Viewer|::internal-nacl-plugin::Native Client|Enables Widevine licenses for playback of HTML audio/video content. (version: 1.4.8.1008)::widevinecdmadapter.dll::Widevine Content Decryption Module"}'
}

headers['Referer'] = PASSPORT_URL

# resp = session.post(POST_URL, data=post_data, headers=headers)

ts = 'window.gen_callback && gen_callback({"retcode":20000000,"msg":"succ","data":{"tid":"ztJRzNSeTZI4vRNqIXL2G8dnoyUfnNBEmuTPtilfVLE=","new_tid":false,"confidence":95}});'
extract_pattern = r'({.*})'
m = re.search(extract_pattern, ts)
s = m.group()
# w: True 3 False 2
# confidence
# tid
gen_visitor = json.loads(s)
tid = gen_visitor.get('data').get('tid')
c = gen_visitor.get('data').get('confidence', 100)
new_tid = gen_visitor.get('data').get('new_tid')
if new_tid == 'False':
    w = 3
else:
    w = 2

INRARNATE_URL = 'https://passport.weibo.com/visitor/visitor?a=incarn' \
                'ate&t={}&w={}&c={}&gc=&cb=cross_domain&from=weibo&_ran' \
                'd={}'.format(tid, w, c, 0.09958761514503123)

resp = session.get(INRARNATE_URL, headers=headers)

m = re.search(extract_pattern, resp.text)
s = json.loads(m.group())
sub = s.get('data').get('sub')
subp = s.get('data').get('subp')
print(sub)
print(subp)
print('sub: {}, subp: {}'.format(sub, subp))
headers.update(Cookie='SUB={};SUBP={};'.format(sub, subp))
print(headers)
resp = session.get('http://weibo.com/u/5860464935?is_all=1', headers=headers)
print(resp.text)
print(session.cookies.get_dict())