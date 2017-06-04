# coding:utf-8
import time

from db.redis_db import Cookies
from logger import log
from wblogin import login
from db import login_info
from tasks.workers import app


@app.task(ignore_result=True)
def login_task(name, password):
    login.get_session(name, password)


def batch_login():
    """
    通过本地调用相关账号进行登录，该方法可能会有用
    """
    infos = login_info.get_login_info()
    for info in infos:
        login_task(info.name, info.password, info.need_verify)
        time.sleep(10)


# worker设置并发数为1，所以可以通过sleep()限制不同账号登录速度，账号登录速度过快，ip会被微博系统设定为异常ip
@app.task(ignore_result=True)
def excute_login_task():
    infos = login_info.get_login_info()
    # 每次登陆前清楚所有堆积的登录任务
    Cookies.check_login_task()
    log.crawler.info('本轮模拟登陆开始')
    for info in infos:
        app.send_task('tasks.login.login_task', args=(info.name, info.password), queue='login_queue',
                      routing_key='for_login')
        time.sleep(10)

