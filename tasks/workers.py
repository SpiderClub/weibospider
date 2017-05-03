from celery import Celery
from config.conf import get_backend, get_brocker


# todo 为不同任务设置任务路由
# include的作用就是注册服务化函数
app = Celery('weibo_task', include=['tasks.login', 'tasks.repost', 'tasks.user'], broker=get_brocker(), backend=get_backend())
app.conf.update(
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=True,
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
)


app.conf.CELERYBEAT_SCHEDULE = {
    'login_task': {
        'task': 'tasks.login.excute_login_task',
        'schedule': 60*60*20.0,
    },
    'repost_task': {
        'task': 'tasks.repost.excute_repost_task',
        'schedule': 60*60*2.0,
    },
    'user_task': {
        'task': 'tasks.user.excute_user_task',
        'schedule': 60.0*3
    }
}