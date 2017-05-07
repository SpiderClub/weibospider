# coding:utf-8
from datetime import timedelta
from celery import Celery
from kombu import Exchange, Queue
from config.conf import get_backend, get_brocker


# include的作用就是注册服务化函数
app = Celery('weibo_task', include=['tasks.login', 'tasks.user'], broker=get_brocker(),
             backend=get_backend())


app.conf.beat_schedule = {
    'user_task': {
        'task': 'tasks.user.excute_user_task',
        'schedule': timedelta(minutes=3),
    },
    'login_task': {
        'task': 'tasks.login.excute_login_task',
        'schedule': timedelta(hours=10),
    },
    # 'repost_task': {
    #     'task': 'tasks.repost.excute_repost_task',
    #     'schedule': 60*60*2.0,
    # },
}


app.conf.update(
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=True,
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_QUEUES=(
        Queue('login_queue', exchange=Exchange('login', type='direct'), routing_key='for_login'),
        Queue('user_crawler', exchange=Exchange('user_info', type='direct'), routing_key='for_user_info'),
        Queue('fans_followers', exchange=Exchange('fans_followers', type='direct'), routing_key='for_fans_followers')
    )
)


