## 关于本项目
- 分布式微博爬虫。实现内容包括用户信息，微博信息，微博转发关系等
- 该项目本来是我们项目组的一个子模块，作用是舆情分析。整个系统比较庞大，我只能开源自己写
的代码部分，希望能帮到对微博数据采集有需求的同学，对爬虫进阶感兴趣的同学也可以看看。该项目
*从模拟登陆到各个页面的请求*、*从简单页面到复杂页面解析处理和相关的异常处理*、
*从单机到分布式迁移*都做了大量的工作和反复测试，花了我绝大部分业余的时间。
- 与该项目类似的项目大概有[SinaSpider](https://github.com/LiuXingMing/SinaSpider),[weibo_terminater](https://github.com/jinfagang/weibo_terminater)。
前者是一个基于```scrapy```的项目，爬的是移动版微博用户信息，质量还不错；后者嘛,还是用户
自己判断吧。

## 你可以用它来干嘛
- 微博舆情分析，特别是**热门微博转发分析**
- 微博数据分析，比如基于**微博用户信息**的分析
- 作为自然语言处理的语料
- 该项目很适合**爬虫进阶学习**

## 为何选择本项目
- 项目爬取的是PC端的微博信息，那么为何不采集移动端的呢？虽然它的限制更少，并且解析
的工作量也更小，但是数据采集经验比较丰富的同学应该也知道**移动端的微博和用户信息并不全面**，
所以在项目设计的时候定位就是**PC端的微博数据采集**。
- 稳定！项目可以长期稳定运行。在速度和稳定性之间，项目选择了后者。并且对于抓取微博和解析微博
可能出现的大量异常，都在项目中处理了。
- 由于本项目与本人实际工作挂钩，所以可以放心它会长期更新。目前已经迭代近一年了。


## TODO
- [x] 添加搜索接口，可以对某个指定话题进行搜索
- [ ] 将存储后端从Oracle转向Mysql
- [x] 优化代码，让程序运行更加快速和稳定(水平有限，已经优化过一次了)
- [x] 修复某些时候抓取失败的问题(已添加重试机制)
- [x] 改成分布式爬虫(使用celery做分布式任务调度和管理)
- [ ] 测试单机单账号访问阈值
- [ ] 测试单机多账号访问效果
- [ ] 验证UA头使用百度、Google等搜索引擎的时候请求是否放宽了
- [ ] 验证登录状态的cookies和代理ip（主要是异地）是否可以成功抓取
- [ ] 完善文档，包括python版本，怎么快速创建虚拟环境，然后安装相关依赖库和直接使用
dockerfile部署项目;讲解微博的反爬虫策略；讲解微博扩散信息抓取思路
- [ ] 在执行单个任务(比如分析指定微博的传播)的时候使用进度条
- [ ] 微博评论信息抓取（用作语料）
- [ ] 可视化展示某条微博具体传播信息，微博用户信息等
- [ ] 实现断点续传的功能（在repost抓取的时候，如果转发数目特别多，暂存相关信息到redis
中，以防当前worker挂了又必须重头抓取）

## 项目结构

```
    config/
        sql/
            spider.sql  # 项目所用表
    db/
        __init__.py
        basic_db.py # 数据库元操作
        login_info.py # 微博账号管理操作
        models.py # sqlalchemy中用到的models
        redis_db.py # redis相关操作，比如管理cookies和urls
        seed_ids.py # 种子用户id管理操作
        user.py # 用户相关操作
    decorator/
        __init__.py
        decorators.py # 项目中用到的装饰器，比如处理超时和模版解析异常
    logger/
        __init__.py
        log.py        # 日志操作
    logs/             # 该目录用于存放日志文件，由于程序没有创建文件夹的权限，所以需要提前建好
    page_get/
        __init__.py
        basic.py      # 基本的数据抓取操作
        user.py       # 微博用户抓取
    page_parse/
        user/
            __init__.py
            enterprise.py # 解析服务号
            person.py     # 解析个人用户
            public.py     # 公共模版解析
    tasks/
        __init__.py
        workers.py        # celery worker
        login.py          # 模拟登陆相关任务
        user.py           # 用户抓取相关任务
    tests/                # 一些解析模版，没多少用
    utils/                # 工具类
    wblogin/
        __init__.py
        login.py          # 微博模拟登陆具体实现
    headers.py            # 请求头，主要是UA
    login_first.py        # 由于celery的定时器会有一定时间的间隔，所以第一次需要手动登陆
    test_wbspider.py      # 没什么用的单元测试
    requirements.txt      # 项目相关依赖

```
有的文件和模块在项目代码中存在，却没有在项目结构中呈现，那么就说明该模块或者该文件还未进行
修改（oracle=>mysql）或者稳定性测试，实现并且测试完成后会补充


## 配置和使用
- 由于高版本的celery不支持windows,所以务必在**类Unix系统**部署，如果需要在windows
上部署的话，可以把celery版本降为3.1.25: ```pip install celery==3.1.25```，这是
celery最后支持的一个windows版本；**特别注意，windows平台上celery的定时功能不可用！**
- 安装相关依赖```pip install -r requirements.txt```,cx_Oracle的安装可能会
出问题，windows平台请看[这里](http://rookiefly.cn/detail/69)，linux平台请
看[这里](http://rookiefly.cn/detail/79)

- 打开[配置文件](./config/spider.yaml)修改数据库和微博账号相关配置
- 打开[sql文件](./config/sql/spider.sql)查看并使用建表语句
- 入口文件
 - [login.py](./tasks/login.py)和[login_first.py](login_first.py):微博登
 陆客户端程序
 - [user.py](./tasks/user.py):微博用户抓取程序
 - [repost.py](./tasks/repost.py)和[repost_first.py](repost_first.py):微
 博程序
 - [search.py](./tasks/search.py):微博搜索程序


- 微博登录和数据采集:采用celery来进行分布式任务调度
 - celery的broker和backend统一采用redis，分布式部署的时候需要关闭redis的保护
 模式，或者为redis设置密码
 - 启动登录定时任务和worker节点进行登录,定时登录是为了维护cookie的时效性，据我实验，
 微博的cookie有效时长为24小时。
   - 切换到tasks目录，首先启动worker(在多个分布式节点启动，**分散登录地点**)：```celery
   -A tasks.workers
   worker --loglevel=info --concurrency=1```
   - 第一次登陆微博的时候，为了让抓取任务能马上执行，需要在其中一个节点，切换到项目根目录执行```python
   login_first.py```获取首次登陆的cookie
   - 同理，第一次执行转发微博抓取，也需要执行```python repost_first.py```
   - 在一个分布式节点上，切换到tasks目录，再启动beat任务(beat只启动一个，否则会重复执行定时任务)：```
   celery beat -A
   tasks.workers -l info```
   - 通过*flower*监控节点健康状况：```flower -A tasks.workers --port=6666```
   (此处应有掌声)
 - 为了保证cookie的可用性，除了做定时登录以外，另外也从redis层面将cookie过期时间设置
 为23小时，每次更新就重设过期时间


## 其它说明
- 建议使用linux或者mac作为worker节点，作者并未在win平台上做稳定性测试
- [sql表](./config/sql/spider.sql)中关于weibo_sina_users和
weibo_search_data有一些没有sql注释的列，是老项目使用API获取的，目前已无法获取，
所以可根据自身需要删除或修改
- 本项目目前默认采用单线程进行抓取，因为多线程和协程等方式抓取会极大增加封号的危险，只能
在速度和稳定性之间进行取舍。可能在~~尝试代理IP有效性后~~弄清楚了微博的反爬虫策略后，会采
用多线程(也可能采用非阻塞IO)。目前只能通过分布式的方式来提高抓取速度。
- 如果是**开发版，可能会存在运行出问题的情况**，所以建议通过[release](https://github.com/ResolveWang/WeiboSpider/releases)页面下载稳定版
- 文档方面，暂时不会撰写该项目的相关文档。等时间宽裕了，会写一个关于该项目的详细使用和
开发教程。如果目前有什么问题，可以给该项目提issue,也可以加我微信交流，我的微信号是
```wpm_wx```，添加的时候请备注微博爬虫。
- 如果试用了本项目，觉得项目还不错的，麻烦多多宣传啦，觉得项目太渣或是有一些好的想法，欢迎
拍砖、吐槽或者提PR。随手点个```star```也是对本人工作的肯定和鼓励。送人玫瑰，手有余香:blush:。

## 本项目目前的一些数据可视化展示(使用的**d3.js**)（这部分代码目前还未实现，因为之前的数据可视化是一个队友做的，不方便开源她的代码）:

对[某条指定微博](http://weibo.com/1973665271/E6HiqDiCg?refer_flag=1001030103_&type=comment#_rnd1473216182746)进行分析

微博传播情况

![微博扩散](./img/kuosan.png)

转发该微博的用户性别比例

![用户性别比例](./img/sex.png)

转发该微博的时间

![转发曲线](./img/reposttime.png)

转发该微博的地域分析

![转发地域](./img/diyu.png)

