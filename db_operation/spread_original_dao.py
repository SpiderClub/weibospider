# -*-coding:utf-8 -*-
from db_operation import db_connect
from weibo_decorator.decorators import save_decorator


@save_decorator
def save(user, mid, post_time, source, reposts_count, comments_count, root_url):
    conn = db_connect.get_con()
    select_sql = "select * from weibo_spread_original where status_mid = '"+str(mid)+"'"
    r = db_connect.db_queryall(conn, select_sql)
    if len(r) > 0:
        print('已经存在了')
        db_connect.db_close(conn)
        return
    insert_sql = 'insert into weibo_spread_original (user_id,user_screenname,user_province,user_city,user_location,' \
                 'user_description,user_url,user_profileimageurl,user_gender,user_followerscount,user_friendscount,' \
                 'user_statusescount,user_createdat,user_verifiedtype,user_verifiedreason,status_createdat,' \
                 'status_mid,status_source,status_repostscount,status_commentscount,status_url) ' + " values (" \
                 ":user_id,:user_screenname,:user_province,:user_city,:user_location,:user_description,:user_url," \
                 ":user_profileimageurl,:user_gender,:user_followerscount,:user_friendscount,:user_statusescount," \
                 ":user_createdat,:user_verifiedtype,:user_verifiedreason,:status_createdat,:status_mid," \
                 ":status_source,:status_repostscount,:status_commentscount,:status_url)"
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
    db_connect.db_close(conn)

