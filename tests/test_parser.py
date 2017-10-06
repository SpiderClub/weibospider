import os

import pytest
import requests

from page_parse import search
from login import (
    get_session, get_cookies)


@pytest.fixture(scope='module', autouse=True)
def cookies():
    return get_cookies()


@pytest.fixture(scope='module', autouse=True)
def session():
    login_account = os.getenv('WEIBO_ACCOUNT')
    login_pass = os.getenv('WEIBO_PASS')
    return get_session(login_account, login_pass)


def test_parse_user_info():
    pass


def test_parse_weibo_info():
    pass


@pytest.mark.parametrize(
    'url, is_login', [
        ('http://s.weibo.com/weibo/%E7%81%AB%E5%BD%B1&scope=ori&suball=1&page=1', 0),
        ('http://s.weibo.com/weibo/%E7%81%AB%E5%BD%B1&scope=ori&suball=1&page=2', 1)
    ])
def test_parse_search_info(url, is_login, cookies, session):
    if is_login == 1:
        content = session.get(url).text
        assert len(search.get_search_info(content)) > 0
    else:
        content = requests.get(url, cookies=cookies).text
        assert len(search.get_search_info(content)) > 0


def test_parse_home_info():
    pass


def test_parse_comment_info():
    pass


def test_parse_repost_info():
    pass
