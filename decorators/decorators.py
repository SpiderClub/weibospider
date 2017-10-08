import time
import collections
from functools import wraps, partial
from traceback import format_tb

from db.basic import db_session
from logger import (
    parser, crawler, storage, other)
from utils import KThread
from exceptions import Timeout


def timeout_decorator(func):
    @wraps(func)
    def time_limit(*args, **kargs):
        try:
            return func(*args, **kargs)
        except Exception as e:
            crawler.error('failed to crawl {url}，here are details:{e}, stack is {stack}'.format(url=args[0], e=e,
                                                                                                stack=format_tb
                                                                                                (e.__traceback__)[0]))
            return ''

    return time_limit


def db_commit_decorator(func):
    @wraps(func)
    def session_commit(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            storage.error('DB operation error，here are details:{}'.format(e))
            db_session.rollback()
    return session_commit


def parse_decorator(return_value):
    """
    :param return_value: catch exceptions when parsing pages, return the default value
    :return: the default value is whatever you want, usually it's 0,'',[],False,{} or None
    """
    def page_parse(func):
        @wraps(func)
        def handle_error(*keys):
            try:
                return func(*keys)
            except Exception as e:
                parser.error('Failed to parse the page, {} is raised, here are details:{}'.format(
                    e, format_tb(e.__traceback__)[0]
                ))
                return return_value

        return handle_error

    return page_parse


# it can be blocked when crawling pages even if we set timeout=out_time in requests.get()
def timeout(seconds):
    def crwal_decorator(func):
        def _new_func(oldfunc, result, oldfunc_args, oldfunc_kwargs):
            result.append(oldfunc(*oldfunc_args, **oldfunc_kwargs))

        @wraps(func)
        def wrapper(*args, **kwargs):
            result = []
            # create new args for _new_func, because we want to get the func return val to result list
            new_kwargs = {
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
                    raise Timeout('request timeout')
                finally:
                    return ''
            else:
                if result:
                    return result[0]
                else:
                    return ''
        return wrapper

    return crwal_decorator


def retry(times=-1, delay=0, exceptions=Exception, logger=other):
    """
    inspired by https://github.com/invl/retry
    :param times: retry times
    :param delay: internals between each retry
    :param exceptions: exceptions may raise in retry
    :param logger: log for retry
    :return: func result or None
    """
    def _inter_retry(caller, retry_time, retry_delay, es):
        while retry_time:
            try:
                return caller()
            except es as e:
                retry_time -= 1
                if not retry_time:
                    logger.error("max tries for {} times, {} is raised, details: func name is {}, func args are {}".
                                 format(times, e, caller.func.__name__, (caller.args, caller.keywords)))
                    raise
                time.sleep(retry_delay)

    def retry_oper(func):
        @wraps(func)
        def _wraps(*args, **kwargs):
            return _inter_retry(partial(func, *args, **kwargs), times, delay, exceptions)
        return _wraps
    return retry_oper
