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
    else:
        set_seed_crawled(user_id, 2)
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
    url = base_url.format('100505', user_id)
    html = get_page(url)

    if not is_404(html):
        domain = public.get_userdomain(html)

        if domain == '103505' or domain == '100306':
            url = base_url.format(domain, user_id)
            html = get_page(url)
            user = get_user_detail(user_id, html)
        elif domain == '100505':
            user = get_user_detail(user_id, html)
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
        set_seed_crawled(user_id, 1)
        storage.info('已经成功保存ID为{id}的用户信息'.format(id=user_id))

        return user
    else:
        set_seed_crawled(user_id, 2)
        return None


# 进行用户个人资料抓取的时候，查询是否已存在于数据库，如果没有，那么就保存，有就直接从里面取出来
# todo 改进用户信息抓取策略，以提高抓取效率
def get_profile(user_id):
    """
    默认为个人用户，如果为作家，则需要再做一次抓取，而为企业用户，它会重定向到企业主页，直接解析即可
    登陆后可以根据http://weibo.com/u/userId来进行确定用户主页，不知道稳定不，todo 测试这个路径
    好像'http://weibo.com/p/100505' + user_id + '/info?mod=pedit_more' 这个路径可以解决大部分路径问题，只是非普通用户
    会被重定向到主页，有的并不行，比如domain=100106
    """
    # 判断数据库是否存在
    user = get_user_by_uid(user_id)

    if user:
        # 防止在插入数据库的时候encode()出问题
        for key in user.__dict__:
            if user.__dict__[key] is None:
                setattr(user, key, '')

        storage.info('ID为{id}的用户信息已经存在于数据库中'.format(id=user_id))

    else:
        user = get_url_from_web(user_id)

    return user

