# -*-coding:utf-8 -*-
#  获取用户资料
from logger.log import storage
from entities.user import User
from page_get.basic import get_page
from page_parse.basic import is_404
from db.user_dao import save_user, get_user
from page_parse.user import enterprise, person, public


# 进行用户个人资料抓取的时候，查询是否已存在于数据库，如果没有，那么就保存，有就直接从里面取出来
# todo 改进用户信息抓取策略，以提高抓取效率
def get_profile(user_id):
    """
    默认为个人用户，如果为作家，则需要再做一次抓取，而为企业用户，它会重定向到企业主页，直接解析即可
    登陆后可以根据http://weibo.com/u/userId来进行确定用户主页，不知道稳定不，todo 测试这个路径
    好像'http://weibo.com/p/100505' + user_id + '/info?mod=pedit_more' 这个路径可以解决大部分路径问题，只是非普通用户
    会被重定向到主页，有的并不行，比如domain=100106
    """
    user = User()
    # 判断数据库是否存在
    info = get_user(user_id)

    if info:
        user.id = user_id
        user.screen_name = info.get('name')
        user.province = info.get('province')
        user.city = info.get('city')
        user.location = info.get('location')
        user.description = info.get('description')
        user.headimg_url = info.get('headimg_url')
        user.blog_url = info.get('blog_url')
        user.domain_name = info.get('domain_name')
        user.gender = info.get('gender')
        user.followers_count = info.get('followers_count')
        user.friends_count = info.get('friends_count')
        user.status_count = info.get('status_count')
        user.birthday = info.get('birthday')
        user.verify_type = info.get('verify_type')
        user.verify_info = info.get('verify_info')
        user.register_time = info.get('register_time')

        # 防止在插入数据库的时候encode()出问题
        for key in user.__dict__:
            if user.__dict__[key] is None:
                setattr(user, key, '')

        storage.info('ID为{id}的用户信息已经存在于数据库中'.format(id=user_id))

    else:
        url = 'http://weibo.com/p/100505{}/info?mod=pedit_more'.format(user_id)
        html = get_page(url)

        # todo 这里能不能不抓home页直接抓资料页,从而少做一次请求，减少封号的危险
        if not is_404(html):
            domain = public.get_userdomain(html)

            if domain == '100505' or domain == '103505' or domain == '100306':
                user = person.get_detail(html)
                if user is not None:
                    user.followers_count = person.get_fans(html)
                    user.friends_count = person.get_friends(html)
                    user.status_count = person.get_status(html)
                else:
                    user = User()
            else:
                # 为了尽可能少抓取url,所以这里不适配所有服务号
                if domain == '100106':
                    url = 'http://weibo.com/p/{domain}{uid}/home'.format(domain=domain, uid=user_id)
                    html = get_page(url)
                    if html == '':
                        return user

                user.followers_count = enterprise.get_fans(html)
                user.friends_count = enterprise.get_friends(html)
                user.status_count = enterprise.get_status(html)
                user.description = enterprise.get_description(html).encode('gbk', 'ignore').decode('gbk')

            # 公共解析部分
            user.id = user_id
            user.screen_name = public.get_username(html)
            user.headimg_url = public.get_headimg(html)
            user.verify_type = public.get_verifytype(html)
            user.verify_info = public.get_verifyreason(html, user.verify_type)

            save_user(user)
            storage.info('已经成功保存ID为{id}的用户信息'.format(id=user_id))

    return user

