# coding:utf-8

################################
# spider settings              #
################################

# request intervals
min_crawl_interval = 10  # min interval of http request
max_crawl_interval = 20  # max interval of http request
request_time_out = 200   # timeout for crawling and storing user info
excp_interval = 5 * 60   # time for sleeping when crawling raises exceptions
max_retries = 3          # retries for crawling

# request pages
max_search_page = 50    # max search page for crawling
max_home_page = 50      # max user home page for crawling
max_comment_page = float('+inf')   # max comment page for crawling, default is total pages
max_repost_page = float('+inf')    # max repost page for crawling, default is total pages
max_dialogue_page = float('+inf')  # max dialogue page for crawling, default is total pages

# You should set the args below if you login from unnormal place
# register and buy recaptcha recognition
yundama_username = 'xxxxx'  # account for yundama
yundama_passwd = 'xxxx'  # password for yundama

# logs settings
log_dir = 'logs'
log_name = 'weibo.log'


###################################
# crawling strategy settings      #
###################################
# only crawl weibo after and affect to home crawler, default is all
time_after = '1970-01-01 00:00:00'

# The value of running_mode can be normal or quick.
# In normal mode, it will be more stable, while in quick mode, the crawling speed will
# be much faster, and the weibo account almostly will be banned
# see https://github.com/SpiderClub/weibospider/wiki/分布式微博爬虫的普通模式与极速模式 for details
running_mode = 'normal'
# The value of crawling mode can be accurate or normal
# In normal mode, the spider won't crawl the weibo content of "展开全文" when execute home crawl tasks or search crawl
# tasks, so the speed will be much quicker.
# In accurate mode,the spider will crawl the info of "展开全文",which will be slower, but more details will be given.
crawling_mode = 'normal'

# each cookie can be shared on multi servers
# if you choose quick mode, your cookie will be used util it's banned
share_host_count = 5
# the expire time(hours) of each weibo cookies
cookie_expire_time = 23
# the expire time(days) of each no login cookies
nologin_cookie_expire_time = 15

# if you want to download images,set the value below to 1,else 0
images_allow = 1
# the default image path is '${user.home}/weibospider/images'
# if you want to change another directory for download image, just set the path below
images_path = ''

# the value can be large or thumbnail
image_type = 'large'

######################################
# mysql database settings            #
######################################
db_host = '127.0.0.1'
db_port = '3306'
db_user = 'root'
db_pass = '123456'
db_name = 'weibo'
db_type = 'mysql'

#######################################
# redis settings                      #
#######################################
redis_host = '127.0.0.1'
redis_port = 6379
redis_pass = ''
cookies = 1  # store and fetch cookies
urls = 2  # the crawled urls and crawling result(failure or success)
broker = 5  # broker for celery
backend = 6  # backed for celery
id_name = 8  # user id and names，for repost info analysis. Could be safely deleted after repost tasks
# expire_time (hours) for redis db2, if they are useless to you, you can set the value smaller
data_expire_time = 48
# redis sentinel for ha,default the redis server is single
# sentinel: [('2.2.2.2',26379), ('3.3.3.3',26379))]
sentinel = ''
master = ''  # redis sentinel master name, if you don't need it, just set master: ''
socket_timeout = 5  # sockt timeout for redis sentinel, if you don't need it, just set master: ''

###############################
# warning by email            #
###############################
# notice:your email must open smtp & pop3 service
email_server = 'smtp.sina.com'
email_port = 587
email_from = 'xxx@sina.com'  # sendingemailaccount
email_password = 'xxxx'  # youremailpasswd
email_to = 'xxx@139.com'  # bind 139 email,so your phone will receive the warning message
subject = 'Warning Of Weibo Spider'
warning_info = 'Please find out the reason why the spider stops working'


##############################
# mornitor and bug trace     #
##############################

# error tracking
# for more information about this section see:
# https://sentry.io
# sentry url conbined by: http://sentry_token@sentry_host:sentry_port/sentry_uri
use_sentry = False
sentry_dsn = ''

# prometheus monitor
# for more information about this section see:
# https://prometheus.io/
use_prometheus = False
exporter_host = '0.0.0.0'
exporter_port = 8000
