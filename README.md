## 关于本项目 :octocat:
[![](https://img.shields.io/badge/python-3.4-green.svg)](https://www.python.org/download/releases/3.4.0/) [![](https://img.shields.io/badge/python-3.5-green.svg)](https://www.python.org/downloads/release/python-352/)
[![](https://img.shields.io/badge/python-3.6-green.svg)](https://www.python.org/downloads/release/python-360/) [![](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)
[![](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/ResolveWang)
- 实现内容包括用户信息、用户主页所有微博、微博搜索、微博评论和微博转发关系抓取等
- 本项目基于本人实际的工作，并对此做了大量的修改和改进。希望能帮到对微博数据采集有需求的同学，对爬虫进阶
感兴趣的同学也可以看看。该项目*从模拟登陆到各个页面的请求*、*从简单页面到复杂页面解析处理和相关的异常处理*、
*从单机到分布式迁移*都做了大量的工作和反复测试，花了我绝大部分业余的时间。
- 本项目不会承诺每天能抓到多少数据，因为**数据量的大小很大程度上取决于用户可用微博账户的数量**
- 与该项目类似的项目大概有[SinaSpider](https://github.com/LiuXingMing/SinaSpider),[weibo_terminater](https://github.com/jinfagang/weibo_terminater)。

## 你可以用它来干嘛 :u6709:
- **爬虫进阶学习**，对于需要学习Python进阶和爬虫的同学来说，都可以读读源码
- 微博舆情分析
- 论文撰写的一些数据，本项目会将抓到的**所有数据**不定时公布（资源和精力有限，暂时只有[19.1w条微博用户数据](https://pan.baidu.com/s/1caTyAa)）
- 自然语言处理的**语料**，比如热门微博的所有评论

## 为何选择本项目 :star:
- 功能全面：包括了用户信息抓取、指定关键字搜索结果增量抓取、指定用户主页所有微博抓取、评论抓取和转发关系抓取等
- 数据全面：PC端展现的数据量比移动端更加丰富。并且相比于其它同类项目对微博的简单分析，本项目做了大量细致的工作，
比如不同```domain```不同用户的解析策略、不同```domain```不同用户的主页分析策略等
- 稳定！项目可以长期稳定运行。
  - 为了保证程序能长期稳定运行，数据所有的网络请求都是通过抓包手动分析的，未用任何自动化工具，
  包括模拟登陆！从另一个方面来说，抓取速度也是比较有保证的（主要还是看账号数量）
  - 通过合理的阈值设定，账号可以保证安全
  - 即使账号不可用或者登陆失败，项目都对其做了处理（智能冻结账号，出错重试等），以保证每次请求都是有效的，并及时把错误反馈给用户
  - 通过大量的异常检测和处理，几乎捕获了所有的解析和抓取异常。编写了大量的解析代码来获取足够全面的信息
- 复用性和二次开发性很好。项目很多地方都有详细的代码注释，方便阅读。即使本项目不能完全满足你
对微博数据采集和分析的需求，你也可以自己在该项目的基础上做二次开发，项目已经在微博抓取和各个
模版解析上做了大量工作。
- 由于本项目与本人实际工作有一些关联(代码并不是工作中使用的代码)，所以可以放心它会长期更新。目前已经迭代一年有余了。
- 丰富文档支持：请点击[wiki](https://github.com/ResolveWang/WeiboSpider/wiki)查看**所有文档**。如果文档仍然不能解决你的问题，推荐提issue，我们开发者看到后都会积极回答，也可以
通过加QQ群(群号：499500161, 暗号：微博爬虫)进行交流。


## TODO :dart:
- 微博内容抓取相关
  - [x] 模拟登陆，账号请放置在[sql文件](./config/sql/spider.sql)的*login_info*表中,如果账号不需要验证码就能登录，请将`need_verify`字段设置为0，否则就设置为1，并且在[云打码](http://www.yundama.com/)
  官网注册一个云打码用户账号，并进行适当充值
  - [x] 微博常见用户和企业用户信息抓取：通过粉丝和关注进行增量式抓取，起始种子参见[sql文件](./config/sql/spider.sql)的*seed_ids*表。你也可以自己指定
  想抓取的用户信息，只需要把用户对应的uid放到`seed_ids`中
  - [x] 微博搜索功能，搜索词由自己指定，参考[sql文件](./config/sql/spider.sql)的*keywords*表。搜索词也可以自己指定。
  - [x] 指定用户的主页：主要是原创微博内容，你也可以修改文件[home.py](./tasks/home.py)中的`home_url`和`ajax_home_url`中的`is_ori=1`为`is_all=1`来
  抓取用户的所有微博。目前指定用户是基于已有的[seed_ids](./config/sql/spider.sql)表中的```home_crawled=0```的用户，你也可以自己指定想要抓取的用户。
  - [x] 指定微博的评论：主要是抓取针对该微博的评论，即根评论。你可以通过修改[comment.py](./page_parse/comment.py)中的`get_comment_list()`
  来抓取指定微博的所有评论，包括根评论和子评论。目前抓取的评论是从`weibo_data`表中选取的`comment_crawled=0`的微博，你可以指定微博mid来定制化爬取评论。
  - [x] 指定微博的转发情况：主要是热门微博的转发信息

- 反爬虫相关
  - [x] 测试单机单账号访问阈值，这个问题和下面一个问题可以参考 [issue#17](https://github.com/ResolveWang/WeiboSpider/issues/17)和[issue#18](https://github.com/ResolveWang/WeiboSpider/issues/18)
  - [x] 测试单机多账号访问效果
  - [ ] 验证不同模块，微博系统的容忍度是否相同
  - [ ] 验证UA头使用百度、Google等搜索引擎的时候请求是否放宽了：先通过寻找哪些内容是不用
 登录就能查看的，这一点主要是从移动端找，因为PC端限制更加严格，然后伪装UA测试请求量。在这个
 基础上再使用登录的账号测试
  - [x] 验证登录状态的cookies和代理ip是否可以成功抓取：测试结果是可以使用登录后的cookie
 从别的地方进行数据采集，根据这一点，可以考虑使用代理IP，但是代理IP的质量和稳定性可能会
 有问题，可能需要找一个或者自己写一个**高可用**的代理池，这一点还**有待考察**)
  - [x] 验证移动端登录Cookie和PC端是否可共享，如果可以共享则为PC端大规模抓取提供了可能，因为基于
  移动端的异地模拟登陆难度比PC端要小。目前异地账号使用打码平台进行验证码识别，并未采用移动端的方式登录
  - [x] 比较单IP和单账号哪个的限制更多，从而制定更加高效的数据采集方案：测试得知，经常是
 账号被封了，然后同一个IP用别的账号还能登陆，所以账号的限制比IP更加严格

- 其它
  - [x] 优化代码，让程序运行更加快速和稳定：水平有限，已经优化过一次了。下一次可能
    要等一段时间了
  - [x] 修复某些时候抓取失败的问题(已添加重试机制)
  - [x] 改成分布式爬虫(使用Celery做分布式任务调度和管理)
  - [x] 完善文档，包括怎么快速**创建虚拟环境**，怎么**安装相关依赖库**，怎么**使用该项目**(请查看三个演示视频(链接: https://pan.baidu.com/s/1kVHUWGv 密码: ydhs))；
  讲解**celery的基本概念和用法**（请查看[wiki](https://github.com/ResolveWang/WeiboSpider/wiki)中关于celery构建分布式爬虫的系列文章);
  讲解微博的反爬虫策略(具体请查看[issue17](https://github.com/ResolveWang/WeiboSpider/issues/17)、[issue18](https://github.com/ResolveWang/WeiboSpider/issues/18));
  各个```tasks```模块的作用和使用方法（请查看wiki中关`1task queue`的[说明](https://github.com/ResolveWang/WeiboSpider/wiki/WeibSpider%E4%B8%AD%E6%89%80%E6%9C%89%E4%BB%BB%E5%8A%A1%E5%8F%8A%E5%85%B6%E4%BD%9C%E7%94%A8%E8%AF%B4%E6%98%8E)）。
  - [ ] 寻找能解决redis单点故障的方案
  - [ ] 完善代码注释，方便用户做二次开发
  - [x] 支持Dockerfile部署项目
  - [ ] 可视化展示某条微博具体传播信息，微博用户信息等。这个优先级会比较低，目前重点
    解决数据抓取和复杂页面解析的问题

## 项目结构 :bell:

- 功能模块
 - 微博模拟登陆任务 [login.py](./tasks/login.py)
 - 微博用户抓取任务 [user.py](./tasks/user.py)
 - 微博特定话题搜索任务 [search.py](./tasks/search.py)
 - 微博用户主页信息抓取任务 [home.py](./tasks/home.py)
 - 微博评论抓取任务 [comment.py](./tasks/comment.py)
 - 微博转发抓取任务 [repost.py](./tasks/repost.py)

```
    config/
        sql/
            spider.sql      # 项目所用表
            create_all.py   # 可直接运行该文件生成项目所需要的数据表
        __init__.py
        conf.py             # 获取配置文件的信息
        spider.yaml         # 配置文件信息，包括Mysql配置、Redis配置和一些抓取参数设定
    db/
        __init__.py
        basic_db.py         # 数据库元操作
        keywords_wbdata.py  # 关键词_微博数据关联表
        login_info.py       # 微博账号管理操作
        models.py           # sqlalchemy中用到的models
        redis_db.py         # redis相关操作
        search_words.py     # 搜索话题相关操作
        seed_ids.py         # 种子用户id管理操作
        tables.py           # 数据库对应的表
        user.py             # 微博用户相关操作
        wb_data.py          # 微博数据相关操作
        weibo_comment.py    # 微博评论相关操作
        weibo_repost.py     # 微博转发相关操作
    decorators/
        __init__.py
        decorator.py        # 项目中用到的装饰器，比如超时处理、解析异常处理
    logger/
        __init__.py
        log.py              # 日志操作
    logs/                   # 该目录用于存放日志文件
        celery.log          # celery相关log(最为详细)
        weibo.log           # 程序log
    page_get/
        __init__.py
        basic.py            # 基本的数据抓取操作
        status.py           # 微博详情页信息解析模块
        user.py             # 微博用户抓取
    page_parse/
        user/
            __init__.py
            enterprise.py   # 解析服务号
            person.py       # 解析个人用户
            public.py       # 公共模版解析，比如左边部分和上边部分代码，可通用
        basic.py            # 微博返回内容解析，作用看是否为正常响应
        comment.py          # 评论解析
        home.py             # 用户主页微博数据解析
        repost.py           # 微博转发信息解析表
        search.py           # 微博搜索结果解析
        status.py           # 微博具体信息
    tasks/
        __init__.py
        comment.py          # 评论抓取任务
        home.py             # 用户主页微博抓取任务
        login.py            # 模拟登陆相关任务
        repost.py           # 转发信息抓取相关任务
        search.py           # 搜索相关任务
        user.py             # 用户抓取相关任务
        workers.py          # celery worker配置

    tests/                  # 一些解析模版，主要在开发解析模块的时候使用
    utils/                  # 工具类
        __init__.py
        code_verification.py# 验证码识别相关
        util_cls.py         # 工具类
    wblogin/
        __init__.py
        login.py          # 微博模拟登陆具体实现
    env.sh                # 创建虚拟环境相关的文件
    create_all.py         # 创建数据库相关的语句
    headers.py            # 请求头，主要是UA
    test_wbspider.py      # 没什么用的单元测试
    requirements.txt      # 项目相关依赖
    login_first.py        # 由于celery的定时器会有一定时间的间隔，所以**第一次需要手动登**，并且需要保证数据表`login_info`中已经插入了可用微博登陆账号
    search_first.py       # 如果想快速启动微博搜索任务，可以在定时任务运行之前运行该文件，前提是数据表`keywords`中已有数据
    comment_first.py      # 如果想快速启动评论抓取任务，可以在定时任务执行之前运行该文件，前提是数据表`weibo_data`中已有数据
    home_first.py         # 如果想快速启动用户主页微博抓取任务，可以在定时任务执行之前运行该文件，前提是数据表`wbuser`中已有数据
    repost_first.py       # 如果想快速启动微博转发抓取任务，可以在定时任务执行之前运行该文件，前提是数据表`weibo_data`中已有数据
    LICENSE
    .gitignore
    .gitattributes
```


## 配置和使用 :sparkles:


### 配置

**如果搭建项目环境比较困难，可以查看演示视频(链接: https://pan.baidu.com/s/1eSy2qzw 密码: ypn5)**

- 环境配置:小白和新手请直接查看[这里](https://github.com/ResolveWang/WeiboSpider/wiki/%E5%88%86%E5%B8%83%E5%BC%8F%E7%88%AC%E8%99%AB%E7%8E%AF%E5%A2%83%E9%85%8D%E7%BD%AE)
  - 考虑到Python3是趋势和一些将该项目用于学习的用户，项目运行环境为**Python3.x**
  - 项目存储后端使用**Mysql**，所以需要在存储服务器上**安装Mysql**,注意设置字符集编码为**utf-8**
  - 由于项目是使用[celery](http://docs.celeryproject.org/en/latest/)做分布式任务调度，所以
需要使用broker和各个分布式节点通信，项目使用的是Redis，所以需要先安装[Redis](https://redis.io/download)。
注意修改Redis的配置文件让它能监听除本机外的别的节点的请求，**建议给Redis设置密码**，如
果没设置密码，需要关闭保护模式(不推荐，这个**有安全风险**)才能和各个节点通信。如果害怕遇到Redis单点
故障，可以使用Redis主从配置。

- 项目相关配置
  - 安装相关依赖```pip install -r requirements.txt```，这里celery版本用的3.1.25，目的是**兼容windows用户**，**如果你是linux或者mac用户，那么建议celery版本升级成4**。
  **特别注意，Windows平台上Celery的定时功能不可用！所以如果需要用到定时任务分发的话，请务必将beat部署到linux或者mac上**.
  - 对Python虚拟环境了解的朋友可以使用 `source env.sh`，直接创建项目需要的虚拟环境和安装相关依赖。注意如果Python发行版是`anaconda`而非Python官网下载的发行版，那么需要修改`env.sh`文件中的 `pip install virtualenv`
  为`conda install virtualenv`.虚拟环境默认安装在项目根目录，文件夹是`.env`。通过该方式就不需要执行`pip install -r requirements.txt`了，shell脚本已经为你做了这一步了。
  - 打开[配置文件](./config/spider.yaml)修改数据库相关配置。如果你的账号不是常用地登录
  的话（比如通过淘宝购买），登录会出现验证码，目前本项目通过打码平台进行验证码识别，选择的打码平台
  是[云打码](http://www.yundama.com/)，你需要在[spider.yaml](./config/spider.yaml)中**设置云打码平台你所注册
  的用户名和密码**并进行适当充值。一块钱大概可以识别160个验证码。也可以选择别的打码平台，又好用的欢迎推荐 T.T
  - 在项目根目录下，运行`python create_all.py`创建该项目需要的表


---

上面其实已经介绍完整个项目的配置流程了.如果大家对docker比较熟悉，也可以使用基于docker的方式进行部署。
如果大家有使用docker的经验，估计也不用我多说了吧，只是要注意一点，构建镜像的时候需要在项目的根目录，因为在构建
镜像的过程中会拷贝`WeiboSpider`整个项目，目前用的硬编码，除了挂载可以灵活一点也没找到别的办法。镜像构建语句可以
是
> docker build -f WeiboSpider/Dockerfile -t resolvewang/weibospider:v1.0 .

构建好镜像后运行容器默认是接受所有任务路由，如果只接收部分，直接覆盖`CMD`的命令即可，比如我只想执行login任务，那么
> docker run --name resolvewang/weibospider:v1.0 celery -A tasks.workers -Q login_queue worker -l info -c 1

又比如通过docker启动定时器
> docker run --name spiderbeater resolvewang/weibospider:v1.0 celery beat -A tasks.workers -l info


### 使用

- 入口文件：如果有同学有**修改源码**的需求，那么建议**从入口文件开始阅读**
  - [login.py](./tasks/login.py)和[login_first.py](login_first.py):PC端微博登陆程序
  - [user.py](./tasks/user.py)和[user_first.py](user_first.py):微博用户抓取程序
  - [search.py](./tasks/search.py)和[search_first.py](search_first.py):微博话题搜索程序
  - [home.py](./tasks/home.py)和[home_first.py](home_first.py):微博用户主页所有微博抓取程序
  - [comment.py](./tasks/comment.py)和[comment_first.py](comment_first.py):微博评论抓取
  - [repost.py](./tasks/repost.py)和[repost_first.py](repost_first.py):转发信息抓取

- 基本用法：请按照**启动worker=>运行login_first.py=> 启动定时任务或者别的任务**这个顺序进行
  - **在分布式节点上启动worker**。需要在启动worker的时候**指定分布式节点的queue**,queue的作用是配置节点可以接收什么任务，不可以接收什么任务。
比如我需要在节点1执行登录和用户抓取任务，那么启动worker的语句就是```celery -A tasks.workers -Q login_queue,user_crawler worker -l info -c 1 -Ofair```。如果不指定，
即运行`celery -A tasks.workers worker -l info -c 1`，那么所有任务都可以在该节点实现。所有的queue及作用和更多关于worker的知识请
在[wiki](https://github.com/ResolveWang/WeiboSpider/wiki/WeibSpider%E4%B8%AD%E6%89%80%E6%9C%89%E4%BB%BB%E5%8A%A1%E5%8F%8A%E5%85%B6%E4%BD%9C%E7%94%A8%E8%AF%B4%E6%98%8E)中查看
  - 如果是**第一次运行该项目**，为了在抓取任务运行之前能有cookies，需要在任意一个节点上，切换到项目根目录执行```python
login_first.py```**获取首次登陆的cookie**，需要注意它只会分发任务到指定了```login_queue```的节点上或者未指定 `-Q`的节点上
  - 在其中一个分布式节点上，切换到项目根目录，再启动定时任务(beat只启动一个，否则会重复执行定时任务)：
```celery beat -A tasks.workers -l info```，因为beat任务会有一段时间的延迟(比如登录任务会延迟10个小时再执行)，所以第二步要通过```python login_first.py```来获取worker
首次运行需要的cookie.如果你想马上启动其他任务，而非等定时任务启动，那么可以执行相应的  `*.first.py`，比如我想在worker启动和login_first.py执行后就执行用户抓取任务，那么就通过
```python user_first.py```来执行
  - **通过*flower*监控节点健康状况**：先在任意一个节点，切换到项目根目录，再执行```flower -A tasks.workers```，通过'http://xxxx:5555' 访问所有节点信息，这里的```xxxx```指的是节点的IP.
如果需要让外网访问，可以这样`celery -A tasks.workers flower --address=0.0.0.0 --port=5555`


- 其它
  - 定时登录是为了维护cookie的时效性，据我实验，PC端微博的cookie有效时长为24小时,因此设置定时执行登录的任务频率必须小于24小时，该项目默认20小时就定时登录一次。
  - 为了保证cookie的可用性，除了做定时登录以外(可能项目代码有未知的bug)，另外也**从redis层面将cookie过期时间设置为23小时**，每次更新cookie就重设过期时间
  - 如果读了上述配置说明还不能顺利运行或者运行该项目的时候出了任何问题，欢迎提issue或者添加QQ群（群号是:499500161, 暗号是：微博爬虫）询问，目前群里用户比较少，有问题我必回！


## 常见问题 :question:
1. 问：项目部署好复杂啊，我也没有多台机器，我可以单机而不是单节点运行吗？
答：可以通过单机运行，单机运行的话，需要对代码做少许修改。主要修改方法是找到你需要的功能的
入口文件，然后跟着改，需要改的地方是```@app.task```这些函数的代码。以登录为例，如果需要
单机登录的话，那么就先到[login模块](./tasks/login.py)中把```send_task()```这条语句
去掉，直接改成调用```login_task()```函数即可。这里```send_task()```是网络调用，修改
后就成了本地调用了

2. 关于redis的问题：为什么我在给redis设置密码后，并且把redis设置成了守护进程，但是没起作用？
答：其实这个问题和项目关系不是特别大吧。。。不过考虑到有的同学并不熟悉redis，我这里还是阐明一下，
如果在linux上面搭redis的话，当我们修改了```redis.conf```文件后，我们在启动redis的时候也**需要指定redis.conf
文件**，启动之前，最好把```redis-server```加入到环境变量中。比如我的```redis.conf```放在```/etc/redis```中，
那么我可以通过先切换到```/etc/redis```目录，再通过```redis-server redis.conf```来启动redis server，也可以
直接```redis-server /etc/redis/redis.conf```来启动，前提是 **redis-server**文件需要在环境变量中.另外，还得
注意一点，如果是centos的话，redis3.2.7可能会在`make&&make install` 阶段报错，建议下载redis3.2.8

3. 这个项目的模拟登陆和抓取的时候是怎么处理验证码的啊？
答：这个项目~~并没有处理验证码~~在**模拟登陆阶段会判断账号是否需要验证码**，对于需要验证码的账号，通过打码平台识别验证码进行
操作，我选择的是[云打码](http://www.yundama.com/)（另外一个微博爬虫项目作者推荐的,发现确实好用）；对于微博账号抓取的时
候被封出现的验证码，目前的处理是从数据库和redis中删除该账号对应的信息，因为要复现登录后被封需要一些时间来测试，等项目功能方
面的代码实现得差不多了，可能会考虑这个问题，毕竟验证码的成本比账号低。

另外，我们应该尽量规避验证码，比如模拟登陆的时候尽量在账号常用地登录，还有一个点就是测试微博的容忍边界，小于它的阈值做采集
就不容易被封（不过速度很慢），毕竟按规矩来被封的风险要小得多。如果有图形图像识别的牛人解决了验证码的问题，欢迎提PR，帮助更多人。

4. 这个项目能在windows上执行吗？
答：window上可以执行worker节点，beat节点是不可以的，因为windows不支持crontab。如果要混用windows和linux，那么一定
要将celery版本降级为3.1.25。虽然celery4和celery3都可以同时跑，但是这样做flower是没法同时监控两个版本的worker的。

5. 这个项目一天能抓多少数据？
答：这个实在是没办法保证。数据量由你的账号和分布式节点数量决定的，最关键的是账号数量，目前我6个账号，4个节点，每天抓取量大概
2w条，如果需要更快，那么更多的账号是必不可少的。所以用户需要在速度和稳定性上做一些考量。

6. 这个项目解析模块为什么用bs而不用xpath,会不会性能很差？
答：项目在一年半以前开始启动，那时候还没接触到xpath，所以选了bs。但是本项目的瓶颈并不在解析模块上，解析再快，还是会被IO请求
所拖累，因为微博服务端对相同cookie的一个时间段的访问次数有限制，并且bs的解析速度也不算慢了。

其它问题暂时还没发现，如果有朋友在使用中遇到问题，欢迎提issue或者直接加我微信询问，我看到的话都会回答的。


## 其它说明 :heavy_exclamation_mark:
- 本项目**运行环境是Python3.x**，由于Py2和Py3关于字符编码完全不同，所以如果需要在Py2上运行该程序，需要修改解析模块的相关代码
- 建议**使用linux或者mac**作为worker节点，windows平台也可以作为worker节点，**但是一定不能作为beat节点**，并且celery版本要注意一致。
- 在运行项目之前，需要在数据库中建表，建表语句参见[sql表](./config/sql/spider.sql)，也需要**把自己的多个微博账号存入表(weibo.login_info)中**，把
搜索关键词存入关键词表(keywords)中。这里我已经预插入用户抓取用的一些种子用户了，如果想抓别的用户，请在种子用户表(seed_ids)中做插入操作。
- 目前该项目已经抓取将近十万条微博用户数据，如果有需要数据的同学，可以开issue。我是打算数据量大了过后再进行分享。
- 本项目目前默认采用单线程进行抓取，因为多线程和协程等方式抓取会极大增加封号的危险，只能
在速度和稳定性之间进行取舍。可能在~~尝试代理IP有效性后~~弄清楚了微博的反爬虫策略后，可能会采
用多线程(也可能采用非阻塞IO)。目前只能通过分布式的方式来提高抓取速度，分布式目前已经可用，所以具有较强的横向扩展性。
- 如果不需要登录的模块建议就别使用cookie进行抓取，因为这样账号的负载更小。至于哪些信息不需要登录，且是有价值的，这个还会再进行调研，和等待用户的反馈。
- 如果是**开发版，可能会存在运行出问题的情况**，所以建议通过[release](https://github.com/ResolveWang/WeiboSpider/releases)页面下载稳定版
- 文档方面，考虑到该项目的受众包括不会Python而单纯想拿微博数据的同学和一些想学爬虫进阶的同学，等项目功能完成差不多了，
我会写一个比较详细的使用文档和开发文档。目前在[WiKi](https://github.com/ResolveWang/WeiboSpider/wiki)中
有一些零散的知识点，在本页有关于该项目的使用方法。如果仍然会遇到问题，可以给该项目**提issue**,也可以**加QQ群交流**，群号是:499500161, 暗号是：微博爬虫，**提供人肉文档支持!**
- 项目由于目前是一个人开发的（估计吃瓜群众**积极提PR**），所以速度比较慢，目前我只会关注自己会用到或者觉得有趣的部分，有别的
需求的朋友可以提feture，如果恰巧也懂Python，**欢迎提PR**
- 如果试用了本项目，**觉得项目还不错的，麻烦多多宣传**啦。觉得项目太渣或是大家有一些有意义、有趣的想法，欢迎
拍砖、吐槽或者**提PR**,作者接受一切有意义的建议和提问。另外，随手点个```star```也是对本人工作的肯定和鼓励:kissing_heart:，
作者也接受捐赠:laughing:。送人玫瑰，手有余香:blush:。


## 如何贡献 :loudspeaker:
- 如果遇到使用中有什么问题，可以在[issue](https://github.com/ResolveWang/WeiboSpider/issues)中提出来
- 代码中如果有逻辑不合理或者内容不完善的地方，可以fork后进行修改，然后Pull Request，如果一经采纳，就会将你加入[contributors](https://github.com/ResolveWang/WeiboSpider/graphs/contributors),
注意提PR之前，**检查一下代码风格是否符合PEP8**
- 欢迎在[issue](https://github.com/ResolveWang/WeiboSpider/issues)中提有意义的future
- 希望有仔细研究过微博反爬虫策略的同学积极提建议

点击查看[贡献者名单](https://github.com/ResolveWang/WeiboSpider/wiki/%E8%B4%A1%E7%8C%AE%E8%80%85%E5%90%8D%E5%8D%95)

## 一点想法 :laughing:
- 目前我有一个比较有趣的想法：我也加了一个QQ群，是关于微博爬虫数据抓取的。看群里很多时候都有
同学在求微博数据，包括用户信息数据、微博数据、评论数据、用户主页微博等等，各种各样的数据。由于
微博限制得比较严格，单人想获取千万级甚至亿级的数据，需要特别大的成本，主要是账号的成本，那么为何
不把数据放共享呢？由于本项目是一个分布式的爬虫程序，所以对数据有要求的同学只需要在自己的服务器或者
本机上跑该程序，把抓取的结果放在一个大家都可以用的地方，人多力量大，采集量自然就多，这样也方便
了自己，方便了别人。并且使用者可以只用自己的worker节点执行自己关心的数据的抓取任务。当然这也有一些问题，
最主要的就是数据如何保护，不会被别人恶意破坏。这个目前只是一个想法，如果反馈比较热烈，可能在功能都实现
得差不多了，会搞这么一个东西，想起来还是比较有意思。

## 赞助本项目:thumbsup:
- [微信或者支付宝打赏作者](https://github.com/ResolveWang/WeiboSpider/wiki/%E6%8D%90%E8%B5%A0%E8%AF%A5%E9%A1%B9%E7%9B%AE)
- [捐赠记录](https://github.com/ResolveWang/WeiboSpider/wiki/%E6%8D%90%E8%B5%A0%E8%AF%A5%E9%A1%B9%E7%9B%AE)

如果本项目对你有用，欢迎对本项目进行捐赠，捐赠时候请留下你的```github ID```，当然您也可以匿名捐赠。

## 致谢:heart:
- 感谢大神[Ask](https://github.com/ask)的[celery](https://github.com/celery/celery)分布式任务调度框架
- 感谢大神[kennethreitz](https://github.com/kennethreitz/requests)的[requests](https://github.com/kennethreitz/requests)库
- 感谢提PR和issue的同学，这里特别感谢[yun17](https://github.com/yun17)同学，为本项目做了大量的贡献
- 感谢所有捐赠的网友,所有捐款都会贡献部分(20%)给[celery](http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html),用以支持和鼓励其发展！
而[requests](http://docs.python-requests.org/en/master/)未提供donate方式，所以目前只能通过[saythanks.io](https://saythanks.io/to/kennethreitz)对其表示谢意。
- 感谢所有`star`支持的网友


最后，祝大家玩得高兴，用得舒心！