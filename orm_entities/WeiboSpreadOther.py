from orm_entities import *


class WeiboSpreadOther(Base):
    __tablename__ = 'weibo_spread_other'
    user_id = Column(String(20))
    user_screenname = Column(String(64))
    user_province = Column(String(20))
    user_city = Column(String(20))
    user_location = Column(String(64))
    user_description = Column(String(2048))
    user_url = Column(String(128))
    user_profileimageurl = Column(String(128))
    user_gender = Column(String(100))
    user_followerscount = Column(Integer)
    user_friendscount = Column(Integer)
    user_statusescount = Column(Integer)
    user_createdat = Column(String(32))
    user_verifiedtype = Column(Integer)
    user_verifiedreason = Column(String(128))
    status_createdat = Column(String(32))
    status_mid = Column(String(20), primary_key=True)
    status_source = Column(String(50))
    status_repostscount = Column(Integer)
    status_commentscount = Column(Integer)
    upper_user_id = Column(String(20), primary_key=True)
    original_status_id = Column(String(32))
    status_url = Column(String(128))

    @staticmethod
    @dbtimeout_decorator(0)
    @save_decorator
    def save(sos):
        ins_count = 0
        session = get_dbsession()
        for so in sos:
            session.add(so)
            session.commit()
            ins_count += 1
        print('一共插入了{total}条数据'.format(total=ins_count))
        session_close(session)

if __name__ == '__main__':
    s = get_dbsession()
    rs = s.query(WeiboSpreadOther).filter(WeiboSpreadOther.user_id == '2134654523').one()
    print(rs.__dict__)