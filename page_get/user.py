from db.models import User
from logger import storage
from .basic import get_page
from page_parse import is_404
from db.dao import (
    UserOper, SeedidsOper)
from page_parse.user import (
    enterprise, person, public)

BASE_URL = 'http://weibo.com/p/{}{}/info?mod=pedit_more'


def get_user_detail(user_id, html):
    user = person.get_detail(html, user_id)
    if user is not None:
        user.uid = user_id
        user.follows_num = person.get_friends(html)
        user.fans_num = person.get_fans(html)
        user.wb_num = person.get_status(html)
    return user


def get_enterprise_detail(user_id, html):
    user = User(user_id)
    user.follows_num = enterprise.get_friends(html)
    user.fans_num = enterprise.get_fans(html)
    user.wb_num = enterprise.get_status(html)
    user.description = enterprise.get_description(html).encode('gbk', 'ignore').decode('gbk')
    return user


def get_url_from_web(user_id):
    """
    Get user info according to user id.
    If user domain is 100505,the url is just 100505+userid;
    If user domain is 103505 or 100306, we need to request once more to get his info
    If user type is enterprise or service, we just crawl their home page info
    :param: user id
    :return: user entity
    """
    if not user_id:
        return None

    url = BASE_URL.format('100505', user_id)
    html = get_page(url, auth_level=1)

    if not is_404(html):
        domain = public.get_userdomain(html)

        # writers(special users)
        if domain == '103505' or domain == '100306':
            url = BASE_URL.format(domain, user_id)
            html = get_page(url)
            user = get_user_detail(user_id, html)
        # normal users
        elif domain == '100505':
            user = get_user_detail(user_id, html)
        # enterprise or service
        else:
            user = get_enterprise_detail(user_id, html)

        if user is None:
            return None

        user.name = public.get_username(html)
        user.head_img = public.get_headimg(html)
        user.verify_type = public.get_verifytype(html)
        user.verify_info = public.get_verifyreason(html, user.verify_type)
        user.level = public.get_level(html)

        if user.name:
            UserOper.add_one(user)
            storage.info('Has stored user {id} info successfully'.format(id=user_id))
            return user
        else:
            return None

    else:
        return None


def get_profile(user_id):
    """
    :param user_id: uid
    :return: user info and is crawled or not
    """
    user = UserOper.get_user_by_uid(user_id)

    if user:
        storage.info('user {id} has already crawled'.format(id=user_id))
        SeedidsOper.set_seed_crawled(user_id, 1)
        is_crawled = 1
    else:
        user = get_url_from_web(user_id)
        if user is not None:
            SeedidsOper.set_seed_crawled(user_id, 1)
        else:
            SeedidsOper.set_seed_crawled(user_id, 2)
        is_crawled = 0

    return user, is_crawled


def get_user_profile(user_id):
    """
    :param user_id: uid
    :return: user info and is crawled or not
    """
    user = UserOper.get_user_by_uid(user_id)

    if user:
        storage.info('user {id} has already crawled'.format(id=user_id))
    else:
        user = get_url_from_web(user_id)
    return user


def get_fans_or_followers_ids(user_id, crawl_type):
    """
    Get followers or fans
    :param user_id: user id
    :param crawl_type: 1 stands for fans，2 stands for follows
    :return: lists of fans or followers
    """

    # todo check fans and followers the special users,such as writers
    # todo deal with conditions that fans and followers more than 5 pages
    if crawl_type == 1:
        fans_or_follows_url = 'http://weibo.com/p/100505{}/follow?relate=fans&page={}#Pl_Official_HisRelation__60'
    else:
        fans_or_follows_url = 'http://weibo.com/p/100505{}/follow?page={}#Pl_Official_HisRelation__60'

    cur_page = 1
    max_page = 6
    user_ids = list()
    while cur_page < max_page:
        url = fans_or_follows_url.format(user_id, cur_page)
        page = get_page(url)
        if cur_page == 1:
            urls_length = public.get_max_crawl_pages(page)
            if max_page > urls_length:
                max_page = urls_length + 1
        # get ids and store relations
        user_ids.extend(public.get_fans_or_follows(page, user_id, crawl_type))

        cur_page += 1

    return user_ids
