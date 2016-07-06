# 保存全局变量
login_name = '15708437303'
login_password = 'rookiefly'

host = '202.115.44.140'
port = '1521'
user = 'dangban'
password = '85418825'
dbname = 'ntci'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 '
                  'Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive'
}
max_len = 5   # 批量插入用户数据
time_out = 200   # 设置抓取和存储一个用户资料超时时间
limit = 3 # 批量插入的最大数据量
count = 0 # 计数器，每次抓取一个url则进行一次计数
