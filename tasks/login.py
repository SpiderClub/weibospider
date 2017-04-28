import time
from celery import Celery
from config.get_config import get_backend, get_brocker
from wblogin import login
from db import login_info


# todo 设置任务路由
app = Celery('weibo_task', include=['tasks.login'], broker=get_brocker(), backend=get_backend())
app.conf.update(
    timezone='Asia/Shanghai',
    CELERY_ENABLE_UTC=True,
)

# 20小时自动登录一次
app.conf.beat_schedule = {
    'login_task': {
        'task': 'tasks.login.excute_login_task',
        'schedule': 60*60*20.0,
    },
}


@app.task
def login_task(name, password):
    login.get_session(name, password)


# 注意设置 --conccurency=1，并让两次登录有一些间隔
@app.task
def excute_login_task():
    infos = login_info.get_login_info()
    for info in infos:
        app.send_task('tasks.login.login_task', args=(info['name'], info['password']))
        time.sleep(10)


