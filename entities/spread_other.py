# -*-coding:utf-8 -*-
class SpreadOther(object):
    def __init__(self):
        self.id = ''
        self.screen_name = ''
        self.city = ''
        self.province = ''
        self.location = ''
        self.description = ''
        self.headimg_url = ''
        self.blog_url = ''
        self.domain_name = ''
        self.gender = ''
        self.friends_count = 0   # 关注数
        self.followers_count = 0   # 粉丝数
        self.status_count = 0   # 微博数
        self.birthday = ''
        self.register_time = ''
        self.verify_type = 0
        self.verify_info = ''

        self.mid = ''
        self.reposts_count = 0
        self.comments_count = 0
        self.like_count = 0
        self.upper_user_id = ''   # 上层转发用户id
        self.upper_user_name = ''   # 上层转发用户名
        self.original_status_id = ''  # 源微博id
        self.status_url = ''  # 当前微博url
        self.status_post_time = ''
        self.device = ''

    def __str__(self):
        return 'id={id},name={name},upperid={upperid},uppername={uppername}'.format(id=self.id, name=self.screen_name,
                                                                                    upperid=self.upper_user_id,
                                                                                    uppername=self.upper_user_name)
