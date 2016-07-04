import redis
import requests
import json
from gl import headers
from do_login import login_info


def store_cookie():
    cookie_dict = login_info.get_session()['cookie']
    r = redis.Redis(host='localhost', port=6379, db=0)
    cookiestr = json.dumps(cookie_dict)
    r.set('userinfo_cookie', cookiestr)


def get_cookie():
    r = redis.Redis(host='localhost', port=6379, db=0)
    return json.loads(r.get('userinfo_cookie').decode('utf-8'))


if __name__ == '__main__':
    store_cookie()
    cookie = get_cookie()
    content = requests.get('http://weibo.com/p/1005051921017243/info?mod=pedit_more', cookies=cookie, headers=headers).text
    print(content)