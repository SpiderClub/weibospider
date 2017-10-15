![weiblo spider logo](http://opqm8qbph.bkt.clouddn.com/weibospider.jpg)

---

[![](https://img.shields.io/badge/python-3-brightgreen.svg)](https://www.python.org/downloads/)
[![](https://travis-ci.org/ResolveWang/weibospider.svg?branch=master)](https://travis-ci.org/ResolveWang/weibospider)
[![GitHub issues](https://img.shields.io/github/issues/ResolveWang/weibospider.svg)](https://github.com/ResolveWang/weibospider/issues)
[![](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/ResolveWang)
[![](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 为何选择本项目 :star:
- 功能全面：包括了**用户信息抓取**、**指定关键字搜索结果增量抓取**、**指定用户主页所有原创微博抓取**、**评论抓取**和**转发关系抓取**等
- 数据全面：**PC端展现的数据量比移动端更加丰富**。并且相比于*其它同类项目*对微博的简单分析，本项目做了大量细致的工作，
比如不同`domain`不同用户的解析策略、不同`domain`不同用户的主页分析策略等
- 稳定！**项目可以长期稳定运行**。
  - 为了保证程序能长期稳定运行，数据所有的网络请求都是通过抓包手动分析的，未用任何自动化工具，包括模拟登陆！
  从另一个方面来说，抓取速度也是比较有保证的
  - 通过合理的阈值设定，账号可以保证安全。**但是不推荐用户使用自己的常用账号**
  - 即使账号不可用或者登陆失败，项目都对其做了处理（智能冻结账号，出错重试等），以保证每次请求都是有效的，并及时把错误反馈给用户
  - 通过大量的异常检测和处理，几乎捕获了所有的解析和抓取异常。编写了大量的解析代码来获取足够全面的信息
- 复用性和**二次开发性很好**。项目很多地方都有详细的代码注释，方便阅读。即使本项目不能完全满足你
对微博数据采集和分析的需求，你也可以自己在该项目的基础上做二次开发，项目已经在微博抓取和各个
模版解析上做了大量工作。
- 该项目会长期更新，目前已经迭代一年有余了。
- 丰富文档支持：请点击[wiki](https://github.com/ResolveWang/WeiboSpider/wiki)查看**所有文档**。如果文档仍然不能解
决你的问题，欢迎提issue，维护者看到后都会积极回答，也可以通过加QQ群(群号：499500161, 暗号：微博爬虫，**务必备注加群信息，否则
视为广告处理**)进行交流。

## 配置和使用 :sparkles:

关于详细配置请大家耐心阅读[这篇文档](https://github.com/ResolveWang/weibospider/wiki/%E9%A1%B9%E7%9B%AE%E5%85%B7%E4%BD%93%E9%85%8D%E7%BD%AE%E5%92%8C%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E)及该文档提及的相关文档。

## 常见问题 :question:
项目常见问题请查看[项目使用常见问题](https://github.com/ResolveWang/weibospider/wiki/%E9%A1%B9%E7%9B%AE%E4%BD%BF%E7%94%A8%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98)


## 其它说明 :heavy_exclamation_mark:
一些补充说明请查看[项目补充说明](https://github.com/ResolveWang/weibospider/wiki/%E9%A1%B9%E7%9B%AE%E8%A1%A5%E5%85%85%E8%AF%B4%E6%98%8E)


## TODO :dart:
关于项目下一步计划和已完成的目标可以查看[这篇文章](https://github.com/ResolveWang/weibospider/wiki/%E9%A1%B9%E7%9B%AE%E8%AE%A1%E5%88%92%E5%92%8C%E8%BF%9B%E5%B1%95)


## 赞助本项目:thumbsup:

如果本项目确实解决了你的刚需，或者对你有较大的启发，不妨请作者喝杯咖啡或者买本新书。

- [微信或者支付宝打赏作者](https://github.com/ResolveWang/WeiboSpider/wiki/%E6%8D%90%E8%B5%A0%E8%AF%A5%E9%A1%B9%E7%9B%AE)
- [捐赠记录](https://github.com/ResolveWang/WeiboSpider/wiki/%E6%8D%90%E8%B5%A0%E8%AF%A5%E9%A1%B9%E7%9B%AE)

## 如何贡献 :octocat:
- 如果遇到使用中有什么问题，可以在[issue](https://github.com/ResolveWang/WeiboSpider/issues)中提出来
- 代码中如果有逻辑不合理或者内容不完善的地方，可以fork后进行修改，然后Pull Request，你也可以添加一些较实用的功能
- 可以帮助实现`todo`中的需求
- 欢迎在[issue](https://github.com/ResolveWang/WeiboSpider/issues)中提有意义的future
- 希望有仔细研究过微博反爬虫策略的同学积极提建议

点击查看[贡献者名单](./AUTHORS.rst)

## 重要声明 :loudspeaker:
该项目开发的初衷是为了对部分信息进行监控，并且获取一些自然语言处理所需的语料，在**数据抓取的时候对爬虫访问频率进行了较为严格的控制**。
后来在技术和兴趣的驱动下，才慢慢扩展了分布式和对微博反爬虫策略的探究。

所以作者希望用户能合理使用该项目（通过[配置文件](./config/spider.yaml)控制访问频率），本着`够用就行`的原则，不要做`竭泽而渔`
的事情，对微博系统的正常运行和维护造成较大的困扰。

## 致谢:heart:
- 感谢大神[Ask](https://github.com/ask)的[celery](https://github.com/celery/celery)分布式任务调度框架
- 感谢大神[kennethreitz](https://github.com/kennethreitz/requests)的[requests](https://github.com/kennethreitz/requests)库
- 感谢提PR和issue的同学，这里特别感谢[yun17](https://github.com/yun17)，为本项目做了大量的贡献
- 感谢所有捐赠和给`star`支持的网友
