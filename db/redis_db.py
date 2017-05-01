import json
import redis
from config.conf import get_redis_args


redis_args = get_redis_args()


class Cookies(object):
    rd_con = redis.StrictRedis(host=redis_args.get('host'), port=redis_args.get('port'), db=redis_args.get('cookies'))

    @classmethod
    def store_cookies(cls, name, cookies):
        pickled_cookies = json.dumps(cookies)
        cls.rd_con.set(name, pickled_cookies)
        # 为cookie设置过期时间，防止某些账号登录失败，还会获取到失效cookie
        cls.rd_con.expire(name, 20 * 60 * 60)

    @classmethod
    def fetch_cookies(cls):
        random_name = cls.rd_con.randomkey()
        return random_name, json.loads(cls.rd_con.get(random_name).decode('utf-8'))

    @classmethod
    def delete_cookies(cls, name):
        cls.rd_con.delete(name)
        return True


class Urls(object):
    rd_con = redis.StrictRedis(host=redis_args.get('host'), port=redis_args.get('port'), db=redis_args.get('urls'))

    @classmethod
    def store_crawl_url(cls, url, result):
        cls.rd_con.set(url, result)
