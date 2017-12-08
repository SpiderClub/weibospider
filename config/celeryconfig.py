from datetime import timedelta

from kombu import (
    Exchange, Queue)


timezone = 'Asia/Shanghai'
enable_utc = True
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']


task_queues = {
    'login': {
        'exchange': 'login',
        'routing_key': 'login'
    },
    'gen_cookies': {
        'exchange': 'gen_cookies',
        'exchange_type': 'fanout'
    },
    'user': {
        'exchange': 'user',
        'routing_key': 'user'
    },
    'search': {
        'exchange': 'search',
        'routing_key': 'search'
    },
    'home': {
        'exchange': 'home',
        'routing_key': 'home'
    },
    'comment': {
        'exchange': 'comment',
        'routing_key': 'comment'
    },
    'repost': {
        'exchange': 'repost',
        'routing_key': 'repost'
    },
    'download': {
        'exchange': 'download',
        'routing_key': 'download'
    }
}

task_routes = {
    'tasks.login.execute_login_task': {
        'queue': 'login',
        'routing_key': 'login.all'
    },
    'tasks.login.login_task': {
        'queue': 'login',
        'routing_key': 'login.each'
    },
    'tasks.login.gen_cookies': {
        'queue': 'gen_cookies',
        'routing_key': 'gen_cookies'
    }
}

app.conf.update(
    CELERYBEAT_SCHEDULE={
        'login_task': {
            'task': 'tasks.login.execute_login_task',
            'schedule': timedelta(hours=20),
            'options': {'queue': 'login_queue', 'routing_key': 'for_login'}
        },
        'user_task': {
            'task': 'tasks.user.execute_user_task',
            'schedule': timedelta(minutes=3),
            'options': {'queue': 'user_crawler', 'routing_key': 'for_user_info'}
        },
        'search_task': {
            'task': 'tasks.search.execute_search_task',
            'schedule': timedelta(hours=2),
            'options': {'queue': 'search_crawler', 'routing_key': 'for_search_info'}
        },
        'home_task': {
            'task': 'tasks.home.execute_home_task',
            'schedule': timedelta(hours=10),
            'options': {'queue': 'home_crawler', 'routing_key': 'home_info'}
        },
        'comment_task': {
            'task': 'tasks.comment.execute_comment_task',
            'schedule': timedelta(hours=10),
            'options': {'queue': 'comment_crawler', 'routing_key': 'comment_info'}
        },
        'repost_task': {
            'task': 'tasks.repost.execute_repost_task',
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

        Queue('download_queue', exchange=Exchange('download_queue', type='direct'), routing_key='for_download'),
    ),

)