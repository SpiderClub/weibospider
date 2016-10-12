import configparser
import os

cf = configparser.ConfigParser()
config_path = os.path.join(os.getcwd(), 'config/spider.conf')
cf.read_file(open(config_path))


def get_oracle_args():
    return dict(cf.items('oracle_db'))


def get_redis_args():
    return dict(cf.items('redis_db'))


def get_weibo_args():
    return dict(cf.items('weibo_account'))

if __name__ == '__main__':
    print(dict(get_weibo_args()))
