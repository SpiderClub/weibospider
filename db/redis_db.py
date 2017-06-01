# coding:utf-8
import datetime
import json
import re

import redis
from config.conf import get_redis_args

redis_args = get_redis_args()


class Cookies(object):
    rd_con = redis.StrictRedis(host=redis_args.get('host'), port=redis_args.get('port'),
                               password=redis_args.get('password'), db=redis_args.get('cookies'))

    rd_con_broker = redis.StrictRedis(host=redis_args.get('host'), port=redis_args.get('port'),
                                      password=redis_args.get('password'), db=redis_args.get('broker'))

    @classmethod
    def store_cookies(cls, name, cookies):
        pickled_cookies = json.dumps(
            {'cookies': cookies, 'loginTime': datetime.datetime.now().timestamp()})
        cls.rd_con.hset('account', name, pickled_cookies)
        cls.rd_con.lpush('account_queue', name)

    @classmethod
    def fetch_cookies(cls):
        for i in range(cls.rd_con.llen('account_queue')):
            name = cls.rd_con.rpop('account_queue').decode('utf-8')
            if name:
                j_account = cls.rd_con.hget('account', name).decode('utf-8')
                if j_account:
                    cls.rd_con.lpush('account_queue', name)  # 当账号不存在时，这个name也会清除，并取下一个name
                    account = json.loads(j_account)
                    login_time = datetime.datetime.fromtimestamp(account['loginTime'])
                    if datetime.datetime.now() - login_time > datetime.timedelta(hours=20):
                        cls.rd_con.hdel('account', name)
                        continue  # 丢弃这个过期账号,account_queue会在下次访问的时候被清除,这里不清除是因为分布式的关系
                    return name, account['cookies']
            else:
                return None

    @classmethod
    def delete_cookies(cls, name):
        cls.rd_con.hdel('account', name)
        return True

    @classmethod
    def check_login_task(cls):
        if cls.rd_con_broker.llen('login_queue') > 0:
            cls.rd_con_broker.delete('login_queue')


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
