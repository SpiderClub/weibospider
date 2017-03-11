import time
from requests.exceptions import SSLError as ResE
from requests.packages.urllib3.exceptions import SSLError as SslE
from ssl import SSLEOFError as SsE
from wblogin import login
from logger.log import other


def _get_session(d):
    is_success = 0
    try:
        session_cookie = login.get_session()
    except (SsE, ResE, SslE):
        return is_success

    if session_cookie:
        d.setdefault('session', session_cookie.get('session'))
        is_success = 1

    return is_success


def get_session(d):
    while 1:
        is_sucess = _get_session(d)
        if is_sucess:
            time.sleep(10*60*60)
        else:
            other.info('一分钟后重试模拟登录')
            time.sleep(60)





