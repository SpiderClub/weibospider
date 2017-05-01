import unittest


class TestWeiboSpider(unittest.TestCase):
    def get_login_info(self):
        from db import login_info
        infos = login_info.get_login_info()
        self.assertEqual(len(infos), 8)

    def test_login(self):
        from wblogin.login import get_session
        sc = get_session('15708437303', 'rookiefly')
        if sc:
            print('登陆成功')
        else:
            raise Exception('登录失败')

    def test_crawl_by_cookie(self):
        import requests
        from headers import headers
        from db.cookies_db import fetch_cookies
        test_url = 'http://weibo.com/p/1005051764222885/info?mod=pedit_more'
        cookies = fetch_cookies()
        resp = requests.get(test_url, cookies=cookies, headers=headers)
        self.assertIn('深扒娱乐热点', resp.text)

    def test_get_timeout(self):
        from config.conf import get_timeout
        self.assertEqual(get_timeout(), 200)

    def test_update_repost_comment(self):
        from db.weibosearch_dao import update_repost_comment, get_repost_comment
        mid = '3791583457149221'
        reposts = 42
        comments = 9
        rs = get_repost_comment(mid)
        self.assertNotEqual(rs, (reposts, comments))
        update_repost_comment(mid=mid, reposts=reposts, comments=comments)
        rs = get_repost_comment(mid)
        self.assertEqual(rs, (reposts, comments))

    def test_get_user_from_db(self):
        from db.user_dao import get_user
        # 数据库中存在的数据
        user = get_user('3858873234')
        self.assertEqual(user.get('name'), '景区宝')

        # 数据库中不存在的数据
        user2 = get_user('2674334272')
        self.assertEqual(isinstance(user2, dict), True)

    def test_freeze_account(self):
        from db.login_info import set_account_freeze
        set_account_freeze('13272625419')

    def test_delete_cookies(self):
        from db.cookies_db import delete_cookies
        delete_cookies('15708437303')

