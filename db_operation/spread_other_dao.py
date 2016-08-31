# -*-coding:utf-8 -*-
from db_operation import db_connect
from weibo_decorator.decorators import save_decorator


@save_decorator
def save(sos):
    conn = db_connect.get_con()
    insert_sql = 'insert into weibo_spread_other (user_id,user_screenname,user_province,user_city,user_location,' \
                 'user_description,user_url,user_profileimageurl,user_gender,user_followerscount,user_friendscount,' \
                 'user_statusescount,user_createdat,user_verifiedtype,user_verifiedreason,status_createdat,' \
                 'status_mid,status_source,status_repostscount,status_commentscount,upper_user_id,original_status_id,' \
                 'status_url) ' + " values (:user_id,:user_screenname,:user_province,:user_city,:user_location," \
                 ":user_description,:user_url,:user_profileimageurl,:user_gender,:user_followerscount," \
                 ":user_friendscount,:user_statusescount,:user_createdat,:user_verifiedtype,:user_verifiedreason," \
                 ":status_createdat,:status_mid,:status_source,:status_repostscount,:status_commentscount," \
                 ":upper_user_id,:original_status_id,:status_url)"
    datas = []
    for item in sos:
        if item.id == '':
            continue
        # todo：这里为了防止插入失败暂时使用encode().decode()的方法，待改进
        args = {
            'user_id': item.id,
            'user_screenname': item.screen_name.encode('gbk', 'ignore').decode('gbk'),
            'user_province': item.province.encode('gbk', 'ignore').decode('gbk'),
            'user_city': item.city.encode('gbk', 'ignore').decode('gbk'),
            'user_location': item.location.encode('gbk', 'ignore').decode('gbk'),
            'user_description': item.description.encode('gbk', 'ignore').decode('gbk'),
            'user_url': item.blog_url,
            'user_profileimageurl': item.headimg_url,
            'user_gender': item.gender.encode('gbk', 'ignore').decode('gbk'),
            'user_followerscount': int(item.followers_count),
            'user_friendscount': int(item.friends_count),
            'user_statusescount': int(item.status_count),
            'user_createdat': item.register_time,
            'user_verifiedtype': int(item.verify_type),
            'user_verifiedreason': item.verify_info.encode('gbk', 'ignore').decode('gbk'),
            'status_createdat': item.status_post_time,
            'status_mid': item.mid,
            'status_source': item.device.encode('gbk', 'ignore').decode('gbk'),
            'status_repostscount': int(item.reposts_count),
            'status_commentscount': int(item.comments_count),
            'upper_user_id': item.upper_user_id,
            'original_status_id': item.original_status_id,
            'status_url': item.status_url,
        }
        datas.append(args)
    # 防止个别数据插入失败而导致批量插入失败
    for data in datas:
        db_connect.db_dml_parms(conn, insert_sql, data)
    db_connect.db_close(conn)


