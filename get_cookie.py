import time
from requests.exceptions import SSLError as ResE
from requests.packages.urllib3.exceptions import SSLError as SslE
from ssl import SSLEOFError as SsE
from wblogin import login
from logger.log import other


# todo 如果以后扩散成分布式，需要使cookie序列化放到队列或者内存中
# 这里之所以采用Manager.dict是考虑到如果消费者在做扩散信息采集的时候遇到cookie失效，那么消费者线程可以直接拿到最新的cookie
def _get_session(d):
    is_success = 0
    try:
        session = login.get_session()
    except (SsE, ResE, SslE):
        return is_success

    if session:
        d.setdefault('session', session)
        is_success = 1

    return is_success


def get_session(d):
    # 自动维护最新的cookie
    while 1:
        is_sucess = _get_session(d)
        if is_sucess:
            # 10个小时后重新登录，微博24小时cookie失效
            time.sleep(10*60*60)
        else:
            other.info('一分钟后重试模拟登录')
            time.sleep(60)





