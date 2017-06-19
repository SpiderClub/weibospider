# coding:utf-8
import datetime
import json

import redis
from config.conf import get_redis_args, get_share_host_count
from logger.log import crawler
import socket

redis_args = get_redis_args()
share_host_count = get_share_host_count()


# todo 考虑并发条件下的cookie存取
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
        cls.push_in_queue(name)

    @classmethod
    def push_in_queue(cls, name):
        # 在节点数和任务执行较快的情况下，并不能保证队列中无重复名字。如果账号已在队列，则不重复存储
        for i in range(cls.rd_con.llen('account_queue')):
            tn = cls.rd_con.lindex('account_queue', i)
            if tn:
                if tn == name:
                    return
        cls.rd_con.rpush('account_queue', name)

    @classmethod
    def fetch_cookies(cls):
        # cookies记录被使用的主机数目，当超过上限，则将其放至队尾，未超过则获取并记录
        # todo 这里用hostname来标识不同主机其实是有小问题的，比如不同ip主机名可能相同
        hostname = socket.gethostname()
        # 如果redis中已有相关主机的cookie，则直接取出来
        my_cookies_name = cls.rd_con.hget('host', hostname)
        if my_cookies_name:
            my_cookies = cls.rd_con.hget('account', my_cookies_name)
            if not cls.check_cookies_timeout(my_cookies):  # 没有占用或cookies过期则取一个新的
                my_cookies = json.loads(my_cookies.decode('utf-8'))
                return my_cookies_name, my_cookies['cookies']
            else:
                cls.delete_cookies(my_cookies_name)

        # 如果没有或者过期，则从队列中阻塞获取一个新的cookies
        # 不阻塞在账户少的时候，可能会出现不同主机重复登陆的情况，阻塞之后，原来尝试登陆代码就无效了,需要的话可以设置超时解决
        # 另外阻塞的一个好处是，任务不会在账号出问题的时候被刷没了
        while True:
            # todo notify the users or retry login
            name = cls.rd_con.blpop('account_queue')[1].decode('utf-8')
            if name:
                j_account = cls.rd_con.hget('account', name)

                if cls.check_cookies_timeout(j_account):
                    cls.delete_cookies(name)
                    continue

                j_account = j_account.decode('utf-8')
                # account-host对应关系（一对多）
                hosts = cls.rd_con.hget('cookies_host', name)
                if not hosts:
                    hosts = dict()
                else:
                    hosts = hosts.decode('utf-8')
                    hosts = json.loads(hosts)
                hosts[hostname] = 1
                cls.rd_con.hset('cookies_host', name, json.dumps(hosts))

                # host-account对应关系（一对一）
                account = json.loads(j_account)
                cls.rd_con.hset('host', hostname, name)

                # 塞回头部，下次继续使用
                if len(hosts) < share_host_count:
                    cls.rd_con.lpush('account_queue', name)
                return name, account['cookies']

    @classmethod
    def delete_cookies(cls, name):
        cls.rd_con.hdel('account', name)
        cls.rd_con.hdel('cookies_host', name)
        return True

    @classmethod
    def check_login_task(cls):
        if cls.rd_con_broker.llen('login_queue') > 0:
            cls.rd_con_broker.delete('login_queue')

    @classmethod
    def fresh_login_queue(cls, num):

        for key in cls.rd_con.hkeys('account'):
            if cls.rd_con.llen('account_queue') > num:
                break  # 保持cookies池数量
            cls.push_in_queue(key)
        print('队列总包含{}个可使用cookies'.format(cls.rd_con.llen('account_queue')))

    @classmethod
    def check_cookies_timeout(cls, cookies):
        if cookies is None:
            return True
        if isinstance(cookies, bytes):
            cookies = cookies.decode('utf-8')
        cookies = json.loads(cookies)
        login_time = datetime.datetime.fromtimestamp(cookies['loginTime'])
        if datetime.datetime.now() - login_time > datetime.timedelta(hours=20):
            # 删除过期cookies
            crawler.warning('一个账号已过期')
            return True
        return False


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
