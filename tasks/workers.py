# coding:utf-8
import os
from datetime import timedelta
from celery import Celery
from kombu import Exchange, Queue
from config.conf import get_backend, get_brocker
from celery import platforms

# 允许celery以root身份启动
platforms.C_FORCE_ROOT = True

worker_log_path = os.path.join(os.path.dirname(os.path.dirname(__file__))+'/logs', 'celery.log')
beat_log_path = os.path.join(os.path.dirname(os.path.dirname(__file__))+'/logs', 'beat.log')

# include的作用就是注册服务化函数
app = Celery('weibo_task', include=['tasks.login', 'tasks.user'], broker=get_brocker(),
             backend=get_backend())


app.conf.update(
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=True,
    CELERYD_LOG_FILE=worker_log_path,
    CELERYBEAT_LOG_FILE=beat_log_path,
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERYBEAT_SCHEDULE={
        'user_task': {
            'task': 'tasks.user.excute_user_task',
            'schedule': timedelta(minutes=3),
            'options': {'queue': 'user_crawler', 'routing_key': 'for_user_info'}
        },
        'login_task': {
            'task': 'tasks.login.excute_login_task',
            'schedule': timedelta(hours=10),
            'options': {'queue': 'fans_followers', 'routing_key': 'for_fans_follwers'}
        },
    },
    CELERY_QUEUES=(
        Queue('login_queue', exchange=Exchange('login', type='direct'), routing_key='for_login'),
        Queue('user_crawler', exchange=Exchange('user_info', type='direct'), routing_key='for_user_info'),
        Queue('fans_followers', exchange=Exchange('fans_followers', type='direct'), routing_key='for_fans_followers')
    )
)


