import time
import pytest
import requests

from tests import REQUEST_INTERNAL


class TestWithoutLogin:
    @pytest.mark.parametrize(
        'unique_str, url', [
            ('$CONFIG', 'http://weibo.com/1752613937/Afa5SFjJc'),
            ('$CONFIG', 'http://weibo.com/1319066361/Flttyxak8')
        ])
    def test_crawl_weibo_info_without_login(self, unique_str, url, cookies):
        resp = requests.get(url, cookies=cookies)
        assert unique_str in resp.text
        time.sleep(REQUEST_INTERNAL)

        resp = requests.get(url)
        time.sleep(REQUEST_INTERNAL)
        assert unique_str not in resp.text

    def test_crawl_weibo_comment_without_login(self, cookies):
        comment_url = 'http://weibo.com/aj/v6/comment/big?ajwvr=6&id=4158045430832830&page=1'
        resp = requests.get(comment_url, cookies=cookies)
        assert 'Sina Visitor System' not in resp.text
        time.sleep(REQUEST_INTERNAL)

        resp = requests.get(comment_url)
        assert 'Sina Visitor System' in resp.text
        time.sleep(REQUEST_INTERNAL)

    def test_crawl_weibo_repost_without_login(self, cookies):
        repost_url = 'http://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id=4158045430832830&page=12'
        resp = requests.get(repost_url, cookies=cookies)
        assert 'Sina Visitor System' not in resp.text
        time.sleep(REQUEST_INTERNAL)

        resp = requests.get(repost_url)
        assert 'Sina Visitor System' in resp.text
        time.sleep(REQUEST_INTERNAL)

    @pytest.mark.parametrize(
        'unique_str, url', [
            ('html', 'http://s.weibo.com/ajax/direct/morethan140?mid=4157622578000858'),
            ('html', 'http://s.weibo.com/ajax/direct/morethan140?mid=4157781743129391')
        ])
    def test_get_weibo_cont_from_search_by_mid(self, unique_str, url):
        resp = requests.get(url)
        assert unique_str in resp.text
        time.sleep(REQUEST_INTERNAL)


