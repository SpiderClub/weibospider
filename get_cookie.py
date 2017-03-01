import time
from requests.exceptions import SSLError as ResE
from requests.packages.urllib3.exceptions import SSLError as SslE
from ssl import SSLEOFError as SsE
from weibo_login import login_info
from logger.log import other


def get_session(d):
    while True:
        try:
            d.setdefault('session', login_info.get_session()['session'])
            if d['session'] is None:
                time.sleep(60*5)
                other.log('本次登录失败，账号是{}')
                d['session'] = login_info.get_session()['session']
        except (SsE, ResE, SslE):
            # 预防因为网络问题导致的登陆不成功
            print('本次登陆出现问题,一分钟后重试')
            time.sleep(60)
            d['session'] = login_info.get_session()['session']
        else:
            time.sleep(60*60*10)




