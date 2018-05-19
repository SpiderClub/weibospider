import pytest

from weibospider.db.basic import get_db_session
from weibospider.db.models import User
from weibospider.db.tables import (
    wbuser, login_info,
    keywords, weibo_data)
from weibospider.db.dao import (
    UserOper, LoginInfoOper, KeywordsOper,
    SeedidsOper, WbDataOper, )
from weibospider.db.redis_db import (
    Cookies, Urls, IdNames, urls_con)


FAKE_ID = '111111'
FAKE_IDS = ['111111', '222222', '111111']
FAKE_STR = 'test'


class TestMysql:
    def test_user_oper(self):
        user_list = list()
        for fake_id in FAKE_IDS:
            user_list.append(User(fake_id))
        UserOper.add_all(user_list)
        with get_db_session() as db:
            rs = db.execute('select * from {}'.format(wbuser.name))
            assert rs.rowcount > 0

        assert UserOper.get_user_by_uid('5') is None
        assert UserOper.get_user_by_uid(FAKE_ID) is not None

    def test_login_oper(self):
        infos = LoginInfoOper.get_login_info()
        assert len(infos) == 0
        with get_db_session() as db:
            db.execute("insert into {} ({}.name) values (".format(
                login_info.name, login_info.name) + FAKE_ID + ")")
        infos = LoginInfoOper.get_login_info()
        assert len(infos) == 1
        LoginInfoOper.freeze_account(FAKE_ID, 0)
        infos = LoginInfoOper.get_login_info()
        assert len(infos) == 0

    def test_keywords_oper(self):
        with get_db_session() as db:
            db.execute("insert into {} ({}.keyword) values ('".format(
                keywords.name, keywords.name) + FAKE_STR + "')")
        assert len(KeywordsOper.get_search_keywords()) == 1

    def test_seedids_oper(self):
        SeedidsOper.insert_seeds(FAKE_IDS)
        assert len(SeedidsOper.get_seed_ids()) == 2
        assert SeedidsOper.get_seed_by_id(FAKE_ID) is not None

        SeedidsOper.set_seed_crawled(FAKE_ID, 1)
        assert len(SeedidsOper.get_seed_ids()) == 1

    def test_weibodata_oper(self):
        with get_db_session() as db:
            db.execute("insert into {} ({}.weibo_id) values ('".format(
                weibo_data.name, weibo_data.name) + FAKE_ID + "')")
        assert WbDataOper.get_weibo_by_mid(FAKE_ID) is not None
        assert len(WbDataOper.get_comment_not_crawled()) == 1
        assert len(WbDataOper.get_repost_not_crawled()) == 1

        WbDataOper.set_comment_crawled(FAKE_ID)
        WbDataOper.set_repost_crawled(FAKE_ID)

        assert len(WbDataOper.get_comment_not_crawled()) == 0
        assert len(WbDataOper.get_repost_not_crawled()) == 0


class TestRedis:
    @pytest.fixture(scope='class', autouse=True)
    def flush_db(self):
        urls_con.flushall()

    def test_store_and_fetch_cookies(self):
        assert Cookies.fetch_cookies() is None
        Cookies.store_cookies(FAKE_STR, FAKE_STR)
        assert Cookies.fetch_cookies() is not None

    def test_del_cookies(self):
        Cookies.delete_cookies(FAKE_STR)
        assert Cookies.fetch_cookies() is None

    def test_store_urls(self):
        Urls.store_crawl_url(FAKE_STR, 1)
        assert urls_con.get(FAKE_STR) is not None

    def test_store_and_fetch_name_id(self):
        IdNames.store_id_name(FAKE_STR, FAKE_ID)
        rs = IdNames.fetch_uid_by_name(FAKE_STR)
        assert rs == FAKE_ID