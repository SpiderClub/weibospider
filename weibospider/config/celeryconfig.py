TIMEZONE_FIXER = 8 * 60 * 60


class CeleryConfig:
    # celery4的timezone有问题，目前只能硬编码
    enable_utc = False
    task_ignore_result = True
    worker_prefetch_multiplier = 2
    # timeout for celery worker to execute a task
    # task_soft_time_limit = 5 * 60 * 60

    timezone = 'Asia/Shanghai'
    accept_content = ['json']
    task_serializer = 'json'
    result_serializer = 'json'
    # 可见性超时需要设置的比eta的时间长，
    # 否则celery会把相同任务发送给别的worker执行
    broker_transport_options = {'visibility_timeout': 43200 * 2}
    # app.conf.task_always_eager = True

    task_queues = {
        'login': {
            'exchange': 'login',
            'exchange_type': 'topic',
            'routing_key': 'login.*'
        },
        'gen_cookies': {
            'exchange': 'gen_cookies',
            'exchange_type': 'fanout'
        },

        'search': {
            'exchange': 'search',
            'exchange_type': 'topic',
            'routing_key': 'search.*'
        },

        'user': {
            'exchange': 'user',
            'exchange_type': 'topic',
            'routing_key': 'user.*'
        },

        'repost': {
            'exchange': 'repost',
            'exchange_type': 'topic',
            'routing_key': 'repost.*'
        },

        'comment': {
            'exchange': 'comment',
            'exchange_type': 'topic',
            'routing_key': 'comment.*'
        },

        'download': {
            'exchange': 'download',
            'exchange_type': 'topic',
            'routing_key': 'download.*'
        },

        'home': {
            'exchange': 'home',
            'exchange_type': 'topic',
            'routing_key': 'home.*'
        },

        'praise': {
            'exchange': 'praise',
            'exchange_type': 'topic',
            'routing_key': 'praise.*'
        },

        'dialogue': {
            'exchange': 'dialogue',
            'exchange_type': 'topic',
            'routing_key': 'dialogue.*'
        },
    }

    task_routes = {
        'tasks.login.execute_login_task': {
            'queue': 'login',
            'routing_key': 'login.all'
        },
        'tasks.login.do_login': {
            'queue': 'login',
            'routing_key': 'login.each'
        },
        'tasks.login.gen_cookies': {
            'queue': 'gen_cookies',
            'routing_key': 'gen_cookies'
        },

        'tasks.search.execute_search_task': {
            'queue': 'search',
            'routing_key': 'search.all',
        },
        'tasks.search.search_keyword': {
            'queue': 'search',
            'routing_key': 'search.each',
        },

        'tasks.user.execute_user_task': {
            'queue': 'user',
            'routing_key': 'user.profiles',
        },
        'tasks.user.crawl_user_info': {
            'queue': 'user',
            'routing_key': 'user.profile',
        },
        'tasks.user.execute_relation_task': {
            'queue': 'user',
            'routing_key': 'user.relations',
        },
        'tasks.user.crawl_followers_fans': {
            'queue': 'user',
            'routing_key': 'user.relation',
        },

        'tasks.repost.execute_repost_task': {
            'queue': 'repost',
            'routing_key': 'repost.all',
        },
        'tasks.repost.crawl_repost_page': {
            'queue': 'repost',
            'routing_key': 'repost.each',
        },

        'tasks.comment.execute_comment_task': {
            'queue': 'comment',
            'routing_key': 'comment.all'
        },

        'tasks.comment.crawl_comment_page': {
            'queue': 'comment',
            'routing_key': 'comment.page_num'
        },

        'tasks.comment.crawl_comment_by_page': {
            'queue': 'comment',
            'routing_key': 'comment.each'
        },

        'tasks.downloader.execute_download_task': {
            'queue': 'download',
            'routing_key': 'download.all'
        },
        'tasks.downloader.download_img': {
            'queue': 'download',
            'routing_key': 'download.each'
        },

        'tasks.home.execute_home_task': {
            'queue': 'download',
            'routing_key': 'home.all'
        },
        'tasks.home.crawl_weibo_datas': {
            'queue': 'download',
            'routing_key': 'home.page_num'
        },
        'tasks.home.crawl_ajax_page': {
            'queue': 'download',
            'routing_key': 'home.each'
        },

        'tasks.praise.execute_praise_task': {
            'queue': 'praise',
            'routing_key': 'praise.all'
        },
        'tasks.praise.crawl_praise_page': {
            'queue': 'praise',
            'routing_key': 'praise.page_num'
        },
        'tasks.praise.crawl_praise_by_page': {
            'queue': 'praise',
            'routing_key': 'praise.each'
        },

        'tasks.dialogue.execute_dialogue_task': {
            'queue': 'dialogue',
            'routing_key': 'dialogue.all'
        },
        'tasks.dialogue.crawl_dialogue': {
            'queue': 'dialogue',
            'routing_key': 'dialogue.page_num'
        },
        'tasks.dialogue.crawl_dialogue_by_comment_page': {
            'queue': 'dialogue',
            'routing_key': 'dialogue.each'
        },
    }

    # 根据用户自己的场景设置定时周期
    beat_schedule = {
        'login': {
            'task': 'tasks.login.execute_login_task',
            'schedule': 60 * 60 * 10.0,
        },
        'gen_cookies': {
            'task': 'tasks.login.do_gen_cookie',
            'schedule': 60 * 60 * 20.0,
        },
        'search': {
            'task': 'tasks.search.execute_search_task',
            'schedule': 60 * 60 * 2.0,
        },
        'user': {
            'task': 'tasks.user.execute_user_task',
            'schedule': 60 * 1.0,
            # TODO 查阅超时的正确用法
            # 上次任务没执行完，则直接设置为超时(超时时间和调度间隔一致)
            'options': {
                'expires': 60 * 60 * 10.0 + TIMEZONE_FIXER
            }
        },
        'relation': {
            'task': 'tasks.user.execute_relation_task',
            'schedule': 60 * 60 * 5.0,
        },
        'repost': {
            'task': 'tasks.repost.execute_repost_task',
            'schedule': 60 * 60 * 2.0,
        },
        'download': {
            'task': 'tasks.downloader.execute_download_task',
            'schedule': 60 * 60 * 2.0,
        },
        'comment': {
            'task': 'tasks.comment.execute_comment_task',
            'schedule': 60 * 60 * 2.0,
        },
        'home': {
            'task': 'tasks.home.execute_home_task',
            'schedule': 60 * 60 * 2.0,
        },
        'praise': {
            'task': 'tasks.praise.execute_praise_task',
            'schedule': 60 * 60 * 2.0,
        },
        'dialogue': {
            'task': 'tasks.praise.execute_praise_task',
            'schedule': 60 * 60 * 2.0,
        },
    }



