# coding:utf-8
import os
from datetime import timedelta
from celery import Celery
from kombu import Exchange, Queue
from config.conf import get_broker_or_backend
from celery import platforms

# 允许celery以root身份启动
platforms.C_FORCE_ROOT = True

worker_log_path = os.path.join(os.path.dirname(os.path.dirname(__file__))+'/logs', 'celery.log')
beat_log_path = os.path.join(os.path.dirname(os.path.dirname(__file__))+'/logs', 'beat.log')

tasks = ['tasks.login', 'tasks.user', 'tasks.search', 'tasks.home', 'tasks.comment', 'tasks.repost']

# include的作用就是注册服务化函数
app = Celery('weibo_task', include=tasks, broker=get_broker_or_backend(1), backend=get_broker_or_backend(2))

app.conf.update(
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=True,
    CELERYD_LOG_FILE=worker_log_path,
    CELERYBEAT_LOG_FILE=beat_log_path,
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERYBEAT_SCHEDULE={
        'login_task': {
            'task': 'tasks.login.excute_login_task',
            'schedule': timedelta(hours=20),
            'options': {'queue': 'login_queue', 'routing_key': 'for_login'}
        },
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
        'home_task': {
            'task': 'tasks.home.excute_home_task',
            'schedule': timedelta(hours=10),
            'options': {'queue': 'home_crawler', 'routing_key': 'home_info'}
        },
        'comment_task': {
            'task': 'tasks.comment.excute_comment_task',
            'schedule': timedelta(hours=10),
            'options': {'queue': 'comment_crawler', 'routing_key': 'comment_info'}
        },
        'repost_task': {
            'task': 'tasks.repost.excute_repost_task',
            'schedule': timedelta(hours=10),
            'options': {'queue': 'repost_crawler', 'routing_key': 'repost_info'}
        },
    },
    CELERY_QUEUES=(
        Queue('login_queue', exchange=Exchange('login_queue', type='direct'), routing_key='for_login'),

        Queue('user_crawler', exchange=Exchange('user_crawler', type='direct'), routing_key='for_user_info'),
        Queue('search_crawler', exchange=Exchange('search_crawler', type='direct'), routing_key='for_search_info'),
        Queue('fans_followers', exchange=Exchange('fans_followers', type='direct'), routing_key='for_fans_followers'),

        Queue('home_crawler', exchange=Exchange('home_crawler', type='direct'), routing_key='home_info'),
        Queue('ajax_home_crawler', exchange=Exchange('ajax_home_crawler', type='direct'), routing_key='ajax_home_info'),

        Queue('comment_crawler', exchange=Exchange('comment_crawler', type='direct'), routing_key='comment_info'),
        Queue('comment_page_crawler', exchange=Exchange('comment_page_crawler', type='direct'),
              routing_key='comment_page_info'),

        Queue('repost_crawler', exchange=Exchange('repost_crawler', type='direct'), routing_key='repost_info'),
        Queue('repost_page_crawler', exchange=Exchange('repost_page_crawler', type='direct'),
              routing_key='repost_page_info'),
    ),

)


