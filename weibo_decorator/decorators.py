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
            print(e)
            for i in args:
                print(i)
            print(format_tb(e.__traceback__)[0])
            logging.error('插入失败，具体错误信息为{e},堆栈为{stack}'.format(e=e, stack=format_tb(e.__traceback__)[0]))
            print('插入失败')
            pass
    return save_process


# 用于超时设置
def timeout_decorator(func):
    @wraps(func)
    def time_limit(user_id, session, headers):
        try:
            return func(user_id, session, headers)
        except Exception as e:
            print('抓取{uid}超时'.format(uid=user_id))
            print(format_tb(e.__traceback__)[0])
            logging.error('抓取失败，具体错误信息为{e},堆栈为{stack}'.format(e=e, stack=format_tb(e.__traceback__)[0]))
            return None
    return time_limit




