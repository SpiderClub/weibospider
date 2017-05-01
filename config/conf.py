import os
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
    return cf.get('crawl_interal')


def get_excp_interal():
    return cf.get('excp_interal')


def get_max_page():
    return cf.get('max_page')


def get_max_retries():
    return cf.get('max_retries')


def get_brocker():
    return cf.get('brocker')


def get_backend():
    return cf.get('backend')