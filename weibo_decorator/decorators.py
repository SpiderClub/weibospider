# -*-coding:utf-8 -*-
from functools import wraps
from traceback import format_tb
from utils.util_cls import Timeout, KThread
from logger.log import storage, parser, crawler


# 用于捕捉插入数据时的异常
def save_decorator(func):
    @wraps(func)
    def save_process(*args):
        try:
            func(*args)
        except Exception as e:
            for i in args:
                storage.error('未成功插入的对象属性:{i}'.format(i=i.__dict__))
            storage.error('插入失败，具体错误信息为{e},堆栈为{stack}'.format(e=e, stack=format_tb(e.__traceback__)[0]))
    return save_process


# 用于超时设置
def timeout_decorator(func):
    @wraps(func)
    def time_limit(url, session, *k):
        try:
            return func(url, session, *k)
        except Exception as e:
            crawler.error('抓取{url}失败，具体错误信息为{e},堆栈为{stack}'.format(url=url, e=e,
                                                                   stack=format_tb(e.__traceback__)[0]))
            return None
    return time_limit


# 用于捕捉页面解析的异常, 2表示返回[]，1表示返回空字符串，0表示返回数字0, 3表示返回True,4表示返回{},5返回None
def parse_decorator(return_type):
    def page_parse(func):
        @wraps(func)
        def handle_error(*keys):
            try:
                return func(*keys)
            except Exception as e:
                parser.error(e)

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


# 用于捕捉数据库操作时的异常
def dbtimeout_decorator(return_type):
    def connect_process(func):
        @wraps(func)
        def handle_error(*keys):
            try:
                return func(*keys)
            except Exception as e:
                storage.error(e)
                if return_type == 2:
                    return []
                elif return_type == 1:
                    return None
                else:
                    return False
        return handle_error
    return connect_process


# 即使在抓取的时候设置了超时函数，抓取函数还是可能会超时，这是对get_page超时的完善
def timeout(seconds):
    def crwal_decorator(func):
        def _new_func(oldfunc, result, oldfunc_args, oldfunc_kwargs):
            result.append(oldfunc(*oldfunc_args, **oldfunc_kwargs))

        def _(*args, **kwargs):
            result = []
            new_kwargs = {  # create new args for _new_func, because we want to get the func return val to result list
                'oldfunc': func,
                'result': result,
                'oldfunc_args': args,
                'oldfunc_kwargs': kwargs
            }

            thd = KThread(target=_new_func, args=(), kwargs=new_kwargs)
            thd.start()
            thd.join(seconds)
            alive = thd.isAlive()
            thd.kill()  # kill the child thread

            if alive:
                try:
                    raise Timeout('抓取函数运行超时')
                finally:
                    return ''
            else:
                return result[0]

        _.__name__ = func.__name__

        _.__doc__ = func.__doc__
        return _

    return crwal_decorator