import os

import pytest

from weibospider.db.basic import get_db_session
from weibospider.config import table_create
from weibospider.login import (
    get_session, get_cookies)


@pytest.fixture(scope='session', autouse=True)
def session():
    login_account = os.getenv('WEIBO_ACCOUNT')
    login_pass = os.getenv('WEIBO_PASS')
    s = get_session(login_account, login_pass)
    assert s is not None
    return s


@pytest.fixture(scope='session', autouse=True)
def cookies():
    return get_cookies()


@pytest.fixture(scope='session', autouse=True)
def create_tables():
    drop_db = 'drop database if exists weibo;'
    create_db = 'create database weibo;use weibo;'
    with get_db_session() as db:
        db.execute(drop_db)
        db.execute(create_db)
        rs = db.execute('show tables;')
        assert rs.rowcount == 0
        table_create.create_all_table()
        rs = db.execute('show tables;')
        assert rs.rowcount > 0