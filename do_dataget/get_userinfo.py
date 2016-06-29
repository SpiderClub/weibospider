# -*-coding:utf-8 -*-
#  获取用户资料
import logging
from gl import login_name
from weibo_entities.user import User
from do_dataprocess.get_userprocess import get_enterpriseinfo, get_personalinfo, get_publicinfo
from do_dataprocess.do_statusprocess import status_parse
from do_dataprocess.basic import is_403, is_404
from do_dataget.basic import get_page
from db_operation.user_dao import save_user
from weibo_decorator.decorators import timeout_decorator


# todo 找出更多不同模板
@timeout_decorator
def get_profile(user_id, session, headers):
    """
    默认为个人用户，如果为作家，则需要再做一次抓取，而为企业用户，它会重定向到企业主页，直接解析即可
    登陆后可以根据http://weibo.com/u/userId来进行确定用户主页，不知道稳定不，todo 测试这个路径
    好像'http://weibo.com/p/100505' + user_id + '/info?mod=pedit_more' 这个路径可以通吃，只是非普通用户
    会被重定向到主页
    :param headers:
    :param user_id:
    :param session:
    :return:
    """
    user = User()
    url = 'http://weibo.com/p/100505' + user_id + '/info?mod=pedit_more'
    html = get_page(session, url, headers)

    if is_403(html):
        logging.info('{name}已经被冻结'.format(name=login_name))
    if not is_404(html):
        domain = get_publicinfo.get_userdomain(html)
        if domain == '100505' or domain == '103505' or domain == '100306':
            user = get_personalinfo.get_detail(html)
            user.followers_count = get_personalinfo.get_fans(html)
            user.friends_count = get_personalinfo.get_friends(html)
            user.status_count = get_personalinfo.get_status(html)
        else:
            user.followers_count = get_enterpriseinfo.get_fans(html)
            user.friends_count = get_enterpriseinfo.get_friends(html)
            user.status_count = get_enterpriseinfo.get_status(html)
            user.description = get_enterpriseinfo.get_description(html)

        user.id = user_id
        user.screen_name = get_publicinfo.get_username(html)
        user.headimg_url = get_publicinfo.get_headimg(html)
        user.verify_type = get_publicinfo.get_verifytype(html)
        user.verify_info = get_publicinfo.get_verifyreason(html, user.verify_type)
        print('本次抓取的url为:' + url + '用户id为：' + user_id)
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