import time

from celery import group

from db.redis_db import Cookies
from logger import crawler_logger
from login import get_session
from db.dao import LoginInfoOper
from .workers import app


@app.task
def login_task(name, password):
    get_session(name, password)
    time.sleep(10)


# There should be login interval, if too many accounts login at the same time from the same ip, all the
# accounts can be banned by weibo's anti-cheating system
@app.task
def execute_login_task():
    infos = LoginInfoOper.get_login_info()
    # Clear all stacked login tasks before each time for login
    Cookies.check_login_task()
    crawler_logger.info('The login task is starting...')
    caller = group(login_task.s(info.name, info.password) for info in infos)
    caller.delay()


