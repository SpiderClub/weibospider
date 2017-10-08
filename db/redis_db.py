import json
import socket
import datetime

import redis
from redis.sentinel import Sentinel

from logger import crawler
from config import (
    get_redis_args,
    get_share_host_count,
    get_running_mode,
    get_cookie_expire_time
)


MODE = get_running_mode()
SHARE_HOST_COUNT = get_share_host_count()
REDIS_ARGS = get_redis_args()

password = REDIS_ARGS.get('password', '')
cookies_db = REDIS_ARGS.get('cookies', 1)
urls_db = REDIS_ARGS.get('urls', 2)
broker_db = REDIS_ARGS.get('broker', 5)
backend_db = REDIS_ARGS.get('backend', 6)
id_name_db = REDIS_ARGS.get('id_name', 8)
cookie_expire_time = get_cookie_expire_time()
data_expire_time = REDIS_ARGS.get('expire_time') * 60 * 60

sentinel_args = REDIS_ARGS.get('sentinel', '')
if sentinel_args:
    # default socket timeout is 2 secs
    master_name = REDIS_ARGS.get('master')
    socket_timeout = int(REDIS_ARGS.get('socket_timeout', 2))
    sentinel = Sentinel([(args['host'], args['port']) for args in sentinel_args], password=password,
                        socket_timeout=socket_timeout)
    cookies_con = sentinel.master_for(master_name, socket_timeout=socket_timeout, db=cookies_db)
    broker_con = sentinel.master_for(master_name, socket_timeout=socket_timeout, db=broker_db)
    urls_con = sentinel.master_for(master_name, socket_timeout=socket_timeout, db=urls_db)
    id_name_con = sentinel.master_for(master_name, socket_timeout=socket_timeout, db=id_name_db)
else:
    host = REDIS_ARGS.get('host', '127.0.0.1')
    port = REDIS_ARGS.get('port', 6379)
    cookies_con = redis.Redis(host=host, port=port, password=password, db=cookies_db)
    broker_con = redis.Redis(host=host, port=port, password=password, db=broker_db)
    urls_con = redis.Redis(host=host, port=port, password=password, db=urls_db)
    id_name_con = redis.Redis(host=host, port=port, password=password, db=id_name_db)


class Cookies(object):
    @classmethod
    def store_cookies(cls, name, cookies):
        pickled_cookies = json.dumps(
            {'cookies': cookies, 'loginTime': datetime.datetime.now().timestamp()})
        cookies_con.hset('account', name, pickled_cookies)
        cls.push_in_queue(name)

    @classmethod
    def push_in_queue(cls, name):
        # if the concurrency is large, we can't guarantee there are no reduplicate values
        for i in range(cookies_con.llen('account_queue')):
            tn = cookies_con.lindex('account_queue', i).decode('utf-8')
            if tn:
                if tn == name:
                    return
        cookies_con.rpush('account_queue', name)

    @classmethod
    def fetch_cookies(cls):
        if MODE == 'normal':
            return cls.fetch_cookies_of_normal()

        else:
            return cls.fetch_cookies_of_quick()

    @classmethod
    def fetch_cookies_of_normal(cls):
        # look for available accounts
        for i in range(cookies_con.llen('account_queue')):
            name = cookies_con.lpop('account_queue').decode('utf-8')
            # during the crawling, some cookies can be banned
            # some account fetched from account_queue can be unavailable
            j_account = cookies_con.hget('account', name)
            if not j_account:
                return None
            else:
                j_account = j_account.decode('utf-8')
                if cls.check_cookies_timeout(j_account):
                    cls.delete_cookies(name)
                    continue
                cookies_con.rpush('account_queue', name)
                account = json.loads(j_account)
                return name, account['cookies']
        return None

    @classmethod
    def fetch_cookies_of_quick(cls):
        # record one cookie used by how many host,
        # if the number is bigger than share_host_count，put it to the end of the queue
        # else just fetch and use it
        # todo there are some problems using hostname to mark different hosts because hostname can be the same
        hostname = socket.gethostname()
        my_cookies_name = cookies_con.hget('host', hostname)
        if my_cookies_name:
            my_cookies = cookies_con.hget('account', my_cookies_name)
            # if cookies is expired, fetch a new one
            if not cls.check_cookies_timeout(my_cookies):
                my_cookies = json.loads(my_cookies.decode('utf-8'))
                return my_cookies_name, my_cookies['cookies']
            else:
                cls.delete_cookies(my_cookies_name)

        while True:
            try:
                name = cookies_con.lpop('account_queue').decode('utf-8')
            except AttributeError:
                return None
            else:
                j_account = cookies_con.hget('account', name)

                if cls.check_cookies_timeout(j_account):
                    cls.delete_cookies(name)
                    continue

                j_account = j_account.decode('utf-8')
                # one account maps many hosts（one to many）
                hosts = cookies_con.hget('cookies_host', name)
                if not hosts:
                    hosts = dict()
                else:
                    hosts = hosts.decode('utf-8')
                    hosts = json.loads(hosts)
                hosts[hostname] = 1
                cookies_con.hset('cookies_host', name, json.dumps(hosts))

                # one host maps one account (one to one)
                account = json.loads(j_account)
                cookies_con.hset('host', hostname, name)

                # push the cookie to the head
                if len(hosts) < SHARE_HOST_COUNT:
                    cookies_con.lpush('account_queue', name)
                return name, account['cookies']

    @classmethod
    def delete_cookies(cls, name):
        cookies_con.hdel('account', name)
        if MODE == 'quick':
            cookies_con.hdel('cookies_host', name)
        return True

    @classmethod
    def check_login_task(cls):
        if broker_con.llen('login_queue') > 0:
            broker_con.delete('login_queue')

    @classmethod
    def check_cookies_timeout(cls, cookies):
        if cookies is None:
            return True
        if isinstance(cookies, bytes):
            cookies = cookies.decode('utf-8')
        cookies = json.loads(cookies)
        login_time = datetime.datetime.fromtimestamp(cookies['loginTime'])
        if datetime.datetime.now() - login_time > datetime.timedelta(hours=cookie_expire_time):
            crawler.warning('The account has been expired')
            return True
        return False


class Urls(object):
    @classmethod
    def store_crawl_url(cls, url, result):
        urls_con.set(url, result)
        urls_con.expire(url, data_expire_time)


class IdNames(object):
    @classmethod
    def store_id_name(cls, user_name, user_id):
        id_name_con.set(user_name, user_id)

    @classmethod
    def delele_id_name(cls, user_name):
        id_name_con.delete(user_name)

    @classmethod
    def fetch_uid_by_name(cls, user_name):
        user_id = id_name_con.get(user_name)
        cls.delele_id_name(user_name)
        if user_id:
            return user_id.decode('utf-8')
        return ''
