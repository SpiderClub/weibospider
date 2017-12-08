import time

from celery import group

from db.redis_db import Cookies
from logger import crawler
from login import (
    get_session, get_cookies)
from db.dao import LoginInfoOper
from .workers import app


@app.task
def gen_cookies():
    crawler.info('Gen cookies from each host')


@app.task
def login_task(name, password):
    get_session(name, password)
    time.sleep(10)


# There should be login interval, if too many accounts login at the same time from the same ip, all the
# accounts can be banned by weibo's anti-cheating system
@app.task
def execute_login_task():
    infos = LoginInfoOper.get_login_info()
    if not infos:
        crawler.warning("The spider can't get account from db, "
                        "perhaps all your accounts are baned")
        return

    # Clear all stacked login tasks before each time for login
    Cookies.check_login_task()
    crawler.info('The login task is starting...')
    caller = group(login_task.s(info.name, info.password) for info in infos)
    caller.delay()
    # for info in infos:
    #     app.send_task('tasks.login.login_task', args=(info.name, info.password), queue='login_queue',
    #                   routing_key='for_login')
    #     time.sleep(10)

