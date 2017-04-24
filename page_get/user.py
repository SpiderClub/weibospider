# -*-coding:utf-8 -*-
#  获取用户资料
from entities.user import User
from page_parse.userpage import enterpriseinfo, personalinfo, publicinfo
from page_parse.basic import is_404
from page_get.basic import get_page
from db_operation.user_dao import save_user, get_user
from logger.log import storage


# 进行用户个人资料抓取的时候，查询是否已存在于数据库，如果没有，那么就保存，有就直接从里面取出来
def get_profile(user_id, session, headers):
    """
    默认为个人用户，如果为作家，则需要再做一次抓取，而为企业用户，它会重定向到企业主页，直接解析即可
    登陆后可以根据http://weibo.com/u/userId来进行确定用户主页，不知道稳定不，todo 测试这个路径
    好像'http://weibo.com/p/100505' + user_id + '/info?mod=pedit_more' 这个路径可以解决大部分路径问题，只是非普通用户
    会被重定向到主页，有的并不行，比如domain=100106
    """
    if user_id == '':
        return User()

    user = User()
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
        url = 'http://weibo.com/p/100505' + user_id + '/info?mod=pedit_more'
        html = get_page(url, session, headers)

        if not is_404(html):
            domain = publicinfo.get_userdomain(html)

            if domain == '100505' or domain == '103505' or domain == '100306':
                user = personalinfo.get_detail(html)
                if user is not None:
                    user.followers_count = personalinfo.get_fans(html)
                    user.friends_count = personalinfo.get_friends(html)
                    user.status_count = personalinfo.get_status(html)
                else:
                    user = User()
            else:
                # 为了尽可能少抓取url,所以这里不适配所有服务号
                if domain == '100106':
                    url = 'http://weibo.com/p/'+domain+user_id+'/home'
                    html = get_page(url, session, headers)
                    if html == '':
                        return user

                user.followers_count = enterpriseinfo.get_fans(html)
                user.friends_count = enterpriseinfo.get_friends(html)
                user.status_count = enterpriseinfo.get_status(html)
                user.description = enterpriseinfo.get_description(html).encode('gbk', 'ignore').decode('gbk')

            user.id = user_id
            user.screen_name = publicinfo.get_username(html)
            user.headimg_url = publicinfo.get_headimg(html)
            user.verify_type = publicinfo.get_verifytype(html)
            user.verify_info = publicinfo.get_verifyreason(html, user.verify_type)

            save_user(user)
            storage.info('已经成功保存ID为{id}的用户信息'.format(id=user_id))

    return user

