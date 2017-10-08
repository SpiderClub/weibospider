import time
from urllib import parse as url_parse

import pytest

from page_get import (
    get_cont_of_weibo, get_page, get_profile)
from tasks.comment import crawl_comment_by_page
from tasks.repost import crawl_repost_by_page
from tests import REQUEST_INTERNAL


HOME_AJAX_URL = 'http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain={}&pagebar={}&is_ori=1&id={}{}&page={}' \
           '&pre_page={}&__rnd={}'


@pytest.mark.parametrize(
    'mid', ['4158010915826421', '4159555900113636']
)
def test_crawl_longtext_of_weibo(mid):
    resp_text = get_cont_of_weibo(mid)
    assert resp_text != ''
    time.sleep(REQUEST_INTERNAL)


def test_crawl_first_home_page():
    from page_parse.home import get_ajax_data
    url = 'http://weibo.com/u/1800822823?is_ori=1&is_tag=0&profile_ftype=1&page=1'
    content = get_page(url, auth_level=1)
    assert "['islogin']" in content
    time.sleep(REQUEST_INTERNAL)
    cur_time = int(time.time() * 1000)
    ajax_url_0 = HOME_AJAX_URL.format('100505', 0, '100505', '1800822823', 1, 1, cur_time)
    ajax_url_1 = HOME_AJAX_URL.format('100505', 0, '100505', '1800822823', 1, 1, cur_time + 100)

    content = get_page(ajax_url_0, auth_level=1, is_ajax=True)
    assert 'Sina Visitor System' not in content
    assert len(get_ajax_data(content)) > 0
    time.sleep(REQUEST_INTERNAL)

    content = get_page(ajax_url_1, auth_level=1, is_ajax=True)
    assert 'Sina Visitor System' not in content
    assert len(get_ajax_data(content)) > 0
    time.sleep(REQUEST_INTERNAL)


def test_crawl_first_search_page():
    url = 'http://s.weibo.com/weibo/{}&scope=ori&suball=1&page=1'
    encode_keyword = url_parse.quote('火影')
    cur_url = url.format(encode_keyword, 1)
    search_page = get_page(cur_url, auth_level=1)
    assert "['islogin']" in search_page
    time.sleep(REQUEST_INTERNAL)


@pytest.mark.parametrize(
    'uid, expect', [
        ('1371731565', 'Miss'),
        ('1642351362', 'angelababy')
    ])
def test_crawl_userinfo(uid, expect):
    user = get_profile(uid)[0]
    assert user.name == expect
    time.sleep(REQUEST_INTERNAL)


def test_crawl_comment():
    _, datas = crawl_comment_by_page('4159763183121316', 2)
    assert len(datas) > 0
    time.sleep(REQUEST_INTERNAL)


def test_crawl_repost():
    _, datas = crawl_repost_by_page('4159763183121316', 2)
    assert len(datas) > 0
    time.sleep(REQUEST_INTERNAL)