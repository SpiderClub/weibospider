import time
import pytest
import requests

from page_get import get_profile
from page_parse import search
from page_parse import home
from page_parse import comment
from page_parse import repost
from tests import REQUEST_INTERNAL


@pytest.mark.parametrize(
    'uid, expect_name', [('1642351362', 'angelababy'), ('10503', 'TimYang')]
)
def test_parse_user_info(uid, expect_name):
    user_info = get_profile(uid)[0]
    assert user_info.name == expect_name
    time.sleep(REQUEST_INTERNAL)


@pytest.mark.parametrize(
    'url, is_login', [
        ('http://s.weibo.com/weibo/%E7%81%AB%E5%BD%B1&scope=ori&suball=1&page=1', 1),
        ('http://s.weibo.com/weibo/%E7%81%AB%E5%BD%B1&scope=ori&suball=1&page=2', 1)
    ])
def test_parse_search_info(url, is_login, cookies, session):
    if is_login == 1:
        content = session.get(url).text
        assert len(search.get_search_info(content)) > 0
    else:
        content = requests.get(url, cookies=cookies).text
        assert len(search.get_search_info(content)) > 0
    time.sleep(REQUEST_INTERNAL)


@pytest.mark.parametrize(
    'url, is_login, is_ajax', [
        ('http://weibo.com/u/10503?is_ori=1&is_tag=0&profile_ftype=1&page=1', 0, 0),
        ('http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100505&pagebar=0&is_ori=1&id=10050510503&page=1&'
         'pre_page=1', 0, 1),
        ('http://weibo.com/u/10503?is_ori=1&is_tag=0&profile_ftype=1&page=2', 1, 0),
        ('http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100505&pagebar=0&is_ori=1&id=10050510503&page=2&'
         'pre_page=2', 1, 1)
    ], ids=['req_without_login', 'ajax_req_without_login', 'req_with_login', 'ajax_req_with_login'])
def test_parse_home_info(url, is_login, is_ajax, cookies, session):
    if is_login == 1:
        content = session.get(url).text
        if not is_ajax:
            assert len(home.get_data(content)) > 0
        else:
            assert len(home.get_ajax_data(content)) > 0
    else:
        content = requests.get(url, cookies=cookies).text
        if not is_ajax:
            assert len(home.get_data(content)) > 0
        else:
            assert len(home.get_ajax_data(content)) > 0
    time.sleep(REQUEST_INTERNAL)


def test_parse_comment_info(cookies):
    url = 'http://weibo.com/aj/v6/comment/big?ajwvr=6&id=4141730615319112&page=4'
    content = requests.get(url, cookies=cookies).text
    assert len(comment.get_comment_list(content, '4141730615319112')) > 0
    time.sleep(REQUEST_INTERNAL)


def test_parse_repost_info(cookies):
    url = 'http://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id=4159763183121316&&page=4'
    content = requests.get(url, cookies=cookies).text
    assert len(repost.get_repost_list(content, '4141730615319112')) > 0
    time.sleep(REQUEST_INTERNAL)