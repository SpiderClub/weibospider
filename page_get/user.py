# -*-coding:utf-8 -*-
#  获取用户资料
from db.models import User
from logger.log import storage
from page_get.basic import get_page
from page_parse.basic import is_404
from db.user import save_user, get_user_by_uid
from db.seed_ids import set_seed_crawled
from page_parse.user import enterprise, person, public


base_url = 'http://weibo.com/p/{}{}/info?mod=pedit_more'


def get_user_detail(user_id, html):
    user = person.get_detail(html)
    if user is not None:
        user.uid = user_id
        user.follows_num = person.get_friends(html)
        user.fans_num = person.get_fans(html)
        user.wb_num = person.get_status(html)
    return user


def get_enterprise_detail(user_id, html):
    user = User()
    user.uid = user_id
    user.follows_num = enterprise.get_friends(html)
    user.fans_num = enterprise.get_fans(html)
    user.wb_num = enterprise.get_status(html)
    user.description = enterprise.get_description(html).encode('gbk', 'ignore').decode('gbk')
    return user


def get_url_from_web(user_id):
    """
    根据用户id获取用户资料：如果用户的domain为100505，那么会直接返回用户详细资料；如果是103505或者100306，那么需要再进行
    一次请求，因为用base_url的方式它只会定位到用户主页而不是详细资料页；如果是企业和服务号等，通过base_url访问也会跳转到该
    用户的主页，由于该类用户的详细页价值不大，所以不再进行请求它们的详细页
    :param user_id: 用户id
    :return: 用户类实体
    """
    if not user_id:
        return None

    url = base_url.format('100505', user_id)
    html = get_page(url)

    if not is_404(html):
        domain = public.get_userdomain(html)

        # 作家
        if domain == '103505' or domain == '100306':
            url = base_url.format(domain, user_id)
            html = get_page(url)
            user = get_user_detail(user_id, html)
        # 普通用户
        elif domain == '100505':
            user = get_user_detail(user_id, html)
        # 默认是企业
        else:
            user = get_enterprise_detail(user_id, html)

        if user is None:
            return None

        user.name = public.get_username(html)
        user.head_img = public.get_headimg(html)
        user.verify_type = public.get_verifytype(html)
        user.verify_info = public.get_verifyreason(html, user.verify_type)
        user.level = public.get_level(html)

        # 保存用户信息到数据库
        save_user(user)
        storage.info('已经成功保存ID为{id}的用户信息'.format(id=user_id))

        return user
    else:
        return None


# 进行用户个人资料抓取的时候，查询是否已存在于数据库，如果没有，那么就保存，有就直接从里面取出来
def get_profile(user_id):
    # 判断数据库是否存在该用户信息
    user = get_user_by_uid(user_id)

    if user:
        storage.info('ID为{id}的用户信息已经存在于数据库中'.format(id=user_id))
        set_seed_crawled(user_id, 1)
    else:
        user = get_url_from_web(user_id)
        if user is not None:
            set_seed_crawled(user_id, 1)
        else:
            set_seed_crawled(user_id, 1)

    return user


def get_fans_or_followers_ids(user_id, crawl_type):
    """
    获取用户的粉丝和关注用户
    :param user_id: 用户id
    :param crawl_type: 1表示获取粉丝，2表示获取关注
    :return: 获取的关注或者粉丝列表
    """

    # todo 验证作家等用户的粉丝和关注是否满足;处理粉丝或者关注5页的情况
    if crawl_type == 1:
        ff_url = 'http://weibo.com/p/100505{}/follow?relate=fans&page={}#Pl_Official_HisRelation__60'
    else:
        ff_url = 'http://weibo.com/p/100505{}/follow?page={}#Pl_Official_HisRelation__60'

    cur_page = 1
    max_page = 6
    user_ids = list()
    while cur_page < max_page:
        url = ff_url.format(user_id, cur_page)
        page = get_page(url)
        if cur_page == 1:
            user_ids.extend(public.get_fans_or_follows(page))
            urls_length = public.get_max_crawl_pages(page)
            if max_page > urls_length:
                max_page = urls_length + 1

        cur_page += 1

    return user_ids

