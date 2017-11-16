import os

from yaml import load


__all__ = [
    'db_args', 'email_args', 'redis_args',
    'crawl_args', 'chapcha_args', 'get_broker_and_backend'
]


config_path = os.path.join(os.path.dirname(__file__), 'spider.yaml')


with open(config_path, encoding='utf-8') as f:
    cont = f.read()

cf = load(cont)


db_args = cf.get('db')
email_args = cf.get('email')
redis_args = cf.get('redis')
crawl_args = cf.get('spider')
chapcha_args = cf.get('captcha')


def get_broker_and_backend():
    redis_info = cf.get('redis')
    password = redis_info.get('password')
    sentinel_args = redis_info.get('sentinel', '')
    db = redis_info.get('broker', 5)
    if sentinel_args:
        broker_url = ";".join('sentinel://:{}@{}:{}/{}'.format(password, sentinel['host'], sentinel['port'], db) for
                              sentinel in sentinel_args)
        return broker_url
    else:
        host = redis_info.get('host')
        port = redis_info.get('port')
        backend_db = redis_info.get('backend', 6)
        broker_url = 'redis://:{}@{}:{}/{}'.format(password, host, port, db)
        backend_url = 'redis://:{}@{}:{}/{}'.format(password, host, port, backend_db)
        return broker_url, backend_url






