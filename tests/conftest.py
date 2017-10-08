import os

import pytest

from db.basic import db_session
from config import create_all
from login import (
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
    db_session.execute('drop database if exists weibo;')
    db_session.execute('create database weibo;use weibo;')
    rs = db_session.execute('show tables;')
    assert rs.rowcount == 0
    create_all.create_all_table()
    rs = db_session.execute('show tables;')
    assert rs.rowcount > 0