from django.apps import AppConfig


class WeiboConfig(AppConfig):
    name = 'weibo_config'
    verbose_name = '微博配置'


class WeiboDataConfig(AppConfig):
    name = 'weibo_data'
    verbose_name = '微博数据'