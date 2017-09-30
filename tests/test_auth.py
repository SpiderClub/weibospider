import pytest
import requests

from wblogin import get_cookies_and_headers


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

    def test_crawl_weibo_comment_without_login(self):
        pass

    def test_crawl_weibo_repost_without_login(self):
        pass

    @pytest.mark.parametrize(
        'unique_str, url', [
            ('html', 'http://s.weibo.com/ajax/direct/morethan140?mid=4157622578000858'),
            ('html', 'http://s.weibo.com/ajax/direct/morethan140?mid=4157781743129391')
        ])
    def test_get_weibo_cont_from_search_by_mid(self, unique_str, url):
        resp = requests.get(url)
        assert unique_str in resp.text


class TestWithLogin:
    def test_login(self):
        pass

    def test_crawl_user_info_with_login(self):
        pass

    def test_advance_search_with_login(self):
        pass