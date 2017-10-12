from django.db import models

# Create your models here.

class BaseModel(models.Model):
    DATECREATED = models.DateTimeField('创建时间',auto_now_add=True, blank=True,null=True)
    DATEMODIFED = models.DateTimeField('修改时间',auto_now_add=True, blank=True,null=True)
    DELETED = models.BooleanField('是否删除', default=False,blank =True)
    ENTITY_NAME = models.CharField('实体名', max_length=255, blank=True,null=True)

    class Meta:
        abstract = True

    def to_dict(self):
        data = {}
        for f in self._meta.concrete_fields:
            data[f.name] = f.value_from_object(self)
        return data

class Keywords(BaseModel):
    keyword = models.CharField('关键词', max_length=200, unique=True)
    enable = models.IntegerField('是否启用', default=1)

    def __unicode__(self):
        return self.keyword

    class Meta:
        db_table = 'keywords'  # 自定义表名称为mytable
        verbose_name = '关键词'
        verbose_name_plural = '关键词'


class LoginInFo(BaseModel):
    # db_column='mycname'
    name = models.CharField('用户名', max_length=100, unique=True)
    password = models.CharField('密码', max_length=200)
    enable = models.IntegerField('是否启用', default=1)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'login_info'  # 自定义表名称为mytable
        verbose_name = '微博登陆账号'
        verbose_name_plural = '微博登陆账号'


class Save2kafkalog(models.Model):
    # db_column='mycname'
    createTime = models.CharField('微博发布时间', max_length=20)
    lastWeiboId = models.CharField('最后一个微博ID', max_length=255)
    longCreateTime = models.BigIntegerField('微博发布时间Long')
    spiderTime = models.DateTimeField('采集时间')
    type = models.IntegerField('类型')
    uid = models.CharField('最后一个用户ID', max_length=255)
    lastId = models.IntegerField('采集截止的数据')

    def __unicode__(self):
        return self.lastId

    class Meta:
        db_table = 'save2kafkalog'  # 自定义表名称为mytable
        verbose_name = '保存kafka日志'
        verbose_name_plural = '保存kafka日志'


class Seeds(BaseModel):
    # db_column='mycname'
    uid = models.CharField('用户ID', max_length=20, unique=True, blank=False)
    is_crawled = models.IntegerField('是否采集', default=0)
    # 是否抓取了该用户的前五页粉丝和关注用户的ID，1为已经抓取，0为未抓取，默认是0
    other_crawled = models.IntegerField('是否采集粉丝', default=0)
    home_crawled = models.IntegerField('是否过主页', default=0)

    def __unicode__(self):
        return self.uid

    class Meta:
        db_table = 'seed_ids'  # 自定义表名称为mytable
        verbose_name = '要采集的账号'
        verbose_name_plural = '要采集的账号'


class WbUser(models.Model):
    # db_column='mycname'
    uid = models.CharField('用户ID', max_length=20, unique=True)
    name = models.CharField('昵称', max_length=200)
    gender = models.IntegerField('性别', default=0)
    birthday = models.CharField('生日', max_length=200)
    location = models.CharField('地域信息', max_length=100)
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

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'wbuser'  # 自定义表名称为mytable
        verbose_name = '微博用户信息'
        verbose_name_plural = '微博用户信息'


class WeiboData(models.Model):
    # db_column='mycname'
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

    def __unicode__(self):
        return self.weibo_id

    class Meta:
        db_table = 'weibo_data'  # 自定义表名称为mytable
        verbose_name = '微博信息'
        verbose_name_plural = '微博信息'
