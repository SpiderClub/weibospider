# coding:utf-8
import time
from logger import log
from wblogin import login
from db import login_info
from tasks.workers import app


@app.task(ignore_result=True)
def login_task(name, password):
    login.get_session(name, password)


# worker设置并发数为1，所以可以通过sleep()限制不同账号登录速度
@app.task(ignore_result=True)
def excute_login_task():
    infos = login_info.get_login_info()
    log.crawler.info('本轮模拟登陆开始')
    for info in infos:
        app.send_task('tasks.login.login_task', args=(info.name, info.password), queue='login_queue',
                      routing_key='for_login')
        time.sleep(10)



