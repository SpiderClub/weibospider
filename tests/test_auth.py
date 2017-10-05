import os

import pytest
import requests

from login import (
    get_cookies_and_headers, get_session)


class TestWithoutLogin:
    @pytest.fixture(scope='class', autouse=True)
    def headers(self):
        return get_cookies_and_headers()

    @pytest.mark.parametrize(
        'unique_str, url', [
            ('$CONFIG', 'http://weibo.com/1752613937/Afa5SFjJc'),
            ('$CONFIG', 'http://weibo.com/1319066361/Flttyxak8')
        ])
    def test_crawl_weibo_info_without_login(self, unique_str, url, headers):
        resp = requests.get(url, headers=headers)
        assert unique_str in resp.text

        resp = requests.get(url)
        assert unique_str not in resp.text

    def test_crawl_weibo_comment_without_login(self, headers):
        comment_url = 'http://weibo.com/aj/v6/comment/big?ajwvr=6&id=4158045430832830&page=1'
        resp = requests.get(comment_url, headers=headers)
        assert 'Sina Visitor System' not in resp.text

        resp = requests.get(comment_url)
        assert 'Sina Visitor System' in resp.text

    def test_crawl_weibo_repost_without_login(self, headers):
        repost_url = 'http://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id=4158045430832830&page=12'
        resp = requests.get(repost_url, headers=headers)
        assert 'Sina Visitor System' not in resp.text

        resp = requests.get(repost_url)
        assert 'Sina Visitor System' in resp.text

    @pytest.mark.parametrize(
        'unique_str, url', [
            ('html', 'http://s.weibo.com/ajax/direct/morethan140?mid=4157622578000858'),
            ('html', 'http://s.weibo.com/ajax/direct/morethan140?mid=4157781743129391')
        ])
    def test_get_weibo_cont_from_search_by_mid(self, unique_str, url):
        resp = requests.get(url)
        assert unique_str in resp.text


class TestWithLogin:
    def login(self):
        login_account = os.getenv('WEIBO_ACCOUNT')
        login_pass = os.getenv('WEIBO_PASS')
        session = get_session(login_account, login_pass)
        assert session is not None