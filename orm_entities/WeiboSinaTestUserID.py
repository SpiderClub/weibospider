from orm_entities import *


class WeiboSinaTestUserID(Base):
    __tablename__ = 'weibo_sina_testuserid'
    su_id = Column(String(50), primary_key=True)
    su_flag = Column(Integer)


if __name__ == '__main__':
    session = get_dbsession()
    t = session.query(WeiboSinaTestUserID).filter(WeiboSinaTestUserID.su_id=='1262812064').one()
    t.su_flag = 1
    session.commit()
    session_close(session)

