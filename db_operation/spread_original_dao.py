# -*-coding:utf-8 -*-
from db_operation import db_connect


def save(user, mid, post_time, source, reposts_count, comments_count, root_url):
    """
    :param user: 用户对象
    :param mid: 微博id
    :param post_time: 发表时间
    :param source: 网页源码
    :param reposts_count: 转发数
    :param comments_count: 评论数
    :param root_url: 源微博URL
    :return: 返回的结果用于判断是否需要进行微博扩散的抓取
    """
    select_sql = "select * from weibo_spread_original where status_mid = '{mid}'".format(mid=str(mid))
    child_sql = "select count(*) from weibo_spread_other where original_status_id = '{mid}'".format(mid=str(mid))

    to_crawl = True

    with db_connect.db_execute() as conn:
        r = db_connect.db_queryall(conn, select_sql)
        rc = db_connect.db_queryall(conn, child_sql)

        # 如果数据库存在源微博和它的一些转发信息，我们就认为它不必抓取了
        if len(r) > 0 and rc[0][0] > 0:
            print('关于此条微博的扩散信息已经存于数据库中')
            to_crawl = False
        else:
            insert_sql = (
                        'insert into weibo_spread_original (user_id,user_screenname,user_province,user_city,'
                        'user_location, user_description,user_url,user_profileimageurl,user_gender,'
                        'user_followerscount,user_friendscount,user_statusescount,user_createdat,user_verifiedtype,'
                        'user_verifiedreason,status_createdat,status_mid,status_source,status_repostscount,'
                        'status_commentscount,status_url) values (:user_id,:user_screenname,:user_province,'
                        ':user_city,:user_location,:user_description,:user_url,:user_profileimageurl,:user_gender,'
                        ':user_followerscount,:user_friendscount,:user_statusescount,'
                        ':user_createdat,:user_verifiedtype,:user_verifiedreason,:status_createdat,:status_mid,'
                        ':status_source,:status_repostscount,:status_commentscount,:status_url)'
            )

            args = {
                'user_id': user.id,
                'user_screenname': user.screen_name,
                'user_province': user.province,
                'user_city': user.city,
                'user_location': user.location,
                'user_description': user.description.encode('gbk', 'ignore').decode('gbk'),
                'user_url': user.blog_url,
                'user_profileimageurl': user.headimg_url,
                'user_followerscount': user.followers_count,
                'user_friendscount': user.friends_count,
                'user_statusescount': user.status_count,
                'user_createdat': user.register_time,
                'user_verifiedtype': user.verify_type,
                'user_verifiedreason': user.verify_info.encode('gbk', 'ignore').decode('gbk'),
                'user_gender': user.gender,
                'status_createdat': post_time,
                'status_mid': mid,
                'status_source': source,
                'status_repostscount': reposts_count,
                'status_commentscount': comments_count,
                'status_url': root_url,
            }

            db_connect.db_dml_parms(conn, insert_sql, args)

    return to_crawl

