# -*-coding:utf-8 -*-
# 微博搜索数据


class WeiboSearch(object):
    def __int__(self):
        # 微博相关信息
        self.mid = ''
        self.murl = '' # 微博url
        self.create_time = ''
        self.praise_count = 0
        self.repost_count = 0
        self.comment_count = 0
        self.content = ''
        self.device = ''

        # 用户相关信息
        self.user_id = ''
        self.username = ''
        self.uheadimage = ''
        self.user_home = ''  # 用户主页

        # 某次抓取相关信息
        self.keyword = ''
        self.fetch_time = ''
        self.is_crawled = 0  # 是否抓取过详细信息