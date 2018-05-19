import time

from celery import group

from ..db.redis_db import Cookies
from ..logger import crawler_logger
from ..login import (
    get_session, get_cookies)
from ..db.dao import LoginInfoOper
from .workers import app


# TODO: consider whether to use haipproxy in this project
# TODO: 1.gen cookies from different (proxy)ips
# TODO: 2.use different proxies with the cookies gened above
@app.task
def gen_cookies():
    """gen cookies with different ips"""
    cookies = get_cookies()
    crawler_logger.info('get cookies for no login successfully')
    Cookies.store_no_login_cookie(cookies)


@app.task
def do_login(name, password):
    get_session(name, password)
    time.sleep(10)


# There should be login interval, if too many accounts login
# at the same time from the same ip, all the accounts may be banned
# by weibo's anti-cheating system
@app.task
def execute_login_task():
    infos = LoginInfoOper.get_login_info()
    if not infos:
        crawler_logger.warning("The spider can't get account from db, "
                               "perhaps all your accounts are baned")
        return
    # Clear all stacked login tasks before each time for login
    Cookies.check_login_task()
    crawler_logger.info('The login task is starting...')
    caller = group(do_login.s(info.name, info.password)
                   for info in infos)
    caller()
