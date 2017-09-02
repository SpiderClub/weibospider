## 关于本项目 :octocat:
[![](https://img.shields.io/badge/python-3.4-green.svg)](https://www.python.org/download/releases/3.4.0/) [![](https://img.shields.io/badge/python-3.5-green.svg)](https://www.python.org/downloads/release/python-352/)
[![](https://img.shields.io/badge/python-3.6-green.svg)](https://www.python.org/downloads/release/python-360/) [![](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)
[![](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/ResolveWang)
- 实现内容包括用户信息、用户主页所有微博、微博搜索、微博评论和微博转发关系抓取等
- 本项目基于本人实际的工作，并对此做了大量的修改，可以保证项目的稳定运行

## 为何选择本项目 :star:
- 功能全面：包括了用户信息抓取、指定关键字搜索结果增量抓取、指定用户主页所有微博抓取、评论抓取和转发关系抓取等
- 数据全面：PC端展现的数据量比移动端更加丰富。并且相比于*其它同类项目*对微博的简单分析，本项目做了大量细致的工作，
比如不同`domain`不同用户的解析策略、不同`domain`不同用户的主页分析策略等
- 稳定！项目可以长期稳定运行。
  - 为了保证程序能长期稳定运行，数据所有的网络请求都是通过抓包手动分析的，未用任何自动化工具，包括模拟登陆！
  从另一个方面来说，抓取速度也是比较有保证的
  - 通过合理的阈值设定，账号可以保证安全。**但是不推荐用户使用自己的常用账号**
  - 即使账号不可用或者登陆失败，项目都对其做了处理（智能冻结账号，出错重试等），以保证每次请求都是有效的，并及时把错误反馈给用户
  - 通过大量的异常检测和处理，几乎捕获了所有的解析和抓取异常。编写了大量的解析代码来获取足够全面的信息
- 复用性和二次开发性很好。项目很多地方都有详细的代码注释，方便阅读。即使本项目不能完全满足你
对微博数据采集和分析的需求，你也可以自己在该项目的基础上做二次开发，项目已经在微博抓取和各个
模版解析上做了大量工作。
- 由于**本项目与本人实际工作有关联**(代码并不是工作中使用的代码)，所以可以放心它会长期更新。目前已经迭代一年有余了。
- 丰富文档支持：请点击[wiki](https://github.com/ResolveWang/WeiboSpider/wiki)查看**所有文档**。如果文档仍然不能解
决你的问题，欢迎提issue，维护者看到后都会积极回答，也可以通过加QQ群(群号：499500161, 暗号：微博爬虫，务必备注加群信息，否则
视为广告处理)进行交流。

## 配置和使用 :sparkles:

**使用前请大家务必仔细读项目配置 和 项目使用**


### 配置

**建议新手和小白们先查看演示视频(链接: https://pan.baidu.com/s/1eSy2qzw 密码: ypn5)**

- 环境配置:如果环境配置经验比较少，建议直接点击查看[项目环境配置](https://github.com/ResolveWang/WeiboSpider/wiki/%E5%88%86%E5%B8%83%E5%BC%8F%E7%88%AC%E8%99%AB%E7%8E%AF%E5%A2%83%E9%85%8D%E7%BD%AE)
  - 考虑到Python3是趋势和一些将该项目用于学习的用户，项目运行环境为**Python3.x**
  - 项目存储后端使用**Mysql**，所以需要在存储服务器上**安装Mysql**,注意设置字符集编码为**utf-8**
  - 由于项目是使用[celery](http://docs.celeryproject.org/en/latest/)做分布式任务调度，所以
需要使用broker和各个分布式节点通信，项目使用的是Redis，所以需要先安装[Redis](https://redis.io/download)。
注意修改Redis的配置文件让它能监听除本机外的别的节点的请求，**建议给Redis设置密码**，如
果没设置密码，需要关闭保护模式(不推荐，这个**有安全风险**)才能和各个节点通信。如果害怕遇到Redis单点
故障，可以使用Redis主从配置。

- 项目相关配置
  - 对Python虚拟环境了解的朋友可以使用 `source env.sh`，直接创建项目需要的虚拟环境和安装相关依赖。注意目前`env.sh`中支持的发行版是`CPython`和`Anaconda`，如果Python发行版
  是其它，那么可能需要修改`env.sh`文件中安装`virtualenv`的命令.虚拟环境默认安装在项目根目录，文件夹是`.env`。执行`source env.sh`会默认安装所有项目需要的依赖。
  - 如果不熟悉虚拟环境，可以通过在项目根目录执行```pip install -r requirements.txt```。这里celery版本用的3.1.25，目的是**兼容windows用户**。
  如果你是linux或者mac用户，建议将celery版本升级成4.x。**特别注意，Windows平台上Celery的定时功能不可用！所以如果需要用到定时任务分发的话，请务必将beat部署到linux或者mac上**.
  - 打开[配置文件](./config/spider.yaml)修改数据库相关配置。如果你的账号不是常用地登录
  的话（比如通过淘宝购买），登录会出现验证码，目前本项目通过**打码平台进行验证码识别**，选择的打码平台
  是[云打码](http://www.yundama.com/)，你需要在[spider.yaml](./config/spider.yaml)中**设置云打码平台你所注册
  的用户名和密码**并进行适当充值。一块钱大概可以识别160个验证码。也可以选择别的打码平台，又好用的欢迎推荐 T.T
  - 先手动创建一个名为`weibo`的数据库，然后在项目根目录下，运行`python create_all.py`创建该项目需要的数据库表


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

- 基本用法：请先在数据库中添加基本数据，然后再按照**启动各个节点的worker -> 运行login_first.py -> 启动定时任务或者别的任务**这个顺序进行，下面是详细说明
  - **在分布式节点上启动worker**。需要在启动worker的时候**指定分布式节点的queue**,queue的作用是配置节点可以接收什么任务，不可以接收什么任务。
比如我需要在节点1执行登录和用户抓取任务，那么启动worker的语句就是```celery -A tasks.workers -Q login_queue,user_crawler worker -l info -c 1```。如果不指定`-Q`参数，
即运行`celery -A tasks.workers worker -l info -c 1`，那么**所有任务都能够在该节点执行**。所有的queue及作用和更多关于worker的知识请
在[wiki](https://github.com/ResolveWang/WeiboSpider/wiki/WeibSpider%E4%B8%AD%E6%89%80%E6%9C%89%E4%BB%BB%E5%8A%A1%E5%8F%8A%E5%85%B6%E4%BD%9C%E7%94%A8%E8%AF%B4%E6%98%8E)中查看
  - celery运行定时任务会延迟一个定时周期。如果是**第一次运行该项目**，为了在抓取任务运行之前能有cookies，需要在任意一个节点上，切换到项目根目录执行`pythonlogin_first.py`**获取首次登陆的cookie**，
需要注意它只会分发任务到指定了`login_queue`的节点上或者未指定 `-Q`的节点上
  - 在其中一个分布式节点上，切换到项目根目录，再启动定时任务(beat只启动一个，否则会重复执行定时任务)：
`celery beat -A tasks.workers -l info`。因为beat任务会有一段时间的延迟(比如登录任务会延迟20个小时再执行)，所以第二步要通过```python login_first.py```来获取worker
首次运行需要的cookies.如果你想马上启动其他任务，而非等定时任务启动，那么可以执行相应的  `*.first.py`，比如我想在worker启动和login_first.py执行后就执行用户抓取任务，那么就通过
```python user_first.py```来执行
  - **通过*flower*监控节点健康状况**：先在任意一个节点，切换到项目根目录，再执行```flower -A tasks.workers```，通过'http://xxxx:5555' 访问所有节点信息，这里的```xxxx```指的是节点的IP.
如果需要让外网访问，可以这样`celery -A tasks.workers flower --address=0.0.0.0 --port=5555`
  - 程序默认以普通模式运行，如果想改成极速模式，请修改[配置文件](./config/spider.yaml)中`mode`的值为`quick`。关于极速和普通模式的区别，
  请查看[wiki](https://github.com/ResolveWang/WeiboSpider/wiki/%E5%88%86%E5%B8%83%E5%BC%8F%E5%BE%AE%E5%8D%9A%E7%88%AC%E8%99%AB%E7%9A%84%E6%99%AE%E9%80%9A%E6%A8%A1%E5%BC%8F%E4%B8%8E%E6%9E%81%E9%80%9F%E6%A8%A1%E5%BC%8F)
  - **注意，请在[release](https://github.com/ResolveWang/WeiboSpider/releases)页面下载稳定版本的微博爬虫，master分支不保证能正常和稳定运行**


- 其它
  - 定时登录是为了维护cookie的时效性，据我实验，PC端微博的cookie有效时长为24小时,因此设置定时执行登录的任务频率必须小于24小时，该项目默认20小时就定时登录一次
  - 为了保证cookie的可用性，除了做定时登录以外(可能项目代码有未知的bug)，另外也**从redis层面将cookie过期时间设置为23小时**，每次更新cookie就重设过期时间
  - 如果读了上述配置说明还不能顺利运行或者运行该项目的时候出了任何问题，欢迎提issue或者添加QQ群（群号是:499500161, 暗号是：微博爬虫）询问
  - 如果项目某些地方和你的应用场景不符，可以基于已有代码进行定制化开发，阅读[代码结构](https://github.com/ResolveWang/weibospider/wiki/%E9%A1%B9%E7%9B%AE%E7%BB%93%E6%9E%84)以帮助你快速了解代码的组织方式和核心内容
  - 由于部分同学反映，数据库表有些字段不能见闻知义，所以添加了[数据库表字段设计说明](https://github.com/ResolveWang/weibospider/wiki/%E6%95%B0%E6%8D%AE%E5%BA%93%E8%A1%A8%E5%AD%97%E6%AE%B5%E8%AF%B4%E6%98%8E)

## 常见问题 :question:
1.问：项目部署好复杂啊，我也没有多台机器，我可以单机运行吗？

答：可以单节点运行。除了单节点，也可以通过单机运行，单机运行的话，需要对代码做少许修改。主要修改方法是找到你需要的功能的入口文件，
然后跟着改，需要改的地方是```@app.task```这些函数的代码。以登录为例，如果需要单机登录的话，那么就先到[login模块](./tasks/login.py)
中把```send_task()```这条语句去掉，直接改成调用```login_task()```函数即可。这里```send_task()```是网络调用，修改后就成了本地调用了

2.关于redis的问题：为什么我在给redis设置密码后，并且把redis设置成了守护进程，但是没起作用？

答：其实这个问题和项目关系不是特别大吧。。。不过考虑到有的同学并不熟悉redis，我这里还是阐明一下，
如果在linux上面搭redis的话，当我们修改了```redis.conf```文件后，我们在启动redis的时候也**需要指定redis.conf
文件**，启动之前，最好把```redis-server```加入到环境变量中。比如我的```redis.conf```放在```/etc/redis```中，
那么我可以通过先切换到```/etc/redis```目录，再通过```redis-server redis.conf```来启动redis server，也可以
直接```redis-server /etc/redis/redis.conf```来启动，前提是 **redis-server**文件需要在环境变量中.另外，还得
注意一点，如果是centos的话，redis3.2.7可能会在`make&&make install` 阶段报错，建议下载redis3.2.8

3.这个项目的模拟登陆和抓取的时候是怎么处理验证码的啊？

答：这个项目在**模拟登陆阶段会判断账号是否需要验证码**，对于需要验证码的账号，通过*打码平台识别验证码*进行
操作，我选择的是[云打码](http://www.yundama.com/)；对于微博账号抓取的时候被封出现的验证码，目前的处理是从数据库和
redis中删除该账号对应的信息，因为要复现登录后被封需要一些时间来测试，并且某些情况下会验证手机，而某些情况只是识别验证码，这个
还需要进一步求证。

另外，我们应该尽量规避验证码，比如模拟登陆的时候尽量在账号常用地登录，还有一个点就是测试微博的容忍边界，小于它的阈值做采集
就不容易被封（不过速度很慢），毕竟按规矩来被封的风险要小得多。如果有图形图像识别的牛人解决了验证码的问题，欢迎提PR，帮助更多人。

4.这个项目能在windows上执行吗？

答：window上可以执行worker节点，但是不能执行beat节点（即定时任务）。如果要混用windows和linux，那么一定要将celery版本
降级为3.1.25，且将beat节点部署到linux服务器上。

5.这个项目一天能抓多少数据？

答：如果使用极速模式，3台机器每天可抓上百万的用户信息，可抓上千万的微博信息，它的代价就是账号必然会被封，推荐在网上购买小号进行
抓取。如果采用普通模式，那么三台机器每天可抓大概几万条用户信息，账号较为安全。另外，还有一点是，微博搜索的限制比较严格，速度可能
会比抓用户信息和抓用户主页微博慢，这点可能在后面会针对不同需求的用户进行相应处理。

6.这个项目搜索抓到的数据怎么和手动搜索的数据量不一致？

答：不一致主要是因为搜索是用的高级搜索，默认只搜索原创微博，而用户手动去搜索是搜索的所有微博，包括转发的，所以数据量上会有出入，
如果要抓取所有微博，那么修改[search模块](./tasks/search.py)的`url`和[home模块](./tasks/home.py)中的`home_url`的值即可。

7.可以为这个项目做个web监控和管理页面吗？

答：其实这个需求不是必须的，并且flower已经提供了类似的功能了。使用flower，我们可以监控各个节点的健康状况，且可以看到执行的任务情况


## 其它说明 :heavy_exclamation_mark:
- 本项目**运行环境是Python3.x**，由于Py2和Py3关于字符编码完全不同，所以如果需要在Py2上运行该程序，需要修改解析模块的相关代码
- 建议**使用linux或者mac**作为worker节点，windows平台也可以作为worker节点，**但是一定不能作为beat节点**，并且celery版本要注意一致。
- 目前该项目已经抓取将近三十万条微博用户数据，如果有需要数据的同学，可以开issue。我是打算数据量大了过后再进行分享。
- 目前项目有普通抓取和极速抓取两种模式，细节请查看[分布式微博爬虫的普通模式与极速模式](https://github.com/ResolveWang/WeiboSpider/wiki/%E5%88%86%E5%B8%83%E5%BC%8F%E5%BE%AE%E5%8D%9A%E7%88%AC%E8%99%AB%E7%9A%84%E6%99%AE%E9%80%9A%E6%A8%A1%E5%BC%8F%E4%B8%8E%E6%9E%81%E9%80%9F%E6%A8%A1%E5%BC%8F)
- 建议每台机器上都指定queue，目前发现如果启动worker的时候只指定`-c 1 -l info`而不指定`-Q`的话，可能运行会出现问题
- 如果不需要登录的模块建议就别使用cookie进行抓取，因为这样账号的负载更小。至于哪些信息不需要登录，且是有价值的，这个还会再进行调研，和等待用户的反馈。
- 如果是**开发版，可能会存在运行出问题的情况**，所以建议通过[release](https://github.com/ResolveWang/WeiboSpider/releases)页面下载稳定版
- 文档方面，目前在[WiKi](https://github.com/ResolveWang/WeiboSpider/wiki)中有一些较为系统的知识。如果使用过程中遇到问题，可以给该项目**提issue**,
也可以**加QQ群交流**，群号是:499500161, 暗号是：微博爬虫。**注意加群务必备注信息，否则将视为广告而拒绝！**
- 项目维护者目前只有我一个人，所以功能更新速度可能会比较慢，目前我只会关注自己会用到或者觉得有趣的部分，有别的需求的朋友可以提feture，如果恰巧也懂Python，**欢迎提PR**
- 如果试用了本项目，**觉得项目还不错的，麻烦多多宣传**啦。觉得项目太渣或是大家有一些有意义、有趣的想法，欢迎
拍砖、吐槽或者**提PR**,作者接受一切有意义的建议和提问。另外，随手点个```star```也是对本人工作的肯定和鼓励:kissing_heart:，
作者也接受捐赠:laughing:。送人玫瑰，手有余香:blush:。


## TODO :dart:
- 微博内容抓取相关
  - [x] 模拟登陆，账号请放置在*login_info*表中,如果账号登陆时需要验证码，请在[云打码](http://www.yundama.com/)官网注册一个云打码用户账号，并进行适当充值
  - [x] 微博常见用户和企业用户信息抓取：通过粉丝和关注进行增量式抓取，起始种子（微博用户`uid`）请插入*seed_ids*表
  - [x] 微博搜索功能，搜索词由自己指定
  - [x] 指定用户的主页：主要是原创微博内容，你也可以修改文件[home.py](./tasks/home.py)中的`home_url`和`ajax_home_url`中的`is_ori=1`为`is_all=1`来
  抓取用户的所有微博。目前指定用户是基于已有的`seed_ids`表中的```home_crawled=0```的用户，你也可以自己指定想要抓取的用户。
  - [x] 指定微博的评论：主要是抓取针对该微博的评论，即根评论。你可以通过修改[comment.py](./page_parse/comment.py)中的`get_comment_list()`
  来抓取指定微博的所有评论，包括根评论和子评论。目前抓取的评论是从`weibo_data`表中选取的`comment_crawled=0`的微博，你可以指定微博mid来定制化爬取评论。
  - [x] 指定微博的转发情况：主要是热门微博的转发信息

- 反爬虫相关
  - [x] 测试单机单账号访问阈值，这个问题和下面一个问题可以参考 [issue#17](https://github.com/ResolveWang/WeiboSpider/issues/17)和[issue#18](https://github.com/ResolveWang/WeiboSpider/issues/18)
  - [x] 测试单机多账号访问效果
  - [x] 验证不同模块，微博系统的容忍度是否相同
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
  - [x] 寻找能解决redis单点故障的方案,有兴趣可以查看我写的[这篇文章](https://github.com/ResolveWang/weibospider/wiki/Celery%E9%85%8D%E7%BD%AERedis-Sentinel%E5%81%9A%E9%AB%98%E5%8F%AF%E7%94%A8)
  - [x] 完善代码注释，方便用户做二次开发
  - [x] 支持Dockerfile部署项目
  - [ ] 重构项目，以更加Pythonic的方式构建项目

## 如何贡献 :loudspeaker:
- 如果遇到使用中有什么问题，可以在[issue](https://github.com/ResolveWang/WeiboSpider/issues)中提出来
- 代码中如果有逻辑不合理或者内容不完善的地方，可以fork后进行修改，然后Pull Request，如果一经采纳，就会将你加入[contributors](https://github.com/ResolveWang/WeiboSpider/graphs/contributors),
注意提PR之前，**检查一下代码风格是否符合PEP8并且改动的代码已经在自己机器上做了充足的测试（保证能长期稳定运行）**
- 可以实现`todo`中的需求
- 欢迎在[issue](https://github.com/ResolveWang/WeiboSpider/issues)中提有意义的future
- 希望有仔细研究过微博反爬虫策略的同学积极提建议

点击查看[贡献者名单](https://github.com/ResolveWang/WeiboSpider/wiki/%E8%B4%A1%E7%8C%AE%E8%80%85%E5%90%8D%E5%8D%95)


## 赞助本项目:thumbsup:

如果本项目确实解决了你的刚需，或者对你有较大的启发，不妨请作者喝杯咖啡或者买本新书。

- [微信或者支付宝打赏作者](https://github.com/ResolveWang/WeiboSpider/wiki/%E6%8D%90%E8%B5%A0%E8%AF%A5%E9%A1%B9%E7%9B%AE)
- [捐赠记录](https://github.com/ResolveWang/WeiboSpider/wiki/%E6%8D%90%E8%B5%A0%E8%AF%A5%E9%A1%B9%E7%9B%AE)


## 致谢:heart:
- 感谢大神[Ask](https://github.com/ask)的[celery](https://github.com/celery/celery)分布式任务调度框架
- 感谢大神[kennethreitz](https://github.com/kennethreitz/requests)的[requests](https://github.com/kennethreitz/requests)库
- 感谢提PR和issue的同学，这里特别感谢[yun17](https://github.com/yun17)，为本项目做了大量的贡献
- 感谢所有捐赠的网友和给`star`支持的网友

最后，祝大家用得舒心，用着不爽欢迎吐槽！