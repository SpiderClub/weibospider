from orm_entities import *


class WeiboSearchData(Base):
    __tablename__ = 'weibo_search_data'
    se_primarykey = Column(String(200), primary_key=True)
    se_mid = Column(String(50))
    se_userid = Column(String(50))
    se_username = Column(String(70))
    se_uheadimage = Column(String(700))
    se_sid = Column(String(40))
    se_content = Column(String)
    se_picture_address = Column(String)
    se_createtime = Column(DateTime)
    se_device = Column(String(100))
    se_praise_count = Column(Integer)
    se_repost_count = Column(Integer)
    se_comment_count = Column(Integer)
    is_crawled = Column(Integer)

    @staticmethod
    @dbtimeout_decorator(2)
    def get_crawl_urls():
        session = get_dbsession()
        rs = session.query(WeiboSearchData).filter(WeiboSearchData.is_crawled == 0).order_by(desc(WeiboSearchData.
                                                                                                  se_createtime)).all()
        session_close(session)
        datas = []
        for r in rs:
            data = {'url': urljoin(base_url, r.se_userid+'/'+r.se_sid), 'mid': r.se_mid}
            datas.append(data)
        return datas

    @staticmethod
    @dbtimeout_decorator(0)
    def update_weibo_url(mid):
        session = get_dbsession()
        session.query(WeiboSearchData).filter(WeiboSearchData.se_mid == mid).update({WeiboSearchData.is_crawled: 1})
        session.commit()

    @staticmethod
    @save_decorator
    @dbtimeout_decorator(0)
    def update_weibo_repost(mid, reposts_count):
        session = get_dbsession()
        session.query(WeiboSearchData).filter(WeiboSearchData.se_mid == mid).update({WeiboSearchData.se_repost_count:
                                                                                    reposts_count})
        session.commit()


if __name__ == '__main__':
    # s = get_dbsession()
    # t = s.query(WeiboSearchData).filter(WeiboSearchData.se_mid == '3791583814072719').one()
    # session_close(s)
    # # clob字段为空的话取出来是None,因为clob在python中也是一个对象
    # print(t.se_createtime)
    rss = WeiboSearchData.get_crawl_urls()
    print(len(rss))
