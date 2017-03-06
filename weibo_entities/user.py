# -*-coding:utf-8 -*-
# 用户类


class User(object):
    def __init__(self):
        self.id = ''
        self.screen_name = ''
        self.city = ''
        self.province = ''
        self.location = ''
        self.description = ''
        self.headimg_url = ''
        self.blog_url = ''
        self.domain_name = ''
        self.gender = ''
        self.gender_prefer = ''
        self.friends_count = 0
        self.followers_count = 0
        self.status_count = 0
        self.birthday = ''
        self.blood_type = ''
        self.contact_info = ''
        self.work_info = ''
        self.educate_info = ''
        self.owntag_info = ''
        self.register_time = ''
        self.verify_type = 0
        self.verify_info = ''

    def __str__(self):
        return 'id = {id},name={name}, city={city}, gender={gender}, verify_type={vt},verify_info={vi}'.format(
            id=self.id, name=self.screen_name, city=self.city, gender=self.gender, vt=self.verify_type,
            vi=self.verify_info)
