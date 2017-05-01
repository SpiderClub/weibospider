import json
import redis
from config.conf import get_redis_args


redis_args = get_redis_args()
rd_con = redis.StrictRedis(host=redis_args.get('host'), port=redis_args.get('port'), db=redis_args.get('cookies_db'))


def store_cookies(name, cookies):
    pickled_cookies = json.dumps(cookies)
    rd_con.set(name, pickled_cookies)
    # 为cookie设置过期时间，防止某些账号登录失败，还会获取到失效cookie
    rd_con.expire(name, 20*60*60)


def fetch_cookies():
    name = _get_random_key()
    return name, json.loads(rd_con.get(name).decode('utf-8'))


def _get_random_key():
    return rd_con.randomkey()


def delete_cookies(name):
    rd_con.delete(name)