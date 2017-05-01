import redis
from config.conf import get_redis_args


redis_args = get_redis_args()
rd_con = redis.StrictRedis(host=redis_args.get('host'), port=redis_args.get('port'), db=redis_args.get('urls_db'))


# 存储已抓取url和相应结果
def store_crawl_url(url, result):
    rd_con.set(url, result)



