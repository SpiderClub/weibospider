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

tasks = ['tasks.login', 'tasks.user', 'tasks.search', 'tasks.home', 'tasks.comment']
# include的作用就是注册服务化函数
app = Celery('weibo_task', include=tasks, broker=get_brocker(), backend=get_backend())

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
        'search_task': {
            'task': 'tasks.search.excute_search_task',
            'schedule': timedelta(hours=2),
            'options': {'queue': 'search_crawler', 'routing_key': 'for_search_info'}
        },
        'login_task': {
            'task': 'tasks.login.excute_login_task',
            'schedule': timedelta(hours=10),
            'options': {'queue': 'login_queue', 'routing_key': 'for_login'}
        },
        'home_task': {
            'task': 'tasks.home.excute_home_task',
            'schedule': timedelta(hours=10),
            'options': {'queue': 'home_crawler', 'routing_key': 'home_info'}
        },
        'comment_task': {
            'task': 'tasks.home.excute_comment_task',
            'schedule': timedelta(hours=10),
            'options': {'queue': 'home_crawler', 'routing_key': 'home_info'}
        }
    },
    CELERY_QUEUES=(
        Queue('login_queue', exchange=Exchange('login', type='direct'), routing_key='for_login'),
        Queue('user_crawler', exchange=Exchange('user_info', type='direct'), routing_key='for_user_info'),
        Queue('search_crawler', exchange=Exchange('search_info', type='direct'), routing_key='for_search_info'),
        Queue('fans_followers', exchange=Exchange('fans_followers', type='direct'), routing_key='for_fans_followers'),
        Queue('home_crawler', exchange=Exchange('home_crawler', type='direct'), routing_key='home_info'),
        Queue('ajax_home_crawler', exchange=Exchange('ajax_home_crawler', type='direct'), routing_key='ajax_home_info'),
        Queue('comment_crawler', exchange=Exchange('comment_crawler', type='direct'), routing_key='comment_info')
    )
)


