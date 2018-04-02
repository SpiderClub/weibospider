# import os
#
# from yaml import load
#
# <<<<<<< HEAD
#
# __all__ = [
#     'db_args', 'email_args', 'redis_args',
#     'crawl_args', 'chapcha_args', 'get_broker_and_backend'
# ]
#
#
# =======
# >>>>>>> 4dc13b2bfb06496cfd36572f2adf4c297f1315e1
# config_path = os.path.join(os.path.dirname(__file__), 'spider.yaml')
#
# with open(config_path, encoding='utf-8') as f:
#     cont = f.read()
#
# cf = load(cont)
#
#
# <<<<<<< HEAD
# db_args = cf.get('db')
# email_args = cf.get('email')
# redis_args = cf.get('redis')
# crawl_args = cf.get('spider')
# chapcha_args = cf.get('captcha')
# =======
# def get_db_args():
#     return cf.get('db')
#
#
# def get_redis_args():
#     return cf.get('redis')
#
#
# def get_timeout():
#     return cf.get('time_out')
#
#
# def get_crawl_interval():
#     interval = random.randint(cf.get('min_crawl_interval'), cf.get('max_crawl_interval'))
#     return interval
#
#
# def get_excp_interval():
#     return cf.get('excp_interval')
#
#
# def get_max_repost_page():
#     return cf.get('max_repost_page')
#
#
# def get_max_search_page():
#     return cf.get('max_search_page')
#
#
# def get_max_home_page():
#     return cf.get('max_home_page')
#
#
# def get_max_comment_page():
#     return cf.get('max_comment_page')
#
#
# def get_max_dialogue_page():
#     return cf.get('max_dialogue_page')
#
#
# def get_max_retries():
#     return cf.get('max_retries')
# >>>>>>> 4dc13b2bfb06496cfd36572f2adf4c297f1315e1
#
#
# def get_broker_and_backend():
#     redis_info = cf.get('redis')
#     password = redis_info.get('password')
#     sentinel_args = redis_info.get('sentinel', '')
#     db = redis_info.get('broker', 5)
#     if sentinel_args:
#         broker_url = ";".join('sentinel://:{}@{}:{}/{}'.format(password, sentinel['host'], sentinel['port'], db) for
#                               sentinel in sentinel_args)
#         return broker_url
#     else:
#         host = redis_info.get('host')
#         port = redis_info.get('port')
#         backend_db = redis_info.get('backend', 6)
#         broker_url = 'redis://:{}@{}:{}/{}'.format(password, host, port, db)
#         backend_url = 'redis://:{}@{}:{}/{}'.format(password, host, port, backend_db)
#         return broker_url, backend_url
#
#
#
#
#
#
# def get_time_after():
#     return cf.get('time_after')
#
# def get_samefollow_uid():
#     return cf.get('samefollow_uid')
