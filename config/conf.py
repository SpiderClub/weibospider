# coding:utf-8
import os
import random
from yaml import load

config_path = os.path.join(os.path.dirname(__file__), 'spider.yaml')


with open(config_path, encoding='utf-8') as f:
    cont = f.read()

cf = load(cont)


def get_db_args():
    return cf.get('db')


def get_redis_args():
    return cf.get('redis')


def get_timeout():
    return cf.get('time_out')


def get_crawl_interal():
    interal = random.randint(cf.get('min_crawl_interal'), cf.get('max_crawl_interal'))
    return interal


def get_excp_interal():
    return cf.get('excp_interal')


def get_max_repost_page():
    return cf.get('max_repost_page')


def get_max_search_page():
    return cf.get('max_search_page')


def get_max_home_page():
    return cf.get('max_home_page')


def get_max_comment_page():
    return cf.get('max_comment_page')


def get_max_retries():
    return cf.get('max_retries')


def get_broker_or_backend(types):
    """
    :param types: 类型，1表示中间人，2表示消息后端
    :return: 
    """
    redis_info = cf.get('redis')
    host = redis_info.get('host')
    port = redis_info.get('port')
    password = redis_info.get('password')

    if types == 1:
        db = redis_info.get('broker')
    else:
        db = redis_info.get('backend')
    url = 'redis://:{}@{}:{}/{}'.format(password, host, port, db)

    return url


def get_code_username():
    return cf.get('yundama_username')


def get_code_password():
    return cf.get('yundama_passwd')
