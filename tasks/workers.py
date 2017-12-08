from celery import (
    Celery, platforms)

from config import (
    redis_args,
    get_broker_and_backend
)


platforms.C_FORCE_ROOT = True

broker_and_backend = get_broker_and_backend()

tasks = [
    'tasks.login', 'tasks.user', 'tasks.search', 'tasks.home', 'tasks.comment',
    'tasks.repost', 'tasks.downloader'
]

if isinstance(broker_and_backend, tuple):
    broker, backend = broker_and_backend
    app = Celery('weibo_spider', include=tasks, broker=broker, backend=backend)
else:
    master = redis_args.get('master')
    app = Celery('weibo_spider', include=tasks, broker=broker_and_backend)
    app.conf.broker_transport_options = {'master_name': master}



