import redis, requests, json, time
from gl import headers
from do_login import login_info
from requests.exceptions import SSLError as rsle
from requests.packages.urllib3.exceptions import SSLError as rpuese
from ssl import SSLEOFError as sse


# 将cookie存入内存数据库中，每次都从内存数据库取cookie来进行请求
# todo: 为什么某些时候请求不会成功
def store_cookie():
    cookie_dict = login_info.get_session()['cookie']
    r = redis.Redis(host='localhost', port=6379, db=0)
    cookiestr = json.dumps(cookie_dict)
    r.set('userinfo_cookie', cookiestr)


def get_cookie():
    r = redis.Redis(host='localhost', port=6379, db=0)
    return r.get('userinfo_cookie').decode('utf-8')


def get_session(q):
    while True:
        try:
            session = login_info.get_session()['session']
            if session is None:
                # todo: 邮件通知
                time.sleep(60*5)
                session = login_info.get_session()['session']
        except (sse, rsle, rpuese):
            # 预防因为网络问题导致的登陆不成功
            print('本次登陆出现问题')
            time.sleep(60)
            session = login_info.get_session()['session']
        finally:
            q.put(session)
            # session24小时过期，但是为了防止某次任务过长，所以周期时间设置比较短
            time.sleep(15*60*60)


if __name__ == '__main__':
    store_cookie()
    #time.sleep(10)
    cookie = get_cookie()
    cookie = json.loads(cookie)
    content = requests.get('http://weibo.com/p/1005051921017243/info?mod=pedit_more', headers=headers, cookies=cookie).text
    print(content)

