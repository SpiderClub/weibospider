from orm_entities import *


class WeiboSpreadOrignal(Base):
    __tablename__ = 'weibo_spread_original'
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
    status_mid = Column(String(20))
    status_source = Column(String(50))
    status_repostscount = Column(Integer)
    status_commentscount = Column(Integer)
    status_url = Column(String(128), primary_key=True)

    @staticmethod
    @dbtimeout_decorator(0)
    def save(wso):
        session = get_dbsession()
        session.add(wso)
        session.commit()

if __name__ == '__main__':
    s = get_dbsession()
    rs = s.query(WeiboSpreadOrignal).filter(WeiboSpreadOrignal.user_id == '3917666225').one()
    print(rs.__dict__)