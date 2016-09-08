# 保存全局变量
login_name = 'yourname'
login_password = 'yourpassword'

# db_type:oracle
host = 'dbip'
port = 'dbport'
user = 'dbuser'
password = 'dbpassword'
dbname = 'dbname'
redis_host = 'localhost'
redis_port = 6379
redis_db = 0
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 '
                  'Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive'
}
max_len = 5   # 批量插入用户数据
time_out = 200   # 设置抓取和存储一个用户资料超时时间
limit = 3  # 批量插入的最大数据量
count = 0  # 计数器，每次抓取一个url则进行一次计数
page_max = 30  # 转发信息最多抓取多少页
