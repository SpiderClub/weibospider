# 关于该程序
## 目的
- 通过**PC端**抓取微博用户信息
- 通过指定话题搜索相关微博
- 通过指定微博ID分析它的具体扩散，生成扩散图
- 测试微博反爬虫机制


## 目前已完成工作
- 微博搜索、微博信息及用户信息解析模块


## TODO
- [x] 添加搜索接口，可以对某个指定话题进行搜索
- [x] 完成微博解析模块，用户解析模块和搜索解析模块
- [x] 判断账号是否正常登录，维护账号的可用性
- [x] 微博用户抓取
- [ ] 指定微博的传播分析及可视化展示
- [ ] 采用布隆过滤器去重网页
- [ ] 测试单机单账号访问阈值
- [ ] 测试单机多账号访问效果
- [ ] 改成分布式爬虫

## 配置和使用
- 安装相关依赖```pip install -r requirements.txt```
- 打开[配置文件](./config/spider.yaml)修改数据库相关配置
- 打开[sql文件](./config/sql/spider.sql)查看并使用建表语句
- 入口文件 
 - [search.py](./search_run.py):微博搜索程序:通过搜索接口搜索相关话题微博
 - [user_crawler.py](./user_crawler.py):微博用户抓取程序，通过指定特定用户来进行增量抓取
 - [repost.py](./repost.py):微博扩散程序，根据指定微博id，查看它转发(扩散)的情况
 - [login.py](./tasks/login.py):微博登陆客户端程序

- 微博登陆:采用celery来调度登录，将获取的cookie序列化后保存到redis
 - celery的broker和backend统一采用redis，分布式部署的时候需要关闭redis的保护模式，或者为redis设置密码
 - 启动登录定时任务和worker节点进行登录,定时登录是为了维护cookie的时效性，据我实验，微博的cookie有效时长为24小时。
   - 先启动worker(在多个节点启动，分散登录地点)：```celery -A tasks.login worker --loglevel=info --concurrency=1```
   - 再启动beat任务(beat只启动一个，否则会重复登录)：```celery beat -A tasks.login --loglevel=info```
 - 为了保证cookie的可用性，从redis层面将cookie过期时间设置为23小时，每次更新就重设过期时间

## 其它知识点
- 关于微博模拟登陆:可以查看我写的一篇[博客]()，里面详细介绍了微博模拟登陆的方法，有一些爬虫基础的同学可以完全无压力看懂
- 本项目目前默认采用单线程进行抓取，因为多线程抓取会极大增加封号的危险。可能在尝试代理IP有效性后，会采用多线程。单线程可用分布式的方式来提高抓取速度。

## 本项目目前的一些数据可视化展示(使用的**d3.js**):
对[某条指定微博](http://weibo.com/1973665271/E6HiqDiCg?refer_flag=1001030103_&type=comment#_rnd1473216182746)进行分析

微博扩散情况

![微博扩散](./img/kuosan.png)

转发该微博的用户性别比例

![用户性别比例](./img/sex.png)

转发该微博的时间

![转发曲线](./img/reposttime.png)

转发该微博的地域分析

![转发地域](./img/diyu.png)
