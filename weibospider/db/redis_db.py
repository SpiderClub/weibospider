import json
import socket
import datetime

import redis
from redis.sentinel import Sentinel

from logger import crawler_logger
from exceptions import NoCookieException
from config import (
    running_mode, share_host_count,
    redis_pass, redis_host,
    redis_port, master,
    sentinel as sentinel_args, socket_timeout,
    cookies as cookies_db, broker as broker_db,
    urls as urls_db, id_name as id_name_db,
    cookie_expire_time, data_expire_time,
    nologin_cookie_expire_time
)


if master and sentinel_args:
    sentinel = Sentinel([(args[0], args[1]) for args in sentinel_args],
                        password=redis_pass,
                        socket_timeout=socket_timeout
                        )

    cookies_con = sentinel.master_for(
        master, socket_timeout=socket_timeout, db=cookies_db)
    broker_con = sentinel.master_for(
        master, socket_timeout=socket_timeout, db=broker_db)
    urls_con = sentinel.master_for(
        master, socket_timeout=socket_timeout, db=urls_db)
    id_name_con = sentinel.master_for(
        master, socket_timeout=socket_timeout, db=id_name_db)
else:
    redis_args = {
        'host': redis_host,
        'port': redis_port,
        'password': redis_pass
    }
    cookies_con = redis.StrictRedis(**redis_args, db=cookies_db)
    broker_con = redis.StrictRedis(**redis_args, db=broker_db)
    urls_con = redis.StrictRedis(**redis_args, db=urls_db)
    id_name_con = redis.StrictRedis(**redis_args, db=id_name_db)


class Cookies(object):
    account_hash_set = 'account'
    cookie_host_maps = 'cookies_host'
    account_queue = 'account_queue'
    without_login_cookies = 'nologin_queue'

    @classmethod
    def store_cookies(cls, name, cookies):
        pickled_cookies = json.dumps(
            {'cookies': cookies, 'loginTime': datetime.datetime.now().timestamp()})
        cookies_con.hset(cls.account_hash_set, name, pickled_cookies)
        cls.push_in_queue(name)

    @classmethod
    def push_in_queue(cls, name):
        # if the concurrency is large, we can't guarantee there are no reduplicate values
        for i in range(cookies_con.llen(cls.account_queue)):
            tn = cookies_con.lindex(cls.account_queue, i).decode('utf-8')
            if tn:
                if tn == name:
                    return
        cookies_con.rpush(cls.account_queue, name)

    @classmethod
    def fetch_cookies(cls):
        if running_mode == 'normal':
            return cls.fetch_cookies_of_normal()

        else:
            return cls.fetch_cookies_of_quick()

    @classmethod
    def fetch_cookies_of_normal(cls):
        # look for available accounts
        for i in range(cookies_con.llen(cls.account_queue)):
            name = cookies_con.lpop(cls.account_queue).decode('utf-8')
            # during the crawling, some cookies can be banned
            # some account fetched from account_queue can be unavailable
            j_account = cookies_con.hget(cls.account_hash_set, name)
            if not j_account:
                return
            else:
                j_account = j_account.decode('utf-8')
                if cls.check_cookies_timeout(j_account):
                    cls.delete_cookies(name)
                    continue
                cookies_con.rpush(cls.account_queue, name)
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
            my_cookies = cookies_con.hget(cls.account_hash_set, my_cookies_name)
            # if cookies is expired, fetch a new one
            if not cls.check_cookies_timeout(my_cookies):
                my_cookies = json.loads(my_cookies.decode('utf-8'))
                return my_cookies_name, my_cookies['cookies'], my_cookies['proxy']
            else:
                cls.delete_cookies(my_cookies_name)

        while True:
            try:
                name = cookies_con.lpop(cls.account_queue).decode('utf-8')
            except AttributeError:
                return None
            else:
                j_account = cookies_con.hget(cls.account_hash_set, name)

                if cls.check_cookies_timeout(j_account):
                    cls.delete_cookies(name)
                    continue

                j_account = j_account.decode('utf-8')
                # one account maps many hosts (one to many)
                hosts = cookies_con.hget(cls.cookie_host_maps, name)
                if not hosts:
                    hosts = dict()
                else:
                    hosts = hosts.decode('utf-8')
                    hosts = json.loads(hosts)
                hosts[hostname] = 1
                cookies_con.hset(cls.cookie_host_maps, name, json.dumps(hosts))

                # one host maps one account (one to one)
                account = json.loads(j_account)
                cookies_con.hset('host', hostname, name)

                # push the cookie to the head
                if len(hosts) < share_host_count:
                    cookies_con.lpush(cls.account_queue, name)
                return name, account['cookies']

    @classmethod
    def delete_cookies(cls, name):
        cookies_con.hdel(cls.account_hash_set, name)
        if running_mode == 'quick':
            cookies_con.hdel(cls.cookie_host_maps, name)
        return True

    @classmethod
    def check_login_task(cls):
        if broker_con.llen(cls.account_queue) > 0:
            broker_con.delete(cls.account_queue)

    @classmethod
    def check_cookies_timeout(cls, cookies):
        if cookies is None:
            return True
        if isinstance(cookies, bytes):
            cookies = cookies.decode('utf-8')
        cookies = json.loads(cookies)
        login_time = datetime.datetime.fromtimestamp(cookies['loginTime'])
        if datetime.datetime.now() - login_time > datetime.timedelta(
                hours=cookie_expire_time):
            crawler_logger.warning('The account has been expired')
            return True
        return False

    # 目前未验证不登录的时候，同一IP不同Cookie是否和只有一个Cookie效果一样
    # 也没验证多个IP使用同一个Cookie的效果
    @classmethod
    def get_nologin_cookie(cls):
        while True:
            if cookies_con.llen(cls.without_login_cookies) == 0:
                raise NoCookieException('目前没有未登录的Cookie')
            pickled_cookies = cookies_con.lpop(cls.without_login_cookies).decode('utf-8')
            cookies_info = json.loads(pickled_cookies)
            gen_time = datetime.datetime.fromtimestamp(cookies_info['gen_time'])
            if (datetime.datetime.now() - gen_time) > datetime.timedelta(
                    days=nologin_cookie_expire_time):
                crawler_logger.warning('This no login cookie is expired')
            else:
                cookies_con.rpush(cls.without_login_cookies, pickled_cookies)
                return cookies_info['cookies']

    @classmethod
    def store_no_login_cookie(cls, cookies):
        # todo 加上添加时间
        pickled_cookies = json.dumps(
            {'cookies': cookies, 'gen_time': datetime.datetime.now().timestamp()})
        cookies_con.rpush(cls.without_login_cookies, pickled_cookies)


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
