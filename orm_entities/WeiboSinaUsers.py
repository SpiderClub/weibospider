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

if __name__ == '__main__':
    session = get_dbsession()
    t = session.query(WeiboSinaUsers).filter(WeiboSinaUsers.su_id == '3858873234').one()
    session_close(session)
    # clob字段为空的话取出来是None,因为clob在python中也是一个对象
    print(t.su_work_info)