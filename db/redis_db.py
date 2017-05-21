# coding:utf-8
import json
import redis
from config.conf import get_redis_args


redis_args = get_redis_args()


class Cookies(object):
    rd_con = redis.StrictRedis(host=redis_args.get('host'), port=redis_args.get('port'),
                               password=redis_args.get('password'), db=redis_args.get('cookies'))

    @classmethod
    def store_cookies(cls, name, cookies):
        pickled_cookies = json.dumps(cookies)
        cls.rd_con.set(name, pickled_cookies)
        # 为cookie设置过期时间，防止某些账号登录失败，还会获取到失效cookie
        cls.rd_con.expire(name, 20 * 60 * 60)

    @classmethod
    def fetch_cookies(cls):
        cookies_count = len(cls.rd_con.keys())
        if cookies_count:
            random_name = cls.rd_con.randomkey()
            return random_name.decode('utf-8'), json.loads(cls.rd_con.get(random_name).decode('utf-8')), cookies_count
        else:
            return None, cookies_count

    @classmethod
    def delete_cookies(cls, name):
        cls.rd_con.delete(name)
        return True


class Urls(object):
    rd_con = redis.StrictRedis(host=redis_args.get('host'), port=redis_args.get('port'),
                               password=redis_args.get('password'), db=redis_args.get('urls'))

    @classmethod
    def store_crawl_url(cls, url, result):
        cls.rd_con.set(url, result)


class IdNames(object):
    rd_con = redis.StrictRedis(host=redis_args.get('host'), port=redis_args.get('port'),
                               password=redis_args.get('password'), db=redis_args.get('id_name'))

    @classmethod
    def store_id_name(cls, user_name, user_id):
        cls.rd_con.set(user_name, user_id)

    @classmethod
    def fetch_uid_by_name(cls, user_name):
        user_id = cls.rd_con.get(user_name)
        if user_id:
            return user_id.decode('utf-8')
        return ''