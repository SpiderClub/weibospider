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

        self.mk_primary = ''  # 主键，由mid和关键词组成

    def __str__(self):
        return 'mid:{mid},murl:{murl},create_time:{create_time},repost_count:{repost_count},user_id:{user_id},' \
               'username:{username}'.format(mid=self.mid, murl=self.murl, user_id=self.user_id,
                                            create_time=self.create_time, repost_count=self.repost_count, username=self.
                                            username)