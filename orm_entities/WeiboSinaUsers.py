from orm_entities import *


class WeiboSinaUsers(Base):
    __tablename__ = 'weibo_sina_users'
    su_id = Column(String(50), primary_key=True)
    su_screen_name = Column(String(100))
    su_province = Column(String(100))
    su_city = Column(String(100))
    su_description = Column(String)
    su_headimg_url = Column(String(200))
    su_blog_url = Column(String(200))
    su_domain_name = Column(String(200))
    su_gender = Column(String(20))
    su_followers_count = Column(Integer)
    su_friends_count = Column(Integer)
    su_statuses_count = Column(Integer)
    su_gender_prefer = Column(String(50))
    su_birthday = Column(String(100))
    su_blood_type = Column(String(50))
    su_contact_info = Column(String)
    su_work_info = Column(String)
    su_educate_info = Column(String)
    su_owntag_info = Column(String)
    su_verifytype = Column(Integer)
    su_verifyinfo = Column(String(500))
    su_register_time = Column(String(100))
    su_update_time = Column(String(100))

    @staticmethod
    @dbtimeout_decorator(1)
    def get_user(uid):
        session = get_dbsession()
        rs = session.query(WeiboSinaUsers).filter(WeiboSinaUsers.su_id == uid).one()
        return rs

    @staticmethod
    @save_decorator
    @dbtimeout_decorator(0)
    def save_user(user):
        session = get_dbsession()
        session.add(user)
        session.commit()

if __name__ == '__main__':
    u = WeiboSinaUsers()
    u.su_id = 'sda'
    WeiboSinaUsers.save_user(u)