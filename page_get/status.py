# -*-coding:utf-8 -*-
#  获取微博信息
import logging
from page_get import user
from page_get.basic import get_page
from page_parse.basic import is_404
from page_parse import status as parse_status
from entities.spread_other_cache import SpreadOtherCache
from entities.spread_other import SpreadOther
from entities.other_and_cache import SpreadOtherAndCache


# 获取当前转发微博信息
def get_status_info(url, user_id, name, mid=''):
    soc = SpreadOtherCache()
    print('当前转发微博url为:' + url)
    repost_cont = get_page(url)

    if not is_404(repost_cont):
        repost_user_id = parse_status.get_userid(repost_cont)
        if repost_user_id == '':
            return None

        repost_user_name = parse_status.get_username(repost_cont)
        soc.set_id(repost_user_id)
        soc.set_name(repost_user_name)

        so = SpreadOther()
        so.id = repost_user_id
        so.screen_name = repost_user_name
        so.upper_user_name = parse_status.get_upperusername(repost_cont, name)
        cur_user = user.get_profile(repost_user_id)
        try:
            so.province = cur_user.province
            so.city = cur_user.city
            so.location = cur_user.location
            so.description = cur_user.description
            so.domain_name = cur_user.domain_name
            so.blog_url = cur_user.blog_url
            so.gender = cur_user.gender
            so.headimg_url = cur_user.headimg_url
            so.followers_count = cur_user.followers_count
            so.friends_count = cur_user.friends_count
            so.status_count = cur_user.status_count
            so.verify_type = cur_user.verify_type
            so.verify_info = cur_user.verify_info
            so.register_time = cur_user.register_time

            if so.screen_name == name:
                so.id = user_id

            so.mid = parse_status.get_mid(repost_cont)
            so.status_post_time = parse_status.get_statustime(repost_cont)
            so.device = parse_status.get_statussource(repost_cont)
            if mid:
                so.original_status_id = mid
            else:
                so.original_status_id = parse_status.get_orignalmid(repost_cont)
            so.comments_count = parse_status.get_commentcounts(repost_cont)
            so.reposts_count = parse_status.get_repostcounts(repost_cont)
            so.like_count = parse_status.get_likecounts(repost_cont)
            so.status_url = url
        except AttributeError as e:
            # todo:找出这里的问题
            logging.info('解析{user_id}失败, 堆栈为{e}'.format(user_id=user_id, e=e))
            logging.info(r'该转发页面的源代码为:\n{repost_cont}'.format(repost_cont=repost_cont))
            return None
        else:
            return SpreadOtherAndCache(so, soc)
    else:
        return None

