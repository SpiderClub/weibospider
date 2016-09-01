# -*-coding:utf-8 -*-
from db_operation import db_connect
from weibo_decorator.decorators import save_decorator


@save_decorator
def save(sos):
    ins_count = 0
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
    for item in sos:
        try:
            args = {
                'user_id': item.id,
                'user_url': item.blog_url,
                'user_profileimageurl': item.headimg_url,
                'user_screenname': item.screen_name.encode('gbk', 'ignore').decode('gbk'),
                'user_province': item.province.encode('gbk', 'ignore').decode('gbk'),
                'user_city': item.city.encode('gbk', 'ignore').decode('gbk'),
                'user_location': item.location.encode('gbk', 'ignore').decode('gbk'),
                'user_description': item.description.encode('gbk', 'ignore').decode('gbk'),
                'user_gender': item.gender.encode('gbk', 'ignore').decode('gbk'),
                'user_verifiedreason': item.verify_info.encode('gbk', 'ignore').decode('gbk'),
                'status_source': item.device.encode('gbk', 'ignore').decode('gbk'),
                'user_followerscount': int(item.followers_count),
                'user_friendscount': int(item.friends_count),
                'user_statusescount': int(item.status_count),
                'status_repostscount': int(item.reposts_count),
                'status_commentscount': int(item.comments_count),
                'user_verifiedtype': int(item.verify_type),
                'user_createdat': item.register_time,
                'status_createdat': item.status_post_time,
                'status_mid': item.mid,
                'upper_user_id': item.upper_user_id,
                'original_status_id': item.original_status_id,
                'status_url': item.status_url,
            }
            db_connect.db_dml_parms(conn, insert_sql, args)
            ins_count += 1
        except Exception as why:
            print(why)
    print('一共插入了{ins}条数据'.format(ins=ins_count))
    db_connect.db_close(conn)


