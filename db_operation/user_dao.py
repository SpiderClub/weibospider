# -*-coding:utf-8 -*-
# 操作用户信息
from db_operation import db_connect


def save_user(user):
    save_sql = ('insert into weibo_sina_users (su_id,su_screen_name,su_province,su_city,su_description,su_headimg_url,'
                'su_blog_url,su_domain_name,su_gender,su_friends_count,su_followers_count,su_statuses_count,'
                'su_gender_prefer,su_birthday,su_blood_type,su_contact_info,su_work_info,su_educate_info,'
                'su_owntag_info,su_register_time,su_verifytype,su_verifyinfo) values(:su_id, :su_screen_name, '
                ':su_province, :su_city, :su_description,:su_headimg_url, :su_blog_url, :su_domain_name, :su_gender, '
                ':su_friends_count, :su_followers_count,:su_status_count, :su_gender_prefer, :su_birthday, '
                ':su_blood_type, :su_contact_info, :su_work_info,:su_educate_info, :su_owntag_info, :su_register_time,'
                ':su_verifytype, :su_verifyinfo)'
                )

    if user.id == '':
        pass

    user_info = {
        'su_id': user.id,
        'su_screen_name': user.screen_name,
        'su_province': user.province,
        'su_city': user.city,
        'su_description': user.description,
        'su_headimg_url': user.headimg_url,
        'su_blog_url': user.blog_url,
        'su_domain_name': user.domain_name,
        'su_gender': user.gender,
        'su_gender_prefer': user.gender_prefer,
        'su_friends_count': int(user.friends_count),
        'su_followers_count': int(user.followers_count),
        'su_status_count': int(user.status_count),
        'su_birthday': user.birthday,
        'su_blood_type': user.blood_type,
        'su_contact_info': user.contact_info,
        'su_work_info': user.work_info,
        'su_educate_info': user.educate_info,
        'su_owntag_info': user.owntag_info,
        'su_register_time': user.register_time,
        'su_verifytype': int(user.verify_type),
        'su_verifyinfo': user.verify_info,
    }

    with db_connect.db_execute() as conn:
        db_connect.db_dml_parms(conn, save_sql, user_info)


def save_users(users):
    save_sql = ('insert into weibo_sina_users (su_id,su_screen_name,su_province,su_city,su_description,su_headimg_url,'
                'su_blog_url,su_domain_name,su_gender,su_friends_count,su_followers_count,su_statuses_count,'
                'su_gender_prefer,su_birthday,su_blood_type,su_contact_info,su_work_info,su_educate_info,'
                'su_owntag_info,su_register_time,su_verifytype,su_verifyinfo) values(:su_id, :su_screen_name, '
                ':su_province, :su_city, :su_description,:su_headimg_url, :su_blog_url, :su_domain_name, :su_gender, '
                ':su_friends_count, :su_followers_count,:su_status_count, :su_gender_prefer, :su_birthday, '
                ':su_blood_type, :su_contact_info, :su_work_info,:su_educate_info, :su_owntag_info, :su_register_time,'
                ':su_verifytype, :su_verifyinfo)'
                )

    datas = []
    for user in users:
        if user.id == '':
            continue

        user_info = {
            'su_id': user.id,
            'su_screen_name': user.screen_name,
            'su_province': user.province,
            'su_city': user.city,
            'su_description': user.description,
            'su_headimg_url': user.headimg_url,
            'su_blog_url': user.blog_url,
            'su_domain_name': user.domain_name,
            'su_gender': user.gender,
            'su_gender_prefer': user.gender_prefer,
            'su_friends_count': int(user.friends_count),
            'su_followers_count': int(user.followers_count),
            'su_status_count': int(user.status_count),
            'su_birthday': user.birthday,
            'su_blood_type': user.blood_type,
            'su_contact_info': user.contact_info,
            'su_work_info': user.work_info,
            'su_educate_info': user.educate_info,
            'su_owntag_info': user.owntag_info,
            'su_register_time': user.register_time,
            'su_verifytype': int(user.verify_type),
            'su_verifyinfo': user.verify_info,
        }
        datas.append(user_info)

    with db_connect.db_execute() as conn:
        db_connect.db_dml_many(conn, save_sql, datas)


def get_user(uid):
    select_sql = ('select su_screen_name,su_province,su_city,su_description,su_headimg_url,su_blog_url,su_domain_name,'
                  'su_gender, su_followers_count,su_friends_count,su_statuses_count,su_birthday,su_verifytype,'
                  'su_verifyinfo,su_register_time from weibo_sina_users where su_id = :suid'
                  )
    # 由于连接关闭所有不能直接返回带状态的rs，不然description读取会异常
    info = dict()
    with db_connect.db_execute() as conn:
        rs = db_connect.db_queryone_params(conn, select_sql, {'suid': uid})
        info.update(
            name=rs[0],
            province=rs[1],
            city=rs[2],
            location='{province} {city}'.format(province=rs[1], city=rs[2]),
            headimg_url=rs[4],
            blog_url=rs[5],
            domain_name=rs[6],
            gender=rs[7],
            followers_count=rs[8],
            friends_count=rs[9],
            status_count=rs[10],
            birthday=rs[11],
            verify_type=rs[12],
            verify_info=rs[13],
            register_time=rs[14]
        )

        try:
            description = rs[3].read()
        except AttributeError:
            description = ''

        info.update(description=description)

    return info
