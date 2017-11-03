from django.db import models


class WbUser(models.Model):
    uid = models.CharField('用户ID', max_length=20, unique=True)
    name = models.CharField('昵称', max_length=200)
    gender = models.IntegerField('性别', default=0)
    birthday = models.CharField('生日', max_length=200)
    location = models.CharField('所在地', max_length=100)
    description = models.CharField('简介', max_length=500)
    register_time = models.CharField('注册时间', max_length=200)
    verify_type = models.IntegerField('认证', default=0)
    follows_num = models.IntegerField('关注数', default=0)
    fans_num = models.IntegerField('粉丝数', default=0)
    wb_num = models.IntegerField('微博数', default=0)
    level = models.IntegerField('级别', default=0)
    tags = models.CharField('标签', max_length=500)
    contact_info = models.CharField('联系信息', max_length=300)
    education_info = models.CharField('教育信息', max_length=300)
    head_img = models.CharField('头像地址', max_length=500)
    work_info = models.CharField('工作信息', max_length=500)
    verify_info = models.CharField('认证信息', max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'wbuser'
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'
        app_label = 'weibo_data'


class WeiboData(models.Model):
    weibo_id = models.CharField('微博ID', max_length=20, unique=True, blank=False)
    weibo_cont = models.TextField('内容')
    repost_num = models.IntegerField('回复数', default=0)
    comment_num = models.IntegerField('评论数', default=0)
    praise_num = models.IntegerField('点赞数', default=0)
    uid = models.CharField('用户Id', max_length=20, blank=False)
    is_origin = models.IntegerField('是否为源微博', default=1)
    device = models.CharField('发布设备', max_length=200)
    weibo_url = models.CharField('URL', max_length=300)
    create_time = models.CharField('发布时间', max_length=200)
    comment_crawled = models.IntegerField('是否抓取评论', default=0)
    repost_crawled = models.IntegerField('回复是否抓取', default=0)

    def __str__(self):
        return self.weibo_id

    class Meta:
        db_table = 'weibo_data'
        verbose_name = '微博信息'
        verbose_name_plural = '微博信息'
        app_label = 'weibo_data'


