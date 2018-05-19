from celery import (
    Celery, platforms)

from ..config.celeryconfig import CeleryConfig
from ..config import (
    redis_pass, redis_host,
    redis_port, master,
    sentinel as sentinel_args, broker as broker_db,
    backend as backend_db
)


tasks = [
    'tasks.login', 'tasks.search',
    'tasks.user', 'tasks.repost',
    'tasks.praise', 'tasks.home',
    'tasks.downloader', 'tasks.comment',
    'tasks.dialogue'
]

platforms.C_FORCE_ROOT = True


def _get_broker_and_backend():
    if sentinel_args and master:
        broker_url = ";".join('sentinel://:{}@{}:{}/{}'.format(
            redis_pass, sentinel[0], sentinel[1], broker_db) for
                              sentinel in sentinel_args)
        return broker_url
    else:
        broker_url = 'redis://:{}@{}:{}/{}'.format(
            redis_pass, redis_host, redis_port, broker_db)
        backend_url = 'redis://:{}@{}:{}/{}'.format(
            redis_pass, redis_host, redis_port, backend_db)
        return broker_url, backend_url


broker_and_backend = _get_broker_and_backend()

if isinstance(broker_and_backend, tuple):
    broker, backend = broker_and_backend
    app = Celery('weibo_spider',  include=tasks, broker=broker, backend=backend)
else:
    app = Celery('weibo_spider', include=tasks, broker=broker_and_backend)
    app.conf.update(
        BROKER_TRANSPORT_OPTIONS={'master_name': master},
    )

app.config_from_object(CeleryConfig)