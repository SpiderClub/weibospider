import os, random
from yaml import load

config_path = os.path.join(os.getcwd(), 'config/spider.yaml')

with open(config_path, encoding='utf-8') as f:
    cont = f.read()

cf = load(cont)


def get_db_args():
    return cf.get('db')


def get_redis_args():
    return cf.get('redis_db')


def get_weibo_args():
    acounts_info = cf.get('weibo_account')
    return random.choice(acounts_info).get('account')

if __name__ == '__main__':
    print(get_weibo_args())
