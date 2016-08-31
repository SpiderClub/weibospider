# -*-coding:utf-8 -*-
#  获取用户资料
from weibo_entities.user import User
from do_dataprocess.get_userprocess import get_enterpriseinfo, get_personalinfo, get_publicinfo
from do_dataprocess.basic import is_404
from do_dataget.basic import get_page
from db_operation.user_dao import save_user, get_user


# 进行用户个人资料抓取的时候，查询是否已存在于数据库，如果没有，那么就保存，有就直接从里面取出来
def get_profile(user_id, session, headers):
    """
    默认为个人用户，如果为作家，则需要再做一次抓取，而为企业用户，它会重定向到企业主页，直接解析即可
    登陆后可以根据http://weibo.com/u/userId来进行确定用户主页，不知道稳定不，todo 测试这个路径
    好像'http://weibo.com/p/100505' + user_id + '/info?mod=pedit_more' 这个路径可以解决大部分路径问题，只是非普通用户
    会被重定向到主页，有的并不行，比如domain=100106
    :param headers:
    :param session:
    :param user_id:
    :return:
    """
    user = User()
    r = get_user(user_id)

    if r:
        user.id = user_id
        user.screen_name = r[0]
        user.province = r[1]
        user.city = r[2]
        user.location = '{province} {city}'.format(province=r[1], city=r[2])
        try:
            user.description = r[3].read()
        except AttributeError:
            user.description = ''
        user.headimg_url = r[4]
        user.blog_url = r[5]
        user.domain_name = r[6]
        user.gender = r[7]
        user.followers_count = r[8]
        user.friends_count = r[9]
        user.status_count = r[10]
        user.birthday = r[11]
        user.verify_type = r[12]
        user.verify_info = r[13]
        user.register_time = r[14]
        print('该用户信息已经存在于数据库中')
    else:
        url = 'http://weibo.com/p/100505' + user_id + '/info?mod=pedit_more'
        html = get_page(url, session, headers)

        if not is_404(html):
            domain = get_publicinfo.get_userdomain(html)

            if domain == '100505' or domain == '103505' or domain == '100306':
                user = get_personalinfo.get_detail(html)
                if user is not None:
                    user.followers_count = get_personalinfo.get_fans(html)
                    user.friends_count = get_personalinfo.get_friends(html)
                    user.status_count = get_personalinfo.get_status(html)
                else:
                    user = User()
            else:
                # 为了尽可能少抓取url,所以这里不适配所有服务号
                if domain == '100106':
                    url = 'http://weibo.com/p'+domain+user_id+'/home'
                    html = get_page(url, session, headers)
                user.followers_count = get_enterpriseinfo.get_fans(html)
                user.friends_count = get_enterpriseinfo.get_friends(html)
                user.status_count = get_enterpriseinfo.get_status(html)
                user.description = get_enterpriseinfo.get_description(html).encode('gbk', 'ignore').decode('gbk')

            user.id = user_id
            user.screen_name = get_publicinfo.get_username(html)
            user.headimg_url = get_publicinfo.get_headimg(html)
            user.verify_type = get_publicinfo.get_verifytype(html)
            user.verify_info = get_publicinfo.get_verifyreason(html, user.verify_type)

            save_user(user)

    return user


if __name__ == '__main__':
    with open('F:/360data/重要数据/桌面/luce.html', 'rb') as f:
        source = f.read().decode('utf-8')
    u = User()
    u.id = get_publicinfo.get_userid(source)
    print(u.id)
    u.screen_name = get_publicinfo.get_username(source)
    u.description = get_personalinfo.get_detail(source).description.encode('gbk', 'ignore').decode('gbk')
    print(u.description)
    save_user(u)