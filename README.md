## 关于本项目
- 分布式微博爬虫,为微博数据抓取而生
- 实现内容包括用户信息，微博信息，微博转发关系等
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
- 作为自然语言处理的**语料**
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
- [x] 验证登录状态的cookies和代理ip（主要是异地）是否可以成功抓取(测试结果是可以使用
登录后的cookie从别的地方进行数据采集，根据这一点，可以考虑使用代理IP，但是代理IP的质量
和稳定性可能会有问题，这一点**有待考察**)
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


## 配置和使用 :sparkles:
- 项目需要的Python解释器环境是Python3.x
- 项目存储后端使用**mysql**，所以需要在存储服务器上安装mysql
- 由于项目是使用[celery](http://docs.celeryproject.org/en/latest/)做分布式任务调度，所以
需要使用broker和各个分布式节点通信，项目使用的是redis，所以需要先安装[redis](https://redis.io/download)。
注意修改redis的配置文件让它能监听除本机外的别的节点的请求，建议给redis设置密码，如果没设置密码，需要关闭保护模式。
- 由于高版本的celery不支持windows,所以请在**类Unix系统**部署。如果实在需要在windows
上部署的话，可以把celery版本降为3.1.25: ```pip install celery==3.1.25```，这是
celery最后支持的一个windows版本；**特别注意，windows平台上celery的定时功能不可用！
所以如果需要用到定时任务分发的话，请务必将beat部署到linux或者mac上**
- 安装相关依赖```pip install -r requirements.txt```

- 打开[配置文件](./config/spider.yaml)修改数据库和微博账号相关配置
- 打开[sql文件](./config/sql/spider.sql)查看并使用建表语句
- 入口文件：如果有同学有修改源码的需求，那么建议从入口文件开始阅读
 - [login.py](./tasks/login.py)和[login_first.py](login_first.py):微博登
 陆客户端程序
 - [user.py](./tasks/user.py):微博用户抓取程序

- 微博登录和数据采集
 - 下面说明该项目分布式抓取的基本用法:
   - 项目使用了任务路由，在```tasks/workers```中可以查看所有的queue,所以需要在启动
   worker的时候**指定节点的queue**,比如我的节点1需要做登录任务和用户信息抓取任务，那么我就
   需要在节点1指定登录任务的queue```login_queue```和抓取用户信息的queue```user_crawler```,
   这里启动worker的语句就应该是```celery -A tasks.workers -Q login_queue,user_crawler worker -l info --concurrency=1```,
   该语句需要切换到项目根目录下执行。这里的节点1只会接收登录和抓取用户信息的任务，而抓取用户粉丝和关注的任务(*fans_followers*)是不会执行的。
   相关知识请参考[celery的任务路由说明](http://docs.celeryproject.org/en/latest/userguide/routing.html)
   - 如果是第一次运行该项目，为了让抓取任务能马上执行，需要在任意一个节点上，切换到项目根目录执行```python
   login_first.py```**获取首次登陆的cookie**（它只会分发任务到指定了```login_queue```的节点上）
   - 在其中一个分布式节点上，切换到项目根目录，再启动beat任务(beat只启动一个，否则会重复执行定时任务)：
   ```celery beat -A tasks.workers -l info```，因为beat任务会有一段时间的延迟(比如登录任务会延迟10个小时再执行)，所以通过```python login_first.py```来获取worker
   首次运行需要的cookie是必须的
   - 通过*flower*监控节点健康状况：先在任意一个节点，切换到项目根目录，再执行```flower -A tasks.workers```，通过'http://xxxx:5555'
   访问所有节点信息，这里的```xxxx```指的是节点的IP
 - 定时登录是为了维护cookie的时效性，据我实验，微博的cookie有效时长为24小时,因此设置定时执行登录的任务频率必须小于24小时。
 - 为了保证cookie的可用性，除了做定时登录以外，另外也从redis层面将cookie过期时间设置为23小时，每次更新cookie就重设过期时间


## 其它说明
- 建议**使用linux或者mac**作为worker节点，windows平台也可以作为worker节点，**但是一定不能作为beat节点**。
- 在运行项目之前，需要在数据库中建表，建表语句参见[sql表](./config/sql/spider.sql)，也需要**把自己的多个微博账号存入表(weibo.login_info)中**
- 本项目目前默认采用单线程进行抓取，因为多线程和协程等方式抓取会极大增加封号的危险，只能
在速度和稳定性之间进行取舍。可能在~~尝试代理IP有效性后~~弄清楚了微博的反爬虫策略后，会采
用多线程(也可能采用非阻塞IO)。目前只能通过分布式的方式来提高抓取速度。
- 如果是**开发版，可能会存在运行出问题的情况**，所以建议通过[release](https://github.com/ResolveWang/WeiboSpider/releases)页面下载稳定版
- 文档方面，暂时不会撰写该项目的相关文档。等时间宽裕了，会写一个关于该项目的详细使用和
开发教程。如果目前有什么问题，可以给该项目提issue,也可以加我微信交流，我的微信号是
```wpm_wx```，添加的时候请备注微博爬虫。
- 如果试用了本项目，觉得项目还不错的，麻烦多多宣传啦，觉得项目太渣或是有一些好的想法，欢迎
拍砖、吐槽或者提PR。随手点个```star```也是对本人工作的肯定和鼓励:kissing_heart:，作者也接受捐赠:laughing:。送人玫瑰，手有余香:blush:。


