# -*-coding:utf-8 -*-
import logging, traceback
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
    def time_limit(url, session, *k):
        try:
            return func(url, session, *k)
        except Exception as e:
            print('抓取{url}超时'.format(url=url))
            logging.error('抓取{url}失败，具体错误信息为{e},堆栈为{stack}'.format(url=url, e=e,
                                                                   stack=format_tb(e.__traceback__)[0]))
            return None
    return time_limit


# 用于捕捉页面解析的异常, 2表示返回空列表，1表示返回空字符串，0表示返回数字0, 3表示返回True,4表示返回{},5返回None
def parse_decorator(return_type):
    def page_parse(func):
        @wraps(func)
        def handle_error(*keys):
            try:
                return func(*keys)
            except Exception as e:
                print(e)
                with open('log.txt', 'a') as f:
                    traceback.print_exc(file=f)
                if return_type == 5:
                    return None
                elif return_type == 4:
                    return {}
                elif return_type == 3:
                    return False
                elif return_type == 2:
                    return []
                elif return_type == 1:
                    return ''
                else:
                    return 0
        return handle_error
    return page_parse
