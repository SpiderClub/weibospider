# 关于该程序
## 目的
- 单机微博爬虫
- 抓取微博用户信息和分析微博信息扩散
- 测试微博反爬虫机制

## 需要的知识
- 基本的**HTTP协议**理解
- 会运用**Python**,了解**Requests**库
- 会使用**re模块**/**Beautifulsoup**解析网页
- 使用**cx_Oracle**存储数据

## 目前的成果
- 微博搜索、微博信息处理、用户信息处理模块具有可复用性
- 可以持续稳定的采集微博和微博用户相关数据(请求频率为**1s/次**，阈值正在测试)
- 微博用户信息和扩散信息已经能够成功采集并可以结合前端进行可视化展示

## todo
- ~~添加搜索接口，可以对某个指定话题进行搜索~~
- 可视化展示
- ~~不用重复抓取已经获取过的转发微博和其源微博~~
- ~~采用布隆过滤器去重网页~~
- 测试单机单账号访问阈值
- 测试单机多账号访问效果
- 优化代码，让程序运行更加快速和稳定
- 修复某些时候抓取失败的问题
- 改成分布式爬虫

## 配置和使用
- 安装相关依赖,包括**requests**,**bs4**,**cx_Oracle**,**[pyexecjs](https://github.com/doloopwhile/PyExecJS)**
> pip install requests
> pip install bs4
> cx_Oracle安装请查看我的博客:[ubuntu安装cx_Oracle踩过的那些坑](http://www.rookiefly.cn/detail/79)和[windows安装cx_Oracle踩过的那些坑](http://www.rookiefly.cn/detail/69)
> pip install PyExecJS

- 安装**[phantomjs](http://phantomjs.org/)**并且设置相关环境变量
- 打开[配置文件](./config/get_config.py)修改数据库和微博账号相关配置
- 入口文件 
|文件名|作用|
|---------|------|
|[repost_run.py](./repost_run.py)|微博扩散程序|
|[search_run.py](./search_run.py)|微博搜索程序|

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
