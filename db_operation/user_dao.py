# -*-coding:utf-8 -*-
# 操作用户信息
from db_operation import db_connect
from weibo_decorator.decorators import save_decorator, dbtimeout_decorator
from weibo_entities.user import User
# todo：用orm改进


@save_decorator
def save_user(user):
    save_sql = 'insert into weibo_sina_users (su_id,su_screen_name,su_province,su_city,su_description,su_headimg_url,' \
               'su_blog_url,su_domain_name,su_gender,su_friends_count,su_followers_count,su_statuses_count,' \
               'su_gender_prefer,su_birthday,su_blood_type,su_contact_info,su_work_info,su_educate_info,' \
               'su_owntag_info,su_register_time,su_verifytype,su_verifyinfo) values(:su_id, :su_screen_name, ' \
               ':su_province, :su_city, :su_description,:su_headimg_url, :su_blog_url, :su_domain_name, :su_gender, ' \
               ':su_friends_count, :su_followers_count,:su_status_count, :su_gender_prefer, :su_birthday, ' \
               ':su_blood_type, :su_contact_info, :su_work_info,:su_educate_info, :su_owntag_info, :su_register_time,' \
               ':su_verifytype, :su_verifyinfo)'

    con = db_connect.get_con()

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
    db_connect.db_dml_parms(con, save_sql, user_info)
    db_connect.db_close(con)


@save_decorator
def save_users(users):
    save_sql = 'insert into weibo_sina_users (su_id,su_screen_name,su_province,su_city,su_description,su_headimg_url,' \
               'su_blog_url,su_domain_name,su_gender,su_friends_count,su_followers_count,su_statuses_count,' \
               'su_gender_prefer,su_birthday,su_blood_type,su_contact_info,su_work_info,su_educate_info,' \
               'su_owntag_info,su_register_time,su_verifytype,su_verifyinfo) values(:su_id, :su_screen_name, ' \
               ':su_province, :su_city, :su_description,:su_headimg_url, :su_blog_url, :su_domain_name, :su_gender, ' \
               ':su_friends_count, :su_followers_count,:su_status_count, :su_gender_prefer, :su_birthday, ' \
               ':su_blood_type, :su_contact_info, :su_work_info,:su_educate_info, :su_owntag_info, :su_register_time,' \
               ':su_verifytype, :su_verifyinfo)'

    con = db_connect.get_con()

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
    db_connect.db_dml_many(con, save_sql, datas)
    db_connect.db_close(con)


@dbtimeout_decorator(1)
def get_user(uid):
    select_sql = 'select su_screen_name,su_province,su_city,su_description,su_headimg_url,su_blog_url,su_domain_name,' \
                 'su_gender, su_followers_count,su_friends_count,su_statuses_count,su_birthday,su_verifytype,' \
                 'su_verifyinfo,su_register_time from weibo_sina_users where su_id = :suid'

    con = db_connect.get_con()
    rs = db_connect.db_queryone_params(con, select_sql, {'suid': uid})

    return rs


if __name__ == '__main__':
    user_id = '3008798700'
    r = get_user(user_id)
    iuser = User()
    iuser.id = user_id
    iuser.screen_name = r[0]
    iuser.province = r[1]
    iuser.city = r[2]
    iuser.location = '{province} {city}'.format(province=r[1], city=r[2])
    try:
        iuser.description = r[3].read()
    except AttributeError:
        iuser.description = ''
    iuser.headimg_url = r[4]
    iuser.blog_url = r[5]
    iuser.domain_name = r[6]
    iuser.gender = r[7]
    iuser.followers_count = r[8]
    iuser.friends_count = r[9]
    iuser.status_count = r[10]
    iuser.birthday = r[11]
    iuser.verify_type = r[12]
    iuser.verify_info = r[13]
    iuser.register_time = r[14]

    print(iuser)