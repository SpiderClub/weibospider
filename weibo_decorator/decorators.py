# -*-coding:utf-8 -*-
import logging
from functools import wraps
from traceback import format_tb


# 用于捕捉插入数据时的异常
def save_decorator(func):
    @wraps(func)
    def save_process(*args):
        try:
            func(*args)
        except Exception as e:
            for i in args:
                logging.info('未成功插入的对象属性:{i}'.format(i=i))
            print(format_tb(e.__traceback__)[0])
            logging.error('插入失败，具体错误信息为{e},堆栈为{stack}'.format(e=e, stack=format_tb(e.__traceback__)[0]))
            print('插入失败')
            pass
    return save_process


# 用于超时设置
def timeout_decorator(func):
    @wraps(func)
    def time_limit(session, url, headers, verify):
        try:
            return func(session, url, headers, verify)
        except Exception as e:
            print('抓取{url}超时'.format(url=url))
            logging.error('抓取{url}失败，具体错误信息为{e},堆栈为{stack}'.format(url=url, e=e,
                                                                   stack=format_tb(e.__traceback__)[0]))
            return None
    return time_limit




